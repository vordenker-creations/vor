from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class ForecastingCard(QFrame):
    def __init__(self, title, date, probability, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #0F172A; border-radius: 20px; padding: 20px;")
        l = QVBoxLayout(self)
        l.setSpacing(10)
        
        t = QLabel(title)
        t.setStyleSheet(f"color: {color}; font-weight: 800; font-size: 13px; text-transform: uppercase;")
        l.addWidget(t)
        
        d_lbl = QLabel(date)
        d_lbl.setStyleSheet("color: white; font-size: 22px; font-weight: 800;")
        l.addWidget(d_lbl)
        
        p_h = QHBoxLayout()
        p_h.addWidget(QLabel("Confidence:", styleSheet="color: #94A3B8; font-size: 11px;"))
        p_h.addStretch()
        p_lbl = QLabel(f"{probability}%")
        p_lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 800;")
        p_h.addWidget(p_lbl)
        l.addLayout(p_h)

class AIForecastingPanel(QFrame):
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

        # 1. AI Forecasting Section
        sec1 = QVBoxLayout(); sec1.setSpacing(16)
        sec1.addWidget(QLabel("AI LEARNING FORECASTS", styleSheet="font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;"))
        sec1.addWidget(ForecastingCard("Roadmap Completion", "Jan 12, 2025", 92))
        sec1.addWidget(ForecastingCard("Interview Ready", "Dec 20, 2024", 84, "#10B981"))
        cl.addLayout(sec1)

        # 2. Risk Detection
        sec2 = QVBoxLayout(); sec2.setSpacing(12)
        sec2.addWidget(QLabel("PRODUCTIVITY RISKS", styleSheet="font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;"))
        
        risk = QFrame()
        risk.setStyleSheet("background: #FEF2F2; border: 1px solid #FECACA; border-radius: 16px; padding: 16px;")
        rl = QVBoxLayout(risk)
        rl.addWidget(QLabel("Burnout Risk: High", styleSheet="color: #EF4444; font-weight: 800; font-size: 12px;"))
        rl.addWidget(QLabel("You've exceeded 4h/day study limit for 5 consecutive days.", styleSheet="color: #991B1B; font-size: 11px; line-height: 1.4;"))
        sec2.addWidget(risk)
        cl.addLayout(sec2)

        # 3. Recommendations
        sec3 = QVBoxLayout(); sec3.setSpacing(12)
        sec3.addWidget(QLabel("STRATEGIC SUGGESTIONS", styleSheet="font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;"))
        
        for icon, msg in [("🕒", "Shift Deep Learning to 9AM"), ("🧪", "Add hands-on lab for PyTorch"), ("📝", "Review Flashcards every 48h")]:
            row = QHBoxLayout()
            row.addWidget(QLabel(icon, styleSheet="font-size: 14px; border: none;"))
            row.addWidget(QLabel(msg, styleSheet="font-size: 12px; color: #475569; font-weight: 500; border: none;"), 1)
            sec3.addLayout(row)
        cl.addLayout(sec3)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Actions
        al = QVBoxLayout(); al.setSpacing(10)
        btn_exp = QPushButton("Export Analytics PDF")
        btn_exp.setFixedHeight(46)
        btn_exp.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        al.addWidget(btn_exp)
        self.main_layout.addLayout(al)
