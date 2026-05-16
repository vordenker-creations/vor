import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .ats_sidebar import ATSSidebar
from .ats_widgets import ATSOverviewWidget, KeywordAnalysisWidget
from .ats_intelligence_panel import ATSIntelligencePanel
from components import CollapsiblePanel

class ATSWorkspacePage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("ATSWorkspacePage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Left Internal Sidebar (Collapsible)
        self.sidebar_content = ATSSidebar()
        self.sidebar_content.tab_changed.connect(self._handle_tab_change)
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        self.main_layout.addWidget(self.left_panel)

        # 2. Main Workspace
        self.workspace_container = QWidget()
        self.workspace_layout = QVBoxLayout(self.workspace_container)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(0)

        self._setup_top_header()
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(ATSOverviewWidget())      # 0
        self.stacked_widget.addWidget(KeywordAnalysisWidget())  # 1
        # Add other placeholders
        for _ in range(5): 
            self.stacked_widget.addWidget(self._create_placeholder())
            
        self.workspace_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.workspace_container, 1)

        # 3. Right Intelligence Panel (Collapsible)
        self.intel_panel_content = ATSIntelligencePanel()
        self.right_panel = CollapsiblePanel(self.intel_panel_content, orientation="right")
        self.main_layout.addWidget(self.right_panel)

    def resizeEvent(self, event):
        # Auto-collapse sidebars on small windows
        width = event.size().width()
        if width < 1100:
            if self.left_panel.is_expanded: self.left_panel.toggle()
            if self.right_panel.is_expanded: self.right_panel.toggle()
        elif width > 1300:
            if not self.left_panel.is_expanded: self.left_panel.toggle()
            if not self.right_panel.is_expanded: self.right_panel.toggle()
        super().resizeEvent(event)

    def _setup_top_header(self):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(32, 0, 32, 0)
        hl.setSpacing(24)

        # Title
        title_v = QVBoxLayout()
        title_v.setSpacing(2)
        title_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.tab_title_lbl = QLabel("Overview")
        self.tab_title_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        summary = QLabel("Enterprise Intelligence • Last Scan: 2m ago")
        summary.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600; border: none;")
        
        title_v.addWidget(self.tab_title_lbl)
        title_v.addWidget(summary)
        hl.addLayout(title_v)

        hl.addStretch()

        # Resume Selector
        self.resume_sel = QComboBox()
        self.resume_sel.addItems(["Senior_Dev_Resume.pdf", "AI_Researcher_v2.pdf"])
        self.resume_sel.setFixedWidth(200)
        self.resume_sel.setFixedHeight(36)
        self.resume_sel.setStyleSheet("""
            QComboBox {
                background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                padding: 0 12px; font-size: 12px; font-weight: 600; color: #475569;
            }
            QComboBox::drop-down { border: none; }
        """)
        hl.addWidget(self.resume_sel)

        btn_scan = QPushButton("✨ Run Intelligence Scan")
        btn_scan.setFixedHeight(36)
        btn_scan.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_scan.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: #0F172A; border-radius: 10px;
                font-weight: 800; font-size: 11px; padding: 0 16px; border: none;
            }
            QPushButton:hover { background: #7DD3FC; }
        """)
        hl.addWidget(btn_scan)

        self.workspace_layout.addWidget(header)

    def _create_placeholder(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel("Module Coming Soon")
        lbl.setStyleSheet("color: #94A3B8; font-size: 16px; font-weight: 600;")
        l.addWidget(lbl)
        return w

    def _handle_tab_change(self, idx):
        self.stacked_widget.setCurrentIndex(idx)
        titles = ["Overview", "Keyword Analysis", "Formatting Scanner", "Recruiter Readability", "AI Optimization", "ATS History", "Reports Export"]
        self.tab_title_lbl.setText(titles[idx])
