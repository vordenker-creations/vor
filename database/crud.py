import uuid
import json
from datetime import datetime, timezone
from .local_db import get_connection

def get_current_timestamp():
    return datetime.now(timezone.utc).isoformat()

# ==========================================
# USER PROFILE & CONTEXT
# ==========================================

def get_current_student():
    """Returns the active student and their context from the local database."""
    conn = get_connection()
    student = conn.execute("SELECT * FROM students LIMIT 1").fetchone()
    if not student:
        conn.close()
        return None
        
    student_dict = dict(student)
    context = conn.execute("SELECT * FROM student_context WHERE student_id = ?", (student_dict["id"],)).fetchone()
    
    if context:
        student_dict["context"] = {
            "id": context["id"],
            "raw_input": json.loads(context["raw_input"]) if context["raw_input"] else {},
            "ai_plan": json.loads(context["ai_plan"]) if context["ai_plan"] else None,
            "ai_status": context["ai_status"],
            "ai_last_error": context["ai_last_error"],
            "is_dirty": context["is_dirty"],
            "updated_at": context["updated_at"]
        }
    else:
        student_dict["context"] = {
            "id": None,
            "raw_input": {},
            "ai_plan": None,
            "ai_status": "EMPTY",
            "ai_last_error": None,
            "is_dirty": 0,
            "updated_at": get_current_timestamp()
        }
        
    conn.close()
    return student_dict

def save_student_profile(student_id, email, username, display_name, major, student_year, university=None, birth_year=None, age=None, phone=None, is_dirty=0, created_at=None, updated_at=None):
    """Upserts a student profile locally."""
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = updated_at or get_current_timestamp()
    c_at = created_at or timestamp
    
    cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    
    if row:
        cursor.execute('''
            UPDATE students 
            SET email = ?, username = ?, display_name = ?, major = ?, student_year = ?, university = ?, birth_year = ?, age = ?, phone = ?, is_dirty = ?, updated_at = ?
            WHERE id = ?
        ''', (email, username, display_name, major, student_year, university, birth_year, age, phone, is_dirty, timestamp, student_id))
    else:
        cursor.execute('''
            INSERT INTO students (id, email, username, display_name, major, student_year, university, birth_year, age, phone, created_at, updated_at, is_dirty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, email, username, display_name, major, student_year, university, birth_year, age, phone, c_at, timestamp, is_dirty))
    
    conn.commit()
    conn.close()
    return student_id

def save_student_context(student_id, raw_input_dict, ai_plan_dict=None, ai_status="EMPTY", ai_last_error=None, is_dirty=0, updated_at=None):
    """Saves structured context locally and updates sync status."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM student_context WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    
    context_id = row["id"] if row else str(uuid.uuid4())
    timestamp = updated_at or get_current_timestamp()
    
    raw_input_json = json.dumps(raw_input_dict)
    ai_plan_json = json.dumps(ai_plan_dict) if ai_plan_dict else None

    if row:
        cursor.execute('''
            UPDATE student_context 
            SET raw_input = ?, ai_plan = ?, ai_status = ?, ai_last_error = ?, is_dirty = ?, updated_at = ?
            WHERE student_id = ?
        ''', (raw_input_json, ai_plan_json, ai_status, ai_last_error, is_dirty, timestamp, student_id))
    else:
        cursor.execute('''
            INSERT INTO student_context (id, student_id, raw_input, ai_plan, ai_status, ai_last_error, is_dirty, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (context_id, student_id, raw_input_json, ai_plan_json, ai_status, ai_last_error, is_dirty, timestamp))
    
    conn.commit()
    conn.close()
    return context_id

# ==========================================
# STUDENT GRADES & GPA OPERATIONS
# ==========================================

def get_student_grades(student_id):
    """Retrieves all grades for a student."""
    conn = get_connection()
    grades = conn.execute("SELECT * FROM student_grades WHERE student_id = ? ORDER BY semester ASC, id ASC", (student_id,)).fetchall()
    conn.close()
    return [dict(g) for g in grades]

def add_student_grade(student_id, semester, course_name, credits, grade_value, grade_letter):
    """Adds a new grade entry for the student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO student_grades (student_id, semester, course_name, credits, grade_value, grade_letter)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, semester, course_name, credits, grade_value, grade_letter))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def delete_student_grade(grade_id):
    """Deletes a grade entry."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_grades WHERE id = ?", (grade_id,))
    conn.commit()
    conn.close()

def calculate_gpa(student_id):
    """Calculates the cumulative GPA of a student.
    Returns cumulative GPA (float) and semester-wise GPAs (dict)."""
    conn = get_connection()
    grades = conn.execute("SELECT semester, credits, grade_value FROM student_grades WHERE student_id = ?", (student_id,)).fetchall()
    conn.close()
    
    if not grades:
        return 0.0, {}
        
    total_credits = 0
    weighted_sum = 0.0
    
    semesters = {}
    for g in grades:
        sem = g["semester"]
        cred = g["credits"]
        val = g["grade_value"]
        
        total_credits += cred
        weighted_sum += val * cred
        
        if sem not in semesters:
            semesters[sem] = {"credits": 0, "sum": 0.0}
        semesters[sem]["credits"] += cred
        semesters[sem]["sum"] += val * cred
        
    cumulative_gpa = round(weighted_sum / total_credits, 2) if total_credits > 0 else 0.0
    
    semester_gpas = {}
    for sem, data in semesters.items():
        semester_gpas[sem] = round(data["sum"] / data["credits"], 2) if data["credits"] > 0 else 0.0
        
    return cumulative_gpa, semester_gpas

# ==========================================
# SYNC WORKER HELPERS
# ==========================================

def get_dirty_records():
    """Fetches all records that need to be synced to the server."""
    conn = get_connection()
    students = []
    for row in conn.execute("SELECT * FROM students WHERE is_dirty = 1"):
        s_dict = dict(row)
        s_dict.pop("is_dirty", None)
        students.append(s_dict)
        
    contexts = []
    for row in conn.execute("SELECT * FROM student_context WHERE is_dirty = 1"):
        c_dict = dict(row)
        c_dict.pop("is_dirty", None)
        if c_dict["raw_input"]:
            try:
                c_dict["raw_input"] = json.loads(c_dict["raw_input"])
            except Exception as e:
                print(f"Error parsing raw_input in get_dirty_records: {e}")
        if c_dict["ai_plan"]:
            try:
                c_dict["ai_plan"] = json.loads(c_dict["ai_plan"])
            except Exception as e:
                print(f"Error parsing ai_plan in get_dirty_records: {e}")
        contexts.append(c_dict)
        
    conn.close()
    return {"students": students, "student_context": contexts}


def mark_records_synced(student_ids, context_ids):
    """Marks specific records as clean after successful sync."""
    conn = get_connection()
    cursor = conn.cursor()
    
    for sid in student_ids:
        cursor.execute("UPDATE students SET is_dirty = 0 WHERE id = ?", (sid,))
    for cid in context_ids:
        cursor.execute("UPDATE student_context SET is_dirty = 0 WHERE id = ?", (cid,))
        
    conn.commit()
    conn.close()

# ==========================================
# SESSION MANAGEMENT HELPERS
# ==========================================

def save_session(access_token, token_type, student_id, email, username, display_name=None, major=None, student_year=1):
    """Caches auth session JWT token and upserts local student record."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR REPLACE INTO sync_metadata (key, value) VALUES ('access_token', ?)", (access_token,))
    cursor.execute("INSERT OR REPLACE INTO sync_metadata (key, value) VALUES ('token_type', ?)", (token_type,))
    cursor.execute("INSERT OR REPLACE INTO sync_metadata (key, value) VALUES ('student_id', ?)", (student_id,))
    
    conn.commit()
    conn.close()
    
    # Save the student profile as clean locally (since it is aligned with backend state)
    save_student_profile(
        student_id=student_id,
        email=email,
        username=username,
        display_name=display_name,
        major=major,
        student_year=student_year,
        is_dirty=0
    )

def get_session():
    """Retrieves access token, token type, and student ID of logged-in user."""
    conn = get_connection()
    access_token = conn.execute("SELECT value FROM sync_metadata WHERE key = 'access_token'").fetchone()
    token_type = conn.execute("SELECT value FROM sync_metadata WHERE key = 'token_type'").fetchone()
    student_id = conn.execute("SELECT value FROM sync_metadata WHERE key = 'student_id'").fetchone()
    conn.close()
    
    if access_token and student_id:
        return {
            "access_token": access_token["value"],
            "token_type": token_type["value"] if token_type else "bearer",
            "student_id": student_id["value"]
        }
    return None

def clear_session():
    """Wipes all local cached data, logging the user out."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sync_metadata")
    # Temporarily disable foreign keys to cleanly delete all data
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM student_context")
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    conn.close()

def save_mock_interview(student_id, category, score, feedback, date_str):
    """Saves a new mock interview attempt to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mock_interviews (student_id, category, score, feedback, date_str)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_id, category, score, feedback, date_str))
    conn.commit()
    conn.close()

def get_mock_interviews(student_id):
    """Retrieves all mock interview attempts for a student."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, category, score, feedback, date_str
        FROM mock_interviews
        WHERE student_id = ?
        ORDER BY id DESC
    ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

