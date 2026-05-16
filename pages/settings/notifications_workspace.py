from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor
from .toggle_switch import ToggleSwitch

class NotificationCategoryCard(QFrame):
    def __init__(self, title, icon, desc, parent=None):
        super().__init__(parent)
        self.setFixedHeight(110)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #E2E8F0;
                border-radius: 20px;
            }
            QFrame:hover {
                border-color: #38BDF8;
                background-color: #F8FAFC;
            }
            QFrame[active="true"] {
                border-color: #38BDF8;
                background-color: #F0F9FF;
            }
        """)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(4)
        
        h = QHBoxLayout()
        ico = QLabel(icon); ico.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        h.addWidget(ico); h.addStretch()
        
        self.toggle = ToggleSwitch()
        h.addWidget(self.toggle)
        l.addLayout(h)
        
        t = QLabel(title)
        t.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none; background: transparent;")
        l.addWidget(t)
        
        d = QLabel(desc)
        d.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        l.addWidget(d)

class ChannelCard(QFrame):
    def __init__(self, name, icon, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
            }
            QFrame:hover { border-color: #CBD5E1; }
        """)
        l = QHBoxLayout(self)
        l.setContentsMargins(12, 0, 12, 0)
        l.setSpacing(10)
        
        ico = QLabel(icon); ico.setStyleSheet("font-size: 16px; border: none;")
        l.addWidget(ico)
        
        lbl = QLabel(name)
        lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #1E293B; border: none;")
        l.addWidget(lbl, 1)
        
        self.toggle = ToggleSwitch()
        l.addWidget(self.toggle)

class NotificationsIntelligenceCenter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(32)

        # 1. Hero Analytics
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(40)
        
        info = QVBoxLayout(); info.setSpacing(8)
        tag = QLabel("✨ NOTIFICATION INTELLIGENCE")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("Communication Control")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your notification flow is <b>88% optimized</b>. AI is currently suppressing 12 low-priority interruptions per day.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        stats = QGridLayout(); stats.setSpacing(12)
        def add_metric(val, label, r, c):
            v = QVBoxLayout(); v.setSpacing(2); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l1 = QLabel(val); l1.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
            l2 = QLabel(label); l2.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
            v.addWidget(l1); v.addWidget(l2); stats.addLayout(v, r, c)
            
        add_metric("12", "Active", 0, 0); add_metric("92%", "Focus", 0, 1)
        add_metric("High", "Shield", 1, 0); add_metric("Smart", "Filter", 1, 1)
        hl.addLayout(stats)
        cl.addWidget(hero)

        # 2. Categories
        cat_sec = QWidget()
        cl_v = QVBoxLayout(cat_sec); cl_v.setContentsMargins(0, 0, 0, 0); cl_v.setSpacing(16)
        cl_v.addWidget(QLabel("Notification Categories", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        grid = QGridLayout(); grid.setSpacing(16)
        grid.addWidget(NotificationCategoryCard("System Alerts", "⚠️", "Critical updates and security notifications."), 0, 0)
        grid.addWidget(NotificationCategoryCard("AI Recommendations", "✨", "Career tips and roadmap suggestions."), 0, 1)
        grid.addWidget(NotificationCategoryCard("Interview Reminders", "🎙️", "Upcoming simulation and session alerts."), 1, 0)
        grid.addWidget(NotificationCategoryCard("Milestone Tracking", "🏁", "Progression updates and achievements."), 1, 1)
        cl_v.addLayout(grid)
        cl.addWidget(cat_sec)

        # 3. Communication Channels
        chan_sec = QFrame()
        chan_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        cv = QVBoxLayout(chan_sec); cv.setContentsMargins(24, 24, 24, 24); cv.setSpacing(20)
        cv.addWidget(QLabel("Communication Channels", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        chan_grid = QGridLayout(); chan_grid.setSpacing(16)
        chan_grid.addWidget(ChannelCard("Desktop Push", "🖥️"), 0, 0)
        chan_grid.addWidget(ChannelCard("Email Digest", "✉️"), 0, 1)
        chan_grid.addWidget(ChannelCard("In-App Inbox", "📱"), 1, 0)
        chan_grid.addWidget(ChannelCard("Sound Alerts", "🔊"), 1, 1)
        cv.addLayout(chan_grid)
        cl.addWidget(chan_sec)

        # 4. Focus Mode
        focus_sec = QFrame()
        focus_sec.setStyleSheet("background: #0F172A; border-radius: 24px;")
        fv = QHBoxLayout(focus_sec); fv.setContentsMargins(32, 32, 32, 32); fv.setSpacing(24)
        
        f_info = QVBoxLayout(); f_info.setSpacing(8)
        f_title = QLabel("Productivity Shield")
        f_title.setStyleSheet("color: white; font-size: 18px; font-weight: 800;")
        f_desc = QLabel("Activate Focus Mode to silence all non-critical interruptions during deep work sessions.")
        f_desc.setStyleSheet("color: #94A3B8; font-size: 13px; line-height: 1.4;")
        f_info.addWidget(f_title); f_info.addWidget(f_desc)
        fv.addLayout(f_info, 1)
        
        btn_focus = QPushButton("Enable Focus")
        btn_focus.setFixedSize(140, 44)
        btn_focus.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: #0F172A; border-radius: 12px; font-weight: 800; font-size: 13px;
            }
            QPushButton:hover { background: #7DD3FC; }
        """)
        fv.addWidget(btn_focus)
        cl.addWidget(focus_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
