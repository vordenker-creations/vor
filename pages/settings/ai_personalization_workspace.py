from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QSlider, QComboBox, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QCursor, QLinearGradient, QBrush, QPainter
from .common_widgets import ToggleRow

class PersonalityCard(QFrame):
    def __init__(self, name, icon, desc, parent=None):
        super().__init__(parent)
        self.setFixedHeight(140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #E2E8F0;
                border-radius: 20px;
            }
            QFrame:hover {
                border-color: #38BDF8;
                background-color: #F8FAFC;
            }
            QFrame[selected="true"] {
                border-color: #38BDF8;
                background-color: #F0F9FF;
            }
        """)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(6)
        
        h = QHBoxLayout()
        ico = QLabel(icon); ico.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        h.addWidget(ico); h.addStretch()
        l.addLayout(h)
        
        t = QLabel(name)
        t.setStyleSheet("font-weight: 700; font-size: 14px; color: #0F172A; border: none; background: transparent;")
        l.addWidget(t)
        
        d = QLabel(desc)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        l.addWidget(d)

    def set_selected(self, selected):
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

class AIPersonalityWorkspace(QWidget):
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

        # 1. Hero Analytics
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(24)
        
        info = QVBoxLayout(); info.setSpacing(8)
        tag = QLabel("✨ ADAPTIVE INTELLIGENCE")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("AI Personalization Studio")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your AI Assistant is currently in <b>Mentor Mode</b>. Conversational alignment is at 96%, with optimized proactive coaching active.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        metrics = QGridLayout(); metrics.setSpacing(12)
        def add_metric(val, label, r, c):
            v = QVBoxLayout(); v.setSpacing(2); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l1 = QLabel(val); l1.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
            l2 = QLabel(label); l2.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
            v.addWidget(l1); v.addWidget(l2); metrics.addLayout(v, r, c)
            
        add_metric("Mentor", "Mode", 0, 0); add_metric("96%", "Alignment", 0, 1)
        add_metric("High", "Intensity", 1, 0); add_metric("Active", "Memory", 1, 1)
        hl.addLayout(metrics)
        cl.addWidget(hero)

        # 2. Personality System
        pers_sec = QWidget()
        pl = QVBoxLayout(pers_sec); pl.setContentsMargins(0, 0, 0, 0); pl.setSpacing(16)
        pl.addWidget(QLabel("AI Personalities", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        grid = QGridLayout(); grid.setSpacing(16)
        grid.addWidget(PersonalityCard("Professional", "💼", "Polished, concise, and enterprise-ready assistance."), 0, 0)
        grid.addWidget(PersonalityCard("Mentor Mode", "🎓", "Proactive guidance with deep career insights."), 0, 1)
        grid.addWidget(PersonalityCard("Friendly", "🤝", "Casual, empathetic, and encouraging tone."), 1, 0)
        grid.addWidget(PersonalityCard("Technical", "💻", "Code-heavy, precise, and documentation-focused."), 1, 1)
        pl.addLayout(grid)
        cl.addWidget(pers_sec)

        # 3. Communication Style
        comm_card = QFrame()
        comm_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        cv = QVBoxLayout(comm_card); cv.setContentsMargins(24, 24, 24, 24); cv.setSpacing(24)
        cv.addWidget(QLabel("Communication Style", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        def add_slider(label, val):
            v = QVBoxLayout(); v.setSpacing(8)
            hl = QHBoxLayout()
            hl.addWidget(QLabel(label, styleSheet="font-size: 13px; font-weight: 600; color: #475569; border: none;"))
            hl.addStretch()
            val_lbl = QLabel(val, styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;")
            hl.addWidget(val_lbl)
            v.addLayout(hl)
            s = QSlider(Qt.Orientation.Horizontal)
            s.setStyleSheet("QSlider::groove:horizontal { height: 4px; background: #F1F5F9; border-radius: 2px; } QSlider::handle:horizontal { background: #38BDF8; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }")
            v.addWidget(s); cv.addLayout(v)
            
        add_slider("Response Formality", "Formal")
        add_slider("Explanation Depth", "Comprehensive")
        add_slider("Coaching Intensity", "Proactive")
        
        cl.addWidget(comm_card)

        # 4. Behavior & Memory
        behav_card = QFrame()
        behav_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        bv = QVBoxLayout(behav_card); bv.setContentsMargins(24, 24, 24, 24); bv.setSpacing(20)
        bv.addWidget(QLabel("Intelligence & Memory", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        bv.addWidget(ToggleRow("Adaptive Learning", "Allow AI to learn from your workflows and interaction patterns."))
        bv.addWidget(ToggleRow("Conversational Memory", "Retain context from previous chats for personalized assistance."))
        bv.addWidget(ToggleRow("Proactive Suggestions", "AI will offer insights without being explicitly prompted."))
        bv.addWidget(ToggleRow("Contextual Awareness", "Use active workspace data to improve response accuracy."))
        
        cl.addWidget(behav_card)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
