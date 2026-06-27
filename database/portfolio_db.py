import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "client_store.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_portfolio_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create student_projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        technologies TEXT,
        description TEXT,
        github_url TEXT,
        progress INTEGER DEFAULT 0,
        skills TEXT
    )
    ''')
    
    # Create project_tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        task_name TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY (project_id) REFERENCES student_projects(id) ON DELETE CASCADE
    )
    ''')
    conn.commit()
    
    # Seed default projects and tasks if empty
    cursor.execute("SELECT COUNT(*) FROM student_projects")
    if cursor.fetchone()[0] == 0:
        default_projects = [
            ("AI Career Planner", "Python, PyQt6, Ollama AI", "A desktop application helping students build study roadmaps via generative AI.", "https://github.com", 75, "Python, Machine Learning"),
            ("E-Commerce Web API", "Go, PostgreSQL, Redis", "High-performance backend API with JWT auth and caching layer.", "https://github.com", 100, "Web Dev, Database"),
            ("Stock Tracker App", "React Native, Node.js", "Mobile application tracking real-time crypto and stock assets.", "https://github.com", 33, "Web Dev")
        ]
        
        project_tasks_seed = {
            "AI Career Planner": [
                ("Design UI using PyQt6", 1),
                ("Database schema and SQLite integration", 1),
                ("Integrate Ollama AI API", 1),
                ("Test roadmap generation and output formats", 0)
            ],
            "E-Commerce Web API": [
                ("Setup PostgreSQL and Redis connections", 1),
                ("Implement JWT Authentication", 1),
                ("Design API endpoints and validation", 1),
                ("Write unit tests and API docs", 1)
            ],
            "Stock Tracker App": [
                ("Setup React Native and Expo workspace", 1),
                ("Connect real-time API websocket", 0),
                ("Implement charting visual widgets", 0)
            ]
        }
        
        for title, tech, desc, url, prog, skills in default_projects:
            cursor.execute(
                "INSERT INTO student_projects (title, technologies, description, github_url, progress, skills) VALUES (?, ?, ?, ?, ?, ?)",
                (title, tech, desc, url, prog, skills)
            )
            pid = cursor.lastrowid
            
            # Insert seed tasks
            if title in project_tasks_seed:
                for task_name, completed in project_tasks_seed[title]:
                    cursor.execute(
                        "INSERT INTO project_tasks (project_id, task_name, completed) VALUES (?, ?, ?)",
                        (pid, task_name, completed)
                    )
        conn.commit()
        
    conn.close()

# CRUD operations for Projects
def get_all_projects():
    init_portfolio_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_projects")
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return projects

def add_project(title, technologies, description, github_url, progress, skills):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO student_projects (title, technologies, description, github_url, progress, skills) VALUES (?, ?, ?, ?, ?, ?)",
        (title, technologies, description, github_url, progress, skills)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_project(project_id, title, technologies, description, github_url, progress, skills):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE student_projects SET title = ?, technologies = ?, description = ?, github_url = ?, progress = ?, skills = ? WHERE id = ?",
        (title, technologies, description, github_url, progress, skills, project_id)
    )
    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()

# Task Operations
def get_project_tasks(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project_tasks WHERE project_id = ? ORDER BY id ASC", (project_id,))
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

def add_project_task(project_id, task_name, completed=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO project_tasks (project_id, task_name, completed) VALUES (?, ?, ?)",
        (project_id, task_name, completed)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    recalculate_project_progress(project_id)
    return new_id

def update_project_task(task_id, completed):
    conn = get_connection()
    cursor = conn.cursor()
    # Find project_id first
    cursor.execute("SELECT project_id FROM project_tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row:
        project_id = row["project_id"]
        cursor.execute("UPDATE project_tasks SET completed = ? WHERE id = ?", (completed, task_id))
        conn.commit()
        conn.close()
        recalculate_project_progress(project_id)
    else:
        conn.close()

def delete_project_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Find project_id first
    cursor.execute("SELECT project_id FROM project_tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row:
        project_id = row["project_id"]
        cursor.execute("DELETE FROM project_tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        recalculate_project_progress(project_id)
    else:
        conn.close()

def set_project_tasks(project_id, tasks):
    """Sync tasks: deletes existing ones and replaces them.
    Each item in tasks is a dict or tuple: {"task_name": name, "completed": completed}"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM project_tasks WHERE project_id = ?", (project_id,))
    for t in tasks:
        if isinstance(t, dict):
            name = t["task_name"]
            comp = t.get("completed", 0)
        else:
            name, comp = t
        cursor.execute(
            "INSERT INTO project_tasks (project_id, task_name, completed) VALUES (?, ?, ?)",
            (project_id, name, comp)
        )
    conn.commit()
    conn.close()
    recalculate_project_progress(project_id)

def recalculate_project_progress(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if there are project requirements first
    cursor.execute("SELECT COUNT(*), SUM(completed) FROM project_requirements WHERE project_id = ?", (project_id,))
    row_reqs = cursor.fetchone()
    total_reqs = row_reqs[0]
    completed_reqs = row_reqs[1]
    
    if total_reqs and total_reqs > 0:
        progress = int((completed_reqs or 0) / total_reqs * 100)
        cursor.execute("UPDATE student_projects SET progress = ? WHERE id = ?", (progress, project_id))
        conn.commit()
    else:
        # Fall back to project tasks / milestones
        cursor.execute("SELECT COUNT(*), SUM(completed) FROM project_tasks WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()
        total = row[0]
        completed = row[1]
        if total and total > 0:
            progress = int((completed or 0) / total * 100)
            cursor.execute("UPDATE student_projects SET progress = ? WHERE id = ?", (progress, project_id))
            conn.commit()
        else:
            cursor.execute("UPDATE student_projects SET progress = 0 WHERE id = ?", (project_id,))
            conn.commit()
    conn.close()

# Project Requirements Operations
def get_project_requirements(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project_requirements WHERE project_id = ? ORDER BY id ASC", (project_id,))
    reqs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return reqs

def add_project_requirement(project_id, requirement_text, completed=0, detailed_suggestion=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO project_requirements (project_id, requirement_text, completed, detailed_suggestion) VALUES (?, ?, ?, ?)",
        (project_id, requirement_text, completed, detailed_suggestion)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    recalculate_project_progress(project_id)
    return new_id

def update_project_requirement_status(req_id, completed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project_id FROM project_requirements WHERE id = ?", (req_id,))
    row = cursor.fetchone()
    if row:
        project_id = row["project_id"]
        cursor.execute("UPDATE project_requirements SET completed = ? WHERE id = ?", (completed, req_id))
        conn.commit()
        conn.close()
        recalculate_project_progress(project_id)
    else:
        conn.close()

def update_project_requirement_suggestion(req_id, detailed_suggestion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE project_requirements SET detailed_suggestion = ? WHERE id = ?", (detailed_suggestion, req_id))
    conn.commit()
    conn.close()

def delete_project_requirement(req_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project_id FROM project_requirements WHERE id = ?", (req_id,))
    row = cursor.fetchone()
    if row:
        project_id = row["project_id"]
        cursor.execute("DELETE FROM project_requirements WHERE id = ?", (req_id,))
        conn.commit()
        conn.close()
        recalculate_project_progress(project_id)
    else:
        conn.close()
