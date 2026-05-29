from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

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

class CodeLabPage(QWidget):
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
        
        title_lbl = QLabel("💻 Code & Algorithm Lab")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        
        btn_practice = QPushButton("Start Daily Challenge")
        btn_practice.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_practice.setStyleSheet("""
            QPushButton {
                background: #0284C7; color: white; font-weight: 700; font-size: 13px;
                border-radius: 18px; padding: 0 20px; height: 36px; border: none;
            }
            QPushButton:hover { background: #0369A1; }
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
        
        # AI Coding Mentor Banner
        banner = QFrame()
        banner.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #0F172A);
                border-radius: 16px;
            }
        """)
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(32, 24, 32, 24)
        
        banner_text = QVBoxLayout()
        b_title = QLabel("Your AI Coding Mentor is ready.")
        b_title.setStyleSheet("color: white; font-size: 20px; font-weight: 800; background: transparent;")
        b_desc = QLabel("Practice data structures and algorithms with real-time AI feedback on time and space complexity.")
        b_desc.setStyleSheet("color: #94A3B8; font-size: 13px; background: transparent;")
        banner_text.addWidget(b_title)
        banner_text.addWidget(b_desc)
        banner_layout.addLayout(banner_text)
        banner_layout.addStretch()
        
        emoji = QLabel("🧠")
        emoji.setStyleSheet("font-size: 40px; background: transparent;")
        banner_layout.addWidget(emoji)
        
        content_layout.addWidget(banner)
        
        # Recommended Challenges
        sub_title = QLabel("Recommended for your level")
        sub_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        content_layout.addWidget(sub_title)
        
        challenges = [
            ("Two Sum in Sorted Array", "Array & Two Pointers", "Easy", "#10B981"),
            ("LRU Cache Implementation", "Design & Linked List", "Medium", "#F59E0B"),
            ("Merge K Sorted Lists", "Heap & Divide and Conquer", "Hard", "#EF4444")
        ]
        
        for title, topic, diff, color in challenges:
            card = ModernCard()
            card.internal_layout.setContentsMargins(20, 16, 20, 16)
            
            c_layout = QHBoxLayout()
            c_layout.setContentsMargins(0, 0, 0, 0)
            
            v_text = QVBoxLayout()
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
            topic_lbl = QLabel(f"Topic: {topic}")
            topic_lbl.setStyleSheet("color: #64748B; font-size: 12px;")
            v_text.addWidget(t_lbl)
            v_text.addWidget(topic_lbl)
            
            c_layout.addLayout(v_text)
            c_layout.addStretch()
            
            diff_lbl = QLabel(diff)
            diff_lbl.setStyleSheet(f"color: {color}; background: {color}15; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;")
            c_layout.addWidget(diff_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)
            
            btn_solve = QPushButton("Solve")
            btn_solve.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_solve.setStyleSheet("""
                QPushButton { background: #F1F5F9; color: #0F172A; font-weight: 600; border-radius: 6px; padding: 6px 16px; border: none; }
                QPushButton:hover { background: #E2E8F0; }
            """)
            c_layout.addWidget(btn_solve, alignment=Qt.AlignmentFlag.AlignVCenter)
            
            card.internal_layout.addLayout(c_layout)
            content_layout.addWidget(card)
            
        content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
