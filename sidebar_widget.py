import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QGraphicsDropShadowEffect, QButtonGroup, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QColor
from i18n import _

class SidebarButton(QPushButton):
    """Custom QPushButton configured for the SaaS Sidebar."""
    def __init__(self, text, icon_text=""):
        super().__init__(f"{icon_text}   {text}")
        
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(45)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #64748B;
                border-radius: 10px;
                padding-left: 15px;
                text-align: left;
                font-family: 'Segoe UI', system-ui, sans-serif;
                font-size: 14px;
                font-weight: 500;
                border: none;
                border-left: 4px solid transparent; 
            }
            QPushButton:hover {
                background-color: #E0F2FE;
                color: #0284C7;
                border-left: 4px solid #38BDF8;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
            }
            QPushButton:checked {
                background-color: #E0F2FE;
                color: #0284C7;
                font-weight: 600;
                border-left: 4px solid #38BDF8;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
            }
        """)

class SidebarWidget(QWidget):
    # Signal emitted when a navigation item is clicked. Emits the target index.
    navigation_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            SidebarWidget {
                background-color: #FFFFFF;
                border-right: 1px solid #E2E8F0;
                border-radius: 0px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(4)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 10))
        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 32, 16, 24)
        self.layout.setSpacing(8)

        self._setup_logo_area()
        self._setup_navigation_menu()
        
        self.layout.addStretch()
        
        self._setup_bottom_area()

    def _setup_logo_area(self):
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(8, 0, 0, 16)
        logo_layout.setSpacing(12)

        logo_icon = QLabel("✦")
        logo_icon.setStyleSheet("color: #0284C7; font-size: 24px; font-weight: bold;")
        
        logo_text = QLabel("AI-Career Bridge")
        logo_text.setStyleSheet("""
            color: #0F172A;
            font-size: 16px;
            font-weight: 700;
            font-family: 'Segoe UI', system-ui, sans-serif;
        """)

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        
        self.layout.addLayout(logo_layout)

    def _setup_navigation_menu(self):
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        # Mapping items to the same indices used in main.py:
        menu_items = [
            ("Dashboard (Tổng quan)", "🏠", 0),
            ("Profile & CV Builder (Hồ sơ & CV)", "📝", 1),
            ("Academic Roadmap (Lộ trình học tập)", "🗺️", 4),
            ("Study Tasks & Calendar (Nhiệm vụ & Lịch)", "📅", 2),
            ("Job Portal (Tuyển dụng với AI)", "💼", 5),
            ("AI Mentor & Chat (Trợ lý AI)", "🤖", 6),
            ("Certifications (Chứng chỉ)", "📜", 12),
            ("Notifications (Thông báo)", "🔔", 11),
            ("Settings (Cài đặt)", "⚙️", 8)
        ]

        for text, icon, idx in menu_items:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda ch, i=idx: self.navigation_requested.emit(i))
            self.button_group.addButton(btn, idx)
            self.layout.addWidget(btn)

        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)

    def set_active_index(self, idx):
        btn = self.button_group.button(idx)
        if btn:
            btn.setChecked(True)

    def _setup_bottom_area(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E2E8F0; border: none;")
        separator.setFixedHeight(1)
        self.layout.addWidget(separator)
        
        profile_widget = QWidget()
        profile_widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        profile_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-radius: 8px;
            }
            QWidget:hover {
                background-color: #F1F5F9;
            }
        """)
        # We can link clicking on the profile widget to the Profile page (index 1)
        profile_widget.mousePressEvent = lambda e: self.navigation_requested.emit(1)
        
        profile_layout = QHBoxLayout(profile_widget)
        profile_layout.setContentsMargins(8, 8, 8, 8)
        profile_layout.setSpacing(12)

        avatar = QLabel("JD")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #0284C7;
            color: white;
            border-radius: 18px;
            font-weight: bold;
            font-size: 14px;
        """)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        user_name = QLabel("John Doe")
        user_name.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600;")
        
        user_role = QLabel("Software Engineer")
        user_role.setStyleSheet("color: #64748B; font-size: 12px;")

        info_layout.addWidget(user_name)
        info_layout.addWidget(user_role)
        
        # Settings Icon
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(24, 24)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                color: #475569;
            }
        """)
        # Link settings to Settings page (index 8)
        settings_btn.clicked.connect(lambda: self.navigation_requested.emit(8))

        profile_layout.addWidget(avatar)
        profile_layout.addLayout(info_layout)
        profile_layout.addStretch()
        profile_layout.addWidget(settings_btn)

        self.layout.addWidget(profile_widget)
