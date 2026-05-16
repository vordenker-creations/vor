from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QLineEdit, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class SessionItem(QFrame):
    clicked = pyqtSignal(str)
    
    def __init__(self, title, type_str, score, parent=None):
        super().__init__(parent)
        self.setFixedHeight(72)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.title = title
        
        self.setStyleSheet("""
            SessionItem {
                background-color: transparent;
                border-radius: 12px;
                border: none;
            }
            SessionItem:hover {
                background-color: #F1F5F9;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        t_row = QHBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #1E293B; border: none; background: transparent;")
        t_row.addWidget(title_lbl)
        t_row.addStretch()
        
        score_lbl = QLabel(f"{score}%")
        score_lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #10B981; border: none; background: transparent;")
        t_row.addWidget(score_lbl)
        layout.addLayout(t_row)
        
        type_lbl = QLabel(type_str)
        type_lbl.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        layout.addWidget(type_lbl)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title)
        super().mousePressEvent(event)

class InterviewSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("Interview Simulator")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        layout.addWidget(title)
        
        btn_start = QPushButton("+ Start Interview")
        btn_start.setFixedHeight(44)
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 12px;
                font-size: 14px; font-weight: 700; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        layout.addWidget(btn_start)
        
        # Category Selector
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["HR Behavioral", "Technical Python", "System Design", "Product Management"])
        self.cat_combo.setStyleSheet("""
            QComboBox {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                padding: 6px 10px; font-size: 12px; color: #475569;
            }
        """)
        layout.addWidget(self.cat_combo)
        
        # Search
        search = QLineEdit()
        search.setPlaceholderText("Search sessions...")
        search.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
                padding: 10px 14px; font-size: 13px;
            }
        """)
        layout.addWidget(search)
        
        # Session History
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(4)
        
        sessions = [
            ("Frontend Dev Mock", "Technical • 15m", 88),
            ("HR Behavioral Round", "HR • 20m", 92),
            ("Python Basics Prep", "Technical • 10m", 76),
            ("Leadership Screen", "Executive • 25m", 84)
        ]
        
        for t, d, s in sessions:
            cl.addWidget(SessionItem(t, d, s))
            
        cl.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Bottom Profile Stats
        bottom = QFrame()
        bottom.setStyleSheet("border-top: 1px solid #E2E8F0; padding-top: 16px;")
        bl = QVBoxLayout(bottom)
        bl.setContentsMargins(0, 16, 0, 0)
        bl.setSpacing(12)
        
        stats = QLabel("Total Sessions: 12")
        stats.setStyleSheet("font-size: 12px; font-weight: 600; color: #64748B;")
        bl.addWidget(stats)
        
        layout.addWidget(bottom)
