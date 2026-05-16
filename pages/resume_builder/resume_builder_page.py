import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QComboBox, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .template_sidebar import TemplateSidebar
from .template_card_widget import TemplateCard
from .template_preview_panel import TemplatePreviewPanel
from .ats_workspace_page import ATSWorkspacePage
from components import CollapsiblePanel

class ResumeBuilderPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("ResumeBuilderPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # Mode Switcher Header (Global for Resume Builder)
        self._setup_mode_header()

        self.mode_stack = QStackedWidget()
        
        # Mode 0: Design Workspace (Marketplace)
        self.design_workspace = QWidget()
        self.design_layout = QHBoxLayout(self.design_workspace)
        self.design_layout.setContentsMargins(0, 0, 0, 0)
        self.design_layout.setSpacing(0)
        
        # Left Sidebar (Collapsible)
        self.sidebar_content = TemplateSidebar()
        self.sidebar_content.filter_changed.connect(self._handle_filter_change)
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        self.design_layout.addWidget(self.left_panel)
        
        self.marketplace_container = QWidget()
        self.marketplace_layout = QVBoxLayout(self.marketplace_container)
        self.marketplace_layout.setContentsMargins(0, 0, 0, 0)
        self.marketplace_layout.setSpacing(0)
        self._setup_marketplace_header()
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(32, 32, 32, 40)
        self.grid_layout.setSpacing(24)
        self._load_templates()
        self.scroll.setWidget(self.grid_widget)
        self.marketplace_layout.addWidget(self.scroll)
        self.design_layout.addWidget(self.marketplace_container, 1)
        
        # Right Preview Panel (Collapsible)
        self.preview_panel_content = TemplatePreviewPanel()
        self.right_panel = CollapsiblePanel(self.preview_panel_content, orientation="right")
        self.design_layout.addWidget(self.right_panel)
        
        # Mode 1: ATS Workspace
        self.ats_workspace = ATSWorkspacePage(controller=self.controller)
        
        self.mode_stack.addWidget(self.design_workspace) # 0
        self.mode_stack.addWidget(self.ats_workspace)    # 1
        
        self.root_layout.addWidget(self.mode_stack)

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

    def _setup_mode_header(self):
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)
        
        title = QLabel("Resume Studio")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        hl.addWidget(title)
        
        hl.addStretch()
        
        # Switcher
        switcher = QFrame()
        switcher.setFixedHeight(38)
        switcher.setStyleSheet("background: #F1F5F9; border-radius: 10px; padding: 2px;")
        sl = QHBoxLayout(switcher)
        sl.setContentsMargins(2, 2, 2, 2)
        sl.setSpacing(0)
        
        self.btn_design = QPushButton("Design")
        self.btn_design.setCheckable(True)
        self.btn_design.setChecked(True)
        self.btn_design.setFixedSize(100, 34)
        
        self.btn_analyze = QPushButton("ATS Analyze")
        self.btn_analyze.setCheckable(True)
        self.btn_analyze.setFixedSize(100, 34)
        
        style = """
            QPushButton {
                background: transparent; border: none; border-radius: 8px;
                color: #64748B; font-weight: 700; font-size: 12px;
            }
            QPushButton:checked {
                background: white; color: #0F172A;
            }
        """
        self.btn_design.setStyleSheet(style)
        self.btn_analyze.setStyleSheet(style)
        
        self.btn_design.clicked.connect(lambda: self._set_mode(0))
        self.btn_analyze.clicked.connect(lambda: self._set_mode(1))
        
        sl.addWidget(self.btn_design)
        sl.addWidget(self.btn_analyze)
        hl.addWidget(switcher)
        
        hl.addStretch()
        
        # User / Global Action
        btn_new = QPushButton("New Resume")
        btn_new.setStyleSheet("""
            QPushButton { background: #0F172A; color: white; border-radius: 10px; padding: 8px 16px; font-weight: 700; }
            QPushButton:hover { background: #1E293B; }
        """)
        hl.addWidget(btn_new)
        
        self.root_layout.addWidget(header)

    def _set_mode(self, idx):
        self.mode_stack.setCurrentIndex(idx)
        self.btn_design.setChecked(idx == 0)
        self.btn_analyze.setChecked(idx == 1)

    def _setup_marketplace_header(self):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(32, 0, 32, 0)
        hl.setSpacing(20)
        
        title_v = QVBoxLayout(); title_v.setSpacing(2); title_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title_lbl = QLabel("Template Marketplace")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        count_lbl = QLabel("124 Premium Templates")
        count_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none;")
        title_v.addWidget(title_lbl); title_v.addWidget(count_lbl)
        hl.addLayout(title_v)
        
        hl.addStretch()

        # Zoom Controls
        zoom_layout = QHBoxLayout()
        zoom_layout.setSpacing(8)
        
        self.btn_zoom_out = QPushButton("-")
        self.btn_zoom_out.setFixedSize(32, 32)
        self.btn_zoom_out.setStyleSheet("background: #F1F5F9; border-radius: 8px; font-weight: 800;")
        
        self.zoom_lbl = QLabel("100%")
        self.zoom_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #0F172A; min-width: 40px;")
        self.zoom_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_in.setFixedSize(32, 32)
        self.btn_zoom_in.setStyleSheet("background: #F1F5F9; border-radius: 8px; font-weight: 800;")
        
        self.btn_zoom_out.clicked.connect(lambda: self._handle_zoom(-10))
        self.btn_zoom_in.clicked.connect(lambda: self._handle_zoom(10))
        
        zoom_layout.addWidget(self.btn_zoom_out)
        zoom_layout.addWidget(self.zoom_lbl)
        zoom_layout.addWidget(self.btn_zoom_in)
        hl.addLayout(zoom_layout)
        
        hl.addSpacing(20)
        
        self.view_selector = QComboBox()
        self.view_selector.addItems(["Popular", "ATS Score", "AI Recommended"])
        self.view_selector.setFixedWidth(140); self.view_selector.setFixedHeight(36)
        self.view_selector.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding-left: 8px;")
        hl.addWidget(self.view_selector)
        
        self.marketplace_layout.addWidget(header)
        self.current_zoom = 100

    def _handle_zoom(self, delta):
        new_zoom = max(50, min(150, self.current_zoom + delta))
        if new_zoom == self.current_zoom: return
        self.current_zoom = new_zoom
        self.zoom_lbl.setText(f"{self.current_zoom}%")
        
        # Scale cards
        scale = self.current_zoom / 100.0
        base_w, base_h = 280, 420
        for card in self.cards:
            card.setMinimumWidth(int(base_w * scale))
            card.setMaximumWidth(int(base_w * scale * 1.5))
            card.setMinimumHeight(int(base_h * scale))
        
        # Adjust grid spacing
        self.grid_layout.setSpacing(int(24 * scale))

    def _load_templates(self):
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        templates = [
            {"name": "Prism Architect", "category": "Modern", "ats_score": 98, "color": "#E0F2FE", "is_premium": True, "is_ai_recommended": True},
            {"name": "Minimalist Pro", "category": "Minimal", "ats_score": 95, "color": "#F1F5F9", "is_premium": False, "is_ai_recommended": False},
            {"name": "Nova Developer", "category": "Modern", "ats_score": 96, "color": "#FFF7ED", "is_premium": True, "is_ai_recommended": True},
            {"name": "Executive Slate", "category": "Executive", "ats_score": 94, "color": "#F5F3FF", "is_premium": False, "is_ai_recommended": False}
        ]

        self.cards = []
        for i, tpl in enumerate(templates):
            card = TemplateCard(tpl)
            card.clicked.connect(self._handle_card_click)
            self.cards.append(card)
            self.grid_layout.addWidget(card, i // 3, i % 3)

    def _handle_card_click(self, data):
        for card in self.cards:
            card.set_selected(card.data == data)
        self.preview_panel_content.update_selected_tpl(data)

    def _handle_filter_change(self, filter_name):
        self._load_templates()
