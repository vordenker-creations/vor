import time
from PyQt6.QtCore import QThread, pyqtSignal
from modules.api_client import client, APIClientError
from database import crud

class AIGenerateWorker(QThread):
    # Emits response dict on success
    success = pyqtSignal(dict)
    # Emits error message on failure
    error = pyqtSignal(str)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def run(self):
        try:
            # 1. Read dirty records
            dirty_data = crud.get_dirty_records()
            has_students = len(dirty_data.get("students", [])) > 0
            has_contexts = len(dirty_data.get("student_context", [])) > 0
            
            if has_students or has_contexts:
                # Sanitize local context status to avoid syncing PENDING state
                for c in dirty_data.get("student_context", []):
                    if c.get("ai_status") == "PENDING":
                        c["ai_status"] = "EMPTY"
                # Sync dirty data to backend first
                client.sync(self.token, dirty_data)
                
                # Mark synced only after successful sync
                student_ids = [s["id"] for s in dirty_data["students"]]
                context_ids = [c["id"] for c in dirty_data["student_context"]]
                crud.mark_records_synced(student_ids, context_ids)

            # 2. Trigger generation
            res = client.generate_plan(self.token)
            
            # Save local context status as PENDING
            student_id = res.get("student_id")
            if not student_id:
                # Fallback to local session student_id
                session = crud.get_session()
                student_id = session["student_id"] if session else None
            
            if student_id:
                # Fetch local context to keep raw_input intact
                student_info = crud.get_current_student()
                raw_input = {}
                if student_info and student_info.get("context"):
                    raw_input = student_info["context"].get("raw_input", {})
                
                # Update status to PENDING
                crud.save_student_context(
                    student_id=student_id,
                    raw_input_dict=raw_input,
                    ai_status="PENDING",
                    is_dirty=0
                )
            
            self.success.emit(res)
        except APIClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Failed to generate plan: {str(e)}")


class AIPollWorker(QThread):
    # Emits status ("PENDING", "COMPLETED", "FAILED")
    status_changed = pyqtSignal(str)
    # Emits final context dictionary on success
    finished = pyqtSignal(dict)
    # Emits error message on failure
    error = pyqtSignal(str)

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        max_retries = 200  # 200 checks * 3 seconds = 600 seconds (10 minutes)
        checks = 0
        
        # Get student_id from current session
        session = crud.get_session()
        if not session:
            self.error.emit("No active session found.")
            return
        student_id = session["student_id"]

        while self.running and checks < max_retries:
            try:
                res = client.get_plan_status(self.token)
                status = res.get("status", "EMPTY")
                ai_plan = res.get("ai_plan")
                ai_last_error = res.get("ai_last_error")
                
                # Fetch local context to preserve raw_input
                student_info = crud.get_current_student()
                raw_input = {}
                if student_info and student_info.get("context"):
                    raw_input = student_info["context"].get("raw_input", {})

                if status == "COMPLETED":
                    # Update local database
                    crud.save_student_context(
                        student_id=student_id,
                        raw_input_dict=raw_input,
                        ai_plan_dict=ai_plan,
                        ai_status="COMPLETED",
                        ai_last_error=None,
                        is_dirty=0
                    )
                    # Fetch latest consolidated data and emit
                    updated_student = crud.get_current_student()
                    self.status_changed.emit("COMPLETED")
                    self.finished.emit(updated_student)
                    return

                elif status == "FAILED":
                    # Update local database
                    crud.save_student_context(
                        student_id=student_id,
                        raw_input_dict=raw_input,
                        ai_plan_dict=ai_plan or {},
                        ai_status="FAILED",
                        ai_last_error=ai_last_error or "Generation failed on remote server.",
                        is_dirty=0
                    )
                    updated_student = crud.get_current_student()
                    self.status_changed.emit("FAILED")
                    self.finished.emit(updated_student)
                    return

                elif status == "PENDING":
                    # Keep polling, emit pending state update
                    self.status_changed.emit("PENDING")
                
                else:
                    # If EMPTY or other state, just log
                    self.status_changed.emit(status)

            except Exception as e:
                # Log network errors but keep retrying in case of temporary disconnects
                print(f"AI Poll Worker: Network warning/error on check: {e}")
            
            # Wait for 3 seconds, checking running flag in 100ms intervals for rapid thread cancellation
            for _ in range(30):
                if not self.running:
                    return
                time.sleep(0.1)
                
            checks += 1

        if checks >= max_retries:
            # Reached timeout of 10 minutes (still running locally)
            try:
                student_info = crud.get_current_student()
                raw_input = {}
                if student_info and student_info.get("context"):
                    raw_input = student_info["context"].get("raw_input", {})
                
                # Keep status as PENDING
                crud.save_student_context(
                    student_id=student_id,
                    raw_input_dict=raw_input,
                    ai_status="PENDING",
                    is_dirty=0
                )
            except Exception as e:
                print(f"Error saving pending status on timeout: {e}")
            self.status_changed.emit("PENDING")
            self.error.emit("Academic plan generation is still running. You can refresh manually or leave the page.")
