from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class AICareerInsightCard(QFrame):
    def __init__(self, title, text, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: white; border: 1px solid #E2E8F0; border-radius: 16px;
            }}
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(8)
        
        t = QLabel(title)
        t.setStyleSheet(f"font-size: 11px; font-weight: 800; color: {color}; text-transform: uppercase; letter-spacing: 0.5px; border: none;")
        
        d = QLabel(text)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 13px; color: #475569; border: none; line-height: 1.4;")
        
        l.addWidget(t)
        l.addWidget(d)

class AICareerPanel(QFrame):
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

        # 1. AI Career Insights
        cl.addLayout(self._setup_insights())

        # 2. Readiness Forecasts
        cl.addLayout(self._setup_readiness())

        # 3. Market Intel
        cl.addLayout(self._setup_market())

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Global Actions
        self._setup_actions()

    def _setup_insights(self):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI CAREER INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(AICareerInsightCard("Best Match", "Senior Machine Learning Engineer at top-tier SaaS companies."))
        sec.addWidget(AICareerInsightCard("Skill Gap Alert", "Focus on 'Distributed Training' to unlock High-Demand role tiers.", "#EF4444"))
        return sec

    def _setup_readiness(self):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("READINESS FORECASTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #F8FAFC; border-radius: 16px; padding: 16px; border: 1px solid #E2E8F0;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        
        def add_prog(label, val):
            v = QVBoxLayout(); v.setSpacing(4)
            rl = QHBoxLayout()
            rl.addWidget(QLabel(label, styleSheet="font-size: 12px; color: #475569; font-weight: 600; border: none;"))
            rl.addStretch(); rl.addWidget(QLabel(f"{val}%", styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;"))
            v.addLayout(rl)
            pb = QProgressBar(); pb.setFixedHeight(4); pb.setValue(val); pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 2px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 2px; }")
            v.addWidget(pb); bl.addLayout(v)
            
        add_prog("Interview Ready", 68)
        add_prog("Market Compatibility", 92)
        sec.addWidget(box)
        return sec

    def _setup_market(self):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("MARKET INTELLIGENCE")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        intel = QFrame()
        intel.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        il = QVBoxLayout(intel); il.setSpacing(8)
        il.addWidget(QLabel("Role Demand: High", styleSheet="color: #10B981; font-weight: 800; font-size: 12px;"))
        il.addWidget(QLabel("15% increase in GenAI role postings this month.", styleSheet="color: #94A3B8; font-size: 11px;"))
        sec.addWidget(intel)
        return sec

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_gen = QPushButton("✨ Generate AI Career Path")
        btn_gen.setFixedHeight(46)
        btn_gen.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_exp = QPushButton("Export Career Report")
        btn_exp.setFixedHeight(46)
        btn_exp.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_gen); al.addWidget(btn_exp)
        self.main_layout.addLayout(al)
