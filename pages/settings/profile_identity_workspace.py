from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea, 
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
                             QGridLayout, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QFont, QCursor, QLinearGradient, QBrush, QPainter, QPen

class IdentityHero(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(300)
        self.setStyleSheet("background: transparent; border: none;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Banner
        self.banner = QFrame()
        self.banner.setFixedHeight(160)
        self.banner.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38BDF8, stop:1 #8B5CF6);
            border-top-left-radius: 22px;
            border-top-right-radius: 22px;
            border: none;
        """)
        layout.addWidget(self.banner)

        # 2. Hero Content Container
        self.content = QFrame()
        self.content.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-top: none; border-bottom-left-radius: 22px; border-bottom-right-radius: 22px;")
        cl = QHBoxLayout(self.content)
        cl.setContentsMargins(32, 0, 32, 32)
        cl.setSpacing(24)

        # Avatar (Overlapping banner)
        self.avatar_container = QWidget()
        self.avatar_container.setFixedSize(120, 120)
        
        self.avatar = QFrame(self)
        self.avatar.setFixedSize(120, 120)
        self.avatar.setStyleSheet("background: #E2E8F0; border: 4px solid white; border-radius: 60px;")
        self.avatar.move(32, 100) # Manual position to overlap
        
        avatar_shadow = QGraphicsDropShadowEffect()
        avatar_shadow.setBlurRadius(20); avatar_shadow.setColor(QColor(0,0,0,30)); avatar_shadow.setOffset(0,4)
        self.avatar.setGraphicsEffect(avatar_shadow)
        
        # Spacing for avatar
        cl.addSpacing(120)

        # Info
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.addSpacing(20)
        
        self.name_lbl = QLabel("John Doe")
        self.name_lbl.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        
        self.role_lbl = QLabel("Senior Machine Learning Engineer @ AI Global")
        self.role_lbl.setStyleSheet("font-size: 14px; font-weight: 500; color: #64748B; border: none; background: transparent;")
        
        info_v.addWidget(self.name_lbl)
        info_v.addWidget(self.role_lbl)
        cl.addLayout(info_v, 1)

        # Stats
        stats_h = QHBoxLayout()
        stats_h.setSpacing(32)
        
        def add_stat(val, label):
            v = QVBoxLayout(); v.setSpacing(2); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l1 = QLabel(val); l1.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
            l2 = QLabel(label); l2.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; border: none;")
            v.addWidget(l1); v.addWidget(l2); stats_h.addLayout(v)
            
        add_stat("92", "Branding")
        add_stat("85%", "Profile")
        cl.addLayout(stats_h)

        layout.addWidget(self.content)

class SocialCard(QFrame):
    def __init__(self, icon, name, status="Connected", parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QFrame {
                background: white; border: 1px solid #E2E8F0; border-radius: 16px;
            }
            QFrame:hover { border-color: #38BDF8; background: #F8FAFC; }
        """)
        l = QHBoxLayout(self)
        l.setContentsMargins(16, 0, 16, 0)
        l.setSpacing(12)
        
        ico = QLabel(icon); ico.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        
        info = QVBoxLayout(); info.setSpacing(2); info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        t = QLabel(name); t.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none; background: transparent;")
        s = QLabel(status); s.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {'#10B981' if status=='Connected' else '#64748B'}; border: none; background: transparent;")
        info.addWidget(t); info.addWidget(s)
        
        l.addWidget(ico); l.addLayout(info, 1)
        
        btn = QPushButton("Manage")
        btn.setStyleSheet("background: #F1F5F9; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 6px 12px; color: #475569;")
        l.addWidget(btn)

class ProfileIdentityWorkspace(QWidget):
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

        # 1. Hero
        cl.addWidget(IdentityHero())

        # 2. General Information
        info_sec = QFrame()
        info_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        il = QVBoxLayout(info_sec); il.setContentsMargins(24, 24, 24, 24); il.setSpacing(20)
        
        il.addWidget(QLabel("General Information", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        form_grid = QGridLayout(); form_grid.setSpacing(20)
        
        def add_field(label, widget, r, c):
            v = QVBoxLayout(); v.setSpacing(8)
            lbl = QLabel(label); lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #475569; border: none;")
            widget.setFixedHeight(44)
            widget.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 0 12px; font-size: 13px;")
            v.addWidget(lbl); v.addWidget(widget); form_grid.addLayout(v, r, c)
            
        add_field("Full Name", QLineEdit("John Doe"), 0, 0)
        add_field("Headline", QLineEdit("Senior Machine Learning Engineer @ AI Global"), 0, 1)
        add_field("Organization", QLineEdit("AI Global Corp"), 1, 0)
        add_field("Location", QLineEdit("San Francisco, CA"), 1, 1)
        
        il.addLayout(form_grid)
        
        # Bio
        bio_v = QVBoxLayout(); bio_v.setSpacing(8)
        bio_h = QHBoxLayout()
        bio_h.addWidget(QLabel("Biography", styleSheet="font-size: 13px; font-weight: 600; color: #475569; border: none;"))
        bio_h.addStretch()
        btn_ai_bio = QPushButton("✨ AI Enhance")
        btn_ai_bio.setStyleSheet("background: #E0F2FE; color: #0284C7; border: none; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 4px 10px;")
        bio_h.addWidget(btn_ai_bio)
        bio_v.addLayout(bio_h)
        
        self.bio_edit = QTextEdit()
        self.bio_edit.setPlaceholderText("Tell your professional story...")
        self.bio_edit.setMinimumHeight(120)
        self.bio_edit.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px; font-size: 13px; line-height: 1.5;")
        bio_v.addWidget(self.bio_edit)
        il.addLayout(bio_v)
        
        cl.addWidget(info_sec)

        # 3. Career Identity
        career_sec = QFrame()
        career_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        cl2 = QVBoxLayout(career_sec); cl2.setContentsMargins(24, 24, 24, 24); cl2.setSpacing(20)
        cl2.addWidget(QLabel("Career Identity", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        career_grid = QGridLayout(); career_grid.setSpacing(20)
        
        cb_role = QComboBox(); cb_role.addItems(["Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer"])
        add_field("Desired Career Path", cb_role, 0, 0)
        
        cb_level = QComboBox(); cb_level.addItems(["Junior", "Mid-Level", "Senior", "Lead", "Architect"])
        add_field("Experience Level", cb_level, 0, 1)
        
        le_skills = QLineEdit(); le_skills.setPlaceholderText("e.g. Python, React, Cloud Architecture")
        add_field("Skill Highlights", le_skills, 1, 0)
        
        cb_alignment = QComboBox(); cb_alignment.addItems(["Full-Time", "Contract", "Freelance", "Remote Only"])
        add_field("Work Preference", cb_alignment, 1, 1)
        
        cl2.addLayout(career_grid)
        cl.addWidget(career_sec)

        # 4. Social Presence
        social_sec = QWidget()
        sl = QVBoxLayout(social_sec); sl.setContentsMargins(0, 0, 0, 0); sl.setSpacing(16)
        sl.addWidget(QLabel("Social Presence", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        social_grid = QGridLayout(); social_grid.setSpacing(16)
        social_grid.addWidget(SocialCard("💻", "GitHub", "Connected"), 0, 0)
        social_grid.addWidget(SocialCard("💼", "LinkedIn", "Connected"), 0, 1)
        social_grid.addWidget(SocialCard("🎨", "Dribbble", "Not Linked"), 1, 0)
        social_grid.addWidget(SocialCard("🌐", "Personal Website", "Not Linked"), 1, 1)
        
        sl.addLayout(social_grid)
        cl.addWidget(social_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
