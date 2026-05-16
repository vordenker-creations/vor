from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                             QLineEdit, QFrame, QLabel, QGraphicsDropShadowEffect, QSizePolicy, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize, QRect
from PyQt6.QtGui import QColor, QFont, QCursor

class FloatingActionButton(QPushButton):
    def __init__(self, icon_text, is_primary=False, parent=None):
        super().__init__(icon_text, parent)
        self.is_primary = is_primary
        self.setFixedSize(42, 42)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_style()
        
        # Scale animation
        self._anim = QPropertyAnimation(self, b"size")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def _setup_style(self):
        if self.is_primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0F172A;
                    color: #FFFFFF;
                    border-radius: 21px;
                    font-size: 18px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1E293B;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #334155;
                    border-radius: 21px;
                    font-size: 20px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(15, 23, 42, 0.08);
                }
                QPushButton:pressed {
                    background-color: rgba(15, 23, 42, 0.14);
                }
            """)

    def enterEvent(self, event):
        self._anim.setStartValue(QSize(42, 42))
        self._anim.setEndValue(QSize(44, 44))
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.setStartValue(self.size())
        self._anim.setEndValue(QSize(42, 42))
        self._anim.start()
        super().leaveEvent(event)

class VoiceInteractionButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("🎙️", parent)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_recording = False
        self._setup_style()
        self.clicked.connect(self.toggle_recording)

    def _setup_style(self):
        color = "#38BDF8" if self.is_recording else "#334155"
        bg = "rgba(56, 189, 248, 0.15)" if self.is_recording else "transparent"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border-radius: 20px;
                font-size: 18px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba(56, 189, 248, 0.12);
                color: #38BDF8;
            }}
        """)

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        self._setup_style()
        if self.is_recording:
            self.setText("🛑")
        else:
            self.setText("🎙️")

class ChatInputWidget(QFrame):
    send_requested = pyqtSignal(str)
    attachment_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setObjectName("ChatInputContainer")
        self.setMinimumWidth(400)
        
        self.setStyleSheet("""
            QFrame#ChatInputContainer {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 24px;
            }
        """)
        
        # Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(10)
        self.shadow.setColor(QColor(15, 23, 42, 15))
        self.setGraphicsEffect(self.shadow)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        
        # 1. Plus Button (Left)
        self.btn_attach = FloatingActionButton("+", is_primary=False)
        self.btn_attach.clicked.connect(self._handle_attachment)
        layout.addWidget(self.btn_attach)
        
        # 2. Input Field (Center)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask your AI career mentor...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #0F172A;
                font-size: 14px;
                font-weight: 500;
                padding: 10px 4px;
            }
        """)
        self.input_field.returnPressed.connect(self._on_send)
        layout.addWidget(self.input_field, 1)
        
        # 3. Voice Button (Right)
        self.btn_voice = VoiceInteractionButton()
        layout.addWidget(self.btn_voice)
        
        # 4. Send Button (Right)
        self.btn_send = FloatingActionButton("➤", is_primary=True)
        self.btn_send.clicked.connect(self._on_send)
        layout.addWidget(self.btn_send)

    def _on_send(self):
        text = self.input_field.text().strip()
        if text:
            self.send_requested.emit(text)
            self.input_field.clear()

    def _handle_attachment(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Career Documents", "", "All Files (*);;PDF Files (*.pdf);;Images (*.png *.jpg)")
        if file_path:
            self.attachment_requested.emit()

    def focusInEvent(self, event):
        self.setStyleSheet("""
            QFrame#ChatInputContainer {
                background-color: #FFFFFF;
                border: 1px solid #38BDF8;
                border-radius: 24px;
            }
        """)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet("""
            QFrame#ChatInputContainer {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 24px;
            }
        """)
        super().focusOutEvent(event)
