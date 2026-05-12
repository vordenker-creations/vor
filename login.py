import sys
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QApplication)
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from PyQt6.QtGui import QPainter, QColor, QFont, QCursor

from config import COLOR_BG_APP, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB, COLOR_BORDER
from components import SaaSCard

class LoginPage(QWidget):
    def __init__(self, parent=None, on_login=None, on_register_click=None):
        super().__init__(parent)
        self.on_login = on_login
        self.on_register_click = on_register_click
        self.setObjectName("LoginPage")
        
        # Base Application Background
        self.setStyleSheet(f"background-color: {COLOR_BG_APP};")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.circles = []
        self._generate_circles()
        
        self._setup_sidebar()
        self._setup_content()

    def _generate_circles(self):
        # Modern Neon Colors for background orbs
        colors = [QColor(0, 209, 255), QColor(16, 185, 129), QColor(99, 102, 241)] 
        for _ in range(12):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            r = random.randint(30, 90)
            color = random.choice(colors)
            self.circles.append((x, y, r, color))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for x, y, r, color in self.circles:
            for i in range(4):
                alpha_r = r + (i * 15)
                painter.setPen(QColor(color.red(), color.green(), color.blue(), 20))
                painter.drawEllipse(QPoint(x, y), alpha_r, alpha_r)

    def _setup_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(400)
        # Using a slight semi-transparent overlay to match Glassmorphism vibe
        sidebar.setStyleSheet(f"background-color: rgba(30, 42, 56, 0.4); border-right: 1px solid rgba(255, 255, 255, 0.05);")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(50, 100, 40, 60)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_insight = QLabel("AI INSIGHT")
        lbl_insight.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 36px; font-weight: 900; background: transparent;")
        sidebar_layout.addWidget(lbl_insight)
        
        lbl_desc = QLabel("Elevate your career with AI-driven analytics and personal roadmaps.")
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 15px; margin-top: 15px; background: transparent;")
        sidebar_layout.addWidget(lbl_desc)
        
        sidebar_layout.addSpacing(50)
        
        tags = ["Python", "Neural Networks", "NLP", "Computer Vision", "Data Science", "Cloud AI"]
        for tag in tags:
            btn = QPushButton(f"• {tag}")
            btn.setFixedSize(160, 34)
            # Modern frosted ghost-button look for tags
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.03);
                    color: {COLOR_TEXT_MAIN};
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 17px;
                    font-size: 12px;
                    text-align: left;
                    padding-left: 15px;
                }}
            """)
            sidebar_layout.addWidget(btn)
            sidebar_layout.addSpacing(8)
            
        self.main_layout.addWidget(sidebar)

    def _setup_content(self):
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Central Login Card Container
        self.card = QFrame()
        # Ensure exact specificity so global stylesheets don't accidentally hide the card background or text
        self.card.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(30, 42, 56, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
            }}
        """)
        self.card.setFixedSize(480, 580)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        
        lbl_login = QLabel("LOGIN")
        lbl_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_login.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 30px; font-weight: 800; background: transparent; border: none;")
        card_layout.addWidget(lbl_login)
        
        lbl_sub = QLabel("Access your professional bridge.")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_sub.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 14px; background: transparent; border: none;")
        card_layout.addWidget(lbl_sub)
        
        card_layout.addSpacing(35)
        
        self.email_lbl, self.email_entry = self._create_input("Email Address", "email@vku.udn.vn")
        card_layout.addWidget(self.email_lbl)
        card_layout.addWidget(self.email_entry)
        
        card_layout.addSpacing(15)
        
        self.pass_lbl, self.pass_entry = self._create_input("Password", "••••••••", is_password=True)
        card_layout.addWidget(self.pass_lbl)
        card_layout.addWidget(self.pass_entry)
        
        card_layout.addSpacing(40)
        
        btn_login = QPushButton("LOGIN")
        btn_login.setFixedHeight(48)
        btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Ensure the Login Button text stands out (dark text on bright background)
        # Avoid inheritance from QFrame making text white on cyan
        btn_login.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: #000000;
                font-weight: 800;
                font-size: 14px;
                border-radius: 12px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #33EEFF;
            }}
            QPushButton:pressed {{
                background-color: #00A6CC;
            }}
        """)
        btn_login.clicked.connect(self._handle_login)
        card_layout.addWidget(btn_login)
        
        card_layout.addSpacing(20)
        
        reg_layout = QHBoxLayout()
        reg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_new = QLabel("New here?")
        lbl_new.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 13px; background: transparent; border: none;")
        reg_layout.addWidget(lbl_new)
        
        btn_reg = QPushButton("Create Account")
        btn_reg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_reg.setStyleSheet(f"""
            QPushButton {{
                color: {COLOR_PRIMARY};
                font-weight: bold;
                font-size: 13px;
                background: transparent;
                border: none;
            }}
            QPushButton:hover {{
                color: #33EEFF;
                text-decoration: underline;
            }}
        """)
        btn_reg.clicked.connect(self.on_register_click)
        reg_layout.addWidget(btn_reg)
        
        card_layout.addLayout(reg_layout)
        
        content_layout.addWidget(self.card)
        self.main_layout.addWidget(content_area)

    def _create_input(self, label_text, placeholder, is_password=False):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 12px; font-weight: bold; background: transparent; border: none;")
        
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder)
        if is_password:
            entry.setEchoMode(QLineEdit.EchoMode.Password)
        entry.setFixedHeight(45)
        # Glassmorphic input field style
        entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 0 15px;
                color: {COLOR_TEXT_MAIN};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLOR_PRIMARY};
                background-color: rgba(0, 209, 255, 0.05);
            }}
        """)
        return lbl, entry

    def _handle_login(self):
        email = self.email_entry.text()
        password = self.pass_entry.text()
        if not email or not password:
            self.email_entry.setPlaceholderText("❌ Input Required")
            self.pass_entry.setPlaceholderText("❌ Input Required")
            return
            
        # Logic strictly separated: passes the intent out instead of processing it locally.
        if self.on_login: 
            self.on_login(email, password)
