import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from pages.dashboard import DashboardPage
from pages.profile import ProfilePage
from pages.learning import LearningPage
from pages.community import CommunityPage
from pages.roadmap import RoadmapPage
from pages.recruitment import RecruitmentPage
from pages.ai_mentor_ui import AIMentorPage
from pages.course_detail import CourseDetailPage
from pages.settings import SettingsPage
from login import LoginPage
from register import RegisterPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Career Bridge | Masterclass")
        self.resize(1200, 800)
        self.central_widget = QStackedWidget(); self.setCentralWidget(self.central_widget)
        
        # Auth Pages
        self.login_page = LoginPage(on_login=self._handle_login, on_register_click=lambda: self.central_widget.setCurrentIndex(1))
        self.register_page = RegisterPage(on_back_click=lambda: self.central_widget.setCurrentIndex(0), on_register=self._handle_registration_success)
        self.central_widget.addWidget(self.login_page)    # 0
        self.central_widget.addWidget(self.register_page) # 1
        
        # Main App Layout (Shell)
        self.main_app_widget = QWidget()
        self.main_app_layout = QHBoxLayout(self.main_app_widget); self.main_app_layout.setContentsMargins(0,0,0,0); self.main_app_layout.setSpacing(0)
        self._setup_sidebar()
        self.pages_container = QStackedWidget(); self.main_app_layout.addWidget(self.pages_container)
        
        self.pages_container.addWidget(DashboardPage(controller=self))   # 0
        self.pages_container.addWidget(ProfilePage(controller=self))     # 1
        self.pages_container.addWidget(LearningPage(controller=self))    # 2
        self.pages_container.addWidget(CommunityPage(controller=self))   # 3
        self.pages_container.addWidget(RoadmapPage(controller=self))     # 4
        self.pages_container.addWidget(RecruitmentPage(controller=self)) # 5
        self.pages_container.addWidget(AIMentorPage(controller=self))    # 6
        self.pages_container.addWidget(CourseDetailPage(controller=self))# 7
        self.pages_container.addWidget(SettingsPage(controller=self))    # 8
        
        self.central_widget.addWidget(self.main_app_widget) # 2
        self.setStyleSheet(get_global_stylesheet())

    def _setup_sidebar(self):
        self.sidebar = QWidget(); self.sidebar.setFixedWidth(80); self.sidebar.setStyleSheet("background-color: #1E2A38;")
        layout = QVBoxLayout(self.sidebar); layout.setContentsMargins(0, 20, 0, 20); layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.nav_group = QButtonGroup(self); self.nav_group.setExclusive(True)
        from i18n import _
        nav = [
            ("📊", 0, _("nav_dashboard")), 
            ("👤", 1, _("nav_profile")), 
            ("🎨", 2, _("nav_learning")), 
            ("👥", 3, _("nav_community")), 
            ("🧭", 4, _("nav_roadmap")), 
            ("💼", 5, _("nav_recruitment")), 
            ("🤖", 6, _("nav_ai_mentor")),
<<<<<<< HEAD
            ("⚙️", 8, "Settings")
=======
            ("⚙️", 8, _("settings_tooltip"))
>>>>>>> 9b699e38554945b1a68fc554b4f59c385a4b5718
        ]
        for icon, idx, tooltip in nav:
            btn = QPushButton(icon); btn.setCheckable(True); btn.setFixedSize(60, 60)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(self._nav_style()); btn.clicked.connect(lambda ch, i=idx: self.pages_container.setCurrentIndex(i))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter); layout.addSpacing(10); self.nav_group.addButton(btn, idx)
            if idx == 0: btn.setChecked(True)
        
        # We can add a spacer here if we want settings to be at the bottom, but the original loop just adds them top-down. 
        # I'll let it be top-down, but perhaps I should add a stretch before the settings button? Let's just follow the original loop structure.
        
        self.main_app_layout.addWidget(self.sidebar)

    def _nav_style(self):
        return f"QPushButton {{ background: transparent; color: {COLOR_TEXT_SUB}; font-size: 24px; border-radius: 12px; }} QPushButton:hover {{ background: {COLOR_BG_CARD}; }} QPushButton:checked {{ background: {COLOR_PRIMARY_LIGHT}; color: {COLOR_PRIMARY}; border-left: 3px solid {COLOR_PRIMARY}; border-radius: 0px; }}"

    def show_page(self, name):
        mapping = {"DashboardPage":0, "ProfilePage":1, "LearningPage":2, "CommunityPage":3, "RoadmapPage":4, "RecruitmentPage":5, "AIMentorPage":6, "CourseDetailPage":7, "SettingsPage":8}
        idx = mapping.get(name, 0)
        self.pages_container.setCurrentIndex(idx)
        btn = self.nav_group.button(idx)
<<<<<<< HEAD
        if btn: btn.setChecked(True)
=======
        if btn:
            btn.setChecked(True)
>>>>>>> 9b699e38554945b1a68fc554b4f59c385a4b5718
        else: 
            for b in self.nav_group.buttons(): b.setChecked(False)

    def _handle_login(self, email, password):
        from database import crud
        student = crud.get_current_student()
        if (student and student.get('email') == email) or (email == "admin" and password == "admin"):
            self.central_widget.setCurrentIndex(2)
        elif email and password:
            if not student:
                crud.save_student_profile(email, "Guest User", "Not Specified")
            # Refresh profile page to reflect new DB data
            profile_page = self.pages_container.widget(1)
            if hasattr(profile_page, "show_overview"):
                profile_page.show_overview()
            self.central_widget.setCurrentIndex(2)

    def _handle_registration_success(self, email, password):
        self.login_page.email_entry.setText(email)
        self.central_widget.setCurrentIndex(0)

if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    if sys.platform == "win32":
        try: from ctypes import windll; windll.shcore.SetProcessDpiAwareness(2)
        except: pass
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    if sys.platform == "darwin": font = QFont("SF Pro Text", 10)
    app.setFont(font); window = MainWindow(); window.show(); sys.exit(app.exec())
