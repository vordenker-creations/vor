import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QPen, QBrush

class NeumorphicFrame(QFrame):
    """
    Highly optimized Neumorphism container.
    """
    def __init__(self, radius=25, offset=8, blur=20, bg_color="#F0F2F5", parent=None):
        super().__init__(parent)
        self.radius = radius
        self.offset = offset
        self.blur = blur
        self.bg_color_str = bg_color
        self.bg_color = QColor(bg_color)
        
        # Dark shadow effect
        self.dark_shadow = QGraphicsDropShadowEffect(self)
        self.dark_shadow.setBlurRadius(blur)
        self.dark_shadow.setColor(QColor(163, 177, 198, 150))
        self.dark_shadow.setOffset(offset, offset)
        self.setGraphicsEffect(self.dark_shadow)
        
        self.setStyleSheet(f"background-color: {bg_color}; border-radius: {radius}px;")
        
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Light shadow (top-left)
        # We draw a series of rectangles with decreasing opacity to simulate blur
        for i in range(self.offset):
            alpha = int(255 * (1 - i/self.offset) * 0.5)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(255, 255, 255, alpha))
            painter.drawRoundedRect(self.rect().adjusted(-i, -i, -self.offset, -self.offset), self.radius, self.radius)

        # Main background
        painter.setBrush(QBrush(self.bg_color))
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), self.radius, self.radius)
        
        super().paintEvent(event)

    def add_widget(self, widget, alignment=None):
        if alignment:
            self.content_layout.addWidget(widget, alignment=alignment)
        else:
            self.content_layout.addWidget(widget)
        
    def add_layout(self, l):
        self.content_layout.addLayout(l)


class NeumorphicInput(QLineEdit):
    """
    Modern Neumorphic Input.
    """
    def __init__(self, placeholder, icon_text="", is_password=False, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        if is_password:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            
        self.setFixedHeight(50)
        self.radius = 25
        self.icon_text = icon_text
        
        padding_left = 45 if icon_text else 20
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: #F0F2F5;
                border-radius: {self.radius}px;
                padding-left: {padding_left}px;
                padding-right: 20px;
                color: #334155;
                font-size: 14px;
                font-weight: 500;
                border: none;
            }}
        """)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw Inset Shadow simulation
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        
        # Top-Left Dark
        painter.setPen(QPen(QColor(163, 177, 198, 80), 2))
        painter.drawRoundedRect(rect, self.radius, self.radius)
        
        # Bottom-Right Light
        painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
        painter.drawRoundedRect(rect.adjusted(1, 1, 0, 0), self.radius, self.radius)

        if self.icon_text:
            painter.setPen(QColor("#1E5F74"))
            font = painter.font()
            font.setBold(True)
            font.setPointSize(12)
            painter.setFont(font)
            painter.drawText(self.rect().adjusted(18, 0, 0, 0), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.icon_text)


class NeumorphicButton(QPushButton):
    """
    Neumorphic button with press effect.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.radius = 25
        self.is_pressed = False
        
        self.dark_shadow = QGraphicsDropShadowEffect(self)
        self.dark_shadow.setBlurRadius(15)
        self.dark_shadow.setColor(QColor(163, 177, 198, 180))
        self.dark_shadow.setOffset(4, 4)
        self.setGraphicsEffect(self.dark_shadow)
        
        self.update_style()

    def update_style(self):
        if self.is_pressed:
            self.setGraphicsEffect(None)
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #F0F2F5;
                    border-radius: {self.radius}px;
                    color: #1E5F74;
                    font-weight: bold;
                    border-top: 2px solid #d1d5db;
                    border-left: 2px solid #d1d5db;
                    border-bottom: 2px solid #ffffff;
                    border-right: 2px solid #ffffff;
                }}
            """)
        else:
            self.setGraphicsEffect(self.dark_shadow)
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #F0F2F5;
                    border-radius: {self.radius}px;
                    color: #334155;
                    font-weight: bold;
                    border: none;
                }}
                QPushButton:hover {{ color: #1E5F74; }}
            """)

    def mousePressEvent(self, event):
        self.is_pressed = True
        self.update_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_pressed = False
        self.update_style()
        super().mouseReleaseEvent(event)


class GlowingButton(QPushButton):
    def __init__(self, text, width=None, height=50, parent=None):
        super().__init__(text, parent)
        if width: self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(30, 95, 116, 120))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E5F74, stop:1 #123b49);
                color: white;
                border-radius: {height//2}px;
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 1px;
                border: none;
            }}
            QPushButton:hover {{ background: #25758f; }}
            QPushButton:pressed {{ background: #0c2730; }}
        """)
