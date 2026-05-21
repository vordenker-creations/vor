import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "client_store.db")

def get_connection():
    """Returns a database connection with dictionary-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite tables required for the Local-First architecture."""
    # Check if DB is stale (has password_hash in students table)
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(students)")
            columns = [col[1] for col in cursor.fetchall()]
            conn.close()
            if columns and "password_hash" in columns:
                print("Stale database schema detected. Deleting client_store.db for rebuild...")
                os.remove(DB_PATH)
        except Exception as e:
            print(f"Error checking/deleting stale DB: {e}")

    conn = get_connection()
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Students Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT,
        major TEXT,
        student_year INTEGER DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        is_dirty INTEGER DEFAULT 0
    )
    ''')

    # 2. Student Context Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_context (
        id TEXT PRIMARY KEY,
        student_id TEXT UNIQUE NOT NULL,
        raw_input TEXT NOT NULL,
        ai_plan TEXT,
        ai_status TEXT DEFAULT 'EMPTY',
        ai_last_error TEXT,
        updated_at TEXT NOT NULL,
        is_dirty INTEGER DEFAULT 0,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    )
    ''')

    # 3. Sync Metadata Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sync_metadata (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

# Automatically initialize tables when this module is imported
init_db()

