from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class VisualInsightCard(QFrame):
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

class AIVisualPanel(QFrame):
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

        # 1. AI Design Insights
        self._setup_design_insights(cl)

        # 2. Visual Analytics
        self._setup_visual_analytics(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 3. Actions
        self._setup_actions()

    def _setup_design_insights(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI DESIGN INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(VisualInsightCard("Contrast Check", "Your current accent color has a 7:1 contrast ratio against background, perfect for accessibility."))
        sec.addWidget(VisualInsightCard("Aesthetic Trend", "Glassmorphism is trending in modern SaaS interfaces. Enabling blur will modernize your UI.", "#F59E0B"))
        layout.addLayout(sec)

    def _setup_visual_analytics(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("VISUAL HARMONY")
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
            
        add_fc("Readability Score", 96)
        add_fc("Visual Balance", 88)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_ai = QPushButton("Generate AI Theme")
        btn_ai.setFixedHeight(46)
        btn_ai.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_acc = QPushButton("Analyze Accessibility")
        btn_acc.setFixedHeight(46)
        btn_acc.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_ai); al.addWidget(btn_acc)
        self.main_layout.addLayout(al)
