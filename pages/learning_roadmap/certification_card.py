from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QProgressBar, QGraphicsDropShadowEffect, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class CertificationCard(QFrame):
    clicked = pyqtSignal(dict)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedSize(280, 160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("CertificationCard")
        state = self.data.get("state", "locked")
        
        bg_color = "#FFFFFF"
        border_color = "#E2E8F0"
        if state == "completed":
            bg_color = "#F0FDF4"
            border_color = "#10B981"
        elif state == "in_progress":
            border_color = "#38BDF8"
        elif state == "expiring":
            border_color = "#F59E0B"
            
        self.setStyleSheet(f"""
            QFrame#CertificationCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 22px;
            }}
            QFrame#CertificationCard:hover {{
                border-color: #38BDF8;
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(15, 23, 42, 12))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Header: Logo + AI Tag
        head = QHBoxLayout()
        logo = QLabel(self.data.get("logo", "📜"))
        logo.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        head.addWidget(logo)
        
        head.addStretch()
        
        if self.data.get("is_ai_priority"):
            ai_tag = QLabel("✨ PRIORITY")
            ai_tag.setStyleSheet("color: #8B5CF6; font-weight: 800; font-size: 9px; border: none;")
            head.addWidget(ai_tag)
        layout.addLayout(head)

        # Title & Provider
        info = QVBoxLayout()
        info.setSpacing(2)
        title = QLabel(self.data.get("title", "Certification"))
        title.setWordWrap(True)
        title.setStyleSheet("font-weight: 700; font-size: 14px; color: #0F172A; border: none;")
        
        provider = QLabel(self.data.get("provider", "Organization"))
        provider.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 500; border: none;")
        
        info.addWidget(title)
        info.addWidget(provider)
        layout.addLayout(info)

        layout.addStretch()

        # Footer: Status / Date
        footer = QHBoxLayout()
        date_lbl = QLabel(self.data.get("date", "TBD"))
        date_lbl.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; border: none;")
        footer.addWidget(date_lbl)
        
        footer.addStretch()
        
        status_lbl = QLabel(state.replace("_", " ").upper())
        status_color = "#94A3B8"
        if state == "completed": status_color = "#10B981"
        elif state == "in_progress": status_color = "#38BDF8"
        status_lbl.setStyleSheet(f"font-size: 9px; font-weight: 800; color: {status_color}; letter-spacing: 0.5px; border: none;")
        footer.addWidget(status_lbl)
        
        layout.addLayout(footer)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)

class AchievementBadge(QFrame):
    def __init__(self, icon, title, rarity="Common", parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 100)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(6)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        circle = QFrame()
        circle.setFixedSize(60, 60)
        
        r_color = "#E2E8F0"
        if rarity == "Epic": r_color = "#8B5CF6"
        elif rarity == "Rare": r_color = "#38BDF8"
        elif rarity == "Legendary": r_color = "#F59E0B"
            
        circle.setStyleSheet(f"""
            background: white;
            border: 3px solid {r_color};
            border-radius: 30px;
        """)
        cl = QVBoxLayout(circle)
        ico = QLabel(icon)
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        cl.addWidget(ico)
        
        lbl = QLabel(title)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 10px; font-weight: 700; color: #1E293B; border: none;")
        
        l.addWidget(circle, alignment=Qt.AlignmentFlag.AlignCenter)
        l.addWidget(lbl)
