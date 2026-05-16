from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class AIPersonalizationInsight(QFrame):
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

class AIPersonalizationPanel(QFrame):
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
        self._setup_personalization_insights(cl)

        # 2. Intelligence Analytics
        self._setup_intelligence_analytics(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Global Actions
        self._setup_actions()

    def _setup_personalization_insights(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("ADAPTIVE INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(AIPersonalizationInsight("Workflow Boost", "AI has detected you work best on technical tasks at night. Mode automatically switching to 'Expert' at 9 PM."))
        sec.addWidget(AIPersonalizationInsight("Communication", "Your conversational satisfaction score increased by 14% since enabling 'Mentor Mode'.", "#10B981"))
        layout.addLayout(sec)

    def _setup_intelligence_analytics(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("INTELLIGENCE ANALYTICS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Learning Efficiency: Elite", styleSheet="color: #38BDF8; font-weight: 800; font-size: 12px;"))
        bl.addWidget(QLabel("AI has adapted its communication style to 92% of your preferred technical depth.", styleSheet="color: #94A3B8; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_gen = QPushButton("Generate AI Identity")
        btn_gen.setFixedHeight(46)
        btn_gen.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_reset = QPushButton("Reset Personality")
        btn_reset.setFixedHeight(46)
        btn_reset.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_gen); al.addWidget(btn_reset)
        self.main_layout.addLayout(al)
