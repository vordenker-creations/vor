import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt

from .ai_sidebar import AICareerSidebar
from .ai_chat_canvas import AIChatCanvas
from .ai_insight_panel import AICareerInsights

from components import CollapsiblePanel

class AICareerCoachWorkspace(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("AICareerCoachWorkspace")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Left AI Sidebar
        self.sidebar_content = AICareerSidebar()
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        self.main_layout.addWidget(self.left_panel)

        # 2. Main Chat Canvas
        self.chat_canvas = AIChatCanvas()
        self.main_layout.addWidget(self.chat_canvas, 1)

        # 3. Right Insights Panel
        self.insights_content = AICareerInsights()
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        self.main_layout.addWidget(self.right_panel)

        # Initial Welcome Message
        self.chat_canvas.append_message("Hello! I am your AI Career Coach. How can I help you today?", is_ai=True)
