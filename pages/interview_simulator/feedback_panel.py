from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect, 
                             QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class FeedbackCard(QFrame):
    def __init__(self, title, score, status, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            FeedbackCard {{
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E2E8F0;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        header = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;")
        header.addWidget(t_lbl)
        header.addStretch()
        
        s_lbl = QLabel(f"{score}%")
        s_lbl.setStyleSheet(f"font-size: 14px; font-weight: 800; color: {color};")
        header.addWidget(s_lbl)
        layout.addLayout(header)
        
        bar = QProgressBar()
        bar.setValue(score)
        bar.setFixedHeight(6)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{ background-color: #F1F5F9; border-radius: 3px; border: none; }}
            QProgressBar::chunk {{ background-color: {color}; border-radius: 3px; }}
        """)
        layout.addWidget(bar)
        
        st_lbl = QLabel(status)
        st_lbl.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {color};")
        layout.addWidget(st_lbl)

class CoachingInsight(QFrame):
    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            CoachingInsight {
                background-color: #F0F9FF;
                border-radius: 12px;
                border: 1px solid #BAE6FD;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        
        t_lbl = QLabel(f"✨ {title}")
        t_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #0284C7;")
        layout.addWidget(t_lbl)
        
        d_lbl = QLabel(text)
        d_lbl.setWordWrap(True)
        d_lbl.setStyleSheet("font-size: 12px; color: #1E293B; line-height: 1.4;")
        layout.addWidget(d_lbl)

class FeedbackPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 20)
        layout.setSpacing(24)
        
        title = QLabel("AI Feedback")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(20)
        
        # Realtime Metrics
        cl.addWidget(FeedbackCard("Speaking Confidence", 84, "Excellent", "#10B981"))
        cl.addWidget(FeedbackCard("Clarity Score", 72, "Good progress", "#38BDF8"))
        cl.addWidget(FeedbackCard("Filler Words", 15, "Needs work", "#EF4444"))
        
        # AI Coaching
        coaching_title = QLabel("AI Coaching Insights")
        coaching_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; margin-top: 10px;")
        cl.addWidget(coaching_title)
        
        cl.addWidget(CoachingInsight("Pacing Analysis", "Your speaking speed is 130 wpm. This is ideal for professional communication."))
        cl.addWidget(CoachingInsight("Action Verbs", "Try using more impactful words like 'Spearheaded' instead of 'Managed'."))
        
        cl.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Quick Actions
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(8)
        for action in ["Generate Better Answer", "Retry Question", "Export Report"]:
            btn = QPushButton(action)
            btn.setFixedHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #F1F5F9; color: #1E293B; border-radius: 12px;
                    font-size: 13px; font-weight: 600; border: 1px solid #E2E8F0;
                }
                QPushButton:hover { background-color: #E2E8F0; }
            """)
            actions_layout.addWidget(btn)
        layout.addLayout(actions_layout)
