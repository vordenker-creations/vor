from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout
from PyQt6.QtGui import QColor
from config import COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY

class SaaSCard(QFrame):
    """
    Hardware-accelerated Glassmorphism Card.
    Replaces the old Tkinter GlassCard perfectly.
    """
    def __init__(self, parent=None, border_color=COLOR_BORDER):
        super().__init__(parent)
        
        # Apply CSS for rounded corners and background
        self.setStyleSheet(f"""
            SaaSCard {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {border_color};
                border-radius: 16px;
            }}
        """)
        
        # Hardware-accelerated Drop Shadow (Replacing the fake Tkinter glow)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80)) # Subtle black shadow for depth
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)
    def enterEvent(self, event):
        """Hover effect - change border color smoothly."""
        self.setStyleSheet(f"""
            SaaSCard {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_PRIMARY};
                border-radius: 16px;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"""
            SaaSCard {{
                background-color: {COLOR_BG_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: 16px;
            }}
        """)
        super().leaveEvent(event)
