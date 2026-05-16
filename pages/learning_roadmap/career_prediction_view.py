from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor, QPainter, QBrush, QPen

class CareerNode(QFrame):
    def __init__(self, title, icon, readiness, demand, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 120)
        self.setStyleSheet("""
            QFrame {
                background: white; border: 2px solid #E2E8F0; border-radius: 20px;
            }
            QFrame:hover {
                border-color: #38BDF8;
            }
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 12, 16, 12)
        l.setSpacing(6)
        
        h = QHBoxLayout()
        ico = QLabel(icon); ico.setStyleSheet("font-size: 16px; border: none;")
        tag = QLabel("Recommended")
        tag.setStyleSheet("font-size: 9px; font-weight: 800; color: #38BDF8; background: #38BDF815; padding: 2px 6px; border-radius: 4px; border: none;")
        h.addWidget(ico); h.addStretch(); h.addWidget(tag)
        l.addLayout(h)
        
        t = QLabel(title)
        t.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none;")
        l.addWidget(t)
        
        l.addStretch()
        
        ph = QHBoxLayout()
        ph.addWidget(QLabel("Ready:", styleSheet="font-size: 10px; color: #64748B; border: none;"))
        ph.addStretch()
        ph.addWidget(QLabel(f"{readiness}%", styleSheet="font-size: 10px; font-weight: 800; color: #10B981; border: none;"))
        l.addLayout(ph)

class PredictionMetric(QFrame):
    def __init__(self, title, value, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: white; border: 1px solid #E2E8F0; border-radius: 20px;
            }}
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(8)
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; border: none;")
        
        v = QLabel(value)
        v.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {color}; border: none;")
        
        l.addWidget(t)
        l.addWidget(v)

class CareerPredictionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(32)

        # 1. Career Hero
        hero_card = QFrame()
        hero_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero_card)
        hl.setContentsMargins(32, 32, 32, 32)
        hl.setSpacing(40)
        
        info_v = QVBoxLayout()
        info_v.setSpacing(12)
        pt = QLabel("✨ Top Career Prediction")
        pt.setStyleSheet("font-size: 13px; font-weight: 800; color: #38BDF8; text-transform: uppercase;")
        
        role = QLabel("Senior Machine Learning Engineer")
        role.setStyleSheet("font-size: 28px; font-weight: 800; color: #0F172A; border: none; letter-spacing: -0.5px;")
        
        desc = QLabel("Your current skill graph is 84% aligned with high-growth ML Lead roles. We've identified a specialization branch in <b>Generative AI</b> that could increase your market value by 35%.")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        
        btns = QHBoxLayout()
        btns.setSpacing(12)
        btn_opt = QPushButton("Optimize Roadmap")
        btn_opt.setStyleSheet("background: #0F172A; color: white; border-radius: 12px; font-weight: 700; font-size: 13px; padding: 12px 24px;")
        btn_sim = QPushButton("Simulate Shift")
        btn_sim.setStyleSheet("background: white; border: 1.5px solid #E2E8F0; color: #0F172A; border-radius: 12px; font-weight: 700; font-size: 13px; padding: 12px 24px;")
        btns.addWidget(btn_opt); btns.addWidget(btn_sim); btns.addStretch()
        
        info_v.addWidget(pt); info_v.addWidget(role); info_v.addWidget(desc); info_v.addSpacing(10); info_v.addLayout(btns)
        hl.addLayout(info_v, 1)
        
        stats_v = QVBoxLayout()
        stats_v.setSpacing(16)
        stats_v.addWidget(PredictionMetric("Job Readiness", "84%", "#10B981"))
        stats_v.addWidget(PredictionMetric("Salary Range", "$160k - $240k", "#38BDF8"))
        hl.addLayout(stats_v)
        
        cl.addWidget(hero_card)

        # 2. Branching Map Label
        map_title = QLabel("Specialization Branching Map")
        map_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        cl.addWidget(map_title)

        # 3. Branching Map Canvas (Simplified Grid)
        map_container = QFrame()
        map_container.setStyleSheet("background: #F1F5F9; border-radius: 24px; border: 1px dashed #CBD5E1;")
        map_container.setMinimumHeight(350)
        ml = QGridLayout(map_container)
        ml.setContentsMargins(40, 40, 40, 40)
        ml.setSpacing(32)
        
        ml.addWidget(CareerNode("Current: AI Engineer", "💻", 100, 92), 1, 0)
        
        # Branch 1
        ml.addWidget(CareerNode("ML Ops Architect", "⚙️", 65, 88), 0, 1)
        # Branch 2
        ml.addWidget(CareerNode("Generative AI Lead", "✨", 42, 98), 1, 1)
        # Branch 3
        ml.addWidget(CareerNode("Data Scientist (Senior)", "📊", 78, 85), 2, 1)
        
        cl.addWidget(map_container)
        
        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
