from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class NotificationInsightCard(QFrame):
    def __init__(self, title, text, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 16px;")
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(8)
        
        t = QLabel(f"✨ {title}")
        t.setStyleSheet(f"font-size: 11px; font-weight: 800; color: {color}; text-transform: uppercase; letter-spacing: 0.5px; border: none;")
        
        d = QLabel(text)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 13px; color: #475569; border: none; line-height: 1.4;")
        
        l.addWidget(t)
        l.addWidget(d)

class AINotificationPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(28)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(32)

        # 1. AI Alert Insights
        self._setup_alert_insights(cl)

        # 2. Notification Analytics
        self._setup_notif_analytics(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Global Actions
        self._setup_actions()

    def _setup_alert_insights(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI ALERT INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(NotificationInsightCard("Interruption Detection", "You've had 14 notifications between 2 PM - 4 PM, reducing your focus by 22%."))
        sec.addWidget(NotificationInsightCard("Recommended Quiet Mode", "Enable 'Learning Mode' from 9 AM - 11 AM based on your study patterns.", "#F59E0B"))
        layout.addLayout(sec)

    def _setup_notif_analytics(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("NOTIFICATION ANALYTICS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Shield Mode: Active", styleSheet="color: #10B981; font-weight: 800; font-size: 12px;"))
        bl.addWidget(QLabel("124 potential interruptions blocked this week.", styleSheet="color: #94A3B8; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_focus = QPushButton("Enable Focus Mode")
        btn_focus.setFixedHeight(46)
        btn_focus.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_test = QPushButton("Test Alert System")
        btn_test.setFixedHeight(46)
        btn_test.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_focus); al.addWidget(btn_test)
        self.main_layout.addLayout(al)
