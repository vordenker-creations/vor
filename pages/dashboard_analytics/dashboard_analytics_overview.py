from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .productivity_analytics_panel import AnalyticsMetricCard, ProgressMetricCard
from .activity_heatmap_widget import ActivityHeatmapWidget
from .analytics_insights_sidebar import AnalyticsInsightsSidebar
from .ai_metrics_workspace import AIMetricsPanel

from components import CollapsiblePanel

class AnalyticsToolbar(QFrame):
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
        title = QLabel("Analytics Overview")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        status = QLabel("● Realtime")
        status.setStyleSheet("font-size: 10px; font-weight: 800; color: #10B981; background: #F0FDF4; padding: 2px 8px; border-radius: 6px; border: 1px solid #BBF7D0;")
        
        title_h.addWidget(title); title_h.addWidget(status)
        
        summary = QLabel("Enterprise Productivity Monitoring active")
        summary.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600; border: none;")
        
        info_v.addLayout(title_h); info_v.addWidget(summary)
        layout.addLayout(info_v)

        layout.addStretch()

        # 2. Controls
        self.range_sel = QComboBox()
        self.range_sel.addItems(["Today", "Last 7 Days", "Last 30 Days", "Last 90 Days"])
        self.range_sel.setFixedWidth(140); self.range_sel.setFixedHeight(36)
        self.range_sel.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding-left: 8px;")
        layout.addWidget(self.range_sel)

        btn_report = QPushButton("Generate Report")
        btn_report.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 10px; color: #0F172A; font-weight: 700; font-size: 12px; height: 36px; padding: 0 16px;")
        layout.addWidget(btn_report)

        btn_refresh = QPushButton("↻")
        btn_refresh.setFixedSize(36, 36)
        btn_refresh.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; font-weight: 800; font-size: 16px;")
        layout.addWidget(btn_refresh)

class DashboardAnalyticsOverview(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("DashboardAnalyticsOverview")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Central Workspace
        self.center_workspace = QWidget()
        self.center_layout = QVBoxLayout(self.center_workspace)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)

        self.toolbar = AnalyticsToolbar()
        self.center_layout.addWidget(self.toolbar)

        # Scroll Area for Content
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.grid_widget = QWidget()
        self.grid_layout = QVBoxLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(32, 32, 32, 40)
        self.grid_layout.setSpacing(32)

        self._setup_hero_section()
        self._setup_analytics_grid()
        self._setup_heatmap_section()

        self.grid_layout.addStretch()
        self.scroll.setWidget(self.grid_widget)
        self.center_layout.addWidget(self.scroll)

        self.main_layout.addWidget(self.center_workspace, 1)

        # 2. Right Insights Sidebar
        self.insights_content = AnalyticsInsightsSidebar()
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        self.main_layout.addWidget(self.right_panel)

    def _setup_hero_section(self):
        hero_row = QHBoxLayout()
        hero_row.setSpacing(24)
        
        hero_row.addWidget(AnalyticsMetricCard("Productivity Score", "92/100", "+8%", "Based on 12 workflow metrics", "#10B981"))
        hero_row.addWidget(AnalyticsMetricCard("Task Velocity", "24.5", "+12%", "Avg. tasks per day", "#38BDF8"))
        hero_row.addWidget(AnalyticsMetricCard("AI Efficiency", "88%", "+4%", "Interference vs outcome", "#8B5CF6"))
        
        self.grid_layout.addLayout(hero_row)

    def _setup_analytics_grid(self):
        grid_row = QHBoxLayout()
        grid_row.setSpacing(24)
        
        # Left side column metrics
        v_metrics = QVBoxLayout(); v_metrics.setSpacing(24)
        v_metrics.addWidget(ProgressMetricCard("Learning Progress", 68, "#38BDF8"))
        v_metrics.addWidget(ProgressMetricCard("Skill Mastery", 42, "#10B981"))
        
        # AI Metrics inside the grid
        v_metrics.addWidget(AIMetricsPanel())
        
        grid_row.addLayout(v_metrics, 1)
        
        # Weekly performance trends
        chart_preview = QFrame()
        chart_preview.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        cl = QVBoxLayout(chart_preview); cl.setContentsMargins(24, 24, 24, 24)
        cl.addWidget(QLabel("Weekly Performance Trends", styleSheet="font-size: 15px; font-weight: 700; color: #0F172A; border: none;"))
        
        # Simulated chart visual
        chart_viz = QFrame()
        chart_viz.setStyleSheet("background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px;")
        cl.addWidget(chart_viz)
        
        grid_row.addWidget(chart_preview, 2)
        
        self.grid_layout.addLayout(grid_row)

    def _setup_heatmap_section(self):
        self.grid_layout.addWidget(ActivityHeatmapWidget())
