import sqlite3
import os
import logging
from typing import Dict, Any, List

# Set up database specific logger
logger = logging.getLogger("news_bridge.database")

# Ensure the database file is created in the same directory as database.py to prevent path errors
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")

def get_db_connection() -> sqlite3.Connection:
    """
    Establishes and returns a native connection to the SQLite database.
    Sets the row_factory to sqlite3.Row for dict-like column access.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Failed to establish connection to database at {DB_PATH}: {e}")
        raise e

def initialize_db() -> None:
    """
    Runs database schema initialization.
    Creates the 'jobs' and 'users' tables if they do not exist.
    Seeds the tables with default mock values if they are empty.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Create jobs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            salary TEXT NOT NULL,
            location TEXT NOT NULL,
            posted_by TEXT DEFAULT 'system',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Safe migration for existing tables: add posted_by if missing
        try:
            cursor.execute("ALTER TABLE jobs ADD COLUMN posted_by TEXT DEFAULT 'system';")
            conn.commit()
            logger.info("Migrated jobs table: added 'posted_by' column successfully.")
        except sqlite3.OperationalError:
            # Column already exists
            pass
        
        # 2. Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT DEFAULT '',
            skills TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # 3. Create applications table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            job_id INTEGER NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_email, job_id)
        );
        """)
        
        conn.commit()
        
        # 3. Seed mock jobs if table is empty
        cursor.execute("SELECT COUNT(*) FROM jobs;")
        if cursor.fetchone()[0] == 0:
            mock_jobs = [
                ("Staff Frontend Architect", "Vercel", "$160k - $210k", "San Francisco, CA (Remote)", 
                 "We are looking for an exceptional Staff Frontend Architect to lead the future of web deployment UI. You will work on optimizing rendering paths, improving component design models, and shaping next-generation SaaS features.\n\n### Requirements:\n- 7+ years of building web applications\n- Expertise in React internals and Next.js routers\n- Passion for micro-interactions and performance optimization\n- Strong experience writing clean CSS animations", "system"),
                ("Rust Systems Engineer", "Anthropic", "$180k - $240k", "San Francisco, CA (Onsite)", 
                 "Anthropic is looking for a Rust systems engineer to lead core latency reduction teams. You will work directly at the interface of CUDA pipelines, compiler tooling, and web clients to ensure fast, real-time responses.\n\n### Key Tasks:\n- Build low-latency interfaces in native Rust\n- Integrate WebAssembly backends into the browser UI\n- Optimize memory models and core algorithms", "system"),
                ("DevOps & Cloud Engineer", "Stripe", "$140k - $175k", "Dublin, Ireland (Remote)", 
                 "Join Stripe's Core Infrastructure team to engineer resilient cloud pipelines. This role handles large scaling configurations, automated validation loops, and ensures absolute site reliability for millions of transactions.\n\n### Your Profile:\n- Strong knowledge of AWS cloud services and Terraform configurations\n- Competence in writing production shell files and Go scripts\n- Deep commitment to cloud security best practices", "system"),
                ("Product Engineer", "Linear", "$130k - $160k", "Remote (Global)", 
                 "We are seeking a senior designer/engineer hybrid to craft smooth project management flows. Linear's interface is celebrated for its low latency, high utility, and beautiful typography. You will build core client interactions.\n\n### Specifications:\n- Outstanding mastery of React, CSS variables, and layout systems\n- Deep visual styling eye: spacing, font scale, micro-interactions\n- Ability to work autonomously in global teams", "system"),
                ("Systems Engineer (Node/TS)", "Supabase", "$110k - $145k", "Singapore (Hybrid)", 
                 "Supabase seeks systems devs to work on PostgreSQL client libraries and serverless functions infrastructure. Help open source developers launch products in minutes with reliable server templates and instant API backends.", "system"),
                ("Interactive UI/UX Designer", "Figma", "$150k - $185k", "New York, NY (Hybrid)", 
                 "Help build the canvas of the web. Figma is recruiting creative engineers to push the boundaries of multiplayer design systems. Experience in web canvas, matrix operations, and rich gesture animations is strongly preferred.", "system")
            ]
            cursor.executemany("""
            INSERT INTO jobs (title, company, salary, location, description, posted_by)
            VALUES (?, ?, ?, ?, ?, ?);
            """, mock_jobs)
            conn.commit()
            logger.info("Mock jobs seeded successfully.")

        # 4. Mock user seeding removed as requested to start in pure Guest state.
        pass

        logger.info(f"Database initialized. Tables check/created at: {DB_PATH}")
    except sqlite3.Error as e:
        logger.critical(f"Critical error during database initialization: {e}")
        raise e
    finally:
        if conn:
            conn.close()

# ==================== JOBS CRUD LOGIC ====================

def get_all_jobs() -> List[Dict[str, Any]]:
    """Retrieves all jobs stored in the database, sorted by ID descending."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to query all jobs: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def insert_job(title: str, company: str, salary: str, location: str, description: str, posted_by: str = "system") -> int:
    """
    Inserts a job record into the database.
    Uses parameterized query to secure input fields against SQL injection.
    """
    query = """
    INSERT INTO jobs (title, company, salary, location, description, posted_by)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (title, company, salary, location, description, posted_by))
        conn.commit()
        inserted_id = cursor.lastrowid
        logger.info(f"Successfully inserted job ID {inserted_id} posted by {posted_by} into database.")
        return inserted_id
    except sqlite3.Error as e:
        logger.error(f"Failed to insert job into database: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# ==================== USERS CRUD LOGIC ====================

def create_user(name: str, title: str, email: str, password: str) -> Dict[str, Any]:
    """Inserts a new user registration record into the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (name, title, email, password, bio, skills)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (name, title, email, password, "", ""))
        conn.commit()
        inserted_id = cursor.lastrowid
        logger.info(f"Successfully registered user ID {inserted_id} with email {email}")
        
        cursor.execute("SELECT * FROM users WHERE id = ?;", (inserted_id,))
        row = cursor.fetchone()
        return dict(row)
    except sqlite3.IntegrityError:
        logger.error(f"User registration failed: email {email} already exists.")
        raise ValueError("Email already exists")
    except sqlite3.Error as e:
        logger.error(f"Failed to register user: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_user_by_email(email: str) -> Dict[str, Any]:
    """Retrieves user profile details by email address."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?;", (email,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        logger.error(f"Failed to query user by email {email}: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def update_user_profile(email: str, name: str, title: str, bio: str, skills: str) -> Dict[str, Any]:
    """Updates user information (name, title, bio, skills) for the specified email."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users
        SET name = ?, title = ?, bio = ?, skills = ?
        WHERE email = ?;
        """, (name, title, bio, skills, email))
        conn.commit()
        
        cursor.execute("SELECT * FROM users WHERE email = ?;", (email,))
        row = cursor.fetchone()
        if row:
            logger.info(f"Successfully updated profile for user email: {email}")
            return dict(row)
        return None
    except sqlite3.Error as e:
        logger.error(f"Failed to update user profile for email {email}: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def delete_job(job_id: int, email: str) -> bool:
    """
    Deletes a job from the database if the creator matches the email.
    Returns True if deletion succeeded, False if not found.
    Raises PermissionError if the email does not match the job poster.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT posted_by FROM jobs WHERE id = ?;", (job_id,))
        row = cursor.fetchone()
        if not row:
            return False
            
        if row["posted_by"] != email:
            raise PermissionError("You do not have permission to delete this job")
            
        cursor.execute("DELETE FROM applications WHERE job_id = ?;", (job_id,))
        cursor.execute("DELETE FROM jobs WHERE id = ?;", (job_id,))
        conn.commit()
        logger.info(f"Successfully deleted job ID {job_id} by user {email}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Failed to delete job ID {job_id} from database: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
