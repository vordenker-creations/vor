from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class MatchingCard(QFrame):
    def __init__(self, title, text, icon="✨", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            MatchingCard {
                background-color: #F0F9FF;
                border: 1px solid #BAE6FD;
                border-radius: 18px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        th = QHBoxLayout()
        t_lbl = QLabel(f"{icon} {title}")
        t_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0284C7; border: none; background: transparent;")
        th.addWidget(t_lbl)
        th.addStretch()
        layout.addLayout(th)
        
        d_lbl = QLabel(text)
        d_lbl.setWordWrap(True)
        d_lbl.setStyleSheet("font-size: 13px; color: #1E293B; line-height: 1.6; border: none; background: transparent;")
        layout.addWidget(d_lbl)

class TrackerItem(QFrame):
    def __init__(self, title, company, status, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            TrackerItem {
                background-color: #FFFFFF;
                border: 1.5px solid #E2E8F0;
                border-radius: 14px;
                padding: 12px;
            }
            TrackerItem:hover { border-color: #38BDF8; background-color: #F8FAFC; }
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        
        c_lbl = QLabel(company)
        c_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none; background: transparent;")
        
        info_v.addWidget(t_lbl)
        info_v.addWidget(c_lbl)
        layout.addLayout(info_v, 1)
        
        s_container = QFrame()
        s_container.setStyleSheet(f"background-color: {color}20; border-radius: 8px;")
        sl = QVBoxLayout(s_container)
        sl.setContentsMargins(8, 4, 8, 4)
        
        s_lbl = QLabel(status)
        s_lbl.setStyleSheet(f"font-size: 10px; font-weight: 800; color: {color}; border: none; background: transparent; text-transform: uppercase;")
        sl.addWidget(s_lbl)
        
        layout.addWidget(s_container)

class AIInsightsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(360)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 32, 24, 24)
        layout.setSpacing(32)
        
        # Header
        title_v = QVBoxLayout()
        title_v.setSpacing(4)
        title = QLabel("AI Career Assistant")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        
        status_h = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet("color: #10B981; font-size: 10px;")
        status_lbl = QLabel("AI matching engine is active")
        status_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #64748B;")
        status_h.addWidget(dot)
        status_h.addWidget(status_lbl)
        status_h.addStretch()
        
        title_v.addWidget(title)
        title_v.addLayout(status_h)
        layout.addLayout(title_v)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(28)
        
        # Section 1: Optimization
        opt_v = QVBoxLayout()
        opt_v.setSpacing(12)
        matching_header = QLabel("Optimization Tips")
        matching_header.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A;")
        opt_v.addWidget(matching_header)
        
        opt_v.addWidget(MatchingCard("Skill Gap", "Adding 'Kubernetes' and 'Terraform' to your profile would match 15 more high-paying roles.", "🎯"))
        opt_v.addWidget(MatchingCard("Resume Power", "Your experience at 'Google' is a strong attractor. Highlight your 'Lead' role more prominently.", "💪"))
        cl.addLayout(opt_v)
        
        # Section 2: Application Tracker
        tracker_v = QVBoxLayout()
        tracker_v.setSpacing(12)
        tracker_header = QLabel("Active Applications")
        tracker_header.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A;")
        tracker_v.addWidget(tracker_header)
        
        tracker_v.addWidget(TrackerItem("AI Research Lead", "DeepMind", "Interview", "#10B981"))
        tracker_v.addWidget(TrackerItem("Senior ML Engineer", "OpenAI", "Applied", "#38BDF8"))
        tracker_v.addWidget(TrackerItem("Software Architect", "Microsoft", "Assessment", "#F59E0B"))
        
        cl.addLayout(tracker_v)
        
        # Section 3: Salary Insights
        salary_v = QVBoxLayout()
        salary_v.setSpacing(12)
        salary_header = QLabel("Market Insights")
        salary_header.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A;")
        salary_v.addWidget(salary_header)
        
        salary_card = QFrame()
        salary_card.setStyleSheet("background-color: #F8FAFC; border-radius: 18px; padding: 20px; border: 1px solid #E2E8F0;")
        sl = QVBoxLayout(salary_card)
        sl.setSpacing(8)
        
        salary_val = QLabel("$165,000 - $220,000")
        salary_val.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        
        salary_desc = QLabel("Estimated market value for your current skill set in the US/Remote market.")
        salary_desc.setWordWrap(True)
        salary_desc.setStyleSheet("font-size: 12px; color: #64748B; line-height: 1.5;")
        
        sl.addWidget(salary_val)
        sl.addWidget(salary_desc)
        salary_v.addWidget(salary_card)
        cl.addLayout(salary_v)
        
        cl.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Quick Actions
        actions_v = QVBoxLayout()
        actions_v.setSpacing(10)
        
        actions = [
            ("✨ Generate Cover Letter", "#0F172A", "white"),
            ("📝 Optimize Resume", "#F1F5F9", "#1E293B"),
            ("🚀 Prep for Interview", "#F1F5F9", "#1E293B")
        ]
        
        for text, bg, color in actions:
            btn = QPushButton(text)
            btn.setFixedHeight(48)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg}; color: {color}; border-radius: 14px;
                    font-size: 14px; font-weight: 700; border: none;
                }}
                QPushButton:hover {{ opacity: 0.9; background-color: {bg if bg != "#F1F5F9" else "#E2E8F0"}; }}
            """)
            actions_v.addWidget(btn)
            
        layout.addLayout(actions_v)
