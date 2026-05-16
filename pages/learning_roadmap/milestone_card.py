from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QProgressBar, QGraphicsDropShadowEffect, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class MilestoneCard(QFrame):
    clicked = pyqtSignal(dict)
    
    # States
    LOCKED = "locked"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    AI_PRIORITY = "ai_priority"
    HIGH_RISK = "high_risk"

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.state = data.get("state", self.PLANNED)
        self.progress = data.get("progress", 0)
        
        self.setFixedSize(240, 140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("MilestoneCard")
        
        # State-based styling
        border_color = "#E2E8F0"
        status_color = "#94A3B8"
        bg_color = "#FFFFFF"
        
        if self.state == self.IN_PROGRESS:
            border_color = "#38BDF8"
            status_color = "#38BDF8"
        elif self.state == self.COMPLETED:
            border_color = "#10B981"
            status_color = "#10B981"
            bg_color = "#F0FDF4"
        elif self.state == self.DELAYED:
            border_color = "#F59E0B"
            status_color = "#F59E0B"
        elif self.state == self.HIGH_RISK:
            border_color = "#EF4444"
            status_color = "#EF4444"
        elif self.state == self.AI_PRIORITY:
            border_color = "#8B5CF6"
            status_color = "#8B5CF6"

        self.setStyleSheet(f"""
            QFrame#MilestoneCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 20px;
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(15, 23, 42, 12))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Header
        head = QHBoxLayout()
        icon_lbl = QLabel(self.data.get("icon", "🏁"))
        icon_lbl.setStyleSheet("font-size: 16px; border: none; background: transparent;")
        head.addWidget(icon_lbl)
        
        if self.state == self.AI_PRIORITY:
            badge = QLabel("✨ AI")
            badge.setStyleSheet("color: #8B5CF6; font-weight: 800; font-size: 9px; border: none;")
            head.addWidget(badge)
        head.addStretch()
        
        date_lbl = QLabel(self.data.get("due_date", "TBD"))
        date_lbl.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; border: none;")
        head.addWidget(date_lbl)
        layout.addLayout(head)

        # Title
        title = QLabel(self.data.get("title", "Milestone"))
        title.setWordWrap(True)
        title.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none; background: transparent;")
        layout.addWidget(title)

        layout.addStretch()

        # Progress
        prog_v = QVBoxLayout()
        prog_v.setSpacing(4)
        
        meta = QHBoxLayout()
        pct = QLabel(f"{self.progress}%")
        pct.setStyleSheet(f"font-size: 10px; font-weight: 800; color: {status_color}; border: none;")
        meta.addWidget(pct)
        meta.addStretch()
        
        status = QLabel(self.state.replace("_", " ").upper())
        status.setStyleSheet(f"font-size: 8px; font-weight: 900; color: {status_color}; letter-spacing: 0.5px; border: none;")
        meta.addWidget(status)
        prog_v.addLayout(meta)
        
        pb = QProgressBar()
        pb.setFixedHeight(4)
        pb.setValue(self.progress)
        pb.setTextVisible(False)
        pb.setStyleSheet(f"""
            QProgressBar {{ background-color: #F1F5F9; border-radius: 2px; border: none; }}
            QProgressBar::chunk {{ background-color: {status_color}; border-radius: 2px; }}
        """)
        prog_v.addWidget(pb)
        layout.addLayout(prog_v)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)
