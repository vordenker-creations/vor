from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGraphicsDropShadowEffect, 
                             QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen, QLinearGradient

class TemplateCard(QFrame):
    clicked = pyqtSignal(dict)
    use_template = pyqtSignal(dict)
    preview_requested = pyqtSignal(dict)

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.selected = False
        self.setMinimumWidth(240)
        self.setMaximumWidth(400)
        self.setMinimumHeight(380)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        self.setObjectName("TemplateCard")
        self.setStyleSheet("""
            QFrame#TemplateCard {
                background-color: #FFFFFF;
                border-radius: 22px;
                border: 1px solid #E2E8F0;
            }
            QFrame#TemplateCard[selected="true"] {
                border: 2px solid #38BDF8;
            }
        """)

        # Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(8)
        self.shadow.setColor(QColor(15, 23, 42, 18))
        self.setGraphicsEffect(self.shadow)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 16)
        self.main_layout.setSpacing(12)

        # 1. Preview Area
        self.preview_box = QFrame()
        self.preview_box.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 {self.data.get('color', '#F1F5F9')}, 
                stop:1 #FFFFFF);
            border-radius: 16px;
            border: 1px solid #F1F5F9;
        """)
        self.preview_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        preview_layout = QVBoxLayout(self.preview_box)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Badge Overlay (Simulated)
        if self.data.get('is_premium'):
            badge = QLabel("PREMIUM", self.preview_box)
            badge.setStyleSheet("""
                background: #0F172A; color: white; border-radius: 6px;
                font-size: 9px; font-weight: 800; padding: 4px 8px;
            """)
            badge.move(12, 12)

        self.main_layout.addWidget(self.preview_box)

        # 2. Info Area
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        title_row = QHBoxLayout()
        self.title_lbl = QLabel(self.data.get('name', 'Template Name'))
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; border: none;")
        title_row.addWidget(self.title_lbl)
        
        if self.data.get('is_ai_recommended'):
            ai_tag = QLabel("✨ AI")
            ai_tag.setStyleSheet("color: #8B5CF6; font-weight: 800; font-size: 10px;")
            title_row.addWidget(ai_tag)
        title_row.addStretch()
        info_layout.addLayout(title_row)

        sub_row = QHBoxLayout()
        self.category_lbl = QLabel(self.data.get('category', 'Modern'))
        self.category_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none;")
        
        ats_score = self.data.get('ats_score', 95)
        ats_lbl = QLabel(f"ATS: {ats_score}")
        color = "#10B981" if ats_score > 90 else "#F59E0B"
        ats_lbl.setStyleSheet(f"font-size: 11px; font-weight: 800; color: {color}; background: {color}15; padding: 2px 6px; border-radius: 4px;")
        
        sub_row.addWidget(self.category_lbl)
        sub_row.addStretch()
        sub_row.addWidget(ats_lbl)
        info_layout.addLayout(sub_row)

        self.main_layout.addLayout(info_layout)

        # 3. Actions (Visible on hover or selection)
        self.actions_widget = QWidget()
        self.actions_widget.setFixedHeight(40)
        self.actions_layout = QHBoxLayout(self.actions_widget)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(8)

        self.use_btn = QPushButton("Use Template")
        self.use_btn.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 10px;
                font-weight: 700; font-size: 11px; padding: 8px;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        self.use_btn.clicked.connect(lambda: self.use_template.emit(self.data))
        
        self.preview_btn = QPushButton("👁")
        self.preview_btn.setFixedSize(36, 36)
        self.preview_btn.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #E2E8F0; border-radius: 10px;
                color: #0F172A; font-weight: bold;
            }
            QPushButton:hover { background: #F8FAFC; }
        """)
        self.preview_btn.clicked.connect(lambda: self.preview_requested.emit(self.data))

        self.actions_layout.addWidget(self.use_btn, 1)
        self.actions_layout.addWidget(self.preview_btn)
        
        self.main_layout.addWidget(self.actions_widget)

    def setup_animations(self):
        # Hover Lift Animation
        self.lift_anim = QPropertyAnimation(self, b"pos")
        self.lift_anim.setDuration(200)
        self.lift_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        self.lift_anim.setStartValue(self.pos())
        self.lift_anim.setEndValue(self.pos() - QPoint(0, 6))
        self.lift_anim.start()
        self.shadow.setBlurRadius(35)
        self.shadow.setColor(QColor(15, 23, 42, 28))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.lift_anim.setStartValue(self.pos())
        self.lift_anim.setEndValue(self.pos() + QPoint(0, 6))
        self.lift_anim.start()
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(15, 23, 42, 18))
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.selected = selected
        self.setProperty("selected", str(selected).lower())
        self.style().unpolish(self)
        self.style().polish(self)
