from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QPoint, QParallelAnimationGroup
from PyQt6.QtGui import QColor, QIcon, QFont
from ui_core.tooltip_widget import ModernTooltip

class AnimatedNavButton(QPushButton):
    def __init__(self, icon_text, label_text, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.icon_text = icon_text
        self.label_text = label_text
        self.is_collapsed = False
        
        # Opacity Effects
        self.icon_opacity = QGraphicsOpacityEffect(self)
        self.text_opacity = QGraphicsOpacityEffect(self)
        
        # Layout
        self.content_layout = QHBoxLayout(self)
        self.content_layout.setContentsMargins(12, 0, 12, 0)
        self.content_layout.setSpacing(10)
        
        # Icon Label (Visible only in collapsed mode)
        self.icon_label = QLabel(icon_text)
        self.icon_label.setGraphicsEffect(self.icon_opacity)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 18px; color: #64748B; border: none; background: transparent;")
        
        # Text Label (Visible only in expanded mode)
        self.text_label = QLabel(label_text)
        self.text_label.setGraphicsEffect(self.text_opacity)
        self.text_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #64748B; border: none; background: transparent;")
        
        # Indicator bar (active state)
        self.indicator = QWidget(self)
        self.indicator.setFixedWidth(3)
        self.indicator.setFixedHeight(20)
        self.indicator.setStyleSheet("background-color: #38BDF8; border-radius: 1.5px;")
        self.indicator.move(0, 12)
        self.indicator.hide()
        
        self.content_layout.addWidget(self.icon_label)
        self.content_layout.addWidget(self.text_label)
        self.content_layout.addStretch()
        
        # Initial State: Expanded (Text only)
        self.icon_label.hide()
        self.icon_opacity.setOpacity(0.0)
        self.text_opacity.setOpacity(1.0)
        
        self.update_style()
        
        # Tooltip for collapsed state
        self.tooltip = None

    def update_theme(self, is_dark):
        self.is_dark = is_dark
        self.update_style()

    def update_style(self, hovered=False):
        is_dark = getattr(self, "is_dark", False)
        
        if is_dark:
            active_bg = "#1E293B" if self.isChecked() else ("#334155" if hovered else "transparent")
            active_color = "#38BDF8" if self.isChecked() else ("#F8FAFC" if hovered else "#94A3B8")
        else:
            active_bg = "#F0F9FF" if self.isChecked() else ("#F1F5F9" if hovered else "transparent")
            active_color = "#0284C7" if self.isChecked() else ("#334155" if hovered else "#64748B")
            
        font_weight = "600" if self.isChecked() else "500"
        
        self.setStyleSheet(f"""
            AnimatedNavButton {{
                background-color: {active_bg};
                border-radius: 14px;
                border: none;
            }}
        """)
        self.text_label.setStyleSheet(f"font-size: 14px; font-weight: {font_weight}; color: {active_color}; border: none; background: transparent;")
        self.icon_label.setStyleSheet(f"font-size: 18px; color: {active_color}; border: none; background: transparent;")

    def setChecked(self, checked):
        super().setChecked(checked)
        self.update_style()
        if checked:
            self.indicator.show()
        else:
            self.indicator.hide()

    def setCollapsed(self, collapsed):
        if self.is_collapsed == collapsed:
            return
            
        self.is_collapsed = collapsed
        
        # Animations
        self.anim_group = QParallelAnimationGroup()
        
        if collapsed:
            # Hide text, show icon
            self.icon_label.show()
            
            icon_fade = QPropertyAnimation(self.icon_opacity, b"opacity")
            icon_fade.setDuration(250)
            icon_fade.setStartValue(0.0)
            icon_fade.setEndValue(1.0)
            icon_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            text_fade = QPropertyAnimation(self.text_opacity, b"opacity")
            text_fade.setDuration(200)
            text_fade.setStartValue(1.0)
            text_fade.setEndValue(0.0)
            text_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
            text_fade.finished.connect(self.text_label.hide)
            
            self.anim_group.addAnimation(icon_fade)
            self.anim_group.addAnimation(text_fade)
            
            self.content_layout.setContentsMargins(0, 0, 0, 0)
            self.content_layout.setSpacing(0)
            self.icon_label.setFixedSize(64, 44) # Match collapsed sidebar width
        else:
            # Hide icon, show text
            self.text_label.show()
            
            icon_fade = QPropertyAnimation(self.icon_opacity, b"opacity")
            icon_fade.setDuration(200)
            icon_fade.setStartValue(1.0)
            icon_fade.setEndValue(0.0)
            icon_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
            icon_fade.finished.connect(self.icon_label.hide)
            
            text_fade = QPropertyAnimation(self.text_opacity, b"opacity")
            text_fade.setDuration(250)
            text_fade.setStartValue(0.0)
            text_fade.setEndValue(1.0)
            text_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            self.anim_group.addAnimation(icon_fade)
            self.anim_group.addAnimation(text_fade)
            
            self.content_layout.setContentsMargins(12, 0, 12, 0)
            self.content_layout.setSpacing(10)
            self.icon_label.setFixedSize(0, 44) # Remove icon space but keep height for layout
            
        self.anim_group.start()

    def enterEvent(self, event):
        self.update_style(hovered=True)
        if self.is_collapsed:
            if not self.tooltip:
                self.tooltip = ModernTooltip(self.label_text, self.window())
            
            button_pos = self.mapToGlobal(self.rect().topRight())
            self.tooltip.show_at(button_pos + QPoint(10, 0))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_style(hovered=False)
        if self.tooltip:
            self.tooltip.hide_tooltip()
        super().leaveEvent(event)
