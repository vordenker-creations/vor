from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernCard")
        self.setStyleSheet("""
            #ModernCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(15, 23, 42, 10))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)

class MockInterviewsPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(16)
        
        title_lbl = QLabel("🎙 Mock Interviews")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        
        btn_practice = QPushButton("Start AI Voice Interview")
        btn_practice.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_practice.setStyleSheet("""
            QPushButton {
                background: #8B5CF6; color: white; font-weight: 700; font-size: 13px;
                border-radius: 18px; padding: 0 20px; height: 36px; border: none;
            }
            QPushButton:hover { background: #7C3AED; }
        """)
        header_layout.addWidget(btn_practice)
        
        main_layout.addWidget(header)
        
        # Content Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        # Categories
        cat_title = QLabel("Select Interview Type")
        cat_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        content_layout.addWidget(cat_title)
        
        grid = QGridLayout()
        grid.setSpacing(16)
        
        types = [
            ("Technical: System Design", "Architect scalable systems. Real-world constraints.", "🏗", "#38BDF8"),
            ("Behavioral & Soft Skills", "STAR method, cultural fit, leadership.", "🤝", "#10B981"),
            ("Frontend Engineering", "React, DOM, Web Performance, CSS.", "🎨", "#F59E0B"),
            ("Backend Engineering", "Databases, API design, concurrency.", "⚙", "#6366F1")
        ]
        
        row, col = 0, 0
        for title, desc, icon, color in types:
            card = ModernCard()
            card.internal_layout.setSpacing(12)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.setStyleSheet(card.styleSheet() + """
                #ModernCard:hover { border: 1px solid #CBD5E1; background: #F8FAFC; }
            """)
            
            i_lbl = QLabel(icon)
            i_lbl.setStyleSheet(f"font-size: 32px; background: {color}15; padding: 12px; border-radius: 12px;")
            i_lbl.setFixedSize(56, 56)
            i_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
            
            d_lbl = QLabel(desc)
            d_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
            d_lbl.setWordWrap(True)
            
            card.internal_layout.addWidget(i_lbl)
            card.internal_layout.addWidget(t_lbl)
            card.internal_layout.addWidget(d_lbl)
            card.internal_layout.addStretch()
            
            grid.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        content_layout.addLayout(grid)
        
        # Past Performance
        past_title = QLabel("Recent Interview Feedback")
        past_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; margin-top: 10px;")
        content_layout.addWidget(past_title)
        
        past_card = ModernCard()
        pc_l = past_card.internal_layout
        
        p_row = QHBoxLayout()
        p_info = QVBoxLayout()
        p_t = QLabel("Behavioral Interview - Google Standard")
        p_t.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 700;")
        p_d = QLabel("Date: May 28, 2026 • AI Reviewer: Passed")
        p_d.setStyleSheet("color: #64748B; font-size: 12px;")
        p_info.addWidget(p_t)
        p_info.addWidget(p_d)
        
        p_row.addLayout(p_info)
        p_row.addStretch()
        
        score = QLabel("Score: 8.5/10")
        score.setStyleSheet("color: #10B981; font-weight: 800; font-size: 14px; background: #D1FAE5; padding: 6px 12px; border-radius: 8px;")
        p_row.addWidget(score)
        
        pc_l.addLayout(p_row)
        content_layout.addWidget(past_card)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
