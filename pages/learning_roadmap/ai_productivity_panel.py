from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class AIInsightCard(QFrame):
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

class AIProductivityPanel(QFrame):
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

        # 2. Learning Analytics
        cl.addLayout(self._setup_analytics())

        # 3. Career Alignment
        cl.addLayout(self._setup_career())

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Actions
        self._setup_actions()

    def _setup_insights(self):
        sec = QVBoxLayout()
        sec.setSpacing(16)
        lbl = QLabel("AI PRODUCTIVITY INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(AIInsightCard("Delayed Progress", "The 'PyTorch Deep Learning' milestone is 3 days behind schedule. Suggesting an intensive session.", "#EF4444"))
        sec.addWidget(AIInsightCard("Productivity Boost", "You are most active between 7 PM - 9 PM. We've optimized your upcoming schedule accordingly.", "#10B981"))
        return sec

    def _setup_analytics(self):
        sec = QVBoxLayout()
        sec.setSpacing(12)
        lbl = QLabel("LEARNING ANALYTICS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        card = QFrame()
        card.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0; padding: 16px;")
        l = QVBoxLayout(card)
        l.setSpacing(12)
        
        def add_metric(container_layout, label, val):
            v = QVBoxLayout(); v.setSpacing(4)
            rl = QHBoxLayout()
            rl.addWidget(QLabel(label, styleSheet="font-size: 12px; color: #475569; font-weight: 600; border: none;"))
            rl.addStretch()
            rl.addWidget(QLabel(f"{val}%", styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;"))
            v.addLayout(rl)
            pb = QProgressBar(); pb.setFixedHeight(4); pb.setValue(val); pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 2px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 2px; }")
            v.addWidget(pb)
            container_layout.addLayout(v)
            
        add_metric(l, "Velocity", 84)
        add_metric(l, "Consistency", 92)
        sec.addWidget(card)
        return sec

    def _setup_career(self):
        sec = QVBoxLayout()
        sec.setSpacing(16)
        lbl = QLabel("CAREER ALIGNMENT")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        box = QFrame()
        box.setStyleSheet("background: #0F172A; border-radius: 16px; padding: 16px;")
        bl = QVBoxLayout(box)
        bl.addWidget(QLabel("Role readiness: 78%", styleSheet="color: #38BDF8; font-weight: 800; font-size: 13px;"))
        bl.addWidget(QLabel("Current roadmap aligned with 1,240 Senior AI positions.", styleSheet="color: white; font-size: 11px; font-weight: 500;"))
        sec.addWidget(box)
        return sec

    def _setup_actions(self):
        al = QVBoxLayout()
        al.setSpacing(10)
        
        btn_gen = QPushButton("✨ Generate AI Schedule")
        btn_gen.setFixedHeight(46)
        btn_gen.setStyleSheet("""
            QPushButton { background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none; }
            QPushButton:hover { background: #1E293B; }
        """)
        
        btn_opt = QPushButton("Optimize Schedule")
        btn_opt.setFixedHeight(46)
        btn_opt.setStyleSheet("""
            QPushButton { background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px; }
            QPushButton:hover { background: #F8FAFC; }
        """)
        
        al.addWidget(btn_gen)
        al.addWidget(btn_opt)
        self.main_layout.addLayout(al)
