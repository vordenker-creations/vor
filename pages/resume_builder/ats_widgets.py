from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor, QPainter, QBrush, QPen

class ATSScoreCircle(QWidget):
    def __init__(self, score=85, size=140, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.score = score
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        
        # Background
        painter.setPen(QPen(QColor("#E2E8F0"), 10))
        painter.drawEllipse(rect)
        
        # Progress
        color = QColor("#38BDF8")
        if self.score > 90: color = QColor("#10B981")
        elif self.score < 60: color = QColor("#EF4444")
            
        painter.setPen(QPen(color, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        span = int(-self.score / 100.0 * 360 * 16)
        painter.drawArc(rect, 90 * 16, span)
        
        # Text
        painter.setPen(QColor("#0F172A"))
        font = QFont("Inter", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.score}")

class MetricCard(QFrame):
    def __init__(self, title, value, status="Good", color="#38BDF8", parent=None):
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
        v.setStyleSheet("font-size: 20px; font-weight: 700; color: #0F172A; border: none;")
        
        s = QLabel(status)
        s.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {color}15; padding: 2px 8px; border-radius: 6px; border: none;")
        s.setFixedWidth(s.sizeHint().width() + 16)
        
        l.addWidget(t)
        l.addWidget(v)
        l.addWidget(s)

class ATSOverviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(24)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(32)
        
        # 1. Main Score Row
        score_row = QHBoxLayout()
        score_row.setSpacing(24)
        
        score_card = QFrame()
        score_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        sl = QHBoxLayout(score_card)
        sl.setContentsMargins(32, 32, 32, 32)
        sl.setSpacing(40)
        
        self.score_circ = ATSScoreCircle(85)
        sl.addWidget(self.score_circ)
        
        score_info = QVBoxLayout()
        score_info.setSpacing(8)
        st = QLabel("Overall ATS Score")
        st.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        sd = QLabel("Your resume is well-optimized for <b>Data Science</b> roles.\nMinor formatting issues detected in the header.")
        sd.setWordWrap(True)
        sd.setStyleSheet("font-size: 13px; color: #64748B; border: none;")
        
        btn_opt = QPushButton("✨ AI Quick Fix")
        btn_opt.setFixedSize(140, 36)
        btn_opt.setStyleSheet("""
            QPushButton { background: #0F172A; color: white; border-radius: 10px; font-weight: 700; font-size: 12px; }
            QPushButton:hover { background: #1E293B; }
        """)
        
        score_info.addWidget(st)
        score_info.addWidget(sd)
        score_info.addSpacing(8)
        score_info.addWidget(btn_opt)
        score_info.addStretch()
        sl.addLayout(score_info, 1)
        
        score_row.addWidget(score_card, 3)

        trend_card = QFrame()
        trend_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        tl = QVBoxLayout(trend_card)
        tl.setContentsMargins(24, 24, 24, 24)
        tl.addWidget(QLabel("Score Trend", styleSheet="font-size: 13px; font-weight: 700; color: #0F172A; border: none;"))
        # Mock trend graph placeholder
        graph = QFrame()
        graph.setStyleSheet("background: #F8FAFC; border-radius: 12px; border: 1px dashed #E2E8F0;")
        tl.addWidget(graph)
        score_row.addWidget(trend_card, 2)

        cl.addLayout(score_row)
        
        # 2. Metrics Grid
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(MetricCard("Recruiter Scan", "4.2s", "Fast", "#10B981"), 0, 0)
        grid.addWidget(MetricCard("Keywords", "18/24", "Moderate", "#F59E0B"), 0, 1)
        grid.addWidget(MetricCard("Formatting", "98%", "Excellent", "#10B981"), 0, 2)
        grid.addWidget(MetricCard("AI Confidence", "High", "Verified", "#38BDF8"), 0, 3)
        cl.addLayout(grid)
        
        # 3. Weak Sections
        weak_sec = QFrame()
        weak_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        wl = QVBoxLayout(weak_sec)
        wl.setContentsMargins(24, 24, 24, 24)
        wl.setSpacing(16)
        wl.addWidget(QLabel("Critical Fixes Required", styleSheet="font-size: 15px; font-weight: 700; color: #0F172A; border: none;"))
        
        for issue in ["Missing 'Cloud Computing' keyword", "Header layout parsing conflict", "Invalid date format in Work Experience"]:
            row = QHBoxLayout()
            row.setSpacing(12)
            icon = QLabel("⚠️")
            txt = QLabel(issue)
            txt.setStyleSheet("font-size: 13px; color: #475569; border: none;")
            fix = QPushButton("Fix")
            fix.setStyleSheet("color: #38BDF8; font-weight: 700; border: none; background: transparent;")
            row.addWidget(icon); row.addWidget(txt, 1); row.addWidget(fix)
            wl.addLayout(row)
            
        cl.addWidget(weak_sec)
        cl.addStretch()
        
        scroll.setWidget(container)
        l.addWidget(scroll)

class KeywordAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self)
        l.setContentsMargins(32, 24, 32, 32)
        l.setSpacing(24)
        l.addWidget(QLabel("Keyword Intelligence", styleSheet="font-size: 20px; font-weight: 800; color: #0F172A;"))
        # ... simplified for brevity, following the same SaaS design
        msg = QLabel("Rest of analysis modules (Formatting, Readability, etc.) use this enterprise layout scheme.")
        msg.setStyleSheet("color: #64748B; font-size: 14px;")
        l.addWidget(msg)
        l.addStretch()
