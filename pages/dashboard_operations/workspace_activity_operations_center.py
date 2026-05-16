from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .realtime_activity_timeline import RealtimeActivityTimeline
from .operations_insights_sidebar import OperationsInsightsSidebar
from components import CollapsiblePanel

class OperationsToolbar(QFrame):
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
        title = QLabel("Workspace Activity")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        status = QLabel("● Live Ops")
        status.setStyleSheet("font-size: 10px; font-weight: 800; color: #10B981; background: #F0FDF4; padding: 2px 8px; border-radius: 6px; border: 1px solid #BBF7D0;")
        
        title_h.addWidget(title); title_h.addWidget(status)
        
        summary = QLabel("Operational event stream successfully connected")
        summary.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600; border: none;")
        
        info_v.addLayout(title_h); info_v.addWidget(summary)
        layout.addLayout(info_v)

        layout.addStretch()

        # 2. Controls
        self.filter_sel = QComboBox()
        self.filter_sel.addItems(["All Activity", "AI Operations", "Productivity", "System"])
        self.filter_sel.setFixedWidth(140); self.filter_sel.setFixedHeight(36)
        self.filter_sel.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding-left: 8px;")
        layout.addWidget(self.filter_sel)

        btn_logs = QPushButton("Export Logs")
        btn_logs.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 10px; color: #0F172A; font-weight: 700; font-size: 12px; height: 36px; padding: 0 16px;")
        layout.addWidget(btn_logs)

        btn_refresh = QPushButton("↻")
        btn_refresh.setFixedSize(36, 36)
        btn_refresh.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; font-weight: 800; font-size: 16px;")
        layout.addWidget(btn_refresh)

class WorkspaceActivityOperationsCenter(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("WorkspaceActivityOperationsCenter")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Central Workspace
        self.center_workspace = QWidget()
        self.center_layout = QVBoxLayout(self.center_workspace)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)

        self.toolbar = OperationsToolbar()
        self.center_layout.addWidget(self.toolbar)

        # Scroll Area for Timeline
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.timeline_container = QWidget()
        self.timeline_layout = QVBoxLayout(self.timeline_container)
        self.timeline_layout.setContentsMargins(40, 32, 40, 40)
        self.timeline_layout.setSpacing(32)

        # Hero Stats
        self._setup_hero_stats()
        
        # Timeline
        self.timeline = RealtimeActivityTimeline()
        self.timeline_layout.addWidget(self.timeline)
        
        self.timeline_layout.addStretch()
        self.scroll.setWidget(self.timeline_container)
        self.center_layout.addWidget(self.scroll)

        self.main_layout.addWidget(self.center_workspace, 1)

        # 2. Right Insights Sidebar
        self.insights_content = OperationsInsightsSidebar()
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        self.main_layout.addWidget(self.right_panel)

    def _setup_hero_stats(self):
        hero_row = QHBoxLayout()
        hero_row.setSpacing(24)
        
        from ..dashboard_analytics.productivity_analytics_panel import AnalyticsMetricCard
        hero_row.addWidget(AnalyticsMetricCard("Active Ops", "12", "Running", "System threads active", "#38BDF8"))
        hero_row.addWidget(AnalyticsMetricCard("Throughput", "1.2k", "msg/s", "Realtime data stream", "#10B981"))
        hero_row.addWidget(AnalyticsMetricCard("Stability", "99.9%", "Uptime", "Core platform health", "#8B5CF6"))
        
        self.timeline_layout.addLayout(hero_row)
