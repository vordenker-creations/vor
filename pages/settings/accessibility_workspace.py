from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QSlider, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QCursor
from .common_widgets import ToggleRow

class AccessibilityHeroMetric(QFrame):
    def __init__(self, title, value, status="Optimized", color="#38BDF8", parent=None):
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

class ReadabilityPreview(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.setStyleSheet("""
            QFrame {
                background: #F8FAFC;
                border: 1px dashed #CBD5E1;
                border-radius: 16px;
            }
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        
        self.title = QLabel("Interface Readability Preview")
        self.title.setStyleSheet("font-weight: 800; font-size: 16px; color: #0F172A; border: none;")
        l.addWidget(self.title)
        
        self.content = QLabel("The quick brown fox jumps over the lazy dog. This text adapts in realtime to your accessibility preferences. High readability and inclusive design are core to our productivity platform.")
        self.content.setWordWrap(True)
        self.content.setStyleSheet("color: #475569; font-size: 14px; line-height: 1.6; border: none;")
        l.addWidget(self.content)
        l.addStretch()

    def update_scaling(self, size, spacing):
        self.content.setStyleSheet(f"color: #475569; font-size: {size}px; line-height: {spacing}%; border: none;")

class AccessibilityWorkspace(QWidget):
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
        tag = QLabel("✨ INCLUSIVE EXPERIENCE")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("Accessibility Center")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your workspace comfort score is <b>Elite</b>. AI has verified that your interface contrast and motion settings meet WCAG AAA standards.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        grid = QGridLayout(); grid.setSpacing(12)
        grid.addWidget(AccessibilityHeroMetric("Comfort", "98/100", "High", "#10B981"), 0, 0)
        grid.addWidget(AccessibilityHeroMetric("Motion", "Stable", "Reduced", "#38BDF8"), 0, 1)
        grid.addWidget(AccessibilityHeroMetric("Reading", "Perfect", "Optimized", "#10B981"), 1, 0)
        grid.addWidget(AccessibilityHeroMetric("Focus", "Visible", "Strong", "#8B5CF6"), 1, 1)
        hl.addLayout(grid)
        cl.addWidget(hero)

        # 2. Readability Studio
        read_card = QFrame()
        read_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        rl = QVBoxLayout(read_card); rl.setContentsMargins(24, 24, 24, 24); rl.setSpacing(24)
        rl.addWidget(QLabel("Readability & Typography", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        self.preview = ReadabilityPreview()
        rl.addWidget(self.preview)
        
        controls = QGridLayout(); controls.setSpacing(20)
        
        def add_control(label, min_v, max_v, current_v, suffix, r, c, callback):
            v = QVBoxLayout(); v.setSpacing(8)
            hl = QHBoxLayout()
            hl.addWidget(QLabel(label, styleSheet="font-size: 13px; font-weight: 600; color: #475569; border: none;"))
            hl.addStretch()
            val_lbl = QLabel(f"{current_v}{suffix}", styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;")
            hl.addWidget(val_lbl)
            v.addLayout(hl)
            s = QSlider(Qt.Orientation.Horizontal)
            s.setRange(min_v, max_v); s.setValue(current_v)
            s.setStyleSheet("QSlider::groove:horizontal { height: 4px; background: #F1F5F9; border-radius: 2px; } QSlider::handle:horizontal { background: #38BDF8; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }")
            s.valueChanged.connect(lambda v: val_lbl.setText(f"{v}{suffix}"))
            s.valueChanged.connect(callback)
            v.addWidget(s); controls.addLayout(v, r, c)
            
        add_control("Base Font Size", 8, 24, 14, "px", 0, 0, lambda v: self.preview.update_scaling(v, 160))
        add_control("Line Spacing", 100, 250, 160, "%", 0, 1, lambda v: self.preview.update_scaling(14, v))
        rl.addLayout(controls)
        cl.addWidget(read_card)

        # 3. Behavior Section
        behav_card = QFrame()
        behav_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        bl = QVBoxLayout(behav_card); bl.setContentsMargins(24, 24, 24, 24); bl.setSpacing(20)
        bl.addWidget(QLabel("Motion & Navigation", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        bl.addWidget(ToggleRow("Reduce Motion", "Minimize animations and transition effects throughout the workspace."))
        bl.addWidget(ToggleRow("Strong Focus Ring", "Enhance visibility of the active element during keyboard navigation."))
        bl.addWidget(ToggleRow("High Contrast Mode", "Adaptive interface contrast for maximum visibility and clarity."))
        bl.addWidget(ToggleRow("Screen Reader Optimized", "Enable semantic labels and optimized navigation flow for screen readers."))
        
        cl.addWidget(behav_card)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
