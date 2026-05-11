from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import json
from typing import Annotated

from core.database import get_db
from models import models

router = APIRouter(prefix="/api/v1/sync", tags=["Sync"])

@router.post("")
def sync_all(payload: dict, db: Annotated[Session, Depends(get_db)]):
    """
    Master sync endpoint for Background Worker.
    Receives batch dirty records from the client SQLite and upserts them.
    """
    try:
        # 1. Sync Students
        students = payload.get("students", [])
        for s in students:
            student_id = uuid.UUID(s["id"])
            existing = db.query(models.Student).filter(models.Student.id == student_id).first()
            if existing:
                existing.email = s["email"]
                # In real app, only update password_hash if changed
                # existing.password_hash = s["password_hash"]
                existing.username = s["full_name"] or "Unknown"
            else:
                new_student = models.Student(
                    id=student_id,
                    email=s["email"],
                    username=s["full_name"] or "Unknown",
                    password_hash=s["password_hash"]
                )
                db.add(new_student)

        # 2. Sync Contexts
        contexts = payload.get("student_context", [])
        for c in contexts:
            context_id = uuid.UUID(c["id"])
            student_id = uuid.UUID(c["student_id"])
            
            # parse JSON string back to dict
            raw_input_data = json.loads(c["raw_input"]) if isinstance(c["raw_input"], str) else c["raw_input"]

            existing_c = db.query(models.StudentContext).filter(models.StudentContext.id == context_id).first()
            if existing_c:
                existing_c.raw_input = raw_input_data
            else:
                new_context = models.StudentContext(
                    id=context_id,
                    student_id=student_id,
                    raw_input=raw_input_data
                )
                db.add(new_context)

        db.commit()
        return {"status": "success", "message": "Batch synced successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")
