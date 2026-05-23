from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from ui_core.components import SaaSCard
from database import crud

class SettingsPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_header()
        
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(24)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self._setup_account_section()
        self._setup_about_section()
        
        # Logout Button
        logout_layout = QHBoxLayout()
        logout_btn = QPushButton("Log Out")
        logout_btn.setFixedSize(160, 44)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover { background-color: #DC2626; }
        """)
        logout_btn.clicked.connect(self._handle_logout)
        logout_layout.addWidget(logout_btn)
        logout_layout.addStretch()
        
        self.content_layout.addSpacing(16)
        self.content_layout.addLayout(logout_layout)
        
        self.main_layout.addWidget(self.content_container, stretch=1)
        
    def _setup_header(self):
        header = QFrame()
        header.setFixedHeight(84)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(32, 0, 32, 0)
        
        info = QVBoxLayout()
        info.setSpacing(4)
        info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        
        sub = QLabel("Manage your account and application preferences")
        sub.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none;")
        
        info.addWidget(title)
        info.addWidget(sub)
        layout.addLayout(info)
        layout.addStretch()
        
        self.main_layout.addWidget(header)
        
    def _setup_account_section(self):
        card = SaaSCard(self)
        
        title = QLabel("Account Information")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        card.internal_layout.addWidget(title)
        card.internal_layout.addSpacing(12)
        
        student = crud.get_current_student()
        email_str = student.get("email", "Unknown") if student else "Not logged in"
        name_str = student.get("name", "Student") if student else "Unknown"
        
        def add_row(lbl, val):
            row = QHBoxLayout()
            label = QLabel(lbl)
            label.setStyleSheet("color: #64748B; font-weight: 600; font-size: 13px; background: transparent; border: none;")
            label.setFixedWidth(100)
            value = QLabel(val)
            value.setStyleSheet("color: #0F172A; font-weight: 500; font-size: 13px; background: transparent; border: none;")
            row.addWidget(label)
            row.addWidget(value)
            row.addStretch()
            card.internal_layout.addLayout(row)
            
        add_row("Name:", name_str)
        card.internal_layout.addSpacing(8)
        add_row("Email:", email_str)
        card.internal_layout.addSpacing(8)
        add_row("Status:", "Active Student")
        
        self.content_layout.addWidget(card)
        
    def _setup_about_section(self):
        card = SaaSCard(self)
        
        title = QLabel("About")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        card.internal_layout.addWidget(title)
        card.internal_layout.addSpacing(12)
        
        desc = QLabel("AI-Career Bridge (Academic Local-First App)\nVersion 1.0.0")
        desc.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.5; background: transparent; border: none;")
        card.internal_layout.addWidget(desc)
        
        self.content_layout.addWidget(card)
        
    def _handle_logout(self):
        if self.controller and hasattr(self.controller, 'logout'):
            self.controller.logout()
