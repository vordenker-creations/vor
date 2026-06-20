import os
import sys
from PyQt6.QtCore import QThread, pyqtSignal

# Ensure vor directory is in sys.path so weblink is importable from anywhere inside vor
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../vor/modules
parent_dir = os.path.dirname(current_dir)                # .../vor
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

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

class JobApplyWorker(QThread):
    """
    QThread worker to submit job applications asynchronously.
    Emits success() or error(str) upon completion.
    """
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, job_id, email, display_name, major=None, student_year=1):
        super().__init__()
        self.job_id = job_id
        self.email = email
        self.display_name = display_name
        self.major = major
        self.student_year = student_year

    def run(self):
        try:
            web_client.apply_job(self.job_id, self.email, self.display_name, self.major, self.student_year)
            self.success.emit()
        except web_client.WebClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")

class ApplicationsFetchWorker(QThread):
    """
    QThread worker to fetch the list of applied job IDs for a student in the background.
    Emits success(list) or error(str) upon completion.
    """
    success = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        try:
            applied_ids = web_client.get_applications(self.email)
            self.success.emit(applied_ids)
        except web_client.WebClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")

