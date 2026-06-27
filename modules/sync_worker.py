import time
import requests
import os
import sys
from PyQt6.QtCore import QThread, pyqtSignal

# Ensure the parent directory is in the path to import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud
from core.config import SERVER_URL

class SyncWorker(QThread):
    sync_success = pyqtSignal(int) # Emits number of records synced
    sync_error = pyqtSignal(str)   # Emits error messages

    def __init__(self, server_url=SERVER_URL):
        super().__init__()
        self.server_url = server_url
        self.running = False

    def start_worker(self):
        if not self.running:
            self.running = True
            self.start()
            print("Background Sync QThread started.")

    def stop_worker(self):
        self.running = False
        self.wait(2000) # Wait up to 2 seconds for clean exit
        print("Background Sync QThread stopped.")

    def run(self):
        retry_delay = 10
        while self.running:
            try:
                # 0. Check if student session is active
                session = crud.get_session()
                if not session:
                    # No active session, wait and retry
                    time.sleep(2)
                    continue

                access_token = session["access_token"]

                # 1. Fetch data that needs syncing from local SQLite
                dirty_data = crud.get_dirty_records()
                
                has_students = len(dirty_data.get("students", [])) > 0
                has_contexts = len(dirty_data.get("student_context", [])) > 0

                if has_students or has_contexts:
                    # 2. Send to server
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {access_token}"
                    }
                    response = requests.post(f"{self.server_url}/api/v1/sync", json=dirty_data, headers=headers, timeout=(3, 10))
                    
                    if response.status_code == 200:
                        # 3. Mark as clean locally
                        student_ids = [s["id"] for s in dirty_data["students"]]
                        context_ids = [c["id"] for c in dirty_data["student_context"]]
                        
                        crud.mark_records_synced(student_ids, context_ids)
                        
                        total_synced = len(student_ids) + len(context_ids)
                        self.sync_success.emit(total_synced)
                        print(f"Sync Worker: Successfully synced {total_synced} records.")
                        retry_delay = 10
                    else:
                        err_msg = f"Server returned {response.status_code}"
                        self.sync_error.emit(err_msg)
                        print(f"Sync Worker: {err_msg}")
                        retry_delay = 30
            
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.sync_error.emit("Server offline")
                print("Sync Worker: Local Sync Server is offline. Retrying in 60s...")
                retry_delay = 60
            
            except Exception as e:
                self.sync_error.emit(str(e))
                print(f"Sync Worker Error: {e}. Retrying in 30s...")
                retry_delay = 30
            
            # Sleep for the determined delay (in 1s increments for fast shutdown)
            for _ in range(retry_delay):
                if not self.running:
                    break
                time.sleep(1)

# Singleton instance
worker = SyncWorker()

