import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from database import crud
from modules.sync_worker import worker

# Authentication Pages
from login import LoginPage
from register import RegisterPage

# Main Application Pages
from pages.dashboard import DashboardPage
from pages.profile import ProfilePage
from pages.learning import LearningPage
from pages.community import CommunityPage
from pages.settings import SettingsPage
from pages.chat_ui import ChatPage
from pages.course_detail import CourseDetailPage
from pages.ai_mentor_ui import AIMentorPage
from pages.recruitment import RecruitmentPage
from pages.resume_builder import ResumeBuilderPage
from pages.interview_simulator import InterviewSimulatorPage
from pages.learning_roadmap import LearningRoadmapPage
from pages.job_portal.job_portal_page import JobPortalPage as ModernJobPortalPage
from command_palette import CommandPaletteOverlay
from sidebar_component import SidebarComponent
from neumorphic_components import NeumorphicFrame


class MainWindow(QMainWindow):
    def __init__(self, on_logout=None):
        super().__init__()
        worker.start_worker()
        self.on_logout_callback = on_logout
        self.setWindowTitle("AI-Career Bridge")
        self.resize(1350, 850)
        self.setMinimumSize(1000, 700)

        # 1. MAIN LAYOUT
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainContainer")
        self.setCentralWidget(self.central_widget)

        self.main_app_layout = QHBoxLayout(self.central_widget)
        self.main_app_layout.setContentsMargins(0, 0, 0, 0)
        self.main_app_layout.setSpacing(0)

        # 2. LEFT SIDEBAR
        self.sidebar = SidebarComponent(self)
        self.sidebar.navigation_requested.connect(self.show_page)
        self.main_app_layout.addWidget(self.sidebar)

        # 3. CONTENT AREA
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(30, 20, 30, 30)
        self.content_layout.setSpacing(20)

        # Top Global Actions Bar (Transparent, minimal)
        self.global_actions_bar = QWidget()
        self.global_actions_bar.setFixedHeight(50)
        header_h = QHBoxLayout(self.global_actions_bar)
        header_h.setContentsMargins(10, 0, 10, 0)
        header_h.setSpacing(12)

        self.btn_toggle_sidebar = QPushButton("☰")
        self.btn_toggle_sidebar.setFixedSize(38, 38)
        self.btn_toggle_sidebar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle_sidebar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #000000;
                border-radius: 12px;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(15, 23, 42, 0.08);
            }
            QPushButton:pressed {
                background-color: rgba(15, 23, 42, 0.14);
            }
        """)
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(10)
        btn_shadow.setColor(QColor(15, 23, 42, 15))
        btn_shadow.setOffset(0, 2)
        self.btn_toggle_sidebar.setGraphicsEffect(btn_shadow)
        self.btn_toggle_sidebar.clicked.connect(self.sidebar.toggle_collapse)
        header_h.addWidget(self.btn_toggle_sidebar)

        header_h.addStretch()

        self.btn_status = QPushButton("✨ AI Intelligence")
        self.btn_status.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #38BDF8;
                font-weight: 700;
                padding: 4px 10px;
                font-size: 11px;
                border: none;
            }
        """)
        header_h.addWidget(self.btn_status)

        # Logout button
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                font-weight: 600;
                border: none;
                padding: 4px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #EF4444;
            }
        """)
        self.btn_logout.clicked.connect(self.logout)
        header_h.addWidget(self.btn_logout)

        self.content_layout.addWidget(self.global_actions_bar)

        # Pages container
        self.pages_wrapper = NeumorphicFrame(radius=20, offset=4, blur=15)
        self.pages_wrapper.content_layout.setContentsMargins(20, 20, 20, 20)
        self.pages_container = QStackedWidget()
        self.pages_wrapper.add_widget(self.pages_container)
        self.content_layout.addWidget(self.pages_wrapper, 1)

        self.main_app_layout.addWidget(self.content_area, 1)

        # Initialize Pages
        self._init_pages()

        # Force layout system evaluation on tab switch
        self.pages_container.currentChanged.connect(self._force_layout_recalc)

        # Command Palette
        self.command_palette = CommandPaletteOverlay(self)
        self.command_palette.hide()

        # Global Styles
        self.setStyleSheet(get_global_stylesheet())

    def logout(self):
        crud.clear_session()
        if self.on_logout_callback:
            self.on_logout_callback()

    def _init_pages(self):
        self.pages_container.addWidget(DashboardPage(controller=self))  # 0
        self.pages_container.addWidget(ResumeBuilderPage(controller=self))  # 1
        self.pages_container.addWidget(LearningPage(controller=self))  # 2
        self.pages_container.addWidget(CommunityPage(controller=self))  # 3
        self.pages_container.addWidget(LearningRoadmapPage(controller=self))  # 4
        self.pages_container.addWidget(InterviewSimulatorPage(controller=self))  # 5
        self.pages_container.addWidget(AIMentorPage(controller=self))  # 6
        self.pages_container.addWidget(CourseDetailPage(controller=self))  # 7
        self.pages_container.addWidget(SettingsPage(controller=self))  # 8
        self.pages_container.addWidget(ChatPage(controller=self))  # 9
        self.pages_container.addWidget(ModernJobPortalPage(controller=self))  # 10
        self.pages_container.addWidget(ProfilePage(controller=self))  # 11

    def show_page(self, idx_or_name):
        if isinstance(idx_or_name, int):
            idx = idx_or_name
        else:
            mapping = {
                "DashboardPage": 0,
                "ResumeBuilderPage": 1,
                "LearningPage": 2,
                "CommunityPage": 3,
                "LearningRoadmapPage": 4,
                "InterviewSimulatorPage": 5,
                "AIMentorPage": 6,
                "CourseDetailPage": 7,
                "SettingsPage": 8,
                "ChatPage": 9,
                "JobPortalPage": 10,
                "ProfilePage": 11
            }
            idx = mapping.get(idx_or_name, 0)
        self.pages_container.setCurrentIndex(idx)
        
        # Trigger refresh on newly selected widget if defined
        active_widget = self.pages_container.widget(idx)
        if active_widget and hasattr(active_widget, "refresh"):
            active_widget.refresh()

    def overview_page_start_polling(self):
        dashboard = self.pages_container.widget(0)
        if dashboard and hasattr(dashboard, "refresh"):
            dashboard.refresh()

    def _force_layout_recalc(self, index):
        active_widget = self.pages_container.widget(index)
        if active_widget:
            active_widget.updateGeometry()
        self.pages_wrapper.content_layout.invalidate()
        self.pages_wrapper.content_layout.activate()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_K:
            self.command_palette.show_centered()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        print("Shutting down Application...")
        worker.stop_worker()
        event.accept()


class LoadingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F8FAFC;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        logo = QLabel("✦")
        logo.setStyleSheet("font-size: 48px; color: #38BDF8; font-weight: bold; background: transparent; border: none;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        self.label = QLabel("Restoring session...")
        self.label.setStyleSheet("font-size: 15px; font-weight: 600; color: #0F172A; background: transparent; border: none;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        progress = QProgressBar()
        progress.setRange(0, 0)  # Indeterminate
        progress.setFixedHeight(6)
        progress.setFixedWidth(200)
        progress.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 3px; } QProgressBar::chunk { background: #38BDF8; border-radius: 3px; }")
        layout.addWidget(progress, alignment=Qt.AlignmentFlag.AlignCenter)


class AppController(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Career Bridge - Authentication")
        self.resize(450, 650)  # Set reasonable size dedicated for Auth windows
        self.setMinimumSize(400, 550)

        # Setup Login
        self.login_page = LoginPage(
            on_login=self.handle_login,
            on_register_click=self.show_register
        )

        # Setup Register
        self.register_page = RegisterPage(
            on_back_click=self.show_login,
            on_register=self.handle_register
        )

        self.addWidget(self.login_page)  # Index 0
        self.addWidget(self.register_page)  # Index 1

        self.main_window = None

        # Check session on startup
        session = crud.get_session()
        if session:
            self.loading_page = LoadingPage()
            self.addWidget(self.loading_page)  # Index 2
            self.setCurrentIndex(2)
            
            from modules.auth_worker import SessionRestoreWorker
            self.restore_worker = SessionRestoreWorker(session["access_token"])
            self.restore_worker.success.connect(self.handle_restore_success)
            self.restore_worker.error.connect(self.handle_restore_error)
            self.restore_worker.start()
        else:
            self.show_login()

    def show_login(self):
        self.setCurrentIndex(0)

    def show_register(self):
        self.setCurrentIndex(1)

    def handle_restore_success(self, student_info):
        print(f"Session restored successfully: {student_info.get('email')}")
        self.show_main_app(student_info)

    def handle_restore_error(self, err_msg):
        print(f"Session restore failed: {err_msg}")
        crud.clear_session()
        self.show_login()

    def handle_login(self, student_info):
        print(f"Login success for: {student_info.get('email')}")
        self.show_main_app(student_info)

    def handle_register(self, res):
        print(f"Registration success for: {res.get('email')}")
        student_info = crud.get_current_student()
        self.show_main_app(student_info)

    def show_main_app(self, student_info=None):
        if not self.main_window:
            self.main_window = MainWindow(on_logout=self.handle_logout)

        if student_info:
            self.main_window.sidebar.update_user_info(
                student_info.get("display_name"),
                student_info.get("major")
            )
            
            context = student_info.get("context", {})
            if context.get("ai_status") == "PENDING":
                self.main_window.overview_page_start_polling()

        self.main_window.show()
        self.hide()

    def handle_logout(self):
        if self.main_window:
            self.main_window.hide()
        self.show()
        self.setCurrentIndex(0)


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    if sys.platform == "darwin":
        font = QFont("SF Pro Text", 10)
    app.setFont(font)

    controller = AppController()
    controller.show()

    sys.exit(app.exec())