import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, 
                             QComboBox, QTextEdit, QLineEdit, QGraphicsDropShadowEffect,
                             QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QSize, QRectF
from PyQt6.QtGui import QCursor, QColor, QLinearGradient, QPainter, QBrush, QFont, QPixmap
from config import *
from i18n import _

# Design Constants based on requirements
COLOR_BG = "#F8FAFC"
COLOR_CARD = "#FFFFFF"
COLOR_BORDER = "#E2E8F0"
COLOR_PRIMARY = "#38BDF8"
COLOR_SECONDARY = "#2DD4BF"
COLOR_TEXT_PRIMARY = "#0F172A"
COLOR_TEXT_SECONDARY = "#64748B"
SPACING = 8
MARGINS = 24

class ModernCard(QFrame):
    """Base card widget with modern styling and smooth hover effects."""
    def __init__(self, parent=None, radius=20, padding=16):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_CARD};
                border: 1px solid {COLOR_BORDER};
                border-radius: {radius}px;
            }}
        """)
        
        # Soft Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(8)
        self.shadow.setColor(QColor(18, 55, 105, 20))
        self.setGraphicsEffect(self.shadow)
        
        # Animations
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        self.anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.offset_anim = QPropertyAnimation(self.shadow, b"yOffset")
        self.offset_anim.setDuration(300)
        self.offset_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(padding, padding, padding, padding)
        self.layout.setSpacing(SPACING * 2)

    def enterEvent(self, event):
        self.anim.setEndValue(35)
        self.offset_anim.setEndValue(8)
        self.anim.start()
        self.offset_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.setEndValue(20)
        self.offset_anim.setEndValue(4)
        self.anim.start()
        self.offset_anim.start()
        super().leaveEvent(event)

class Avatar(QLabel):
    """Circular avatar placeholder."""
    def __init__(self, size=40, color="#E2E8F0", text=""):
        super().__init__()
        self.setFixedSize(size, size)
        self.color = color
        self.text = text
        self.setStyleSheet(f"background: transparent; border: none;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        
        if self.text:
            painter.setPen(QColor(COLOR_TEXT_SECONDARY))
            font = QFont("Inter", 10, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text)

class GroupItem(QPushButton):
    """Sidebar group item."""
    def __init__(self, name, members, icon="📁", badge=0):
        super().__init__()
        self.setFixedHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #F1F5F9;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(12)
        
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon_lbl)
        
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: 600; font-size: 14px;")
        text_layout.addWidget(name_lbl)
        
        meta_lbl = QLabel(f"● {members} online")
        meta_lbl.setStyleSheet(f"color: {COLOR_SECONDARY}; font-size: 12px; font-weight: 500;")
        text_layout.addWidget(meta_lbl)
        
        layout.addWidget(text_container)
        layout.addStretch()
        
        if badge > 0:
            badge_lbl = QLabel(str(badge))
            badge_lbl.setFixedSize(20, 20)
            badge_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge_lbl.setStyleSheet(f"""
                background-color: {COLOR_PRIMARY};
                color: white;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            """)
            layout.addWidget(badge_lbl)

class PostCard(ModernCard):
    """Feed post card."""
    def __init__(self, user, role, time, content):
        super().__init__(radius=20, padding=20)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(12)
        
        header.addWidget(Avatar(size=44, color="#F1F5F9", text=user[0]))
        
        info = QVBoxLayout()
        info.setSpacing(2)
        
        name_row = QHBoxLayout()
        name_row.setSpacing(8)
        name_lbl = QLabel(user)
        name_lbl.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-weight: 700; font-size: 15px;")
        name_row.addWidget(name_lbl)
        
        role_badge = QLabel(role)
        role_badge.setStyleSheet(f"""
            background-color: #F1F5F9;
            color: {COLOR_TEXT_SECONDARY};
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
        """)
        name_row.addWidget(role_badge)
        name_row.addStretch()
        
        info.addLayout(name_row)
        
        time_lbl = QLabel(time)
        time_lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px;")
        info.addWidget(time_lbl)
        
        header.addLayout(info)
        self.layout.addLayout(header)
        
        # Content
        text = QLabel(content)
        text.setWordWrap(True)
        text.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 14px; line-height: 1.5;")
        self.layout.addWidget(text)
        
        # Actions
        actions = QHBoxLayout()
        actions.setSpacing(16)
        
        for icon, label in [("❤️", "Like"), ("💬", "Comment"), ("🔗", "Share")]:
            btn = QPushButton(f"{icon} {label}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLOR_TEXT_SECONDARY};
                    border: none;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    color: {COLOR_PRIMARY};
                }}
            """)
            actions.addWidget(btn)
        actions.addStretch()
        self.layout.addLayout(actions)

class CommunityPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("CommunityPage")
        self.setStyleSheet(f"background-color: {COLOR_BG};")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_top_header()
        
        # Central Area
        central_container = QWidget()
        self.central_layout = QHBoxLayout(central_container)
        self.central_layout.setContentsMargins(MARGINS, MARGINS, MARGINS, MARGINS)
        self.central_layout.setSpacing(MARGINS)
        
        self._setup_sidebar()
        self._setup_main_feed()
        self._setup_insights()
        
        self.main_layout.addWidget(central_container)

    def _setup_top_header(self):
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet(f"background-color: {COLOR_CARD}; border-bottom: 1px solid {COLOR_BORDER};")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(MARGINS, 0, MARGINS, 0)
        
        title = QLabel(_("Community Workspace"))
        title.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 20px; font-weight: 800; letter-spacing: -0.5px;")
        h_layout.addWidget(title)
        
        h_layout.addStretch()
        
        # Search Bar
        search = QLineEdit()
        search.setPlaceholderText(_("Search communities..."))
        search.setFixedWidth(300)
        search.setStyleSheet(f"""
            QLineEdit {{
                background-color: #F1F5F9;
                border: 1px solid {COLOR_BORDER};
                border-radius: 10px;
                padding: 8px 15px;
                color: {COLOR_TEXT_PRIMARY};
            }}
        """)
        h_layout.addWidget(search)
        
        self.main_layout.addWidget(header)

    def _setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING)
        
        lbl = QLabel(_("MY COMMUNITIES"))
        lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-weight: 800; font-size: 11px; letter-spacing: 1px; margin-bottom: 8px;")
        layout.addWidget(lbl)
        
        groups = [
            ("AI Engineers", "1.2k", "🤖", 3),
            ("Full-Stack Devs", "850", "💻", 0),
            ("UI/UX Designers", "420", "🎨", 12),
            ("Cloud Architects", "310", "☁️", 0),
            ("Data Science Hub", "2.1k", "📊", 5)
        ]
        
        for name, m, icon, badge in groups:
            layout.addWidget(GroupItem(name, m, icon, badge))
        
        layout.addStretch()
        
        # Create Community Button
        btn_create = QPushButton(_("+ Create New Group"))
        btn_create.setFixedHeight(44)
        btn_create.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_create.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {COLOR_PRIMARY};
                border: 2px dashed {COLOR_PRIMARY};
                border-radius: 12px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: #F0F9FF;
            }}
        """)
        layout.addWidget(btn_create)
        
        self.central_layout.addWidget(sidebar)

    def _setup_main_feed(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        # Custom ScrollBar Styling
        scroll.verticalScrollBar().setStyleSheet(f"""
            QScrollBar:vertical {{ border: none; background: transparent; width: 8px; }}
            QScrollBar::handle:vertical {{ background: #CBD5E1; border-radius: 4px; min-height: 20px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ border: none; background: none; }}
        """)
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Community Banner
        banner = QFrame()
        banner.setFixedHeight(160)
        banner.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_PRIMARY}, stop:1 {COLOR_SECONDARY});
                border-radius: 22px;
            }}
        """)
        b_layout = QVBoxLayout(banner)
        b_layout.setContentsMargins(32, 32, 32, 32)
        
        b_title = QLabel("AI Engineers Collective")
        b_title.setStyleSheet("color: white; font-size: 28px; font-weight: 800; letter-spacing: -1px;")
        b_layout.addWidget(b_title)
        
        b_stats = QLabel("12,402 Members  •  1,209 Online  •  32 Active Discussions")
        b_stats.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 14px; font-weight: 500;")
        b_layout.addWidget(b_stats)
        
        layout.addWidget(banner)
        
        # Create Post Area
        create_post = ModernCard(radius=20, padding=20)
        cp_layout = QHBoxLayout()
        cp_layout.setSpacing(16)
        cp_layout.addWidget(Avatar(size=44, color="#F1F5F9", text="ME"))
        
        cp_input = QPushButton(_("Share something with the community..."))
        cp_input.setStyleSheet(f"""
            QPushButton {{
                background-color: #F8FAFC;
                border: 1px solid {COLOR_BORDER};
                border-radius: 22px;
                color: {COLOR_TEXT_SECONDARY};
                text-align: left;
                padding-left: 20px;
                height: 44px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #F1F5F9;
            }}
        """)
        cp_layout.addWidget(cp_input)
        
        create_post.layout.addLayout(cp_layout)
        
        cp_actions = QHBoxLayout()
        cp_actions.setContentsMargins(60, 0, 0, 0)
        for icon, label in [("📄", "File"), ("📊", "Poll"), ("💻", "Code")]:
            btn = QPushButton(f"{icon} {label}")
            btn.setStyleSheet(f"background: transparent; border: none; color: {COLOR_TEXT_SECONDARY}; font-weight: 600; padding: 5px 10px;")
            cp_actions.addWidget(btn)
        cp_actions.addStretch()
        create_post.layout.addLayout(cp_actions)
        layout.addWidget(create_post)
        
        # Post Cards
        posts = [
            ("Alex Rivera", "Senior ML Engineer", "2 hours ago", 
             "Just published a new guide on optimizing Transformer inference using TensorRT. Check it out in the documents tab! 🔥"),
            ("Sarah Chen", "Full-Stack Developer", "5 hours ago",
             "Looking for collaborators for an open-source AI-powered note-taking app. Tech stack: Next.js, FastAPI, and Pinecone."),
            ("Marcus Thorne", "UI Designer", "Yesterday",
             "What are your thoughts on the new design trends in AI interfaces? I'm seeing a lot of glassmorphism returning.")
        ]
        
        for user, role, time, content in posts:
            layout.addWidget(PostCard(user, role, time, content))
        
        layout.addStretch()
        scroll.setWidget(container)
        self.central_layout.addWidget(scroll)

    def _setup_insights(self):
        insights = QWidget()
        insights.setFixedWidth(320)
        layout = QVBoxLayout(insights)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # AI Recommendations
        rec_card = ModernCard(radius=20, padding=20)
        rec_card.layout.addWidget(QLabel("AI RECOMMENDATIONS", styleSheet=f"color: {COLOR_TEXT_SECONDARY}; font-weight: 800; font-size: 11px; letter-spacing: 1px;"))
        
        for name, reason in [("Dr. Emily Watson", "Matches your interest in NLP"), ("Project 'Aurora'", "Trending in your tech stack")]:
            item = QWidget()
            il = QHBoxLayout(item); il.setContentsMargins(0,0,0,0)
            avatar = Avatar(size=32, color="#F1F5F9", text=name[0])
            il.addWidget(avatar)
            text_l = QVBoxLayout(); text_l.setSpacing(2)
            n_lbl = QLabel(name); n_lbl.setStyleSheet(f"font-weight: 600; color: {COLOR_TEXT_PRIMARY}; font-size: 13px;")
            r_lbl = QLabel(reason); r_lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 11px;")
            text_l.addWidget(n_lbl); text_l.addWidget(r_lbl)
            il.addLayout(text_l)
            il.addStretch()
            btn_plus = QPushButton("+")
            btn_plus.setFixedSize(24, 24)
            btn_plus.setStyleSheet(f"border: 1px solid {COLOR_BORDER}; border-radius: 12px; color: {COLOR_TEXT_PRIMARY};")
            il.addWidget(btn_plus)
            rec_card.layout.addWidget(item)
        
        layout.addWidget(rec_card)
        
        # Upcoming Events
        event_card = ModernCard(radius=20, padding=20)
        event_card.layout.addWidget(QLabel("UPCOMING EVENTS", styleSheet=f"color: {COLOR_TEXT_SECONDARY}; font-weight: 800; font-size: 11px; letter-spacing: 1px;"))
        
        events = [
            ("Deep Learning Workshop", "Tomorrow, 10:00 AM", "📅"),
            ("Networking Mixer", "Fri, 6:00 PM", "🤝")
        ]
        for title, time, icon in events:
            ev = QWidget(); evl = QHBoxLayout(ev); evl.setContentsMargins(0,0,0,0)
            evl.addWidget(QLabel(icon))
            det = QVBoxLayout(); det.setSpacing(2)
            det.addWidget(QLabel(title, styleSheet=f"font-weight: 600; font-size: 13px; color: {COLOR_TEXT_PRIMARY};"))
            det.addWidget(QLabel(time, styleSheet=f"color: {COLOR_TEXT_SECONDARY}; font-size: 11px;"))
            evl.addLayout(det)
            event_card.layout.addWidget(ev)
            
        layout.addWidget(event_card)
        
        # Active Members
        active_card = ModernCard(radius=20, padding=20)
        active_card.layout.addWidget(QLabel("ACTIVE MEMBERS", styleSheet=f"color: {COLOR_TEXT_SECONDARY}; font-weight: 800; font-size: 11px; letter-spacing: 1px;"))
        
        members_row = QHBoxLayout()
        members_row.setSpacing(-10) # Overlapping avatars
        for i in range(5):
            members_row.addWidget(Avatar(size=36, color=["#38BDF8", "#2DD4BF", "#F472B6", "#FB923C", "#A78BFA"][i], text=chr(65+i)))
        members_row.addStretch()
        active_card.layout.addLayout(members_row)
        active_label = QLabel("+ 1,204 others currently active")
        active_label.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px; font-weight: 500;")
        active_card.layout.addWidget(active_label)
        
        layout.addWidget(active_card)
        layout.addStretch()
        
        self.central_layout.addWidget(insights)
