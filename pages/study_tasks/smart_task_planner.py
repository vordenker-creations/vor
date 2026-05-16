from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .kanban_column import KanbanColumn
from .ai_productivity_sidebar import AIProductivitySidebar
from components import CollapsiblePanel

class PlannerToolbar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(74)
        self.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(24)

        # 1. Title & Status
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        info_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title_h = QHBoxLayout()
        title_h.setSpacing(12)
        title = QLabel("Smart Task Planner")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        badge = QLabel("Productivity active")
        badge.setStyleSheet("font-size: 10px; font-weight: 800; color: #10B981; background: #F0FDF4; padding: 2px 8px; border-radius: 6px; border: 1px solid #BBF7D0;")
        
        title_h.addWidget(title); title_h.addWidget(badge); title_h.addStretch()
        
        summary = QLabel("Realtime AI-powered learning operations center")
        summary.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600; border: none;")
        
        info_v.addLayout(title_h); info_v.addWidget(summary)
        layout.addLayout(info_v)

        layout.addStretch()

        # 2. Controls
        self.cat_sel = QComboBox()
        self.cat_sel.addItems(["All Categories", "Development", "Design", "AI/ML", "Mathematics"])
        self.cat_sel.setFixedWidth(160); self.cat_sel.setFixedHeight(36)
        self.cat_sel.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding-left: 8px;")
        layout.addWidget(self.cat_sel)

        btn_ai = QPushButton("✨ AI Plan Tasks")
        btn_ai.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 10px; 
                font-weight: 700; font-size: 12px; height: 36px; padding: 0 16px;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        layout.addWidget(btn_ai)

        btn_create = QPushButton("+ Create Task")
        btn_create.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: white; border-radius: 10px; 
                font-weight: 700; font-size: 12px; height: 36px; padding: 0 16px; border: none;
            }
            QPushButton:hover { background: #0EA5E9; }
        """)
        layout.addWidget(btn_create)

class SmartTaskPlanner(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("SmartTaskPlanner")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Central Workspace
        self.center_workspace = QWidget()
        self.center_layout = QVBoxLayout(self.center_workspace)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)

        self.toolbar = PlannerToolbar()
        self.center_layout.addWidget(self.toolbar)

        # Hero Stats
        self._setup_hero_stats()

        # Kanban Board
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.board_container = QWidget()
        self.board_layout = QHBoxLayout(self.board_container)
        self.board_layout.setContentsMargins(32, 24, 32, 32)
        self.board_layout.setSpacing(24)
        self.board_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._setup_columns()
        
        self.scroll.setWidget(self.board_container)
        self.center_layout.addWidget(self.scroll, 1)

        self.main_layout.addWidget(self.center_workspace, 1)

        # 2. Right Insights Sidebar
        self.insights_content = AIProductivitySidebar()
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        self.main_layout.addWidget(self.right_panel)

    def _setup_hero_stats(self):
        hero = QFrame()
        hero.setFixedHeight(120)
        hero.setStyleSheet("background: transparent; border: none;")
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(32, 24, 32, 0)
        hl.setSpacing(24)
        
        from ..dashboard_analytics.productivity_analytics_panel import AnalyticsMetricCard
        hl.addWidget(AnalyticsMetricCard("Active Tasks", "14", "Tasks", "4 high priority", "#38BDF8"))
        hl.addWidget(AnalyticsMetricCard("Efficiency", "92%", "+8%", "Learning velocity", "#10B981"))
        hl.addWidget(AnalyticsMetricCard("Study Streak", "12", "Days", "Daily consistency", "#8B5CF6"))
        hl.addStretch()
        
        self.center_layout.addWidget(hero)

    def _setup_columns(self):
        titles = [
            ("Backlog", "#64748B"),
            ("Planned", "#3B82F6"),
            ("In Progress", "#F59E0B"),
            ("Focus Session", "#8B5CF6"),
            ("Review", "#10B981"),
            ("Completed", "#94A3B8")
        ]
        
        for title, color in titles:
            col = KanbanColumn(title, color=color)
            if title == "Planned":
                col.add_task({"title": "Design System Layouts", "category": "Design", "priority": "High", "due_date": "Tomorrow", "focus_time": "1.5h"})
                col.add_task({"title": "Algorithm Lab Report", "category": "AI/ML", "priority": "Critical", "due_date": "Today", "focus_time": "2h"})
            elif title == "In Progress":
                col.add_task({"title": "Python Advanced Patterns", "category": "Development", "priority": "Medium", "due_date": "Today", "focus_time": "1h", "progress": 65})
            elif title == "Focus Session":
                col.add_task({"title": "PyQt6 Event Loop Study", "category": "AI/ML", "priority": "AI Recommended", "due_date": "Now", "focus_time": "45m", "progress": 20})
                
            self.board_layout.addWidget(col)
