from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor, QPainter, QBrush, QPen

class ATSScoreCard(QFrame):
    def __init__(self, score, parent=None):
        super().__init__(parent)
        self.setFixedHeight(180)
        self.setStyleSheet("""
            ATSScoreCard {
                background-color: #0F172A;
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)
        
        # Circular Score (Custom paint would be better, but using CSS for simplicity)
        self.score_lbl = QLabel(str(score))
        self.score_lbl.setFixedSize(80, 80)
        self.score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_lbl.setStyleSheet(f"""
            color: #38BDF8; font-size: 28px; font-weight: 800;
            border: 4px solid #38BDF8; border-radius: 40px;
            background: transparent;
        """)
        layout.addWidget(self.score_lbl)
        
        title = QLabel("ATS Score")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: 700;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        status = QLabel("Highly Optimized")
        status.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 500;")
        layout.addWidget(status, alignment=Qt.AlignmentFlag.AlignCenter)

class RecommendationCard(QFrame):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            RecommendationCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        t_lbl = QLabel(f"✨ {title}")
        t_lbl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 700;")
        layout.addWidget(t_lbl)
        
        d_lbl = QLabel(description)
        d_lbl.setWordWrap(True)
        d_lbl.setStyleSheet("color: #64748B; font-size: 12px; line-height: 1.4;")
        layout.addWidget(d_lbl)

class ATSPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(360)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 20)
        layout.setSpacing(24)
        
        # Section 1: Score
        layout.addWidget(ATSScoreCard(82))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(24)
        
        # Section 2: Missing Keywords
        kw_header = QLabel("Missing Keywords")
        kw_header.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        cl.addWidget(kw_header)
        
        kw_flow = QHBoxLayout()
        kw_flow.setSpacing(8)
        for kw in ["Cloud Architecture", "Docker", "Agile"]:
            lbl = QLabel(kw)
            lbl.setStyleSheet("""
                background-color: #FEF2F2; color: #EF4444; padding: 6px 12px;
                border-radius: 8px; font-size: 11px; font-weight: 700;
            """)
            kw_flow.addWidget(lbl)
        kw_flow.addStretch()
        cl.addLayout(kw_flow)
        
        # Section 3: AI Recommendations
        ai_header = QLabel("AI Recommendations")
        ai_header.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        cl.addWidget(ai_header)
        
        recs = [
            ("Improve Experience", "Use more action verbs like 'Architected' or 'Spearheaded' in your Google role."),
            ("Skills Gap", "Adding 'Kubernetes' would increase your match score by 12% for this job."),
            ("Formatting Fix", "Ensure your dates are in MM/YYYY format for better ATS parsing.")
        ]
        
        for t, d in recs:
            cl.addWidget(RecommendationCard(t, d))
            
        cl.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Section 4: Template Selector (Thumbnail style)
        temp_header = QLabel("Change Template")
        temp_header.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        layout.addWidget(temp_header)
        
        temps = QHBoxLayout()
        temps.setSpacing(12)
        for i in range(3):
            t_mock = QFrame()
            t_mock.setFixedSize(80, 110)
            color = "#38BDF8" if i == 0 else "#E2E8F0"
            t_mock.setStyleSheet(f"background-color: white; border: 2px solid {color}; border-radius: 8px;")
            temps.addWidget(t_mock)
        temps.addStretch()
        layout.addLayout(temps)
