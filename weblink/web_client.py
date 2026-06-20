import requests

from core.config import SERVER_URL

# Centralized configuration
BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

class WebClientError(Exception):
    """
    Custom exception class representing errors in the networking layer.
    """
    def __init__(self, message, status_code=None, original_exception=None):
        super().__init__(message)
        self.status_code = status_code
        self.original_exception = original_exception

def _request(method, endpoint, **kwargs):
    """
    Reusable request wrapper handling standard REST request execution,
    timeouts, connectivity errors, and HTTP status codes.
    """
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    
    if "timeout" not in kwargs:
        kwargs["timeout"] = TIMEOUT
        
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        
        try:
            return response.json()
        except ValueError as e:
            raise WebClientError(
                "Invalid response format from server (expected JSON)",
                status_code=response.status_code,
                original_exception=e
            )
            
    except requests.exceptions.Timeout as e:
        raise WebClientError("Connection timed out. Please try again.", original_exception=e)
    except requests.exceptions.ConnectionError as e:
        raise WebClientError("Cannot connect to server. Please check if the backend is running.", original_exception=e)
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        detail = "An error occurred on the server."
        if e.response is not None:
            try:
                err_data = e.response.json()
                if isinstance(err_data, dict):
                    detail = err_data.get("detail") or err_data.get("message") or detail
            except Exception:
                detail = e.response.text or detail
        raise WebClientError(detail, status_code=status_code, original_exception=e)
    except requests.exceptions.RequestException as e:
        raise WebClientError(f"Network request failed: {str(e)}", original_exception=e)

def get_jobs():
    """
    Retrieves all job listings from the database.
    GET /jobs
    """
    return _request("GET", "jobs")

def get_job_detail(job_id):
    """
    Retrieves detailed info for a single job by id.
    Fallback: retrieves all jobs and filters locally.
    """
    jobs = get_jobs()
    for job in jobs:
        if job.get("id") == job_id:
            return job
    raise WebClientError(f"Job with ID {job_id} not found.", status_code=404)

def create_job(data):
    """
    Posts a new job opportunity to the server.
    POST /post-job
    """
    return _request("POST", "post-job", json=data)

def apply_job(job_id, email, display_name, major=None, student_year=1):
    """
    Submits a new job application.
    POST /apply
    """
    payload = {
        "job_id": job_id,
        "email": email,
        "display_name": display_name,
        "major": major,
        "student_year": student_year
    }
    return _request("POST", "apply", json=payload)

def get_applications(email):
    """
    Retrieves all job IDs applied to by the specified user email.
    GET /applications
    """
    return _request("GET", f"applications?email={email}")

