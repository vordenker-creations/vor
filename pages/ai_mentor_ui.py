import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFont, QColor

def apply_shadow(widget, blur=15, offset=(0, 4), opacity=0.05):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(offset[0])
    shadow.setYOffset(offset[1])
    shadow.setColor(QColor(15, 23, 42, int(255 * opacity)))
    widget.setGraphicsEffect(shadow)
    return shadow

class ModernCard(QFrame):
    def __init__(self, parent=None, radius=20, bg_color="#FFFFFF", border_color="#E2E8F0"):
        super().__init__(parent)
        self.setStyleSheet(f"""
            ModernCard {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: {radius}px;
            }}
        """)
        apply_shadow(self)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(16)

class AIMentorPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("AIMentorPage")
        
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(32)

        # Header breadcrumbs
        header_layout = QHBoxLayout()
        lbl_breadcrumbs = QLabel("AI Mentor  /  <b>Conversation Coach</b>")
        lbl_breadcrumbs.setStyleSheet("color: #64748B; font-size: 14px; font-weight: 600;")
        header_layout.addWidget(lbl_breadcrumbs)
        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        # Body Layout
        body_layout = QVBoxLayout()
        body_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Premium placeholder card
        placeholder_card = ModernCard(radius=24)
        placeholder_card.setFixedWidth(550)
        
        pc_layout = placeholder_card.layout
        pc_layout.setSpacing(20)
        pc_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_lbl = QLabel("🤖")
        icon_lbl.setStyleSheet("font-size: 64px; background: transparent;")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pc_layout.addWidget(icon_lbl)
        
        title_lbl = QLabel("AI Conversation Coach")
        title_lbl.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800; letter-spacing: -0.5px;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pc_layout.addWidget(title_lbl)
        
        badge = QLabel("Coming Soon")
        badge.setStyleSheet("color: #8B5CF6; background: #8B5CF615; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 12px;")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pc_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignCenter)
        
        desc_lbl = QLabel(
            "The interactive conversational chat mentor is currently under development and will be available in a future phase.\n\n"
            "In the meantime, you can customize your profile context in the Profile tab and generate a comprehensive AI Academic Study Plan directly on your Dashboard."
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #475569; font-size: 14px; line-height: 1.6; text-align: center;")
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pc_layout.addWidget(desc_lbl)
        
        btn_dash = QPushButton("Go to Dashboard")
        btn_dash.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_dash.setFixedHeight(44)
        btn_dash.setFixedWidth(200)
        btn_dash.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 12px;
                font-weight: 700; font-size: 13px;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        btn_dash.clicked.connect(self._go_to_dashboard)
        pc_layout.addWidget(btn_dash, alignment=Qt.AlignmentFlag.AlignCenter)
        
        body_layout.addWidget(placeholder_card)
        content_layout.addLayout(body_layout)
        content_layout.addStretch()

    def _go_to_dashboard(self):
        main_win = self.window()
        if hasattr(main_win, "show_page"):
            main_win.show_page(0) # Switch back to Dashboard (index 0)
