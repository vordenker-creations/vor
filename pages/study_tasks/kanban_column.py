from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from .task_card import StudyTaskCard

class KanbanColumn(QWidget):
    task_clicked = pyqtSignal(dict)
    
    def __init__(self, title, count=0, color="#64748B", parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # 1. Column Header
        header = QHBoxLayout()
        header.setContentsMargins(4, 0, 4, 0)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: #0F172A; font-weight: 800; font-size: 15px;")
        
        count_lbl = QLabel(str(count))
        count_lbl.setStyleSheet(f"background: #E2E8F0; color: #64748B; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 800;")
        
        header.addWidget(title_lbl)
        header.addWidget(count_lbl)
        header.addStretch()
        
        add_btn = QPushButton("+")
        add_btn.setFixedSize(24, 24)
        add_btn.setStyleSheet("background: transparent; color: #94A3B8; font-size: 18px; border: none;")
        header.addWidget(add_btn)
        layout.addLayout(header)
        
        # 2. Scroll Area for Tasks
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.column_layout = QVBoxLayout(self.content_widget)
        self.column_layout.setContentsMargins(2, 2, 2, 32)
        self.column_layout.setSpacing(12)
        self.column_layout.addStretch()
        
        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll)

    def add_task(self, data):
        card = StudyTaskCard(data)
        card.clicked.connect(self.task_clicked.emit)
        # Insert before the stretch
        self.column_layout.insertWidget(self.column_layout.count() - 1, card)
