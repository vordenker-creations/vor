from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class ATSNavItem(QPushButton):
    def __init__(self, text, icon="○", badge=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(48)
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
        
        if badge:
            self.badge_lbl = QLabel(badge, self)
            self.badge_lbl.setStyleSheet("""
                background: #EF4444; color: white; border-radius: 8px;
                font-size: 10px; font-weight: 800; padding: 2px 6px;
            """)
            self.badge_lbl.adjustSize()
            # Position badge later in resizeEvent if needed or just use layout

class ATSSidebar(QFrame):
    tab_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 24, 16, 24)
        self.main_layout.setSpacing(20)

        # 1. Header
        header_v = QVBoxLayout()
        header_v.setSpacing(4)
        title = QLabel("ATS Intelligence")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        score_box = QHBoxLayout()
        self.score_lbl = QLabel("Score: 85/100")
        self.score_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #10B981; background: #10B98115; padding: 2px 8px; border-radius: 6px;")
        score_box.addWidget(self.score_lbl)
        score_box.addStretch()
        
        header_v.addWidget(title)
        header_v.addLayout(score_box)
        self.main_layout.addLayout(header_v)

        # 2. Search
        search_container = QFrame()
        search_container.setFixedHeight(40)
        search_container.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;")
        sl = QHBoxLayout(search_container)
        sl.setContentsMargins(10, 0, 10, 0)
        search_icon = QLabel("🔍")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search insights...")
        search_input.setStyleSheet("border: none; background: transparent; font-size: 12px;")
        sl.addWidget(search_icon)
        sl.addWidget(search_input)
        self.main_layout.addWidget(search_container)

        # 3. Navigation
        self.nav_group = QWidget()
        nav_layout = QVBoxLayout(self.nav_group)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(4)

        tabs = [
            ("Overview", 0),
            ("Keyword Analysis", 1),
            ("Formatting Scanner", 2),
            ("Recruiter Readability", 3),
            ("AI Optimization", 4),
            ("ATS History", 5),
            ("Reports Export", 6)
        ]

        self.buttons = []
        for i, (name, idx) in enumerate(tabs):
            btn = ATSNavItem(name)
            btn.clicked.connect(lambda ch, x=idx: self._handle_click(x))
            nav_layout.addWidget(btn)
            self.buttons.append(btn)
            if idx == 0: btn.setChecked(True)

        self.main_layout.addWidget(self.nav_group)
        self.main_layout.addStretch()

        # 4. Footer info
        footer = QFrame()
        footer.setStyleSheet("background: #F8FAFC; border-radius: 12px; padding: 10px;")
        fl = QVBoxLayout(footer)
        fl.addWidget(QLabel("Total Scans: 24", styleSheet="font-size: 11px; color: #64748B; font-weight: 600;"))
        fl.addWidget(QLabel("Avg. Score: 78%", styleSheet="font-size: 11px; color: #64748B; font-weight: 600;"))
        self.main_layout.addWidget(footer)

    def _handle_click(self, idx):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == idx)
        self.tab_changed.emit(idx)
