import sys
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QApplication)
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from PyQt6.QtGui import QPainter, QColor, QFont, QCursor

from config import *
from components import SaaSCard, AnimationEngine

class LoginPage(QWidget):
    def __init__(self, parent=None, on_login=None, on_register_click=None):
        super().__init__(parent)
        self.on_login = on_login
        self.on_register_click = on_register_click
        self.setObjectName("LoginPage")
        self.setStyleSheet(f"background-color: {COLOR_BG_APP};")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self._setup_sidebar()
        self._setup_content()
        self.circles = []
        self._generate_circles()

    def _generate_circles(self):
        colors = [QColor("#00D1FF"), QColor("#10B981"), QColor("#6366F1")]
        for _ in range(15):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            r = random.randint(20, 80)
            color = random.choice(colors)
            self.circles.append((x, y, r, color))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for x, y, r, color in self.circles:
            for i in range(5):
                alpha_r = r + (i * 10)
                painter.setPen(QColor(color.red(), color.green(), color.blue(), 30))
                painter.drawEllipse(QPoint(x, y), alpha_r, alpha_r)

    def _setup_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(400)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(60, 100, 40, 60)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        lbl_insight = QLabel("AI INSIGHT")
        lbl_insight.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 34px; font-weight: bold;")
        sidebar_layout.addWidget(lbl_insight)
        lbl_desc = QLabel("Elevate your career with AI-driven analytics and personal roadmaps.")
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 14px; margin-top: 10px;")
        sidebar_layout.addWidget(lbl_desc)
        sidebar_layout.addSpacing(40)
        tags = ["Python", "Neural Networks", "NLP", "Computer Vision", "Data Science", "Cloud AI"]
        for tag in tags:
            btn = QPushButton(f"• {tag}")
            btn.setFixedSize(150, 32)
            btn.setStyleSheet(f"QPushButton {{ background-color: {COLOR_BG_CARD}; color: {COLOR_TEXT_MAIN}; border: 1px solid {COLOR_BORDER}; border-radius: 16px; font-size: 11px; text-align: left; padding-left: 15px; }}")
            sidebar_layout.addWidget(btn)
            sidebar_layout.addSpacing(5)
        self.main_layout.addWidget(sidebar)

    def _setup_content(self):
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card = SaaSCard()
        self.card.setFixedSize(500, 600)
        card_layout = self.card.internal_layout
        card_layout.setContentsMargins(60, 50, 60, 50)
        lbl_login = QLabel("LOGIN")
        lbl_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_login.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 28px; font-weight: bold;")
        card_layout.addWidget(lbl_login)
        lbl_sub = QLabel("Access your professional bridge.")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_sub.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 14px;")
        card_layout.addWidget(lbl_sub)
        card_layout.addSpacing(40)
        self.email_lbl, self.email_entry = self._create_input("Email Address", "👤 email@vku.udn.vn")
        card_layout.addWidget(self.email_lbl)
        card_layout.addWidget(self.email_entry)
        card_layout.addSpacing(15)
        self.pass_lbl, self.pass_entry = self._create_input("Password", "🔒 ••••••••", is_password=True)
        card_layout.addWidget(self.pass_lbl)
        card_layout.addWidget(self.pass_entry)
        card_layout.addSpacing(40)
        btn_login = QPushButton("LOGIN")
        btn_login.setFixedHeight(45)
        btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_login.setStyleSheet(f"QPushButton {{ background-color: {COLOR_PRIMARY}; color: white; font-weight: bold; font-size: 14px; border-radius: 10px; }} QPushButton:hover {{ background-color: #00B4D8; }}")
        btn_login.clicked.connect(self._handle_login)
        card_layout.addWidget(btn_login)
        card_layout.addSpacing(15)
        reg_layout = QHBoxLayout()
        reg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_new = QLabel("New here?")
        lbl_new.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
        reg_layout.addWidget(lbl_new)
        btn_reg = QPushButton("Create Account")
        btn_reg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_reg.setStyleSheet(f"color: {COLOR_PRIMARY}; font-weight: bold; font-size: 12px; background: transparent; border: none;")
        btn_reg.clicked.connect(self.on_register_click)
        reg_layout.addWidget(btn_reg)
        card_layout.addLayout(reg_layout)
        content_layout.addWidget(self.card)
        self.main_layout.addWidget(content_area)

    def _create_input(self, label_text, placeholder, is_password=False):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 11px; font-weight: bold;")
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder)
        if is_password: entry.setEchoMode(QLineEdit.EchoMode.Password)
        entry.setFixedHeight(40)
        entry.setStyleSheet(f"QLineEdit {{ background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 10px; padding: 0 12px; color: {COLOR_TEXT_MAIN}; }} QLineEdit:focus {{ border: 2px solid {COLOR_PRIMARY}; }}")
        return lbl, entry

    def _handle_login(self):
        email = self.email_entry.text()
        password = self.pass_entry.text()
        if not email or not password:
            self.email_entry.setPlaceholderText("❌ Vui lòng nhập email")
            self.pass_entry.setPlaceholderText("❌ Vui lòng nhập mật khẩu")
            return
        if self.on_login: self.on_login(email, password)
