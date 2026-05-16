from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class IntegrationInsightCard(QFrame):
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

class AIIntegrationPanel(QFrame):
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

        # 1. AI Integration Insights
        self._setup_integration_insights(cl)

        # 2. Ecosystem Analytics
        self._setup_ecosystem_analytics(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 3. Global Actions
        self._setup_actions()

    def _setup_integration_insights(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI WORKFLOW INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(IntegrationInsightCard("Sync Optimization", "Google Calendar events are syncing every 15m. Changing to 'Push-Only' could save 20% battery."))
        sec.addWidget(IntegrationInsightCard("New Recommendation", "Connecting 'Trello' could automate your roadmap task management.", "#F59E0B"))
        layout.addLayout(sec)

    def _setup_ecosystem_analytics(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("ECOSYSTEM ANALYTICS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Integrations: 92% Active", styleSheet="color: #10B981; font-weight: 800; font-size: 12px;"))
        bl.addWidget(QLabel("All APIs are validating correctly. Average sync latency: 120ms.", styleSheet="color: #94A3B8; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_audit = QPushButton("Run Sync Audit")
        btn_audit.setFixedHeight(46)
        btn_audit.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_preset = QPushButton("Apply Smart Preset")
        btn_preset.setFixedHeight(46)
        btn_preset.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_audit); al.addWidget(btn_preset)
        self.main_layout.addLayout(al)
