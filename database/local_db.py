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
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Students Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        major TEXT,
        is_dirty INTEGER DEFAULT 1,
        updated_at TEXT NOT NULL
    )
    ''')

    # 2. Student Context Table (Stores Profile/CV details as JSON)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_context (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        raw_input TEXT,
        ai_generated_profile TEXT,
        is_dirty INTEGER DEFAULT 1,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
    ''')

    # 3. Sync Metadata Table (Tracks last successful sync time)
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
