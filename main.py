import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from core.config import *
from database import crud
from modules.sync_worker import worker
from modules.local_storage import local_data

# Authentication Pages
from pages.auth.login import LoginPage
from pages.auth.register import RegisterPage

from pages.dashboard import DashboardPage
from pages.profile import ProfilePage
from pages.study_tasks.smart_task_planner import SmartTaskPlanner
from pages.settings import SettingsPage
from pages.learning_roadmap import LearningRoadmapPage
from pages.recruitment import RecruitmentPage
from pages.code_lab import CodeLabPage
from pages.mock_interviews import MockInterviewsPage
from pages.project_portfolio import ProjectPortfolioPage
from pages.cv_builder import CVBuilderPage
from pages.community_chat import CommunityChatPage
from pages.skill_tree import SkillTreePage
from ui_core.sidebar_component import SidebarComponent
from ui_core.neumorphic_components import NeumorphicFrame


class MainWindow(QMainWindow):
    def __init__(self, on_logout=None):
        super().__init__()
        worker.start_worker()
        self.on_logout_callback = on_logout
        self.is_dark_mode = False
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
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(20)

        # Pages container
        self.pages_wrapper = NeumorphicFrame(radius=20, offset=4, blur=15)
        self.pages_wrapper.content_layout.setContentsMargins(16, 16, 16, 16)
        self.pages_container = QStackedWidget()
        self.pages_wrapper.add_widget(self.pages_container)
        self.content_layout.addWidget(self.pages_wrapper, 1)

        self.main_app_layout.addWidget(self.content_area, 1)

        # Initialize Pages
        self._init_pages()

        # Force layout system evaluation on tab switch
        self.pages_container.currentChanged.connect(self._force_layout_recalc)

        # Global Styles
        self.setStyleSheet(get_global_stylesheet())

        # Restore last viewed tab from local storage
        last_tab = local_data.get("ui.last_tab", 0)
        if isinstance(last_tab, int) and 0 <= last_tab < self.pages_container.count():
            self.pages_container.setCurrentIndex(last_tab)
            # Also check the corresponding sidebar button
            btn = self.sidebar.button_group.button(last_tab)
            if btn:
                btn.setChecked(True)

    def logout(self):
        crud.clear_session()
        if self.on_logout_callback:
            self.on_logout_callback()

    def toggle_theme(self):
        pass

    def _apply_theme_globally(self, is_dark):
        from core.config import apply_theme
        
        # Apply theme recursively to all top-level windows and dialogs
        for widget in QApplication.topLevelWidgets():
            try:
                apply_theme(widget)
            except Exception:
                continue

    def _init_pages(self):
        self.pages_container.addWidget(DashboardPage(controller=self))  # 0
        self.pages_container.addWidget(QWidget())  # 1 placeholder for index keeping
        self.pages_container.addWidget(SmartTaskPlanner(controller=self))  # 2
        self.pages_container.addWidget(CodeLabPage(controller=self))  # 3
        self.pages_container.addWidget(LearningRoadmapPage(controller=self))  # 4
        self.pages_container.addWidget(MockInterviewsPage(controller=self))  # 5
        self.pages_container.addWidget(RecruitmentPage(controller=self))  # 6
        self.pages_container.addWidget(ProjectPortfolioPage(controller=self))  # 7
        self.pages_container.addWidget(SettingsPage(controller=self))  # 8
        self.pages_container.addWidget(CVBuilderPage(controller=self))  # 9 CV Builder
        self.pages_container.addWidget(CommunityChatPage(controller=self))  # 10 Community Chat
        self.pages_container.addWidget(ProfilePage(controller=self))  # 11
        self.pages_container.addWidget(SkillTreePage(controller=self))  # 12 AI Skill Tree

    def show_page(self, idx_or_name):
        if isinstance(idx_or_name, int):
            idx = idx_or_name
        else:
            mapping = {
                "DashboardPage": 0,
                "SmartTaskPlanner": 2,
                "CodeAlgorithmLab": 3,
                "LearningRoadmapPage": 4,
                "MockInterviews": 5,
                "RecruitmentPage": 6,
                "ProjectPortfolio": 7,
                "SettingsPage": 8,
                "CVBuilder": 9,
                "CommunityChat": 10,
                "ProfilePage": 11,
                "SkillTree": 12
            }
            idx = mapping.get(idx_or_name, 0)
        self.pages_container.setCurrentIndex(idx)

        # Persist last viewed tab
        local_data.save("ui.last_tab", idx)
        
        # Trigger refresh on newly selected widget if defined
        active_widget = self.pages_container.widget(idx)
        if active_widget and hasattr(active_widget, "refresh"):
            active_widget.refresh()
            
        # Ensure any dynamically created widgets during refresh are themed correctly
        self._apply_theme_globally(self.is_dark_mode)

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

    def closeEvent(self, event):
        print("Shutting down Application...")
        # Persist local data to disk
        local_data.save_to_disk()
        worker.stop_worker()
        # Clean up recruitment page background threads
        try:
            recruitment_page = self.pages_container.widget(6)
            if recruitment_page and hasattr(recruitment_page, "cleanup"):
                recruitment_page.cleanup()
        except Exception as e:
            print(f"Error during recruitment cleanup: {e}")
        event.accept()


class ComingSoonPage(QWidget):
    def __init__(self, title_text="Coming Soon", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F8FAFC;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel(title_text)
        lbl.setStyleSheet("color: #64748B; font-size: 24px; font-weight: 700; background: transparent; border: none;")
        layout.addWidget(lbl)

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


import traceback

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handle unhandled exceptions to prevent PyQt6 from crashing with SIGABRT"""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled Exception:\n{error_msg}", file=sys.stderr)

sys.excepthook = global_exception_handler

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