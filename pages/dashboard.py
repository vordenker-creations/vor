import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QProgressBar, QFrame, QSizePolicy,
                             QScrollArea, QLineEdit, QGraphicsDropShadowEffect, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QCursor, QFont

from config import COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB
from components import SaaSCard, StatusPulse, CollapsiblePanel
from database import crud
from i18n import _

# Import sub-modules
from .dashboard_analytics.dashboard_analytics_overview import DashboardAnalyticsOverview
from .dashboard_operations.workspace_activity_operations_center import WorkspaceActivityOperationsCenter

def create_shadow():
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(15, 23, 42, 16))
    return shadow

class IconButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(36, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #E2E8F0;
                border-radius: 18px;
                color: #64748B;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                color: #0F172A;
            }
        """)

class SearchBar(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Search tasks, roadmap, or courses...")
        self.setFixedHeight(40)
        self.setMinimumWidth(260)
        self.setMaximumWidth(400)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 0 16px;
                color: #0F172A;
                font-size: 13px;
            }
            QLineEdit:hover {
                border: 1px solid #CBD5E1;
            }
            QLineEdit:focus {
                background-color: #FFFFFF;
                border: 1px solid #38BDF8;
            }
        """)

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            ModernCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """)
        self.setGraphicsEffect(create_shadow())
        
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(16, 16, 16, 16)
        self.internal_layout.setSpacing(8)

class KPICard(ModernCard):
    def __init__(self, title, value, change, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600;")
        self.internal_layout.addWidget(lbl_title)
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;")
        self.internal_layout.addWidget(lbl_val)
        
        lbl_change = QLabel(change)
        lbl_change.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 600;")
        self.internal_layout.addWidget(lbl_change)
        self.internal_layout.addStretch()

class DashboardOverviewView(QWidget):
    """The original dashboard content."""
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Central Workspace (Scrollable)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        
        self.central_workspace = QWidget()
        self.central_workspace.setStyleSheet("background-color: transparent;")
        self.central_layout = QVBoxLayout(self.central_workspace)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(20)
        
        self._build_welcome_area()
        self._build_analytics_row()
        self._build_roadmap_panel()
        self._build_upcoming_activities()
        self._build_productivity_insights()
        
        self.central_layout.addStretch()
        self.scroll_area.setWidget(self.central_workspace)
        layout.addWidget(self.scroll_area, stretch=1)
        
        # Right Assistant Panel (Collapsible)
        self.right_content = self._build_right_panel()
        self.right_content.setFixedWidth(320)
        self.right_panel = CollapsiblePanel(self.right_content, orientation="right")
        layout.addWidget(self.right_panel)

    def _build_welcome_area(self):
        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setGraphicsEffect(create_shadow())
        banner.setStyleSheet("""
            #BannerFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0F172A, stop:0.6 #1E293B, stop:1 #0284C7);
                border: none;
                border-radius: 16px;
            }
        """)
        l = QHBoxLayout(banner); l.setContentsMargins(32, 24, 32, 24)
        left = QVBoxLayout(); left.setSpacing(0)
        
        student = crud.get_current_student()
        first_name = student["full_name"].split(" ")[-1] if student and student.get("full_name") else "Khoa"
        
        greeting = QLabel(f"Good Morning, {first_name}.")
        greeting.setStyleSheet("color: white; font-size: 26px; font-weight: 800; letter-spacing: -1px; background: transparent;")
        summary = QLabel("✨ You have 3 tasks due today, and you're 80% ready for your Cloud Developer milestone.")
        summary.setStyleSheet("color: #94A3B8; font-size: 14px; margin-top: 6px; margin-bottom: 20px; background: transparent;")
        summary.setWordWrap(True)
        left.addWidget(greeting); left.addWidget(summary)
        
        actions = QHBoxLayout(); actions.setSpacing(10)
        def create_btn(text, icon, is_primary=False):
            btn = QPushButton(f"{icon} {text}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor); btn.setFixedHeight(36)
            if is_primary:
                btn.setStyleSheet("background: #38BDF8; color: #0F172A; font-weight: 700; font-size: 13px; border-radius: 18px; padding: 0 16px; border: none;")
            else:
                btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; font-weight: 600; font-size: 13px; border-radius: 18px; padding: 0 16px; border: 1px solid rgba(255,255,255,0.2);")
            return btn
        
        btn_connect = create_btn("Connect Mentor", "💬")
        btn_connect.clicked.connect(lambda: self.controller.show_page("ChatPage") if self.controller else None)
        actions.addWidget(create_btn("Add Task", "+", True))
        actions.addWidget(create_btn("View Roadmap", "🗺️"))
        actions.addWidget(create_btn("Generate AI Plan", "✨"))
        actions.addWidget(btn_connect); actions.addStretch()
        ac_w = QWidget(); ac_w.setLayout(actions); ac_w.setStyleSheet("background:transparent;"); left.addWidget(ac_w)
        l.addLayout(left, 1)
        
        rocket = QLabel("🚀"); rocket.setStyleSheet("font-size: 56px; background: transparent;")
        glow = QGraphicsDropShadowEffect(); glow.setBlurRadius(30); glow.setColor(QColor(56, 189, 248, 80)); rocket.setGraphicsEffect(glow)
        l.addWidget(rocket, alignment=Qt.AlignmentFlag.AlignCenter)
        self.central_layout.addWidget(banner)

    def _build_analytics_row(self):
        row = QWidget(); layout = QHBoxLayout(row); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(16)
        layout.addWidget(KPICard("Academic Progress", "75%", "+5% this week", "#10B981"))
        layout.addWidget(KPICard("Tasks Completed", "12", "4 pending today", "#F59E0B"))
        layout.addWidget(KPICard("Career Readiness", "80%", "Cloud Dev Role", "#38BDF8"))
        layout.addWidget(KPICard("Community Activity", "350 pts", "Top 10% Contributor", "#8B5CF6"))
        self.central_layout.addWidget(row)

    def _build_roadmap_panel(self):
        container = QWidget(); layout = QVBoxLayout(container); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(12)
        header = QHBoxLayout(); title = QLabel("Academic Roadmap"); title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;"); header.addWidget(title); header.addStretch()
        view_all = QPushButton("View Full Timeline"); view_all.setStyleSheet("color: #38BDF8; font-weight: 600; border: none; background: transparent;"); view_all.setCursor(Qt.CursorShape.PointingHandCursor); header.addWidget(view_all); layout.addLayout(header)
        cards = QHBoxLayout(); cards.setSpacing(16)
        
        def create_card(course, status, color, progress):
            card = ModernCard(); cl = card.internal_layout
            badge = QLabel(status); badge.setStyleSheet(f"color: {color}; background: {color}15; font-size: 10px; font-weight: 700; padding: 3px 6px; border-radius: 4px;"); cl.addWidget(badge, alignment=Qt.AlignmentFlag.AlignLeft)
            lbl = QLabel(course); lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600; margin-top: 6px;"); cl.addWidget(lbl)
            bar = QProgressBar(); bar.setFixedHeight(4); bar.setValue(progress); bar.setTextVisible(False); bar.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border: none; border-radius: 2px; }} QProgressBar::chunk {{ background: {color}; border-radius: 2px; }}"); cl.addWidget(bar); return card

        # Deep Integration: Read from local SQLite
        student = crud.get_current_student()
        courses = student.get("context", {}).get("roadmap", []) if student else []

        if not courses:
            # Fallback to mock data if the DB is empty
            courses = [
                {"title": "Web Dev Fundamentals", "status": "Completed", "progress": 100},
                {"title": "Advanced React & PyQt", "status": "In Progress", "progress": 65},
                {"title": "Cloud Deployment", "status": "Upcoming", "progress": 0}
            ]

        for course in courses:
            status = course["status"]
            if status == "Completed":
                color = "#10B981"
            elif status == "In Progress":
                color = "#38BDF8"
            else:
                color = "#94A3B8"
                
            cards.addWidget(create_card(course["title"], status, color, course["progress"]))

        layout.addLayout(cards); self.central_layout.addWidget(container)

    def _build_upcoming_activities(self):
        container = QWidget(); layout = QHBoxLayout(container); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(20)
        tasks = ModernCard(); tl = tasks.internal_layout; t_header = QLabel("Upcoming Tasks"); t_header.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); tl.addWidget(t_header)
        def add_task(title, tag, color):
            w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0, 0, 0, 0)
            chk = QFrame(); chk.setFixedSize(14, 14); chk.setStyleSheet("border: 2px solid #CBD5E1; border-radius: 3px;"); l.addWidget(chk)
            lbl = QLabel(title); lbl.setStyleSheet("color: #334155; font-size: 13px; font-weight: 500;"); l.addWidget(lbl); l.addStretch()
            badge = QLabel(tag); badge.setStyleSheet(f"color: {color}; background: {color}15; font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 4px;"); l.addWidget(badge); tl.addWidget(w)
        add_task("Finish UI mockups for Module 2", "High", "#EF4444")
        add_task("Review Peer PR #42", "Medium", "#F59E0B")
        add_task("Read Chapter 5: System Design", "Low", "#3B82F6"); tl.addStretch(); layout.addWidget(tasks, stretch=1)
        cal = ModernCard(); cl = cal.internal_layout; c_header = QLabel("Schedule"); c_header.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); cl.addWidget(c_header)
        def add_event(time, title, active=False):
            w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0, 0, 0, 0); l.setSpacing(10)
            tm = QLabel(time); tm.setStyleSheet(f"color: {'#38BDF8' if active else '#64748B'}; font-size: 12px; font-weight: 600; min-width: 40px;"); l.addWidget(tm)
            line = QFrame(); line.setFixedWidth(2); line.setStyleSheet(f"background: {'#38BDF8' if active else '#E2E8F0'}; border-radius: 1px;"); l.addWidget(line)
            desc = QLabel(title); desc.setStyleSheet(f"color: {'#0F172A' if active else '#475569'}; font-size: 13px; font-weight: {'600' if active else '500'};"); l.addWidget(desc); l.addStretch(); cl.addWidget(w)
        add_event("10:00", "Algorithm Lab Sync"); add_event("14:00", "Mentoring: Career in Cloud", True); add_event("16:30", "Project Group Meet"); cl.addStretch(); layout.addWidget(cal, stretch=1); self.central_layout.addWidget(container)

    def _build_productivity_insights(self):
        container = QWidget(); layout = QHBoxLayout(container); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(20)
        graph = ModernCard(); gl = graph.internal_layout; t = QLabel("Productivity & Focus"); t.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); gl.addWidget(t)
        mock = QLabel("[ Productivity Graph Visualization ]"); mock.setAlignment(Qt.AlignmentFlag.AlignCenter); mock.setStyleSheet("color: #94A3B8; font-size: 12px; background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 10px; min-height: 100px;"); gl.addWidget(mock); layout.addWidget(graph, stretch=2)
        ai = ModernCard(); al = ai.internal_layout; t2 = QLabel("✨ Learning Insights"); t2.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); al.addWidget(t2)
        msg = QLabel("You've been studying System Design 30% more this week. Based on your roadmap, you might want to start working on your capstone architecture draft soon."); msg.setWordWrap(True); msg.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.4;"); al.addWidget(msg); al.addStretch(); layout.addWidget(ai, stretch=1); self.central_layout.addWidget(container)

    def _build_right_panel(self):
        panel = QFrame(); panel.setStyleSheet("background-color: transparent; border: none;"); layout = QVBoxLayout(panel); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(20)
        ai = ModernCard(); al = ai.internal_layout; al.setSpacing(12); h = QHBoxLayout(); h.addWidget(StatusPulse(size=8, color="#8B5CF6")); t = QLabel("AI Assistant"); t.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); h.addWidget(t); h.addStretch(); al.addLayout(h)
        msg = QLabel("I noticed you have a mentoring session at 2 PM. Would you like me to prepare a list of questions about Cloud Architecture based on your recent activity?"); msg.setWordWrap(True); msg.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.4;"); al.addWidget(msg)
        btn = QPushButton("✨ Prepare Questions"); btn.setFixedHeight(30); btn.setCursor(Qt.CursorShape.PointingHandCursor); btn.setStyleSheet("background: #38BDF8; color: white; font-weight: 700; border-radius: 15px; font-size: 11px;"); al.addWidget(btn); layout.addWidget(ai)
        notif = ModernCard(); nl = notif.internal_layout; t2 = QLabel("Recent Notifications"); t2.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); nl.addWidget(t2)
        def add_n(t, time, icon="📌"):
            w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0, 0, 0, 0); ic = QLabel(icon); ic.setStyleSheet("font-size: 14px;"); l.addWidget(ic)
            v = QVBoxLayout(); v.setSpacing(2); t_l = QLabel(t); t_l.setStyleSheet("color: #334155; font-size: 12px; font-weight: 500;"); t_l.setWordWrap(True); v.addWidget(t_l)
            tm = QLabel(time); tm.setStyleSheet("color: #94A3B8; font-size: 10px;"); v.addWidget(tm); l.addLayout(v); nl.addWidget(w)
        add_n("Prof. Alan posted a new grade", "10 min ago", "🎓"); add_n("Your AWS Student creds expire soon", "1 hour ago", "⚠️"); layout.addWidget(notif)
        act = ModernCard(); acl = act.internal_layout; t3 = QLabel("Recent Activity"); t3.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;"); acl.addWidget(t3)
        def add_a(a, time):
            w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0, 0, 0, 0); l.setSpacing(10); dot = QFrame(); dot.setFixedSize(6, 6); dot.setStyleSheet("background: #CBD5E1; border-radius: 3px;"); l.addWidget(dot)
            v = QVBoxLayout(); v.setSpacing(2); t_l = QLabel(a); t_l.setStyleSheet("color: #475569; font-size: 12px;"); t_l.setWordWrap(True); v.addWidget(t_l)
            tm = QLabel(time); tm.setStyleSheet("color: #94A3B8; font-size: 10px;"); v.addWidget(tm); l.addLayout(v); acl.addWidget(w)
        add_a("Completed 'React Hooks' Quiz", "Yesterday"); add_a("Joined 'Cloud Engineers' Group", "Yesterday"); add_a("Updated Resume PDF", "2 days ago"); layout.addWidget(act); layout.addStretch(); return panel

class DashboardPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # 1. Top Toolbar (Header)
        self.header = self._build_header()
        root_layout.addWidget(self.header)
        
        # Separator line
        line = QFrame(); line.setFrameShape(QFrame.Shape.HLine); line.setStyleSheet("background-color: #E2E8F0; max-height: 1px; border: none;"); root_layout.addWidget(line)
        
        # 2. Main Stacked Workspace
        self.view_stack = QStackedWidget()
        
        # View 0: Standard Overview
        self.overview_view = DashboardOverviewView(controller=self.controller)
        self.view_stack.addWidget(self.overview_view)
        
        # View 1: Analytics Overview
        self.analytics_view = DashboardAnalyticsOverview(controller=self.controller)
        self.view_stack.addWidget(self.analytics_view)
        
        # View 2: Workspace Activity & Live Ops
        self.activity_view = WorkspaceActivityOperationsCenter(controller=self.controller)
        self.view_stack.addWidget(self.activity_view)
        
        root_layout.addWidget(self.view_stack)

    def _build_header(self):
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)
        
        # Sidebar Toggle
        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setFixedSize(40, 40)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #000000;
                border-radius: 12px;
                font-size: 19px;
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
        self.btn_toggle.setGraphicsEffect(btn_shadow)
        
        if self.controller and hasattr(self.controller, 'sidebar'):
            self.btn_toggle.clicked.connect(self.controller.sidebar.toggle_collapse)
        layout.addWidget(self.btn_toggle)

        # Logo/Title
        title_lbl = QLabel("Dashboard")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(title_lbl)
        
        # Tab Switcher
        tab_container = QFrame()
        tab_container.setStyleSheet("background: #F1F5F9; border-radius: 12px; padding: 2px;")
        tl = QHBoxLayout(tab_container)
        tl.setContentsMargins(2, 2, 2, 2)
        tl.setSpacing(4)
        
        self.btn_overview = QPushButton("Overview")
        self.btn_analytics = QPushButton("Analytics")
        self.btn_activity = QPushButton("Activity")
        
        tab_style = """
            QPushButton {
                border: none; border-radius: 10px; padding: 8px 16px;
                font-size: 13px; font-weight: 700; color: #64748B;
            }
            QPushButton:checked {
                background: white; color: #0F172A;
            }
        """
        self.btn_overview.setStyleSheet(tab_style); self.btn_overview.setCheckable(True); self.btn_overview.setChecked(True)
        self.btn_analytics.setStyleSheet(tab_style); self.btn_analytics.setCheckable(True)
        self.btn_activity.setStyleSheet(tab_style); self.btn_activity.setCheckable(True)
        
        self.btn_overview.clicked.connect(lambda: self._set_view(0))
        self.btn_analytics.clicked.connect(lambda: self._set_view(1))
        self.btn_activity.clicked.connect(lambda: self._set_view(2))
        
        tl.addWidget(self.btn_overview); tl.addWidget(self.btn_analytics); tl.addWidget(self.btn_activity)
        layout.addWidget(tab_container)
        
        layout.addStretch()
        
        # Search
        layout.addWidget(SearchBar())
        
        # Icons
        layout.addWidget(IconButton("📅"))
        layout.addWidget(IconButton("🔔"))
        
        avatar_btn = IconButton("KH")
        avatar_btn.setStyleSheet("QPushButton { background-color: #2DD4BF; color: white; border: none; border-radius: 18px; font-weight: 800; }")
        layout.addWidget(avatar_btn)
        
        return header

    def _set_view(self, idx):
        self.view_stack.setCurrentIndex(idx)
        self.btn_overview.setChecked(idx == 0)
        self.btn_analytics.setChecked(idx == 1)
        self.btn_activity.setChecked(idx == 2)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    page = DashboardPage()
    page.resize(1400, 900)
    page.show()
    sys.exit(app.exec())
