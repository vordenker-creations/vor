from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
from .interview_sidebar import InterviewSidebar
from .interview_workspace import InterviewWorkspace
from .feedback_panel import FeedbackPanel

from components import CollapsiblePanel

class InterviewSimulatorPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("InterviewSimulatorPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Left Sidebar (Collapsible)
        self.sidebar_content = InterviewSidebar()
        self.sidebar_content.setFixedWidth(260)
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        main_layout.addWidget(self.left_panel)
        
        # 2. Main Interaction Workspace
        self.workspace = InterviewWorkspace()
        main_layout.addWidget(self.workspace, 1) # Stretch factor 1
        
        # 3. Right Feedback Panel (Collapsible)
        self.feedback_content = FeedbackPanel()
        self.feedback_content.setFixedWidth(320)
        self.right_panel = CollapsiblePanel(self.feedback_content, orientation="right")
        main_layout.addWidget(self.right_panel)
