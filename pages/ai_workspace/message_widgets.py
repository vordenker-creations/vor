from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QPushButton, QTextBrowser, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

def apply_subtle_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(15, 23, 42, 20))
    widget.setGraphicsEffect(shadow)

class CodeBlockWidget(QFrame):
    def __init__(self, code, language="python", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            CodeBlockWidget {
                background-color: #1E293B;
                border-radius: 12px;
                border: 1px solid #334155;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(36)
        header.setStyleSheet("background-color: #0F172A; border-top-left-radius: 12px; border-top-right-radius: 12px;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 0, 16, 0)
        
        lang_lbl = QLabel(language.upper())
        lang_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 700; border: none;")
        h_layout.addWidget(lang_lbl)
        
        h_layout.addStretch()
        
        copy_btn = QPushButton("Copy")
        copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                color: #94A3B8; background: transparent; border: none; font-size: 11px; font-weight: 600;
            }
            QPushButton:hover { color: #FFFFFF; }
        """)
        h_layout.addWidget(copy_btn)
        
        layout.addWidget(header)
        
        # Code Area
        code_area = QTextBrowser()
        code_area.setPlainText(code)
        code_area.setStyleSheet("""
            QTextBrowser {
                background-color: transparent; border: none; color: #E2E8F0;
                font-family: 'Consolas', 'Monaco', monospace; font-size: 13px;
                padding: 16px;
            }
        """)
        # For simplicity, we won't implement full syntax highlighting here, 
        # but the dark theme makes it look like a modern editor.
        layout.addWidget(code_area)

class UserMessageWidget(QWidget):
    def __init__(self, text, time_str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(12)
        layout.addStretch()
        
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #38BDF8;
                color: white;
                border-radius: 20px;
                border-bottom-right-radius: 4px;
                padding: 12px 18px;
            }
        """)
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(4)
        
        msg_lbl = QLabel(text)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("color: white; font-size: 14px; line-height: 1.5; border: none; background: transparent;")
        c_layout.addWidget(msg_lbl)
        
        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 10px; border: none; background: transparent;")
        time_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        c_layout.addWidget(time_lbl)
        
        layout.addWidget(container)

class AIMessageWidget(QWidget):
    def __init__(self, text, time_str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(12)
        
        avatar = QLabel("✦")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #0F172A;
            color: #38BDF8;
            border-radius: 18px;
            font-size: 18px;
            font-weight: bold;
        """)
        layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)
        
        content_container = QWidget()
        self.content_layout = QVBoxLayout(content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(12)
        
        bubble = QFrame()
        bubble.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
                border-top-left-radius: 4px;
            }
        """)
        apply_subtle_shadow(bubble)
        
        b_layout = QVBoxLayout(bubble)
        b_layout.setContentsMargins(18, 16, 18, 16)
        b_layout.setSpacing(8)
        
        self.text_lbl = QLabel(text)
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setStyleSheet("color: #1E293B; font-size: 14px; line-height: 1.6; border: none; background: transparent;")
        b_layout.addWidget(self.text_lbl)
        
        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet("color: #94A3B8; font-size: 10px; border: none; background: transparent;")
        b_layout.addWidget(time_lbl)
        
        self.content_layout.addWidget(bubble)
        layout.addWidget(content_container)
        layout.addStretch()

    def add_code_block(self, code, language="python"):
        block = CodeBlockWidget(code, language)
        self.content_layout.addWidget(block)
        
    def add_suggestion_chips(self, chips):
        chip_layout = QHBoxLayout()
        chip_layout.setSpacing(8)
        for chip_text in chips:
            btn = QPushButton(chip_text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #F1F5F9; color: #475569; border: 1px solid #E2E8F0;
                    border-radius: 14px; padding: 6px 14px; font-size: 12px; font-weight: 600;
                }
                QPushButton:hover { background-color: #E0F2FE; color: #0284C7; border-color: #38BDF8; }
            """)
            chip_layout.addWidget(btn)
        chip_layout.addStretch()
        self.content_layout.addLayout(chip_layout)
