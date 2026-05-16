from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class AICredentialInsight(QFrame):
    def __init__(self, title, text, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 16px;")
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

class AICertificationPanel(QFrame):
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

        # 1. AI Recommendation Section
        self._setup_recommendations(cl)

        # 2. Industry Validation Section
        self._setup_validation(cl)

        # 3. Forecast Section
        self._setup_forecasts(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Actions
        self._setup_actions()

    def _setup_recommendations(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI CERTIFICATION INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(AICredentialInsight("High Impact", "Earning the 'AWS Solutions Architect' will increase your interview rate by 42%."))
        sec.addWidget(AICredentialInsight("Skill Gap", "Your profile lacks 'Kubernetes' validation. Consider the CKA certification.", "#F59E0B"))
        layout.addLayout(sec)

    def _setup_validation(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("INDUSTRY VALIDATION")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Employer Demand: High", styleSheet="color: #10B981; font-weight: 800; font-size: 13px;"))
        bl.addWidget(QLabel("78% of recruiters in your area look for AWS credentials.", styleSheet="color: #94A3B8; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_forecasts(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("ACHIEVEMENT FORECASTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        def add_fc(label, val):
            v = QVBoxLayout(); v.setSpacing(4)
            rl = QHBoxLayout()
            rl.addWidget(QLabel(label, styleSheet="font-size: 12px; color: #475569; font-weight: 600; border: none;"))
            rl.addStretch(); rl.addWidget(QLabel(f"{val}%", styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;"))
            v.addLayout(rl)
            pb = QProgressBar(); pb.setFixedHeight(4); pb.setValue(val); pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 2px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 2px; }")
            v.addWidget(pb); sec.addLayout(v)
            
        add_fc("Next Cert Readiness", 62)
        add_fc("Employer Match Prob.", 85)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_gen = QPushButton("✨ Generate AI Recommendations")
        btn_gen.setFixedHeight(46)
        btn_gen.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_report = QPushButton("Export Achievement Report")
        btn_report.setFixedHeight(46)
        btn_report.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_gen); al.addWidget(btn_report)
        self.main_layout.addLayout(al)
