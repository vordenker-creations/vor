from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

def apply_subtle_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(15, 23, 42, 20))
    widget.setGraphicsEffect(shadow)

class ToolCard(QFrame):
    def __init__(self, title, description, icon, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            ToolCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 16px;
            }
            ToolCard:hover {
                border-color: #38BDF8;
                background-color: #F8FAFC;
            }
        """)
        apply_subtle_shadow(self)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        header = QHBoxLayout()
        ico_lbl = QLabel(icon)
        ico_lbl.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        header.addWidget(ico_lbl)
        header.addStretch()
        layout.addLayout(header)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none;")
        layout.addWidget(title_lbl)
        
        desc_lbl = QLabel(description)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 12px; color: #64748B; line-height: 1.4; border: none;")
        layout.addWidget(desc_lbl)

class ToolsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(320)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 20)
        layout.setSpacing(24)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(24)
        
        # Section 1: AI Tools
        tools_header = QLabel("AI Career Tools")
        tools_header.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        c_layout.addWidget(tools_header)
        
        tools_grid = QVBoxLayout()
        tools_grid.setSpacing(12)
        
        tools = [
            ("Resume Analyzer", "Deep analysis of your CV.", "📄"),
            ("Career Roadmap", "Personalized skill path.", "🗺️"),
            ("Interview Simulator", "AI-powered mock interviews.", "🎙️"),
            ("Job Matcher", "Find jobs that fit your profile.", "💼")
        ]
        
        for t, d, i in tools:
            tools_grid.addWidget(ToolCard(t, d, i))
        c_layout.addLayout(tools_grid)
        
        # Section 2: AI Context
        context_header = QLabel("AI Memory & Context")
        context_header.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        c_layout.addWidget(context_header)
        
        context_card = QFrame()
        context_card.setStyleSheet("background-color: #F8FAFC; border-radius: 16px; padding: 16px; border: 1px solid #E2E8F0;")
        cl = QVBoxLayout(context_card)
        cl.setSpacing(10)
        
        ctx_items = [
            ("Current Goal", "Software Engineer at Google"),
            ("Active Files", "Resume_2026.pdf, Thesis.docx")
        ]
        for label, val in ctx_items:
            row = QVBoxLayout()
            row.setSpacing(2)
            l_lbl = QLabel(label)
            l_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #94A3B8; border: none;")
            v_lbl = QLabel(val)
            v_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #1E293B; border: none;")
            row.addWidget(l_lbl)
            row.addWidget(v_lbl)
            cl.addLayout(row)
        c_layout.addWidget(context_card)
        
        # Section 3: Quick Actions
        actions_header = QLabel("Quick Actions")
        actions_header.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        c_layout.addWidget(actions_header)
        
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(8)
        for action in ["Generate Resume", "Analyze Assignment", "Summarize PDF"]:
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
        c_layout.addLayout(actions_layout)
        
        c_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
