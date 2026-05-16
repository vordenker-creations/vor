from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QCursor
from .common_widgets import ToggleRow

class SecurityHeroMetric(QFrame):
    def __init__(self, title, value, status="Protected", color="#10B981", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }}
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(6)
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 10px; font-weight: 800; color: #94A3B8; text-transform: uppercase; border: none; background: transparent;")
        
        v = QLabel(value)
        v.setStyleSheet(f"font-size: 20px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        
        s = QLabel(status)
        s.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {color}15; padding: 2px 8px; border-radius: 6px; border: none;")
        s.setFixedWidth(s.sizeHint().width() + 16)
        
        l.addWidget(t)
        l.addWidget(v)
        l.addWidget(s)

class SessionCard(QFrame):
    def __init__(self, device, location, time, is_current=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setStyleSheet(f"""
            QFrame {{
                background: {'#F0F9FF' if is_current else 'white'};
                border: 1px solid {'#38BDF8' if is_current else '#E2E8F0'};
                border-radius: 16px;
            }}
            QFrame:hover {{ border-color: #38BDF8; }}
        """)
        l = QHBoxLayout(self)
        l.setContentsMargins(16, 0, 16, 0)
        l.setSpacing(12)
        
        ico = QLabel("💻" if "Windows" in device or "Mac" in device else "📱")
        ico.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        
        info = QVBoxLayout(); info.setSpacing(2); info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        t = QLabel(f"{device} {'(Current)' if is_current else ''}")
        t.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none; background: transparent;")
        d = QLabel(f"{location} • {time}")
        d.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        info.addWidget(t); info.addWidget(d)
        
        l.addWidget(ico); l.addLayout(info, 1)
        
        if not is_current:
            btn = QPushButton("Revoke")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: #FEF2F2; color: #EF4444; border: 1px solid #FECACA;
                    border-radius: 8px; font-size: 11px; font-weight: 700; padding: 6px 12px;
                }
                QPushButton:hover { background: #FEE2E2; }
            """)
            l.addWidget(btn)

class PrivacySecurityWorkspace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(32)

        # 1. Hero Analytics
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(24)
        
        info = QVBoxLayout(); info.setSpacing(8)
        tag = QLabel("🛡️ ACCOUNT PROTECTION")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #10B981; letter-spacing: 1px;")
        title = QLabel("Security Command Center")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your account security score is <b>94/100</b>. Two-factor authentication is active, and no suspicious sessions were detected.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        grid = QGridLayout(); grid.setSpacing(12)
        grid.addWidget(SecurityHeroMetric("Security", "94%", "Elite", "#10B981"), 0, 0)
        grid.addWidget(SecurityHeroMetric("Privacy", "Strong", "Verified", "#38BDF8"), 0, 1)
        grid.addWidget(SecurityHeroMetric("Threats", "None", "Safe", "#10B981"), 1, 0)
        grid.addWidget(SecurityHeroMetric("Trust", "Level 4", "Maximum", "#8B5CF6"), 1, 1)
        hl.addLayout(grid)
        cl.addWidget(hero)

        # 2. Account Security
        acc_sec = QFrame()
        acc_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        al = QVBoxLayout(acc_sec); al.setContentsMargins(24, 24, 24, 24); al.setSpacing(20)
        al.addWidget(QLabel("Authentication & Access", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        al.addWidget(ToggleRow("Two-Factor Authentication", "Secure your account with an additional verification layer."))
        al.addWidget(ToggleRow("Biometric Unlock", "Use Windows Hello or Touch ID for faster, secure access."))
        
        pwd_h = QHBoxLayout()
        pwd_info = QVBoxLayout(); pwd_info.setSpacing(2)
        pwd_info.addWidget(QLabel("Account Password", styleSheet="font-weight: 600; font-size: 13px; color: #1E293B;"))
        pwd_info.addWidget(QLabel("Last changed 3 months ago. We recommend updating every 6 months.", styleSheet="font-size: 12px; color: #64748B;"))
        pwd_h.addLayout(pwd_info)
        pwd_h.addStretch()
        btn_pwd = QPushButton("Change Password")
        btn_pwd.setStyleSheet("background: #F1F5F9; border-radius: 8px; font-size: 12px; font-weight: 700; padding: 8px 16px; color: #0F172A;")
        pwd_h.addWidget(btn_pwd)
        al.addLayout(pwd_h)
        
        cl.addWidget(acc_sec)

        # 3. Active Sessions
        session_sec = QWidget()
        sl = QVBoxLayout(session_sec); sl.setContentsMargins(0, 0, 0, 0); sl.setSpacing(16)
        sl.addWidget(QLabel("Active Sessions & Devices", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        session_grid = QGridLayout(); session_grid.setSpacing(16)
        session_grid.addWidget(SessionCard("Windows 11 • Desktop App", "San Francisco, US", "Active Now", True), 0, 0)
        session_grid.addWidget(SessionCard("iPhone 15 • Mobile App", "San Francisco, US", "2h ago"), 0, 1)
        session_grid.addWidget(SessionCard("MacBook Pro • Chrome", "London, UK", "Yesterday"), 1, 0)
        sl.addLayout(session_grid)
        cl.addWidget(session_sec)

        # 4. Privacy Permissions
        priv_sec = QFrame()
        priv_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        pl = QVBoxLayout(priv_sec); pl.setContentsMargins(24, 24, 24, 24); pl.setSpacing(20)
        pl.addWidget(QLabel("Privacy & AI Data Permissions", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        pl.addWidget(ToggleRow("Profile Discoverability", "Allow recruiters to find your profile in search results."))
        pl.addWidget(ToggleRow("AI Learning Participation", "Contribute anonymized data to improve career coaching models."))
        pl.addWidget(ToggleRow("Activity Visibility", "Show your current learning progress to community members."))
        
        cl.addWidget(priv_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
