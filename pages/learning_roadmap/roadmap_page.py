import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QComboBox, QStackedWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .roadmap_sidebar import RoadmapSidebar
from .milestone_sidebar import MilestoneSidebar
from .analytics_sidebar import AnalyticsSidebar
from .career_sidebar import CareerSidebar
from .certification_sidebar import CertificationSidebar
from .roadmap_generator_sidebar import RoadmapGeneratorSidebar

from .roadmap_canvas import RoadmapCanvas
from .milestone_tracker_view import MilestoneTrackerView
from .learning_analytics_view import LearningAnalyticsView
from .career_prediction_view import CareerPredictionView
from .certification_tracker_view import CertificationTrackerView
from .roadmap_builder_view import RoadmapBuilderView

from .guidance_panel import GuidancePanel
from .ai_productivity_panel import AIProductivityPanel
from .ai_forecasting_panel import AIForecastingPanel
from .ai_career_panel import AICareerPanel
from .ai_certification_panel import AICertificationPanel
from .ai_generator_panel import AIGeneratorPanel

from components import CollapsiblePanel

class GraphHeader(QFrame):
    view_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(72)
        self.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(24)

        # 1. Title & Progress
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        info_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.title_lbl = QLabel("Python AI Engineer")
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        
        self.prog_lbl = QLabel("45% Completed • 12/24 Skills Mastered")
        self.prog_lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #64748B; border: none;")
        
        info_v.addWidget(self.title_lbl)
        info_v.addWidget(self.prog_lbl)
        layout.addLayout(info_v)

        layout.addStretch()

        # 2. View Mode Selector
        self.view_selector = QComboBox()
        self.view_selector.addItems(["Skill Graph", "Milestone Tracker", "Analytics", "Career AI", "Certifications", "AI Generator"])
        self.view_selector.setFixedWidth(180)
        self.view_selector.setFixedHeight(36)
        self.view_selector.setStyleSheet("""
            QComboBox {
                background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                padding: 0 12px; font-size: 12px; font-weight: 600; color: #475569;
            }
            QComboBox::drop-down { border: none; }
        """)
        self.view_selector.currentIndexChanged.connect(self.view_changed.emit)
        layout.addWidget(self.view_selector)

        # 3. Zoom Controls
        zoom_h = QHBoxLayout()
        zoom_h.setSpacing(4)
        for icon in ["-", "100%", "+"]:
            btn = QPushButton(icon)
            btn.setFixedSize(36 if icon != "100%" else 54, 32)
            btn.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; font-size: 11px; font-weight: 700; color: #475569;")
            zoom_h.addWidget(btn)
        layout.addLayout(zoom_h)

        layout.addStretch()

        # 4. Global Actions
        btn_share = QPushButton("Share")
        btn_share.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 8px 16px; font-weight: 700; font-size: 12px;")
        layout.addWidget(btn_share)
        
        self.btn_action = QPushButton("Generate AI Plan")
        self.btn_action.setStyleSheet("background: #0F172A; color: white; border-radius: 10px; padding: 8px 16px; font-weight: 700; font-size: 12px;")
        layout.addWidget(self.btn_action)

class LearningRoadmapPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("LearningRoadmapPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Left Sidebar Stack
        self.sidebar_stack = QStackedWidget()
        self.sidebar_stack.addWidget(RoadmapSidebar())         # 0
        self.sidebar_stack.addWidget(MilestoneSidebar())       # 1
        self.sidebar_stack.addWidget(AnalyticsSidebar())       # 2
        self.sidebar_stack.addWidget(CareerSidebar())          # 3
        self.sidebar_stack.addWidget(CertificationSidebar())   # 4
        self.sidebar_stack.addWidget(RoadmapGeneratorSidebar()) # 5
        
        self.left_panel = CollapsiblePanel(self.sidebar_stack, orientation="left")
        self.main_layout.addWidget(self.left_panel)

        # Main Workspace Container
        self.workspace_container = QWidget()
        self.workspace_layout = QVBoxLayout(self.workspace_container)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(0)

        # Graph Header
        self.header = GraphHeader()
        self.header.view_changed.connect(self._handle_view_change)
        self.workspace_layout.addWidget(self.header)
        
        # Center Content Stack
        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(RoadmapCanvas())               # 0
        self.content_stack.addWidget(MilestoneTrackerView())        # 1
        self.content_stack.addWidget(LearningAnalyticsView())       # 2
        self.content_stack.addWidget(CareerPredictionView())        # 3
        self.content_stack.addWidget(CertificationTrackerView())    # 4
        self.content_stack.addWidget(RoadmapBuilderView())          # 5
        self.workspace_layout.addWidget(self.content_stack, 1)

        self.main_layout.addWidget(self.workspace_container, 1)

        # Right Guidance Stack
        self.right_stack = QStackedWidget()
        self.right_stack.addWidget(GuidancePanel())            # 0
        self.right_stack.addWidget(AIProductivityPanel())      # 1
        self.right_stack.addWidget(AIForecastingPanel())       # 2
        self.right_stack.addWidget(AICareerPanel())            # 3
        self.right_stack.addWidget(AICertificationPanel())     # 4
        self.right_stack.addWidget(AIGeneratorPanel())         # 5
        
        self.right_panel = CollapsiblePanel(self.right_stack, orientation="right")
        self.main_layout.addWidget(self.right_panel)

    def _handle_view_change(self, idx):
        self.sidebar_stack.setCurrentIndex(idx)
        self.content_stack.setCurrentIndex(idx)
        self.right_stack.setCurrentIndex(idx)
        
        actions = [
            "Generate AI Plan", 
            "Generate AI Schedule", 
            "Generate AI Insights", 
            "Generate Prediction", 
            "Generate Recommendations",
            "Generate AI Roadmap"
        ]
        self.header.btn_action.setText(actions[idx])
