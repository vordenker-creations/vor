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
    context = conn.execute("SELECT raw_input FROM student_context WHERE student_id = ?", (student_dict["id"],)).fetchone()
    
    if context and context["raw_input"]:
        student_dict["context"] = json.loads(context["raw_input"])
    else:
        student_dict["context"] = {}
        
    conn.close()
    return student_dict

def save_student_profile(email, full_name, major):
    """Upserts a student profile and marks it as dirty for sync."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if student exists locally (simplified for one-user local app)
    cursor.execute("SELECT id FROM students WHERE email = ?", (email,))
    row = cursor.fetchone()
    
    student_id = row["id"] if row else str(uuid.uuid4())
    timestamp = get_current_timestamp()

    if row:
        cursor.execute('''
            UPDATE students 
            SET full_name = ?, major = ?, is_dirty = 1, updated_at = ?
            WHERE email = ?
        ''', (full_name, major, timestamp, email))
    else:
        # Dummy password hash for local mock if creating new
        cursor.execute('''
            INSERT INTO students (id, email, password_hash, full_name, major, is_dirty, updated_at)
            VALUES (?, ?, ?, ?, ?, 1, ?)
        ''', (student_id, email, "local_hash", full_name, major, timestamp))
    
    conn.commit()
    conn.close()
    return student_id

def save_student_context(student_id, raw_input_dict):
    """Saves the JSON context (skills, bio) and marks it as dirty."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM student_context WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    
    context_id = row["id"] if row else str(uuid.uuid4())
    timestamp = get_current_timestamp()
    raw_input_json = json.dumps(raw_input_dict)

    if row:
        cursor.execute('''
            UPDATE student_context 
            SET raw_input = ?, is_dirty = 1, updated_at = ?
            WHERE student_id = ?
        ''', (raw_input_json, timestamp, student_id))
    else:
        cursor.execute('''
            INSERT INTO student_context (id, student_id, raw_input, is_dirty, updated_at)
            VALUES (?, ?, ?, 1, ?)
        ''', (context_id, student_id, raw_input_json, timestamp))
    
    conn.commit()
    conn.close()
    return context_id

# ==========================================
# SYNC WORKER HELPERS
# ==========================================

def get_dirty_records():
    """Fetches all records that need to be synced to the server."""
    conn = get_connection()
    
    # Get dirty students
    students = [dict(row) for row in conn.execute("SELECT * FROM students WHERE is_dirty = 1")]
    
    # Get dirty contexts
    contexts = [dict(row) for row in conn.execute("SELECT * FROM student_context WHERE is_dirty = 1")]
    
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
