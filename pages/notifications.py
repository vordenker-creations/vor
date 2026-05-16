import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QGraphicsDropShadowEffect, QSizePolicy, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

class CategoryItem(QPushButton):
    def __init__(self, text, count=0, is_active=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        bg = "#E0F2FE" if is_active else "transparent"
        color = "#0284C7" if is_active else "#64748B"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border-radius: 10px;
                padding-left: 15px;
                text-align: left;
                font-weight: {'700' if is_active else '500'};
                border: none;
            }}
            QPushButton:hover {{ background-color: #F1F5F9; }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        self.setText(text)
        
        if count > 0:
            badge = QLabel(str(count))
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedSize(20, 20)
            badge_bg = "#38BDF8" if is_active else "#E2E8F0"
            badge_fg = "white" if is_active else "#64748B"
            badge.setStyleSheet(f"background-color: {badge_bg}; color: {badge_fg}; border-radius: 10px; font-size: 10px; font-weight: 700; border: none;")
            layout.addStretch()
            layout.addWidget(badge)

class NotificationCard(QFrame):
    def __init__(self, title, desc, time, priority="Normal", type="Info", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            QFrame:hover { border: 1px solid #38BDF8; }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Avatar/Icon
        icon_frame = QFrame()
        icon_frame.setFixedSize(44, 44)
        icon_color = "#38BDF8" if type == "Info" else "#F59E0B"
        icon_frame.setStyleSheet(f"background-color: {icon_color}15; border-radius: 22px; border: none;")
        il = QVBoxLayout(icon_frame)
        il.setContentsMargins(0, 0, 0, 0)
        il.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ic = QLabel("🔔" if type == "Info" else "⚠️")
        ic.setStyleSheet("font-size: 18px; background: transparent; border: none;")
        il.addWidget(ic)
        layout.addWidget(icon_frame)
        
        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        header = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 15px; border: none; background: transparent;")
        time_lbl = QLabel(time)
        time_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; border: none; background: transparent;")
        header.addWidget(t_lbl)
        header.addStretch()
        header.addWidget(time_lbl)
        text_layout.addLayout(header)
        
        d_lbl = QLabel(desc)
        d_lbl.setWordWrap(True)
        d_lbl.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.4; border: none; background: transparent;")
        text_layout.addWidget(d_lbl)
        
        # Actions
        actions = QHBoxLayout()
        p_colors = {"Urgent": "#EF4444", "Normal": "#3B82F6", "Low": "#10B981"}
        p_lbl = QLabel(priority)
        p_lbl.setStyleSheet(f"color: {p_colors.get(priority)}; background: {p_colors.get(priority)}15; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;")
        actions.addWidget(p_lbl)
        actions.addStretch()
        
        for act in ["Mark Read", "Archive"]:
            btn = QPushButton(act)
            btn.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: 700; border: none; background: transparent;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            actions.addWidget(btn)
            
        text_layout.addLayout(actions)
        layout.addLayout(text_layout)

class NotificationsPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_left_sidebar()
        self._setup_main_workspace()
        self._setup_right_panel()

    def _setup_left_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(20)
        
        header = QHBoxLayout()
        h_lbl = QLabel("Notifications")
        h_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        header.addWidget(h_lbl)
        header.addStretch()
        layout.addLayout(header)
        
        read_all = QPushButton("Mark All Read")
        read_all.setStyleSheet("""
            QPushButton {
                background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD;
                border-radius: 8px; padding: 10px; font-weight: 700; font-size: 13px;
            }
            QPushButton:hover { background-color: #E0F2FE; }
        """)
        layout.addWidget(read_all)
        
        search = QLineEdit()
        search.setPlaceholderText("Search categories...")
        search.setStyleSheet("background-color: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;")
        layout.addWidget(search)
        
        # Categories
        layout.addWidget(CategoryItem("All Activity", 12, True))
        layout.addWidget(CategoryItem("Academic Alerts", 3))
        layout.addWidget(CategoryItem("Career Matches", 5))
        layout.addWidget(CategoryItem("Community", 2))
        layout.addWidget(CategoryItem("System Updates", 0))
        
        layout.addStretch()
        self.main_layout.addWidget(sidebar)

    def _setup_main_workspace(self):
        workspace = QWidget()
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(24, 0, 24, 0)
        
        filters = QHBoxLayout()
        for f in ["Recent", "Priority", "Unread"]:
            btn = QPushButton(f)
            btn.setStyleSheet("color: #64748B; font-weight: 600; font-size: 13px; border: none; background: transparent; padding: 0 12px;")
            filters.addWidget(btn)
        t_layout.addLayout(filters)
        
        t_layout.addStretch()
        
        for btn_text in ["Refresh", "AI Summary"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("background-color: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 13px;")
            t_layout.addWidget(btn)
        
        layout.addWidget(toolbar)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        content = QWidget()
        form_layout = QVBoxLayout(content)
        form_layout.setContentsMargins(32, 32, 32, 32)
        form_layout.setSpacing(24)
        
        # KPI Row
        kpi_row = QHBoxLayout()
        for t, v, s in [("New Alerts", "12", "Last 24h"), ("Unread", "08", "Priority"), ("Resolved", "45", "Total"), ("System Health", "99%", "Optimal")]:
            card = QFrame()
            card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
            cl = QVBoxLayout(card)
            t_lbl = QLabel(t)
            t_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase;")
            cl.addWidget(t_lbl)
            v_lbl = QLabel(v)
            v_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 800;")
            cl.addWidget(v_lbl)
            kpi_row.addWidget(card)
        form_layout.addLayout(kpi_row)
        
        # Feed
        f_lbl = QLabel("Recent Activity")
        f_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        form_layout.addWidget(f_lbl)
        form_layout.addWidget(NotificationCard("New Job Match: AI Researcher", "A new position at Tech Corp matches your skills in PyTorch and NLP.", "10 min ago", "Urgent", "Info"))
        form_layout.addWidget(NotificationCard("Deadline Reminder: CS301", "Lab Report 3 is due in 4 hours. Submit now to avoid penalty.", "2 hours ago", "Urgent", "Warning"))
        form_layout.addWidget(NotificationCard("Community Mention", "Alex mentioned you in 'Math Study Group'.", "Yesterday", "Normal", "Info"))
        
        form_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.main_layout.addWidget(workspace, stretch=1)

    def _setup_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(320)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        # AI Assistant
        ai_card = QFrame()
        ai_card.setStyleSheet("background-color: #0F172A; border-radius: 16px;")
        al = QVBoxLayout(ai_card)
        at_lbl = QLabel("✨ AI Summary")
        at_lbl.setStyleSheet("color: #38BDF8; font-weight: 800; font-size: 14px;")
        al.addWidget(at_lbl)
        ad_lbl = QLabel("You have 12 new notifications. The most critical is the CS301 deadline at 5:00 PM.")
        ad_lbl.setWordWrap(True)
        ad_lbl.setStyleSheet("color: #E2E8F0; font-size: 13px; line-height: 1.5;")
        al.addWidget(ad_lbl)
        layout.addWidget(ai_card)
        
        # Quick Actions
        qa_lbl = QLabel("Quick Actions")
        qa_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px;")
        layout.addWidget(qa_lbl)
        for act in ["Clear All History", "Export Log", "Notification Settings"]:
            btn = QPushButton(act)
            btn.setStyleSheet("text-align: left; color: #475569; font-size: 13px; font-weight: 500; border: none; background: transparent;")
            layout.addWidget(btn)
            
        layout.addStretch()
        self.main_layout.addWidget(panel)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = NotificationsPage()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
