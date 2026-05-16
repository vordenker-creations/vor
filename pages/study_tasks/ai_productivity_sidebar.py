from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class ProductivityInsightCard(QFrame):
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

class AIProductivitySidebar(QFrame):
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

        # 1. AI Planning Insights
        self._setup_insights(cl)

        # 2. Performance Alerts
        self._setup_alerts(cl)

        # 3. Smart Recommendations
        self._setup_recommendations(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        self._setup_actions()

    def _setup_insights(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI PRODUCTIVITY INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(ProductivityInsightCard("Optimal Schedule", "Your focus is 24% higher between 9 AM - 11 AM. Shift your 'Algorithm Lab' to this slot."))
        sec.addWidget(ProductivityInsightCard("Workload Warning", "You have 3 critical deadlines tomorrow. Recommend clear backlog session.", "warning"))
        layout.addLayout(sec)

    def _setup_alerts(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("PRODUCTIVITY ALERTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #FEF2F2; border: 1px solid #FECACA; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Overdue: 2 Tasks", styleSheet="color: #EF4444; font-weight: 800; font-size: 12px;"))
        bl.addWidget(QLabel("'UI Mockup v2' and 'Peer Review' are past deadline.", styleSheet="color: #991B1B; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_recommendations(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("SMART RECOMMENDATIONS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Active Deep Work Session", styleSheet="color: #38BDF8; font-weight: 800; font-size: 12px;"))
        bl.addWidget(QLabel("Activate Pomodoro mode for next 45 minutes to finish your Python homework.", styleSheet="color: #94A3B8; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_plan = QPushButton("Generate AI Study Plan")
        btn_plan.setFixedHeight(46)
        btn_plan.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_opt = QPushButton("Optimize Productivity")
        btn_opt.setFixedHeight(46)
        btn_opt.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_plan); al.addWidget(btn_opt)
        self.main_layout.addLayout(al)
