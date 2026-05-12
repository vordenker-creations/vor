import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextBrowser, QLineEdit, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QFont
from config import *
from components import SaaSCard

class AIMentorPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("AIMentorPage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(35, 35, 35, 35)
        
        # Header
        header = QWidget()
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(0, 0, 0, 20)
        lbl_title = QLabel("AI Mentor Chat")
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold;")
        h_layout.addWidget(lbl_title)
        lbl_status = QLabel("🟢 Online")
        lbl_status.setStyleSheet(f"color: {COLOR_SUCCESS}; font-size: 12px; font-weight: bold; margin-left: 15px;")
        h_layout.addWidget(lbl_status)
        h_layout.addStretch()
        self.main_layout.addWidget(header)
        
        # Chat Area
        self.chat_card = SaaSCard()
        card_layout = self.chat_card.internal_layout
        
        self.chat_box = QTextBrowser()
        self.chat_box.setStyleSheet(f"background: transparent; border: none; color: {COLOR_TEXT_MAIN}; font-size: 14px;")
        self.chat_box.setOpenExternalLinks(True)
        card_layout.addWidget(self.chat_box)
        
        # Chips
        self.chips_frame = QWidget()
        chips_layout = QHBoxLayout(self.chips_frame)
        chips_layout.setContentsMargins(0, 10, 0, 10)
        chips_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        chips = ["Phân tích CV", "Gợi ý Roadmap", "Luyện Phỏng vấn", "Giải thích Code"]
        for chip in chips:
            btn = QPushButton(chip)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setFixedHeight(32)
            btn.setStyleSheet(f"QPushButton {{ background: {COLOR_BG_APP}; color: {COLOR_PRIMARY}; border: 1px solid {COLOR_BORDER}; border-radius: 16px; padding: 0 15px; font-weight: bold; font-size: 12px; }} QPushButton:hover {{ background: {COLOR_PRIMARY_LIGHT}; }}")
            btn.clicked.connect(lambda ch, c=chip: self.send_message(c))
            chips_layout.addWidget(btn)
        card_layout.addWidget(self.chips_frame)
        
        self.main_layout.addWidget(self.chat_card)
        
        # Input Area
        input_frame = QWidget()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 10, 0, 0)
        
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Hỏi AI Mentor bất cứ điều gì...")
        self.entry.setFixedHeight(45)
        self.entry.setStyleSheet(f"QLineEdit {{ background: {COLOR_BG_CARD}; border: 1px solid {COLOR_BORDER}; border-radius: 8px; padding: 0 15px; color: {COLOR_TEXT_MAIN}; font-size: 14px; }} QLineEdit:focus {{ border: 1px solid {COLOR_PRIMARY}; }}")
        self.entry.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.entry)
        
        btn_send = QPushButton("Gửi ➔")
        btn_send.setFixedSize(100, 45)
        btn_send.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_send.setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY}; color: white; font-weight: bold; font-size: 14px; border-radius: 8px; }} QPushButton:hover {{ background: #00B4D8; }}")
        btn_send.clicked.connect(self.send_message)
        input_layout.addWidget(btn_send)
        
        self.main_layout.addWidget(input_frame)
        
        # Initial Greeting
        self.append_message("AI Mentor", "Chào bạn, tôi là AI Mentor. Hãy chọn một tùy chọn bên dưới hoặc đặt câu hỏi để tôi hỗ trợ bạn nhé!<br><br>Tôi có thể giúp bạn:<br>- <b>Phân tích CV</b> và gợi ý cải thiện<br>- Xây dựng <b>Roadmap</b> học tập cá nhân hóa<br>- Giải thích các đoạn <code>code</code> phức tạp")

    def append_message(self, sender, text):
        color = COLOR_PRIMARY if sender == "AI Mentor" else "#FFFFFF"
        html = f"<div style='margin-bottom: 15px;'><b style='color: {color};'>{sender}:</b><br>{text}</div>"
        # Simple markdown to HTML conversion for bold and code
        html = html.replace("**", "<b>").replace("`", "<code>") # This is very crude but works for the mock
        self.chat_box.append(html)
        self.chat_box.verticalScrollBar().setValue(self.chat_box.verticalScrollBar().maximum())

    def send_message(self, text=None):
        msg = text if isinstance(text, str) else self.entry.text()
        if not msg.strip(): return
        
        if not isinstance(text, str):
            self.entry.clear()
            
        self.append_message("Bạn", msg)
        
        # Mock AI Response
        QTimer.singleShot(500, lambda: self.append_message("AI Mentor", f"Tôi đang xử lý yêu cầu: <b>{msg}</b>. Bạn đợi một lát nhé. Dưới đây là ví dụ <code>print('Hello World')</code>."))
