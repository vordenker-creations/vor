from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont

class ModernTooltip(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent, Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        
        self.label = QLabel(text)
        self.label.setStyleSheet("color: white; font-size: 12px; font-weight: 500;")
        layout.addWidget(self.label)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 6px;
                border: 1px solid #334155;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.hide()

    def show_at(self, pos):
        self.move(pos)
        self.show()
        
    def hide_tooltip(self):
        self.hide()
