from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen, QLinearGradient

class SkillNode(QFrame):
    clicked = pyqtSignal(dict)
    
    # States
    LOCKED = "locked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    RECOMMENDED = "recommended"
    WEAK = "weak"
    AI_PRIORITY = "ai_priority"

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.state = data.get("state", self.LOCKED)
        self.mastery = data.get("mastery", 0) # 0-100
        
        self.setFixedSize(180, 100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        self.setObjectName("SkillNode")
        
        # Base Styling based on state
        border_color = "#E2E8F0"
        bg_color = "#FFFFFF"
        if self.state == self.IN_PROGRESS:
            border_color = "#38BDF8"
        elif self.state == self.COMPLETED:
            border_color = "#10B981"
            bg_color = "#F0FDF4"
        elif self.state == self.WEAK:
            border_color = "#EF4444"
        elif self.state == self.AI_PRIORITY:
            border_color = "#8B5CF6"
            
        self.setStyleSheet(f"""
            QFrame#SkillNode {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 20px;
            }}
        """)

        # Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(15, 23, 42, 15))
        self.setGraphicsEffect(self.shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        # Header: Icon + AI Tag
        head = QHBoxLayout()
        icon_lbl = QLabel(self.data.get("icon", "🔹"))
        icon_lbl.setStyleSheet("font-size: 16px; border: none; background: transparent;")
        head.addWidget(icon_lbl)
        
        if self.state == self.AI_PRIORITY:
            ai_tag = QLabel("✨ AI")
            ai_tag.setStyleSheet("color: #8B5CF6; font-weight: 800; font-size: 9px; border: none;")
            head.addWidget(ai_tag)
        head.addStretch()
        
        # Mastery Indicator (Dot)
        mastery_dot = QFrame()
        mastery_dot.setFixedSize(8, 8)
        dot_color = "#10B981" if self.mastery > 80 else "#38BDF8" if self.mastery > 30 else "#94A3B8"
        mastery_dot.setStyleSheet(f"background: {dot_color}; border-radius: 4px; border: none;")
        head.addWidget(mastery_dot)
        
        layout.addLayout(head)

        # Title
        title = QLabel(self.data.get("title", "Skill"))
        title.setWordWrap(True)
        title.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none; background: transparent;")
        layout.addWidget(title)

        # Progress / Meta
        meta = QHBoxLayout()
        prog_lbl = QLabel(f"{self.mastery}%")
        prog_lbl.setStyleSheet("font-size: 10px; font-weight: 600; color: #64748B; border: none; background: transparent;")
        meta.addWidget(prog_lbl)
        meta.addStretch()
        
        status_lbl = QLabel(self.state.replace("_", " ").title())
        status_lbl.setStyleSheet("font-size: 9px; font-weight: 800; color: #94A3B8; text-transform: uppercase; border: none; background: transparent;")
        meta.addWidget(status_lbl)
        
        layout.addLayout(meta)

    def setup_animations(self):
        self.lift_anim = QPropertyAnimation(self, b"pos")
        self.lift_anim.setDuration(200)
        self.lift_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor(56, 189, 248, 30))
        # Subtle lift effect
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(15, 23, 42, 15))
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)
