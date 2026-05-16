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
from pages.chat_ui import ChatPage
from login import LoginPage
from register import RegisterPage

from neumorphic_components import NeumorphicFrame, NeumorphicButton, GlowingButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Career Bridge | Masterclass")
        self.resize(1300, 900)
        
        # Pre-calculate decorative elements
        import random
        random.seed(42)
        self.bg_circles = [(random.randint(0, 1300), random.randint(0, 900), random.randint(50, 300)) for _ in range(10)]
        self.network_nodes = [(random.randint(800, 1300), random.randint(0, 400)) for _ in range(8)]

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Auth Pages
        self.login_page = LoginPage(on_login=self._handle_login, on_register_click=lambda: self.central_widget.setCurrentIndex(1))
        self.register_page = RegisterPage(on_back_click=lambda: self.central_widget.setCurrentIndex(0), on_register=self._handle_registration_success)
        self.central_widget.addWidget(self.login_page)    # 0
        self.central_widget.addWidget(self.register_page) # 1
        
        # Main App Layout (Shell)
        self.main_app_widget = QWidget()
        self.main_app_layout = QHBoxLayout(self.main_app_widget)
        self.main_app_layout.setContentsMargins(15, 15, 15, 15)
        self.main_app_layout.setSpacing(20)
        
        self._setup_sidebar()
        
        # Container for pages with a slight margin
        self.pages_wrapper = NeumorphicFrame(radius=30, offset=10, blur=25)
        self.pages_container = QStackedWidget()
        self.pages_wrapper.add_widget(self.pages_container)
        self.main_app_layout.addWidget(self.pages_wrapper, 1)
        
        self.pages_container.addWidget(DashboardPage(controller=self))   # 0
        self.pages_container.addWidget(ProfilePage(controller=self))     # 1
        self.pages_container.addWidget(LearningPage(controller=self))    # 2
        self.pages_container.addWidget(CommunityPage(controller=self))   # 3
        self.pages_container.addWidget(RoadmapPage(controller=self))     # 4
        self.pages_container.addWidget(RecruitmentPage(controller=self)) # 5
        self.pages_container.addWidget(AIMentorPage(controller=self))    # 6
        self.pages_container.addWidget(CourseDetailPage(controller=self))# 7
        self.pages_container.addWidget(SettingsPage(controller=self))    # 8
        self.pages_container.addWidget(ChatPage(controller=self))        # 9
        
        self.central_widget.addWidget(self.main_app_widget) # 2
        self.setStyleSheet(get_global_stylesheet())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Subtle Background Geometry
        painter.setPen(QPen(QColor(30, 95, 116, 15), 1))
        for x, y, r in self.bg_circles:
            painter.drawEllipse(QPoint(x, y), r, r)
            
        # Network lines
        painter.setPen(QPen(QColor(30, 95, 116, 30), 1))
        for i in range(len(self.network_nodes)):
            for j in range(i + 1, len(self.network_nodes)):
                p1 = self.network_nodes[i]
                p2 = self.network_nodes[j]
                # Distance check to only connect close nodes
                dist = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
                if dist < 300:
                    painter.drawLine(p1[0], p1[1], p2[0], p2[1])

    def _setup_sidebar(self):
        # Update main app layout to make sidebar flush with the left edge
        self.main_app_layout.setContentsMargins(0, 0, 20, 0)
        
        self.sidebar_container = QFrame()
        self.sidebar_container.setFixedWidth(80)
        self.sidebar_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-right: 1px solid #E2E8F0;
            }
        """)
        
        # Soft Drop Shadow for the Sidebar
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(4)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.sidebar_container.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self.sidebar_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(10)
        
        # 1. Clean Logo Icon (Text removed as per ICON-ONLY requirement)
        logo = QLabel("✦")
        logo.setStyleSheet("font-size: 28px; color: #38BDF8; font-weight: bold; margin-bottom: 24px; border: none; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        
        # 2. ICON-ONLY BUTTONS IN PRECISE ORDER
        # (Icon, Page Index)
        nav_config = [
            ("📊", 0), # Dashboard
            ("🪪", 1), # Profile & CV
            ("🗺️", 4), # Academic Roadmap
            ("🗓️", 2), # Study Tasks & Calendar
            ("💼", 5), # Job Portal
            ("🪄", 6), # AI Mentor
            ("🌐", 3), # Community
            ("💬", 9), # Messages/Chat
            ("⚙️", 8), # Settings
        ]
        
        for icon, idx in nav_config:
            btn = self._create_nav_button(icon, idx)
            layout.addWidget(btn)
            self.nav_group.addButton(btn, idx)
            if idx == 0: btn.setChecked(True)
        
        self.main_app_layout.insertWidget(0, self.sidebar_container)

    def _create_nav_button(self, icon, idx):
        btn = QPushButton(icon)
        btn.setCheckable(True)
        btn.setFixedSize(80, 64)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # UI/UX STYLING PER REQUIREMENTS
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #64748B;
                font-size: 22px;
                border: none;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                border-radius: 16px;
                margin: 4px 10px;
            }
            QPushButton:checked {
                background-color: #E0F2FE;
                color: #0284C7;
                border-left: 4px solid #38BDF8;
                border-radius: 0px;
                margin: 0px;
            }
        """)
        
        btn.clicked.connect(lambda ch, i=idx: self.pages_container.setCurrentIndex(i))
        return btn

    def show_page(self, name):
        mapping = {"DashboardPage":0, "ProfilePage":1, "LearningPage":2, "CommunityPage":3, "RoadmapPage":4, "RecruitmentPage":5, "AIMentorPage":6, "CourseDetailPage":7, "SettingsPage":8, "ChatPage":9}
        idx = mapping.get(name, 0)
        self.pages_container.setCurrentIndex(idx)
        btn = self.nav_group.button(idx)
        if btn: btn.setChecked(True)
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
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    if sys.platform == "darwin": font = QFont("SF Pro Text", 10)
    app.setFont(font); window = MainWindow(); window.show(); sys.exit(app.exec())
