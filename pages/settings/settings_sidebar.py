from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class SettingsNavItem(QPushButton):
    def __init__(self, text, icon="○", parent=None):
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

class SettingsSidebar(QFrame):
    navigation_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 24, 16, 24)
        self.main_layout.setSpacing(20)

        # 1. Header
        header_v = QVBoxLayout()
        header_v.setSpacing(16)
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        header_v.addWidget(title)
        
        # Mode Selector
        self.btn_ai_mode = QPushButton("✨ AI Personalization")
        self.btn_ai_mode.setFixedHeight(44)
        self.btn_ai_mode.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC; color: #0284C7; border-radius: 12px;
                font-weight: 700; font-size: 13px; border: 1px solid #E0F2FE;
            }
            QPushButton:hover { background-color: #E0F2FE; }
        """)
        header_v.addWidget(self.btn_ai_mode)
        self.main_layout.addLayout(header_v)

        # 2. Search
        search_container = QFrame()
        search_container.setFixedHeight(44)
        search_container.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px;")
        sl = QHBoxLayout(search_container)
        sl.setContentsMargins(12, 0, 12, 0)
        search_icon = QLabel("🔍")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search settings...")
        search_input.setStyleSheet("border: none; background: transparent; font-size: 13px;")
        sl.addWidget(search_icon)
        sl.addWidget(search_input)
        self.main_layout.addWidget(search_container)

        # 3. Navigation
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        nav_layout = QVBoxLayout(container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(4)

        self.sections = [
            "Profile & Identity", "Preferences", "Notifications", "Appearance", 
            "Accessibility", "Privacy & Security", "AI Personalization", 
            "Integrations", "About Application"
        ]

        self.buttons = []
        for i, name in enumerate(self.sections):
            btn = SettingsNavItem(name)
            btn.clicked.connect(lambda ch, idx=i: self._handle_click(idx))
            nav_layout.addWidget(btn)
            self.buttons.append(btn)
            if i == 0: btn.setChecked(True)

        nav_layout.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Bottom Completion Card
        completion_card = QFrame()
        completion_card.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0; padding: 16px;")
        cl = QVBoxLayout(completion_card)
        cl.setSpacing(10)
        
        lbl = QLabel("Profile Completion")
        lbl.setStyleSheet("font-weight: 700; font-size: 12px; color: #0F172A; border: none;")
        cl.addWidget(lbl)
        
        v_h = QHBoxLayout()
        v_lbl = QLabel("85%")
        v_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #38BDF8; border: none;")
        v_h.addWidget(v_lbl); v_h.addStretch(); cl.addLayout(v_h)
        
        pb = QProgressBar()
        pb.setFixedHeight(6); pb.setValue(85); pb.setTextVisible(False)
        pb.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 3px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 3px; }")
        cl.addWidget(pb)
        
        self.main_layout.addWidget(completion_card)

    def _handle_click(self, idx):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == idx)
        self.navigation_requested.emit(idx)
