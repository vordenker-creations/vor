from PyQt6.QtCore import QThread, pyqtSignal
from modules.api_client import client, APIClientError
from database import crud

class LoginWorker(QThread):
    # Emits student_dict on success
    success = pyqtSignal(dict)
    # Emits error message on failure
    error = pyqtSignal(str)

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password

    def run(self):
        try:
            # Call remote login
            res = client.login(self.email, self.password)
            
            # Save session to local SQLite database
            access_token = res["access_token"]
            token_type = res.get("token_type", "bearer")
            student_id = res["student_id"]
            email = res["email"]
            username = res["username"]
            display_name = res.get("display_name")
            
            # Retrieve profile details to populate major/student_year if possible, or use defaults
            major = None
            student_year = 1
            try:
                me_info = client.get_me(access_token)
                major = me_info.get("major")
                student_year = me_info.get("student_year", 1)
            except Exception as e:
                print(f"Auth worker: Optional fetch of profile failed: {e}")

            crud.save_session(
                access_token=access_token,
                token_type=token_type,
                student_id=student_id,
                email=email,
                username=username,
                display_name=display_name,
                major=major,
                student_year=student_year
            )
            
            # Retrieve consolidated student info
            student_info = crud.get_current_student()
            self.success.emit(student_info)
        except APIClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"An unexpected error occurred: {str(e)}")


class RegisterWorker(QThread):
    # Emits token response dict on success
    success = pyqtSignal(dict)
    # Emits error message on failure
    error = pyqtSignal(str)

    def __init__(self, email, password, username, display_name, major, student_year):
        super().__init__()
        self.email = email
        self.password = password
        self.username = username
        self.display_name = display_name
        self.major = major
        self.student_year = student_year

    def run(self):
        try:
            # Call remote register
            res = client.register(
                email=self.email,
                password=self.password,
                username=self.username,
                display_name=self.display_name,
                major=self.major,
                student_year=self.student_year
            )
            
            # Save session immediately to auto-login
            access_token = res["access_token"]
            token_type = res.get("token_type", "bearer")
            student_id = res["student_id"]
            email = res["email"]
            username = res["username"]
            display_name = res.get("display_name")
            
            crud.save_session(
                access_token=access_token,
                token_type=token_type,
                student_id=student_id,
                email=email,
                username=username,
                display_name=display_name,
                major=self.major,
                student_year=self.student_year
            )
            
            self.success.emit(res)
        except APIClientError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"An unexpected error occurred: {str(e)}")


class SessionRestoreWorker(QThread):
    # Emits student info dict on successful restore
    success = pyqtSignal(dict)
    # Emits error on failure
    error = pyqtSignal(str)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def run(self):
        try:
            # Fetch backend profile details using cached JWT
            me_info = client.get_me(self.token)
            
            # Extract fields
            student_id = me_info["id"]
            email = me_info["email"]
            username = me_info["username"]
            display_name = me_info.get("display_name")
            major = me_info.get("major")
            student_year = me_info.get("student_year", 1)
            
            # Save back to SQLite to make sure they are aligned
            crud.save_student_profile(
                student_id=student_id,
                email=email,
                username=username,
                display_name=display_name,
                major=major,
                student_year=student_year,
                is_dirty=0
            )
            
            student_info = crud.get_current_student()
            self.success.emit(student_info)
        except APIClientError as e:
            if e.status_code in (401, 403):
                # Clean local session only for expired / invalid token
                crud.clear_session()
                self.error.emit(f"Session expired: {str(e)}")
            else:
                # Other server error or network issue
                student_info = crud.get_current_student()
                if student_info:
                    self.success.emit(student_info)
                else:
                    self.error.emit(str(e))
        except Exception as e:
            # Any other exception (like a requests ConnectionError/timeout)
            # Try to load cached student
            student_info = crud.get_current_student()
            if student_info:
                self.success.emit(student_info)
            else:
                self.error.emit(str(e))

