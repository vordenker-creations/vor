from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class AIInsightCard(QFrame):
    def __init__(self, title, text, severity="info", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: white; border: 1px solid #E2E8F0; border-radius: 16px;
            }}
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(8)
        
        color = "#38BDF8"
        if severity == "warning": color = "#F59E0B"
        elif severity == "danger": color = "#EF4444"
            
        t = QLabel(f"✨ {title}")
        t.setStyleSheet(f"font-size: 12px; font-weight: 800; color: {color}; text-transform: uppercase;")
        
        d = QLabel(text)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 13px; color: #475569; border: none; line-height: 1.4;")
        
        l.addWidget(t)
        l.addWidget(d)

class ATSIntelligencePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(24)

        # 1. Header
        lbl = QLabel("AI INTELLIGENCE")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        self.main_layout.addWidget(lbl)

        # 2. Insights Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(16)

        cl.addWidget(AIInsightCard("Optimization", "Your resume lacks 'Cloud Infrastructure' keywords which are high-priority for this role.", "warning"))
        cl.addWidget(AIInsightCard("Formatting", "Great work on the section hierarchy! ATS parsers will find this very readable.", "info"))
        cl.addWidget(AIInsightCard("Recruiter Advice", "Keep your summary under 3 sentences for maximum engagement.", "info"))
        
        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 3. Monitor
        monitor = QFrame()
        monitor.setStyleSheet("background: #F8FAFC; border-radius: 16px; padding: 12px;")
        ml = QVBoxLayout(monitor)
        ml.addWidget(QLabel("LIVE ATS MONITOR", styleSheet="font-size: 10px; font-weight: 800; color: #94A3B8;"))
        
        live_row = QHBoxLayout()
        pulse = QFrame()
        pulse.setFixedSize(8, 8)
        pulse.setStyleSheet("background: #10B981; border-radius: 4px;")
        live_row.addWidget(pulse)
        live_row.addWidget(QLabel("Analyzing changes...", styleSheet="font-size: 12px; color: #475569; font-weight: 600;"))
        ml.addLayout(live_row)
        self.main_layout.addWidget(monitor)

        # 4. Actions
        btn_scan = QPushButton("Run Full Scan")
        btn_scan.setFixedHeight(46)
        btn_scan.setStyleSheet("""
            QPushButton { background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; }
            QPushButton:hover { background: #1E293B; }
        """)
        self.main_layout.addWidget(btn_scan)
