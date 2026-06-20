import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List
import json

from database import (
    initialize_db, 
    insert_job, 
    get_all_jobs, 
    create_user, 
    get_user_by_email, 
    update_user_profile,
    delete_job,
    get_db_connection
)
from models import JobCreate, UserRegister, UserLogin, UserProfileUpdate

# Configure logging with standard production layout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("news_bridge.server")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total active connections: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        message = json.dumps(data)
        logger.info(f"WebSocket broadcasting message to {len(self.active_connections)} clients: {data}")
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message to connection: {e}")
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events handler for FastAPI. Runs database initialization
    before the server starts accepting traffic.
    """
    logger.info("Initializing server startup routines...")
    try:
        initialize_db()
        logger.info("Startup routines completed successfully.")
    except Exception as e:
        logger.critical(f"Startup routine failed: {e}")
        raise e
    yield
    logger.info("Shutting down server...")

# Initialize FastAPI App
app = FastAPI(
    title="AI-Career Bridge API",
    description="Production-ready API for managing tech/web recruiter job listings and recruiter profiles",
    version="1.1.0",
    lifespan=lifespan
)

# Set up CORS middleware (allow_credentials=False avoids wildcard collision in modern browsers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamic path resolution to locate the frontend 'web/' directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

# ==================== STATIC FILE ROUTING ====================

@app.get("/")
async def serve_index():
    """Serves the main dashboard page at the root URL."""
    return FileResponse(os.path.join(WEB_DIR, "index.html"))

@app.get("/style.css")
async def serve_css():
    """Serves the custom glassmorphism stylesheet."""
    return FileResponse(os.path.join(WEB_DIR, "style.css"))

@app.get("/app.js")
async def serve_js():
    """Serves the dashboard logic and API connector script."""
    return FileResponse(os.path.join(WEB_DIR, "app.js"))

# ==================== JOBS API ROUTING ====================

@app.get("/jobs", status_code=status.HTTP_200_OK)
async def list_jobs():
    """Retrieves all jobs stored in the SQLite database."""
    logger.info("GET /jobs request received.")
    try:
        jobs = get_all_jobs()
        return jobs
    except Exception as e:
        logger.error(f"Error querying job listings: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve job listings from the database."
        )

@app.post("/post-job", status_code=status.HTTP_201_CREATED)
async def post_job(job: JobCreate):
    """
    Endpoint to receive job postings, validate payloads via Pydantic,
    and save them into the SQLite database.
    """
    logger.info(f"POST /post-job request received. Title: '{job.title}', Company: '{job.company}'")
    try:
        insert_job(
            title=job.title,
            company=job.company,
            salary=job.salary,
            location=job.location,
            description=job.description,
            posted_by=job.posted_by
        )
        logger.info("Job successfully stored in database.")
        return {
            "success": True,
            "message": "Job posted successfully"
        }
    except Exception as e:
        logger.error(f"Internal processing failed for /post-job: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing and saving the job posting."
        )

@app.delete("/jobs/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job_listing(job_id: int, email: str):
    """
    Endpoint to delete a job listing, verifying permissions.
    """
    logger.info(f"DELETE /jobs/{job_id} requested by email: {email}")
    try:
        success = delete_job(job_id=job_id, email=email)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job listing not found."
            )
        return {
            "success": True,
            "message": "Job listing deleted successfully."
        }
    except PermissionError as perm_err:
        logger.warning(f"Unauthorized delete attempt: {perm_err}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(perm_err)
        )
    except Exception as e:
        logger.error(f"Error executing delete for job ID {job_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job listing."
        )

@app.put("/jobs/{job_id}", status_code=status.HTTP_200_OK)
async def update_job_listing(job_id: int, job: JobCreate, email: str):
    """
    Endpoint to update a job listing, verifying owner permissions.
    """
    logger.info(f"PUT /jobs/{job_id} requested by email: {email}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT posted_by FROM jobs WHERE id = ?;", (job_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job listing not found."
            )
        
        if row["posted_by"] != email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to edit this job."
            )
            
        cursor.execute("""
            UPDATE jobs 
            SET title = ?, company = ?, salary = ?, location = ?, description = ?
            WHERE id = ?;
        """, (job.title, job.company, job.salary, job.location, job.description, job_id))
        conn.commit()
        
        return {"success": True, "message": "Job listing updated successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"Error executing update for job ID {job_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update job listing."
        )
    finally:
        if conn:
            conn.close()

@app.post("/apply", status_code=status.HTTP_201_CREATED)
async def apply_to_job(payload: dict):
    """Records a new job application in the SQLite database."""
    email = payload.get("email")
    job_id = payload.get("job_id")
    display_name = payload.get("display_name") or email
    major = payload.get("major") or ""
    student_year = payload.get("student_year") or 1
    if not email or not job_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and job_id are required fields."
        )
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        from datetime import datetime
        local_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO applications (user_email, job_id, applied_at, student_major, student_year, student_name)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_email, job_id) DO UPDATE SET
                applied_at = excluded.applied_at,
                student_major = CASE WHEN excluded.student_major != '' THEN excluded.student_major ELSE student_major END,
                student_year = CASE WHEN excluded.student_year != 1 THEN excluded.student_year ELSE student_year END,
                student_name = CASE WHEN excluded.student_name != '' THEN excluded.student_name ELSE student_name END;
        """, (email, job_id, local_now, major, student_year, display_name))
        
        # Query job title and company for notification
        cursor.execute("SELECT title, company FROM jobs WHERE id = ?;", (job_id,))
        job_row = cursor.fetchone()
        conn.commit()
        
        if job_row:
            job_title = job_row["title"]
            job_company = job_row["company"]
            message_text = f"Ứng viên {display_name} vừa ứng tuyển vào vị trí {job_title} tại {job_company}!"
        else:
            job_title = f"Công việc ID {job_id}"
            job_company = "Hệ thống"
            message_text = f"Ứng viên {display_name} vừa ứng tuyển vào công việc ID {job_id}!"
            
        logger.info(f"Broadcasting notification: {message_text}")
        
        applicant_data = {
            "name": display_name,
            "email": email,
            "major": major or "Chưa cập nhật",
            "student_year": student_year,
            "job_title": job_title,
            "job_company": job_company
        }
        
        # Broadcast toast notification
        await manager.broadcast({
            "type": "notification",
            "message": message_text,
            "applicant": applicant_data
        })
        
        # Broadcast chat room message notification
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        await manager.broadcast({
            "type": "chat",
            "username": "Hệ thống (Thông báo)",
            "message": message_text,
            "timestamp": timestamp
        })
            
        return {"success": True, "message": "Job application registered."}
    except Exception as e:
        logger.error(f"Failed to record application: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit application."
        )
    finally:
        if conn:
            conn.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data_str = await websocket.receive_text()
            logger.info(f"WebSocket received raw message: {data_str}")
            try:
                data = json.loads(data_str)
                if data.get("type") == "chat":
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%H:%M")
                    await manager.broadcast({
                        "type": "chat",
                        "username": data.get("username", "Ẩn danh"),
                        "message": data.get("message", ""),
                        "timestamp": timestamp
                    })
            except Exception as e:
                logger.error(f"WebSocket error parsing chat message: {e}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/applications", status_code=status.HTTP_200_OK)
async def get_user_applications(email: str):
    """Retrieves all job IDs applied to by the specified user email."""
    logger.info(f"GET /applications requested for email: {email}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT job_id FROM applications WHERE user_email = ?;", (email,))
        rows = cursor.fetchall()
        return [row["job_id"] for row in rows]
    except Exception as e:
        logger.error(f"Failed to query applications for email {email}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve applied job listings."
        )
    finally:
        if conn:
            conn.close()

@app.get("/notifications", status_code=status.HTTP_200_OK)
async def get_recent_notifications():
    """Retrieves all notifications generated from recent job applications."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.user_email, a.job_id, a.applied_at, a.student_major, a.student_year, a.student_name, j.title, j.company 
            FROM applications a
            LEFT JOIN jobs j ON a.job_id = j.id
            ORDER BY a.applied_at DESC
            LIMIT 10;
        """)
        rows = cursor.fetchall()
        
        notifications = []
        for row in rows:
            display_name = row["student_name"] or row["user_email"]
            job_title = row["title"]
            job_company = row["company"]
            applied_at = row["applied_at"]
            
            if job_title:
                message = f"Ứng viên {display_name} vừa ứng tuyển vào vị trí {job_title} tại {job_company}!"
            else:
                job_title = f"Công việc ID {row['job_id']}"
                job_company = "Hệ thống"
                message = f"Ứng viên {display_name} vừa ứng tuyển vào công việc ID {row['job_id']}!"
                
            try:
                time_part = applied_at.split()[1][:5] if " " in applied_at else applied_at[:5]
            except:
                time_part = "Gần đây"
                
            applicant_data = {
                "name": display_name,
                "email": row["user_email"],
                "major": row["student_major"] or "Chưa cập nhật",
                "student_year": row["student_year"] or 1,
                "job_title": job_title,
                "job_company": job_company
            }
                
            notifications.append({
                "message": message,
                "timestamp": time_part,
                "applicant": applicant_data
            })
            
        return notifications
    except Exception as e:
        logger.error(f"Failed to fetch notifications: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notifications."
        )
    finally:
        if conn:
            conn.close()

# ==================== USER API ROUTING ====================

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    """Registers a new user profile in the database."""
    logger.info(f"POST /register request received for email: {user.email}")
    try:
        registered_user = create_user(
            name=user.name,
            title=user.title,
            email=user.email,
            password=user.password
        )
        return {
            "success": True,
            "user": {
                "name": registered_user["name"],
                "title": registered_user["title"],
                "email": registered_user["email"],
                "bio": registered_user["bio"],
                "skills": registered_user["skills"],
                "created_at": registered_user["created_at"]
            }
        }
    except ValueError as val_err:
        logger.warning(f"Registration failed: {val_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )
    except Exception as e:
        logger.error(f"Internal registration error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user account."
        )

@app.post("/login", status_code=status.HTTP_200_OK)
async def login_user(credentials: UserLogin):
    """Authenticates user credentials and returns profile information."""
    logger.info(f"POST /login request received for email: {credentials.email}")
    try:
        user = get_user_by_email(credentials.email)
        if not user or user["password"] != credentials.password:
            logger.warning(f"Failed login attempt for email: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        logger.info(f"Successful login for email: {credentials.email}")
        return {
            "success": True,
            "user": {
                "name": user["name"],
                "title": user["title"],
                "email": user["email"],
                "bio": user["bio"],
                "skills": user["skills"],
                "created_at": user["created_at"]
            }
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"Internal login error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication."
        )

@app.post("/update-profile", status_code=status.HTTP_200_OK)
async def update_profile(profile: UserProfileUpdate):
    """Updates the user profile values in the SQLite database."""
    logger.info(f"POST /update-profile request received for email: {profile.email}")
    try:
        updated_user = update_user_profile(
            email=profile.email,
            name=profile.name,
            title=profile.title,
            bio=profile.bio,
            skills=profile.skills
        )
        if not updated_user:
            logger.warning(f"Profile update failed: User not found with email: {profile.email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found."
            )
        
        return {
            "success": True,
            "user": {
                "name": updated_user["name"],
                "title": updated_user["title"],
                "email": updated_user["email"],
                "bio": updated_user["bio"],
                "skills": updated_user["skills"],
                "created_at": updated_user["created_at"]
            }
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"Internal profile update error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile information."
        )
