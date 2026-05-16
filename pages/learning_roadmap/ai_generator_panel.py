from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class GeneratorInsightCard(QFrame):
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

class AIGeneratorPanel(QFrame):
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

        # 2. Path Forecasting
        self._setup_forecasts(cl)

        # 3. Market Alignment
        self._setup_alignment(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Actions
        self._setup_actions()

    def _setup_insights(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("AI PLANNING INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(GeneratorInsightCard("Path Optimization", "We've reordered your ML modules to prioritize PyTorch, saving you 2 weeks of prep time."))
        sec.addWidget(GeneratorInsightCard("Skill Gap", "Your target role requires 'Kubernetes'. Adding this to the next phase of your roadmap.", "#F59E0B"))
        layout.addLayout(sec)

    def _setup_forecasts(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("COMPLETION FORECASTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box); bl.setSpacing(10)
        bl.addWidget(QLabel("Est. Completion: 4 Months", styleSheet="color: #38BDF8; font-weight: 800; font-size: 13px;"))
        bl.addWidget(QLabel("Confidence Score: 92%", styleSheet="color: white; font-size: 11px;"))
        sec.addWidget(box)
        layout.addLayout(sec)

    def _setup_alignment(self, layout):
        sec = QVBoxLayout(); sec.setSpacing(12)
        lbl = QLabel("CAREER ALIGNMENT")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        def add_item(label, val):
            v = QVBoxLayout(); v.setSpacing(4)
            rl = QHBoxLayout()
            rl.addWidget(QLabel(label, styleSheet="font-size: 12px; color: #475569; font-weight: 600; border: none;"))
            rl.addStretch(); rl.addWidget(QLabel(f"{val}%", styleSheet="font-size: 11px; font-weight: 700; color: #10B981; border: none;"))
            v.addLayout(rl)
            pb = QProgressBar(); pb.setFixedHeight(4); pb.setValue(val); pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 2px; border: none; } QProgressBar::chunk { background: #10B981; border-radius: 2px; }")
            v.addWidget(pb); sec.addLayout(v)
            
        add_item("Market Demand", 88)
        add_item("Role Compatibility", 94)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout(); al.setSpacing(10)
        btn_opt = QPushButton("✨ Optimize Schedule")
        btn_opt.setFixedHeight(46)
        btn_opt.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none;")
        btn_sim = QPushButton("Simulate Learning Path")
        btn_sim.setFixedHeight(46)
        btn_sim.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px;")
        al.addWidget(btn_opt); al.addWidget(btn_sim)
        self.main_layout.addLayout(al)
