import threading
import time
import requests
import os
import sys

# Ensure the parent directory is in the path to import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud

class SyncWorker:
    def __init__(self, server_url="http://100.95.50.104:8000"):
        self.server_url = server_url
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._sync_loop, daemon=True)
            self.thread.start()
            print("Background Sync Worker started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
            print("Background Sync Worker stopped.")

    def _sync_loop(self):
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
                        print("Sync Worker: Successfully synced and marked records as clean.")
                    else:
                        print(f"Sync Worker: Server returned {response.status_code}")
            
            except Exception as e:
                print(f"Sync Worker Error: {e}. Will retry later.")
            
            # Sleep for 10 seconds before checking again
            time.sleep(10)

# Singleton instance
worker = SyncWorker()
