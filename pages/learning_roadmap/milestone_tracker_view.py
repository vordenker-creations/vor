from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .milestone_card import MilestoneCard

class MilestoneTrackerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Timeline Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.timeline_layout = QVBoxLayout(self.content_widget)
        self.timeline_layout.setContentsMargins(40, 32, 40, 40)
        self.timeline_layout.setSpacing(32)

        self._setup_mock_timeline()
        
        self.scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll)

    def _setup_mock_timeline(self):
        phases = [
            ("Phase 1: Foundation", "completed", [
                {"title": "Python Core Mastery", "progress": 100, "due_date": "Oct 12", "state": "completed", "icon": "🐍"},
                {"title": "Algorithms & Logic", "progress": 100, "due_date": "Oct 20", "state": "completed", "icon": "🔢"}
            ]),
            ("Phase 2: Deep Learning", "in_progress", [
                {"title": "PyTorch Fundamentals", "progress": 45, "due_date": "Nov 05", "state": "in_progress", "icon": "🔥", "is_ai_priority": True},
                {"title": "Neural Network Arch", "progress": 10, "due_date": "Nov 15", "state": "planned", "icon": "🧠"}
            ]),
            ("Phase 3: Advanced AI", "locked", [
                {"title": "Transformers & LLMs", "progress": 0, "due_date": "Dec 01", "state": "locked", "icon": "💬"},
                {"title": "Deployment Scalability", "progress": 0, "due_date": "Dec 15", "state": "locked", "icon": "☁️"}
            ])
        ]

        for phase_title, status, milestones in phases:
            phase_v = QVBoxLayout()
            phase_v.setSpacing(16)
            
            # Phase Header
            head = QHBoxLayout()
            lbl = QLabel(phase_title)
            lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
            head.addWidget(lbl)
            head.addStretch()
            phase_v.addLayout(head)
            
            # Milestone Grid for the phase
            grid = QGridLayout()
            grid.setSpacing(20)
            for i, m in enumerate(milestones):
                card = MilestoneCard(m)
                grid.addWidget(card, 0, i)
            grid.setColumnStretch(len(milestones), 1)
            
            phase_v.addLayout(grid)
            
            line = QFrame()
            line.setFixedHeight(1)
            line.setStyleSheet("background: #E2E8F0; margin: 10px 0;")
            phase_v.addWidget(line)
            
            self.timeline_layout.addLayout(phase_v)
            
        self.timeline_layout.addStretch()
