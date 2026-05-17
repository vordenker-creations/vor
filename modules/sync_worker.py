import time
import requests
import os
import sys
from PyQt6.QtCore import QThread, pyqtSignal

# Ensure the parent directory is in the path to import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud

class SyncWorker(QThread):
    sync_success = pyqtSignal(int) # Emits number of records synced
    sync_error = pyqtSignal(str)   # Emits error messages

    def __init__(self, server_url="http://100.95.50.104:8000"):
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
        while self.running:
            try:
                # 1. Fetch data that needs syncing from local SQLite
                dirty_data = crud.get_dirty_records()
                
                has_students = len(dirty_data["students"]) > 0
                has_contexts = len(dirty_data["student_context"]) > 0

                if has_students or has_contexts:
                    print(f"Sync Worker: Found {len(dirty_data['students'])} students and {len(dirty_data['student_context'])} contexts to sync.")
                    
                    # 2. Send to server
                    print(f"Pushing to {self.server_url}/api/v1/sync")
                    response = requests.post(f"{self.server_url}/api/v1/sync", json=dirty_data, timeout=5)
                    
                    if response.status_code == 200:
                        # 3. Mark as clean locally
                        student_ids = [s["id"] for s in dirty_data["students"]]
                        context_ids = [c["id"] for c in dirty_data["student_context"]]
                        crud.mark_records_synced(student_ids, context_ids)
                        
                        total_synced = len(student_ids) + len(context_ids)
                        self.sync_success.emit(total_synced)
                        print("Sync Worker: Successfully synced and marked records as clean.")
                    else:
                        err_msg = f"Server returned {response.status_code}"
                        self.sync_error.emit(err_msg)
                        print(f"Sync Worker: {err_msg}")
            
            except Exception as e:
                self.sync_error.emit(str(e))
                print(f"Sync Worker Error: {e}. Will retry later.")
            
            # Sleep for 10 seconds before checking again (in 1s increments for fast shutdown)
            for _ in range(10):
                if not self.running:
                    break
                time.sleep(1)

# Singleton instance
worker = SyncWorker()
