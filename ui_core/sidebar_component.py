from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QButtonGroup, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QSize, QRect, QParallelAnimationGroup
from PyQt6.QtGui import QColor, QFont
from ui_core.animated_nav_button import AnimatedNavButton

class SidebarComponent(QFrame):
    navigation_requested = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.is_collapsed = False
        
        self.setStyleSheet("""
            SidebarComponent {
                background-color: #FFFFFF;
                border-right: 1px solid #E2E8F0;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 20, 16, 20)
        self.main_layout.setSpacing(8)
        
        self._setup_header()
        self._setup_nav()
        self.main_layout.addStretch()
        self._setup_footer()
        
    def _setup_header(self):
        self.header_container = QWidget()
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setContentsMargins(8, 0, 8, 12)
        self.header_layout.setSpacing(10)
        
        self.logo_label = QLabel("✦")
        self.logo_label.setStyleSheet("font-size: 20px; color: #38BDF8; font-weight: bold; border: none; background: transparent;")
        
        self.title_label = QLabel("AI-Career Bridge")
        self.title_label.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A; border: none; background: transparent; letter-spacing: -0.4px;")
        
        self.header_layout.addWidget(self.logo_label)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        
        self.main_layout.addWidget(self.header_container)
        

        
    def _setup_nav(self):
        self.nav_container = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(4)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        nav_items = [
            ("⌂", "Dashboard", 0),
            ("🗺", "Academic Roadmap", 4),
            ("🗓", "Study Tasks", 2),
            ("⚙", "Settings", 8),
        ]
        
        self.nav_buttons = []
        for icon, label, idx in nav_items:
            btn = AnimatedNavButton(icon, label)
            btn.clicked.connect(lambda ch, i=idx: self.navigation_requested.emit(i))
            self.button_group.addButton(btn, idx)
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            if idx == 0: btn.setChecked(True)
            
        self.main_layout.addWidget(self.nav_container)
        
    def _setup_footer(self):
        self.footer_container = QFrame()
        self.footer_container.setFixedHeight(64)
        self.footer_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
            QFrame:hover {
                background-color: #F8FAFC;
                border-radius: 12px;
            }
        """)
        self.footer_container.setCursor(Qt.CursorShape.PointingHandCursor)
        self.footer_container.mousePressEvent = lambda event: self.navigation_requested.emit(11)
        
        self.footer_layout = QHBoxLayout(self.footer_container)
        self.footer_layout.setContentsMargins(8, 8, 8, 8)
        self.footer_layout.setSpacing(12)
        
        self.avatar_label = QLabel("ST")
        self.avatar_label.setFixedSize(40, 40)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38BDF8, stop:1 #0284C7);
            color: white;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        """)
        
        self.user_info_container = QWidget()
        self.user_info_layout = QVBoxLayout(self.user_info_container)
        self.user_info_layout.setContentsMargins(0, 0, 0, 0)
        self.user_info_layout.setSpacing(2)
        
        self.user_name_label = QLabel("Student")
        self.user_name_label.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        
        self.user_role_label = QLabel("Undeclared Major")
        self.user_role_label.setStyleSheet("font-size: 12px; color: #64748B; border: none; background: transparent; font-weight: 500;")
        
        self.user_info_layout.addWidget(self.user_name_label)
        self.user_info_layout.addWidget(self.user_role_label)
        
        self.footer_layout.addWidget(self.avatar_label)
        self.footer_layout.addWidget(self.user_info_container)
        self.footer_layout.addStretch()
        
        self.main_layout.addWidget(self.footer_container)

    def toggle_collapse(self):
        new_width = 80 if not self.is_collapsed else 260
        self.is_collapsed = not self.is_collapsed
        
        # Width animation
        self.anim_group = QParallelAnimationGroup()
        
        width_anim = QPropertyAnimation(self, b"minimumWidth")
        width_anim.setDuration(300)
        width_anim.setStartValue(self.width())
        width_anim.setEndValue(new_width)
        width_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        width_anim_max = QPropertyAnimation(self, b"maximumWidth")
        width_anim_max.setDuration(300)
        width_anim_max.setStartValue(self.width())
        width_anim_max.setEndValue(new_width)
        width_anim_max.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        self.anim_group.addAnimation(width_anim)
        self.anim_group.addAnimation(width_anim_max)
        
        # Opacity animation for text elements to make it smoother
        # Skip complex opacity for now, just toggle visibility
        self.title_label.setVisible(not self.is_collapsed)
        self.user_info_container.setVisible(not self.is_collapsed)
        
        for btn in self.nav_buttons:
            btn.setCollapsed(self.is_collapsed)
            
        if self.is_collapsed:
            self.main_layout.setContentsMargins(10, 24, 10, 24)
            self.header_layout.setContentsMargins(0, 0, 0, 16)
            self.logo_label.setFixedSize(60, 30)
            self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.footer_layout.setContentsMargins(4, 8, 4, 8)
            self.avatar_label.setFixedSize(40, 40)
        else:
            self.main_layout.setContentsMargins(20, 24, 20, 24)
            self.header_layout.setContentsMargins(4, 0, 4, 16)
            self.logo_label.setFixedSize(28, 30)
            self.logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.footer_layout.setContentsMargins(8, 8, 8, 8)
            self.avatar_label.setFixedSize(40, 40)
            
        self.anim_group.start()

    def update_user_info(self, display_name, major):
        # Update user name
        self.user_name_label.setText(display_name or "Student")
        # Update major/role
        self.user_role_label.setText(major or "Undeclared Major")
        # Update avatar initials
        initials = ""
        if display_name:
            parts = display_name.split()
            if len(parts) > 1:
                initials = parts[0][0].upper() + parts[-1][0].upper()
            elif len(parts) == 1:
                initials = parts[0][:2].upper()
        if not initials:
            initials = "ST"
        self.avatar_label.setText(initials)
