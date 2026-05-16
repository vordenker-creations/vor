from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QStackedWidget
from PyQt6.QtCore import Qt
from .ai_career_coach_workspace import AICareerCoachWorkspace

class AIWorkspacePage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("AIWorkspacePage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # We use a stack in case we add more specialized AI child workspaces later
        self.stack = QStackedWidget()
        
        # 1. AI Career Coach Workspace
        self.career_coach = AICareerCoachWorkspace(controller=self.controller)
        self.stack.addWidget(self.career_coach)
        
        main_layout.addWidget(self.stack)
