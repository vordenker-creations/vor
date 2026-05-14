import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QProgressBar, QFrame, QSizePolicy,
                             QScrollArea, QLineEdit, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QCursor

from config import COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB
from components import SaaSCard, StatusPulse
from i18n import _

def create_shadow():
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 10))
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

class ActionButton(QPushButton):
    def __init__(self, text, icon="", is_primary=False, parent=None):
        super().__init__(f"{icon} {text}" if icon else text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(36)
        
        if is_primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #38BDF8;
                    color: white;
                    font-weight: 600;
                    font-size: 13px;
                    border-radius: 18px;
                    padding: 0 16px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #0EA5E9;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #0F172A;
                    font-weight: 600;
                    font-size: 13px;
                    border-radius: 18px;
                    padding: 0 16px;
                    border: 1px solid #E2E8F0;
                }
                QPushButton:hover {
                    background-color: #F8FAFC;
                    border: 1px solid #CBD5E1;
                }
            """)

class SearchBar(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Search tasks, roadmap, or courses... (Ctrl+K)")
        self.setFixedHeight(40)
        self.setMinimumWidth(350)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #F1F5F9;
                border: 1px solid transparent;
                border-radius: 20px;
                padding: 0 16px;
                color: #0F172A;
                font-size: 13px;
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
                border-radius: 20px;
            }
        """)
        self.setGraphicsEffect(create_shadow())
        
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)
        self.internal_layout.setSpacing(12)

class KPICard(ModernCard):
    def __init__(self, title, value, change, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 600;")
        self.internal_layout.addWidget(lbl_title)
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #0F172A; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;")
        self.internal_layout.addWidget(lbl_val)
        
        lbl_change = QLabel(change)
        lbl_change.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 600;")
        self.internal_layout.addWidget(lbl_change)
        self.internal_layout.addStretch()

class DashboardPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # 1. Top Toolbar (Header)
        root_layout.addWidget(self._build_header())
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #E2E8F0; max-height: 1px; border: none;")
        root_layout.addWidget(line)
        
        # Body Layout
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(24, 24, 24, 24)
        body_layout.setSpacing(24)
        
        # 2. Central Workspace (Scrollable)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        
        self.central_workspace = QWidget()
        self.central_workspace.setStyleSheet("background-color: transparent;")
        self.central_layout = QVBoxLayout(self.central_workspace)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(24)
        
        self._build_welcome_area()
        self._build_analytics_row()
        self._build_roadmap_panel()
        self._build_upcoming_activities()
        self._build_productivity_insights()
        
        self.central_layout.addStretch()
        self.scroll_area.setWidget(self.central_workspace)
        
        body_layout.addWidget(self.scroll_area, stretch=1)
        
        # 3. Right Assistant Panel
        body_layout.addWidget(self._build_right_panel())
        
        root_layout.addWidget(body_widget)

    def _build_header(self):
        header = QWidget()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)
        
        # Breadcrumbs
        breadcrumbs = QLabel("Dashboard  /  <b>Spring Semester</b>")
        breadcrumbs.setStyleSheet("color: #64748B; font-size: 14px;")
        layout.addWidget(breadcrumbs)
        
        layout.addStretch()
        
        # Search
        layout.addWidget(SearchBar())
        
        # Icons
        layout.addWidget(IconButton("📅"))
        layout.addWidget(IconButton("🔔"))
        layout.addWidget(IconButton("✨")) # AI assistant quick button
        
        avatar_btn = IconButton("KH")
        avatar_btn.setStyleSheet(avatar_btn.styleSheet() + "QPushButton { background-color: #2DD4BF; color: white; border: none; }")
        layout.addWidget(avatar_btn)
        
        return header

    def _build_welcome_area(self):
        banner = ModernCard()
        banner.setStyleSheet("""
            ModernCard {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E0F2FE, stop:1 #CCFBF1);
                border: 1px solid #BAE6FD;
                border-radius: 20px;
            }
        """)
        
        layout = banner.internal_layout
        layout.setContentsMargins(32, 32, 32, 32)
        
        greeting = QLabel("Good Morning, Khoa.")
        greeting.setStyleSheet("color: #0F172A; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; background: transparent;")
        layout.addWidget(greeting)
        
        summary = QLabel("✨ You have 3 tasks due today, and you're 80% ready for your Cloud Developer milestone.")
        summary.setStyleSheet("color: #334155; font-size: 15px; margin-top: 4px; margin-bottom: 12px; background: transparent;")
        layout.addWidget(summary)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        actions_layout.addWidget(ActionButton("Add Task", "+", is_primary=True))
        actions_layout.addWidget(ActionButton("View Roadmap", "🗺️"))
        actions_layout.addWidget(ActionButton("Generate AI Plan", "✨"))
        actions_layout.addWidget(ActionButton("Connect Mentor", "💬"))
        actions_layout.addStretch()
        
        # Use an inner widget for background transparency trick
        actions_container = QWidget()
        actions_container.setStyleSheet("background: transparent;")
        actions_container.setLayout(actions_layout)
        layout.addWidget(actions_container)
        
        self.central_layout.addWidget(banner)

    def _build_analytics_row(self):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        layout.addWidget(KPICard("Academic Progress", "75%", "+5% this week", "#10B981"))
        layout.addWidget(KPICard("Tasks Completed", "12", "4 pending today", "#F59E0B"))
        layout.addWidget(KPICard("Career Readiness", "80%", "Cloud Dev Role", "#38BDF8"))
        layout.addWidget(KPICard("Community Activity", "350 pts", "Top 10% Contributor", "#8B5CF6"))
        
        self.central_layout.addWidget(row)

    def _build_roadmap_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        header = QHBoxLayout()
        title = QLabel("Academic Roadmap")
        title.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()
        view_all = QPushButton("View Full Timeline")
        view_all.setStyleSheet("color: #38BDF8; font-weight: 600; border: none; background: transparent;")
        view_all.setCursor(Qt.CursorShape.PointingHandCursor)
        header.addWidget(view_all)
        layout.addLayout(header)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        def create_roadmap_card(course, status, color, progress):
            card = ModernCard()
            cl = card.internal_layout
            
            badge = QLabel(status)
            badge.setStyleSheet(f"color: {color}; background-color: {color}20; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 6px;")
            badge.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            cl.addWidget(badge)
            
            lbl = QLabel(course)
            lbl.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 600; margin-top: 8px;")
            cl.addWidget(lbl)
            
            bar = QProgressBar()
            bar.setFixedHeight(6)
            bar.setValue(progress)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"""
                QProgressBar {{ background-color: #F1F5F9; border: none; border-radius: 3px; }}
                QProgressBar::chunk {{ background-color: {color}; border-radius: 3px; }}
            """)
            cl.addWidget(bar)
            
            return card

        cards_layout.addWidget(create_roadmap_card("Web Dev Fundamentals", "Completed", "#10B981", 100))
        cards_layout.addWidget(create_roadmap_card("Advanced React & PyQt", "In Progress", "#38BDF8", 65))
        cards_layout.addWidget(create_roadmap_card("Cloud Deployment", "Upcoming", "#94A3B8", 0))
        
        layout.addLayout(cards_layout)
        self.central_layout.addWidget(container)

    def _build_upcoming_activities(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Tasks Panel (left)
        tasks_panel = ModernCard()
        tl = tasks_panel.internal_layout
        
        t_header = QLabel("Upcoming Tasks")
        t_header.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        tl.addWidget(t_header)
        
        def add_task(title, tag, color):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            chk = QFrame()
            chk.setFixedSize(16, 16)
            chk.setStyleSheet("border: 2px solid #CBD5E1; border-radius: 4px;")
            l.addWidget(chk)
            lbl = QLabel(title)
            lbl.setStyleSheet("color: #334155; font-size: 14px; font-weight: 500;")
            l.addWidget(lbl)
            l.addStretch()
            badge = QLabel(tag)
            badge.setStyleSheet(f"color: {color}; background-color: {color}20; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px;")
            l.addWidget(badge)
            tl.addWidget(w)
        
        add_task("Finish UI mockups for Module 2", "High", "#EF4444")
        add_task("Review Peer PR #42", "Medium", "#F59E0B")
        add_task("Read Chapter 5: System Design", "Low", "#3B82F6")
        tl.addStretch()
        
        layout.addWidget(tasks_panel, stretch=1)
        
        # Calendar Panel (right)
        cal_panel = ModernCard()
        cl = cal_panel.internal_layout
        
        c_header = QLabel("Schedule")
        c_header.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        cl.addWidget(c_header)
        
        def add_event(time_str, title, is_active=False):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(12)
            
            tm = QLabel(time_str)
            tm.setStyleSheet(f"color: {'#38BDF8' if is_active else '#64748B'}; font-size: 13px; font-weight: 600; min-width: 45px;")
            l.addWidget(tm)
            
            line = QFrame()
            line.setFixedWidth(2)
            line.setStyleSheet(f"background-color: {'#38BDF8' if is_active else '#E2E8F0'};")
            l.addWidget(line)
            
            desc = QLabel(title)
            desc.setStyleSheet(f"color: {'#0F172A' if is_active else '#475569'}; font-size: 14px; font-weight: {'600' if is_active else '500'};")
            l.addWidget(desc)
            l.addStretch()
            cl.addWidget(w)
            
        add_event("10:00", "Algorithm Lab Sync")
        add_event("14:00", "Mentoring: Career in Cloud", is_active=True)
        add_event("16:30", "Project Group Meet")
        cl.addStretch()
        
        layout.addWidget(cal_panel, stretch=1)
        
        self.central_layout.addWidget(container)

    def _build_productivity_insights(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Graph Mockup
        graph_card = ModernCard()
        gl = graph_card.internal_layout
        g_title = QLabel("Productivity & Focus")
        g_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        gl.addWidget(g_title)
        
        mock_graph = QLabel("[ Productivity Graph Visualization ]")
        mock_graph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mock_graph.setStyleSheet("color: #94A3B8; font-size: 13px; background-color: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px; min-height: 120px;")
        gl.addWidget(mock_graph)
        layout.addWidget(graph_card, stretch=2)
        
        # AI Insights
        ai_card = ModernCard()
        al = ai_card.internal_layout
        a_title = QLabel("✨ Learning Insights")
        a_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        al.addWidget(a_title)
        
        msg = QLabel("You've been studying System Design 30% more this week. Based on your roadmap, you might want to start working on your capstone architecture draft soon.")
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #475569; font-size: 14px; line-height: 1.5;")
        al.addWidget(msg)
        al.addStretch()
        layout.addWidget(ai_card, stretch=1)
        
        self.central_layout.addWidget(container)

    def _build_right_panel(self):
        panel = QWidget()
        panel.setFixedWidth(320)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # 1. AI Assistant Card
        ai_card = ModernCard()
        al = ai_card.internal_layout
        al.setSpacing(16)
        
        header = QHBoxLayout()
        pulse = StatusPulse(size=10, color="#8B5CF6")
        header.addWidget(pulse)
        title = QLabel("AI Assistant")
        title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()
        al.addLayout(header)
        
        ai_msg = QLabel("I noticed you have a mentoring session at 2 PM. Would you like me to prepare a list of questions about Cloud Architecture based on your recent activity?")
        ai_msg.setWordWrap(True)
        ai_msg.setStyleSheet("color: #475569; font-size: 14px; line-height: 1.5;")
        al.addWidget(ai_msg)
        
        btn_prep = ActionButton("Prepare Questions", "✨", is_primary=True)
        btn_prep.setFixedHeight(32)
        al.addWidget(btn_prep)
        layout.addWidget(ai_card)
        
        # 2. Recent Notifications
        notif_card = ModernCard()
        nl = notif_card.internal_layout
        n_title = QLabel("Recent Notifications")
        n_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        nl.addWidget(n_title)
        
        def add_notif(title, time_str, icon="📌"):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            
            ic = QLabel(icon)
            ic.setStyleSheet("font-size: 16px;")
            l.addWidget(ic)
            
            vl = QVBoxLayout()
            vl.setSpacing(2)
            t = QLabel(title)
            t.setStyleSheet("color: #334155; font-size: 13px; font-weight: 500;")
            t.setWordWrap(True)
            vl.addWidget(t)
            
            tm = QLabel(time_str)
            tm.setStyleSheet("color: #94A3B8; font-size: 11px;")
            vl.addWidget(tm)
            
            l.addLayout(vl)
            nl.addWidget(w)
            
        add_notif("Prof. Alan posted a new grade", "10 min ago", "🎓")
        add_notif("Your AWS Student creds expire soon", "1 hour ago", "⚠️")
        layout.addWidget(notif_card)
        
        # 3. Recent Activity
        act_card = ModernCard()
        acl = act_card.internal_layout
        ac_title = QLabel("Recent Activity")
        ac_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        acl.addWidget(ac_title)
        
        def add_activity(action, time_str):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(12)
            
            dot = QFrame()
            dot.setFixedSize(8, 8)
            dot.setStyleSheet("background-color: #CBD5E1; border-radius: 4px;")
            l.addWidget(dot)
            
            vl = QVBoxLayout()
            vl.setSpacing(2)
            t = QLabel(action)
            t.setStyleSheet("color: #475569; font-size: 13px;")
            t.setWordWrap(True)
            vl.addWidget(t)
            
            tm = QLabel(time_str)
            tm.setStyleSheet("color: #94A3B8; font-size: 11px;")
            vl.addWidget(tm)
            
            l.addLayout(vl)
            acl.addWidget(w)
            
        add_activity("Completed 'React Hooks' Quiz", "Yesterday")
        add_activity("Joined 'Cloud Engineers' Group", "Yesterday")
        add_activity("Updated Resume PDF", "2 days ago")
        layout.addWidget(act_card)
        
        layout.addStretch()
        return panel

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    page = DashboardPage()
    page.resize(1400, 900)
    page.show()
    sys.exit(app.exec())