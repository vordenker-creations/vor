import os
import sys
from PyQt6.QtCore import QThread, pyqtSignal

# Ensure workspace root is in sys.path so weblink is importable from anywhere
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../vor/modules
parent_dir = os.path.dirname(current_dir)                # .../vor
workspace_root = os.path.dirname(parent_dir)             # ... (workspace root)
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from weblink import web_client

class JobsFetchWorker(QThread):
    """
    QThread worker to fetch the list of all jobs in the background.
    Emits success(list) or error(str) upon completion.
    """
    success = pyqtSignal(list)
    error = pyqtSignal(str)

    def run(self):
        try:
            jobs = web_client.get_jobs()
            self.success.emit(jobs)
        except web_client.WebClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")

class JobDetailFetchWorker(QThread):
    """
    QThread worker to fetch details for a specific job in the background.
    Emits success(dict) or error(str) upon completion.
    """
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id

    def run(self):
        try:
            job_detail = web_client.get_job_detail(self.job_id)
            self.success.emit(job_detail)
        except web_client.WebClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")
