import requests
from core.config import SERVER_URL

class APIClientError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class APIClient:
    def __init__(self, base_url=SERVER_URL):
        self.base_url = base_url

    def register(self, email, password, username=None, display_name=None, major=None, student_year=1):
        """Registers a new student on the backend.
        
        POST /api/v1/auth/register
        """
        payload = {
            "email": email,
            "password": password,
            "username": username,
            "display_name": display_name,
            "major": major,
            "student_year": int(student_year)
        }
        try:
            url = f"{self.base_url}/api/v1/auth/register"
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code in (200, 201):
                return response.json()
            else:
                try:
                    err_detail = response.json().get("detail", "Registration failed")
                except:
                    err_detail = f"Server returned {response.status_code}"
                raise APIClientError(err_detail, response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Network error: {str(e)}")

    def login(self, email, password):
        """Logs in a student.
        
        POST /api/v1/auth/login
        """
        payload = {
            "email": email,
            "password": password
        }
        try:
            url = f"{self.base_url}/api/v1/auth/login"
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                try:
                    err_detail = response.json().get("detail", "Invalid email or password")
                except:
                    err_detail = f"Server returned {response.status_code}"
                raise APIClientError(err_detail, response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Network error: {str(e)}")

    def get_me(self, token):
        """Fetches the authenticated student's profile details.
        
        GET /api/v1/auth/me
        """
        headers = {"Authorization": f"Bearer {token}"}
        try:
            url = f"{self.base_url}/api/v1/auth/me"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                try:
                    err_detail = response.json().get("detail", "Failed to retrieve student details")
                except:
                    err_detail = f"Server returned {response.status_code}"
                raise APIClientError(err_detail, response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Network error: {str(e)}")

    def sync(self, token, payload):
        """Pushes dirty records to the server.
        
        POST /api/v1/sync
        """
        headers = {"Authorization": f"Bearer {token}"}
        try:
            url = f"{self.base_url}/api/v1/sync"
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                try:
                    err_detail = response.json().get("detail", "Sync failed")
                except:
                    err_detail = f"Server returned {response.status_code}"
                raise APIClientError(err_detail, response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Network error: {str(e)}")

    def generate_plan(self, token):
        """Triggers AI plan generation for the authenticated student.
        
        POST /api/v1/ai/generate_academic_plan
        """
        headers = {"Authorization": f"Bearer {token}"}
        try:
            url = f"{self.base_url}/api/v1/ai/generate_academic_plan"
            response = requests.post(url, json={}, headers=headers, timeout=15)
            if response.status_code in (200, 201):
                return response.json()
            else:
                try:
                    err_detail = response.json().get("detail", "Failed to trigger AI plan generation")
                except:
                    err_detail = f"Server returned {response.status_code}"
                raise APIClientError(err_detail, response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Network error: {str(e)}")

    def get_plan_status(self, token):
        """Checks the status of the AI plan generation.
        
        GET /api/v1/ai/academic_plan_status
        """
        headers = {"Authorization": f"Bearer {token}"}
        try:
            url = f"{self.base_url}/api/v1/ai/academic_plan_status"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                try:
                    err_detail = response.json().get("detail", "Failed to check academic plan status")
                except:
                    err_detail = f"Server returned {response.status_code}"
                raise APIClientError(err_detail, response.status_code)
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Network error: {str(e)}")

# Singleton instance
client = APIClient()
