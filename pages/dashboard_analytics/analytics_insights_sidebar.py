from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class AIAnalyticsInsightCard(QFrame):
    def __init__(self, title, text, severity="info", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 16px;")
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(8)
        
        color = "#38BDF8"
        if severity == "warning": color = "#F59E0B"
        elif severity == "danger": color = "#EF4444"
            
        t = QLabel(f"✨ {title}")
        t.setStyleSheet(f"font-size: 11px; font-weight: 800; color: {color}; text-transform: uppercase; letter-spacing: 0.5px; border: none;")
        
        d = QLabel(text)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 13px; color: #475569; border: none; line-height: 1.4;")
        
        l.addWidget(t)
        l.addWidget(d)

class AnalyticsInsightsSidebar(QFrame):
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

        # 1. AI Insights
        cl.addLayout(self._setup_insights())

        # 2. Performance Alerts
        cl.addLayout(self._setup_alerts())

        # 3. Quick Actions
        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        self._setup_actions()

    def _setup_insights(self):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI ANALYTICS INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(AIAnalyticsInsightCard("Productivity Peak", "You are 24% more efficient on technical tasks during morning sessions (8AM - 11AM)."))
        sec.addWidget(AIAnalyticsInsightCard("Learning Gap", "Your retention for 'PyQt6' modules is slightly below average. Suggesting 15m review session.", "warning"))
        return sec

    def _setup_alerts(self):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("PERFORMANCE ALERTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #F8FAFC; border-radius: 16px; padding: 16px; border: 1px solid #E2E8F0;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Interruption Level: Moderate", styleSheet="color: #F59E0B; font-weight: 800; font-size: 12px;"))
        bl.addWidget(QLabel("12 distractions detected in your last deep work session.", styleSheet="color: #64748B; font-size: 11px;"))
        sec.addWidget(box)
        return sec

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_opt = QPushButton("Optimize Workflows")
        btn_opt.setFixedHeight(46)
        btn_opt.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_focus = QPushButton("Activate Focus Mode")
        btn_focus.setFixedHeight(46)
        btn_focus.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_opt); al.addWidget(btn_focus)
        self.main_layout.addLayout(al)
