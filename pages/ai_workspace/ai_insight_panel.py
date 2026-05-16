from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

class InsightCard(QFrame):
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

class AICareerInsights(QFrame):
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

        # 1. AI Memory Section
        self._setup_memory_section(cl)

        # 2. Key Insights
        self._setup_insights_section(cl)

        # 3. Stats
        self._setup_stats_section(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Actions
        self._setup_actions()

    def _setup_memory_section(self, layout):
        sec = QVBoxLayout()
        sec.setSpacing(12)
        lbl = QLabel("AI MEMORY")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        mem_card = QFrame()
        mem_card.setStyleSheet("background: #F8FAFC; border-radius: 16px; padding: 12px; border: 1px solid #E2E8F0;")
        ml = QVBoxLayout(mem_card)
        ml.setSpacing(10)
        
        memories = [
            ("Targeting Senior Roles", "🎯"),
            ("Prefers Remote Work", "🏠"),
            ("Focusing on Python/AWS", "💻")
        ]
        for text, icon in memories:
            row = QHBoxLayout()
            row.addWidget(QLabel(icon, styleSheet="font-size: 14px; border: none;"))
            row.addWidget(QLabel(text, styleSheet="font-size: 12px; color: #475569; font-weight: 500; border: none;"))
            row.addStretch()
            ml.addLayout(row)
        sec.addWidget(mem_card)
        layout.addLayout(sec)

    def _setup_insights_section(self, layout):
        sec = QVBoxLayout()
        sec.setSpacing(16)
        lbl = QLabel("STRATEGIC INSIGHTS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        sec.addWidget(InsightCard("Skill Gap", "You need 2 more AWS certifications to reach 'Expert' level for your target role."))
        sec.addWidget(InsightCard("Resume Strength", "Your recent updates improved your ATS score by 12% in the Technical section.", "#10B981"))
        layout.addLayout(sec)

    def _setup_stats_section(self, layout):
        sec = QVBoxLayout()
        sec.setSpacing(12)
        lbl = QLabel("CAREER PROGRESS")
        lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)
        
        def add_stat(label, val):
            row = QVBoxLayout()
            row.setSpacing(4)
            rl = QHBoxLayout()
            rl.addWidget(QLabel(label, styleSheet="font-size: 12px; color: #475569; font-weight: 600; border: none;"))
            rl.addStretch()
            rl.addWidget(QLabel(f"{val}%", styleSheet="font-size: 11px; color: #38BDF8; font-weight: 700; border: none;"))
            row.addLayout(rl)
            pb = QProgressBar()
            pb.setFixedHeight(4)
            pb.setValue(val)
            pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #F1F5F9; border-radius: 2px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 2px; }")
            row.addWidget(pb)
            sec.addLayout(row)
            
        add_stat("Interview Readiness", 75)
        add_stat("Market Compatibility", 92)
        layout.addLayout(sec)

    def _setup_actions(self):
        al = QVBoxLayout()
        al.setSpacing(10)
        
        btn_plan = QPushButton("Generate Action Plan")
        btn_plan.setFixedHeight(46)
        btn_plan.setStyleSheet("""
            QPushButton { background: #0F172A; color: white; border-radius: 12px; font-weight: 800; font-size: 13px; border: none; }
            QPushButton:hover { background: #1E293B; }
        """)
        
        btn_save = QPushButton("Save Insight")
        btn_save.setFixedHeight(46)
        btn_save.setStyleSheet("""
            QPushButton { background: white; border: 1px solid #E2E8F0; border-radius: 12px; color: #0F172A; font-weight: 800; font-size: 13px; }
            QPushButton:hover { background: #F8FAFC; }
        """)
        
        al.addWidget(btn_plan)
        al.addWidget(btn_save)
        self.main_layout.addLayout(al)
