from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy, QGridLayout
from PyQt6.QtCore import Qt
from ui_core.components import SaaSCard, ModernSwitch
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
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(24)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # --- Two Column Layout ---
        left_col = QVBoxLayout()
        left_col.setSpacing(24)
        left_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        right_col = QVBoxLayout()
        right_col.setSpacing(24)
        right_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        left_col.addWidget(self._create_profile_card())
        left_col.addWidget(self._create_preferences_card())
        
        right_col.addWidget(self._create_sync_card())
        right_col.addWidget(self._create_danger_zone_card())
        
        self.content_layout.addLayout(left_col, 1)
        self.content_layout.addLayout(right_col, 1)
        
        self.main_layout.addWidget(self.content_container, stretch=1)
        
    def _setup_header(self):
        header = QFrame()
        header.setFixedHeight(84)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)
        
        info = QVBoxLayout()
        info.setSpacing(4)
        info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        
        sub = QLabel("Manage your account, UI preferences, and local data sync.")
        sub.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none;")
        
        info.addWidget(title)
        info.addWidget(sub)
        layout.addLayout(info)
        layout.addStretch()
        
        self.main_layout.addWidget(header)
        
    def _create_profile_card(self):
        card = SaaSCard(self)
        layout = card.internal_layout
        
        title = QLabel("Account Profile")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; background: transparent; border: none;")
        layout.addWidget(title)
        layout.addSpacing(8)
        
        student = crud.get_current_student()
        email_str = student.get("email", "Unknown") if student else "Not logged in"
        name_str = student.get("name", "Student") if student else "Guest User"
        display_name = student.get("display_name", name_str) if student else "Guest"
        
        # Profile Row
        prof_row = QHBoxLayout()
        prof_row.setSpacing(16)
        
        avatar = QLabel(name_str[0].upper())
        avatar.setFixedSize(56, 56)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38BDF8, stop:1 #0284C7);
            color: white; border-radius: 28px; font-weight: 900; font-size: 22px;
        """)
        
        info_v = QVBoxLayout()
        n_lbl = QLabel(display_name)
        n_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; background: transparent;")
        e_lbl = QLabel(email_str)
        e_lbl.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; background: transparent;")
        info_v.addWidget(n_lbl)
        info_v.addWidget(e_lbl)
        
        prof_row.addWidget(avatar)
        prof_row.addLayout(info_v)
        prof_row.addStretch()
        
        btn_edit = QPushButton("Edit Profile")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.setStyleSheet("""
            QPushButton { background: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 12px; font-weight: 600; font-size: 12px; }
            QPushButton:hover { background: #F8FAFC; }
        """)
        if self.controller and hasattr(self.controller, 'show_page'):
            btn_edit.clicked.connect(lambda: self.controller.show_page(1)) # Redirect to Profile
        prof_row.addWidget(btn_edit, alignment=Qt.AlignmentFlag.AlignTop)
        
        layout.addLayout(prof_row)
        return card

    def _create_preferences_card(self):
        card = SaaSCard(self)
        layout = card.internal_layout
        
        title = QLabel("UI & Preferences")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; background: transparent; border: none;")
        layout.addWidget(title)
        
        def add_toggle(text, subtext, default_state=True):
            row = QHBoxLayout()
            row.setContentsMargins(0, 8, 0, 8)
            v = QVBoxLayout()
            t = QLabel(text)
            t.setStyleSheet("font-size: 14px; font-weight: 600; color: #334155; background: transparent;")
            s = QLabel(subtext)
            s.setStyleSheet("font-size: 12px; color: #94A3B8; background: transparent;")
            v.addWidget(t)
            v.addWidget(s)
            
            toggle = ModernSwitch(active_color="#10B981") # Emerald Green
            toggle.set_checked(default_state)
            
            row.addLayout(v)
            row.addStretch()
            row.addWidget(toggle, alignment=Qt.AlignmentFlag.AlignVCenter)
            layout.addLayout(row)

        layout.addSpacing(8)
        add_toggle("Push Notifications", "Receive alerts for mock interview reminders.", True)
        add_toggle("Hardware Acceleration", "Use GPU to render Neumorphic shadows smoothly.", True)
        add_toggle("Compact Mode", "Reduce spacing and paddings in UI lists.", False)
        
        return card

    def _create_sync_card(self):
        card = SaaSCard(self)
        layout = card.internal_layout
        
        title = QLabel("System & Data Sync")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; background: transparent; border: none;")
        layout.addWidget(title)
        layout.addSpacing(12)
        
        desc = QLabel("VOR uses a Local-First architecture. Your AI plans and CVs are saved locally in SQLite and synchronized in the background to the cloud.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.5; background: transparent;")
        layout.addWidget(desc)
        
        layout.addSpacing(16)
        status_box = QFrame()
        status_box.setStyleSheet("background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px;")
        sb_layout = QHBoxLayout(status_box)
        sb_layout.setContentsMargins(16, 12, 16, 12)
        
        icon = QLabel("●")
        icon.setStyleSheet("color: #16A34A; font-size: 14px; background: transparent; border: none;")
        
        lbl = QLabel("Background Sync is Active")
        lbl.setStyleSheet("color: #16A34A; font-size: 13px; font-weight: 700; background: transparent; border: none;")
        
        sb_layout.addWidget(icon)
        sb_layout.addWidget(lbl)
        sb_layout.addStretch()
        
        layout.addWidget(status_box)
        return card

    def _create_danger_zone_card(self):
        card = SaaSCard(self)
        card.setStyleSheet(card.styleSheet() + " #SaaSCard { border: 1px solid #FECACA; }")
        layout = card.internal_layout
        
        title = QLabel("Danger Zone")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #DC2626; background: transparent; border: none;")
        layout.addWidget(title)
        layout.addSpacing(12)
        
        desc = QLabel("These actions cannot be undone. Please be certain before proceeding.")
        desc.setStyleSheet("color: #64748B; font-size: 13px; background: transparent;")
        layout.addWidget(desc)
        
        layout.addSpacing(16)
        
        # Clear Cache Button
        btn_clear = QPushButton("Clear Local Cache")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton { background: white; color: #DC2626; border: 1px solid #FECACA; border-radius: 6px; padding: 10px 16px; font-weight: 700; font-size: 13px; text-align: left; }
            QPushButton:hover { background: #FEF2F2; }
        """)
        
        # Logout Button
        btn_logout = QPushButton("Log Out of Session")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton { background: #EF4444; color: white; border: none; border-radius: 6px; padding: 10px 16px; font-weight: 700; font-size: 13px; text-align: left; }
            QPushButton:hover { background: #DC2626; }
        """)
        btn_logout.clicked.connect(self._handle_logout)
        
        layout.addWidget(btn_clear)
        layout.addWidget(btn_logout)
        
        return card

    def _handle_logout(self):
        if self.controller and hasattr(self.controller, 'logout'):
            self.controller.logout()
