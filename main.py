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
        self.sidebar_container = NeumorphicFrame(radius=30, offset=8, blur=20)
        self.sidebar_container.setFixedWidth(100)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        
        # App Logo
        logo = QLabel("AI")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 24px; font-weight: 900; color: #1E5F74; margin-bottom: 20px;")
        layout.addWidget(logo)
        
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        
        from i18n import _
        nav = [
            ("📊", 0, _("nav_dashboard")), 
            ("👤", 1, _("nav_profile")), 
            ("🎨", 2, _("nav_learning")), 
            ("👥", 3, _("nav_community")), 
            ("🧭", 4, _("nav_roadmap")), 
            ("💼", 5, _("nav_recruitment")), 
            ("🤖", 6, _("nav_ai_mentor")),
            ("⚙️", 8, "Settings"),
            ("💬", 9, "Chat")
        ]
        
        for icon, idx, tooltip in nav:
            btn = QPushButton(icon)
            btn.setCheckable(True)
            btn.setFixedSize(60, 60)
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._nav_style())
            btn.clicked.connect(lambda ch, i=idx: self.pages_container.setCurrentIndex(i))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.nav_group.addButton(btn, idx)
            if idx == 0: btn.setChecked(True)
        
        self.sidebar_container.content_layout.addLayout(layout)
        self.main_app_layout.addWidget(self.sidebar_container)

    def _nav_style(self):
        return f"""
            QPushButton {{ 
                background: transparent; 
                color: {COLOR_TEXT_SUB}; 
                font-size: 22px; 
                border-radius: 16px; 
                border: 1px solid transparent;
                padding: 10px;
            }} 
            QPushButton:hover {{ 
                background: rgba(255, 255, 255, 0.4);
                color: {COLOR_PRIMARY};
            }} 
            QPushButton:checked {{ 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(30, 95, 116, 0.1), stop:1 rgba(30, 95, 116, 0.05));
                color: {COLOR_PRIMARY}; 
                border: 1px solid rgba(30, 95, 116, 0.3);
            }}
        """

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
