from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QSplitter
from PyQt6.QtCore import Qt
from .job_sidebar import JobSidebar
from .job_feed import JobFeed
from .ai_insights_panel import AIInsightsPanel
from .job_preview_panel import JobPreviewPanel
from .application_modal import ApplicationModal

from components import CollapsiblePanel

class JobPortalPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("JobPortalPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Left Sidebar (Collapsible Filters)
        self.sidebar_content = JobSidebar()
        self.sidebar_content.setFixedWidth(260)
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        main_layout.addWidget(self.left_panel)
        
        # 2. Splitter for Feed and Preview
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #E2E8F0;
                width: 1px;
            }
        """)
        
        self.feed = JobFeed()
        self.feed.job_selected.connect(self._handle_job_selection)
        self.feed.apply_requested.connect(self._open_application_modal)
        
        self.preview = JobPreviewPanel(self) # Pass self as parent for clear_selection
        self.preview.apply_clicked.connect(self._open_application_modal)
        
        self.splitter.addWidget(self.feed)
        self.splitter.addWidget(self.preview)
        
        # Set initial sizes (Feed takes all space initially since Preview is 0 max width)
        self.splitter.setStretchFactor(0, 1) # Feed stretches
        self.splitter.setStretchFactor(1, 0) # Preview fixed-ish
        
        main_layout.addWidget(self.splitter, 1)
        
        # 3. Right AI Insights (Collapsible)
        self.insights_content = AIInsightsPanel()
        self.insights_content.setFixedWidth(300)
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        main_layout.addWidget(self.right_panel)

    def _handle_job_selection(self, data):
        self.preview.set_job(data)

    def clear_selection(self):
        """Called by preview panel when closed to clear highlights in feed."""
        if hasattr(self.feed, "job_cards"):
            for card in self.feed.job_cards:
                card.set_selected(False)

    def _open_application_modal(self, data):
        modal = ApplicationModal(data, self)
        modal.exec()
