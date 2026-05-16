from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

from .productivity_metrics_cards import AnalyticsMetricCard, ProgressMetricCard
from .productivity_heatmap_widget import ProductivityHeatmapWidget

class LearningAnalyticsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(32, 32, 32, 40)
        cl.setSpacing(32)

        # 1. Metric Grid
        grid = QGridLayout()
        grid.setSpacing(24)
        
        grid.addWidget(AnalyticsMetricCard("Learning Velocity", "12.4", "+15%", "Skills per month", "#38BDF8"), 0, 0)
        grid.addWidget(AnalyticsMetricCard("Study Consistency", "92%", "+4%", "Daily streak goal", "#10B981"), 0, 1)
        grid.addWidget(AnalyticsMetricCard("Readiness Score", "78", "-2%", "Career alignment", "#F59E0B"), 0, 2)
        cl.addLayout(grid)

        # 2. Main Analytics Row
        row2 = QHBoxLayout()
        row2.setSpacing(24)
        
        # Heatmap
        row2.addWidget(ProductivityHeatmapWidget(), 2)
        
        # Side Metrics
        side_v = QVBoxLayout()
        side_v.setSpacing(20)
        side_v.addWidget(ProgressMetricCard("Roadmap Completion", 45, "#38BDF8"))
        side_v.addWidget(ProgressMetricCard("Skill Mastery", 62, "#10B981"))
        side_v.addWidget(ProgressMetricCard("Consistency Goal", 88, "#8B5CF6"))
        row2.addLayout(side_v, 1)
        
        cl.addLayout(row2)

        # 3. Insights Preview
        insight_sec = QFrame()
        insight_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        il = QVBoxLayout(insight_sec)
        il.setContentsMargins(24, 24, 24, 24)
        il.setSpacing(16)
        
        il.addWidget(QLabel("Deep Intelligence Preview", styleSheet="font-size: 15px; font-weight: 700; color: #0F172A; border: none;"))
        
        for text, impact in [
            ("Your retention is highest during morning sessions (8AM-10AM).", "High Impact"),
            ("Weak pattern detected in 'Algorithms' dependencies.", "Medium Risk"),
            ("You are 3 milestones away from 'Cloud Architect' readiness.", "Career Milestone")
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel("✨", styleSheet="font-size: 14px; border: none;"))
            row.addWidget(QLabel(text, styleSheet="font-size: 13px; color: #475569; border: none;"), 1)
            tag = QLabel(impact)
            tag.setStyleSheet("background: #F1F5F9; color: #64748B; font-size: 10px; font-weight: 700; padding: 4px 8px; border-radius: 6px; border: none;")
            row.addWidget(tag)
            il.addLayout(row)
            
        cl.addWidget(insight_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
