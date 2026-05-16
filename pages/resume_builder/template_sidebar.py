from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea, 
                             QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class FilterItem(QPushButton):
    def __init__(self, text, icon="○", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 10px 16px;
                color: #64748B;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                color: #0F172A;
            }
            QPushButton:checked {
                background-color: #E0F2FE;
                color: #0284C7;
                font-weight: 600;
            }
        """)

class TemplateSidebar(QFrame):
    filter_changed = pyqtSignal(str)
    search_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 24, 20, 24)
        self.main_layout.setSpacing(20)

        # 1. Header
        header = QLabel("Template Studio")
        header.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        self.main_layout.addWidget(header)

        # 2. Search Bar
        search_container = QFrame()
        search_container.setFixedHeight(44)
        search_container.setStyleSheet("""
            background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px;
        """)
        sl = QHBoxLayout(search_container)
        sl.setContentsMargins(12, 0, 12, 0)
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("border: none; color: #94A3B8;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search templates...")
        self.search_input.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #0F172A;")
        self.search_input.textChanged.connect(self.search_requested.emit)
        
        sl.addWidget(search_icon)
        sl.addWidget(self.search_input)
        self.main_layout.addWidget(search_container)

        # 3. Filters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        filter_widget = QWidget()
        self.filter_layout = QVBoxLayout(filter_widget)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_layout.setSpacing(4)

        sections = [
            ("COLLECTIONS", ["All Templates", "Featured", "AI Recommended", "Favorites"]),
            ("STYLE", ["Modern", "Minimal", "Corporate", "Creative", "Executive"]),
            ("ROLES", ["Developer", "Designer", "Manager", "Student"])
        ]

        self.filter_buttons = []
        for section_title, items in sections:
            lbl = QLabel(section_title)
            lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 800; letter-spacing: 1px; margin: 16px 0 8px 12px; border: none;")
            self.filter_layout.addWidget(lbl)
            
            for item in items:
                btn = FilterItem(item)
                btn.clicked.connect(lambda ch, i=item: self._on_filter_clicked(i))
                self.filter_layout.addWidget(btn)
                self.filter_buttons.append(btn)
                if item == "All Templates": btn.setChecked(True)

        self.filter_layout.addStretch()
        scroll.setWidget(filter_widget)
        self.main_layout.addWidget(scroll)

        # 4. Bottom Profile Area
        self.main_layout.addSpacing(20)
        footer = QFrame()
        footer.setFixedHeight(70)
        footer.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0;")
        fl = QHBoxLayout(footer)
        
        avatar = QFrame()
        avatar.setFixedSize(36, 36)
        avatar.setStyleSheet("background: #38BDF8; border-radius: 18px;")
        
        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        name = QLabel("John Doe")
        name.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none;")
        progress = QLabel("Setup: 85%")
        progress.setStyleSheet("font-size: 11px; color: #64748B; border: none;")
        user_info.addWidget(name)
        user_info.addWidget(progress)
        
        fl.addWidget(avatar)
        fl.addLayout(user_info)
        fl.addStretch()
        
        self.main_layout.addWidget(footer)

    def _on_filter_clicked(self, filter_name):
        for btn in self.filter_buttons:
            btn.setChecked(btn.text() == filter_name)
        self.filter_changed.emit(filter_name)
