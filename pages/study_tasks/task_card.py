from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QProgressBar, QGraphicsDropShadowEffect, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class StudyTaskCard(QFrame):
    clicked = pyqtSignal(dict)
    
    # Priority Levels
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    AI_SUGGESTED = "AI Recommended"

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.priority = data.get("priority", self.MEDIUM)
        self.progress = data.get("progress", 0)
        
        self.setFixedWidth(260)
        self.setMinimumHeight(150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("StudyTaskCard")
        
        p_colors = {
            self.CRITICAL: "#EF4444",
            self.HIGH: "#F59E0B",
            self.MEDIUM: "#3B82F6",
            self.LOW: "#10B981",
            self.AI_SUGGESTED: "#8B5CF6"
        }
        color = p_colors.get(self.priority, "#64748B")
        
        self.setStyleSheet(f"""
            QFrame#StudyTaskCard {{
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 18px;
            }}
            QFrame#StudyTaskCard:hover {{
                border-color: {color};
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(15, 23, 42, 10))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # 1. Header: Category & Priority
        head = QHBoxLayout()
        cat_lbl = QLabel(self.data.get("category", "General"))
        cat_lbl.setStyleSheet("""
            background: #F1F5F9; color: #475569; 
            padding: 2px 8px; border-radius: 6px; 
            font-size: 10px; font-weight: 700; border: none;
        """)
        head.addWidget(cat_lbl)
        head.addStretch()
        
        p_lbl = QLabel(self.priority)
        p_lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: 800; border: none;")
        head.addWidget(p_lbl)
        layout.addLayout(head)

        # 2. Title
        self.title_lbl = QLabel(self.data.get("title", "Task Title"))
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setStyleSheet("font-weight: 700; font-size: 14px; color: #0F172A; border: none;")
        layout.addWidget(self.title_lbl)

        # 3. Meta: Due Date & Focus Time
        meta = QHBoxLayout()
        date_lbl = QLabel(f"📅 {self.data.get('due_date', 'Today')}")
        date_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500; border: none;")
        
        time_lbl = QLabel(f"⏱ {self.data.get('focus_time', '45m')}")
        time_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500; border: none;")
        
        meta.addWidget(date_lbl)
        meta.addStretch()
        meta.addWidget(time_lbl)
        layout.addLayout(meta)

        layout.addStretch()

        # 4. Progress
        if self.progress > 0:
            prog_v = QVBoxLayout()
            prog_v.setSpacing(4)
            pb = QProgressBar()
            pb.setFixedHeight(4)
            pb.setValue(self.progress)
            pb.setTextVisible(False)
            pb.setStyleSheet(f"""
                QProgressBar {{ background-color: #F1F5F9; border: none; border-radius: 2px; }}
                QProgressBar::chunk {{ background-color: {color}; border-radius: 2px; }}
            """)
            prog_v.addWidget(pb)
            layout.addLayout(prog_v)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)
