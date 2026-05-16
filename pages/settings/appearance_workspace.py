from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QSlider, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QCursor, QLinearGradient, QBrush, QPainter

class ThemeCard(QFrame):
    def __init__(self, name, colors, parent=None):
        super().__init__(parent)
        self.setFixedHeight(140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #E2E8F0;
                border-radius: 20px;
            }
            QFrame:hover {
                border-color: #38BDF8;
            }
            QFrame[selected="true"] {
                border-color: #38BDF8;
                background-color: #F0F9FF;
            }
        """)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(12, 12, 12, 12)
        l.setSpacing(8)
        
        # Preview Area
        self.preview = QFrame()
        self.preview.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 {colors[0]}, stop:0.5 {colors[1]}, stop:1 {colors[2]});
            border-radius: 12px;
            border: none;
        """)
        l.addWidget(self.preview)
        
        self.name_lbl = QLabel(name)
        self.name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_lbl.setStyleSheet("font-weight: 700; font-size: 12px; color: #1E293B; border: none; background: transparent;")
        l.addWidget(self.name_lbl)

    def set_selected(self, selected):
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

class AppearanceWorkspace(QWidget):
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

        # 1. Hero Overview
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(40)
        
        info = QVBoxLayout(); info.setSpacing(8)
        tag = QLabel("✨ VISUAL INTELLIGENCE")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("Appearance Studio")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your current interface harmony is <b>94% optimized</b>. AI suggests subtle adjustments to the accent gradient for better readability.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        stats = QGridLayout(); stats.setSpacing(12)
        def add_stat(val, label, r, c):
            v = QVBoxLayout(); v.setSpacing(2); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l1 = QLabel(val); l1.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
            l2 = QLabel(label); l2.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
            v.addWidget(l1); v.addWidget(l2); stats.addLayout(v, r, c)
            
        add_stat("Elite", "Aesthetic", 0, 0); add_stat("Fluent", "Style", 0, 1)
        add_stat("94%", "Harmony", 1, 0); add_stat("Adaptive", "Mode", 1, 1)
        hl.addLayout(stats)
        cl.addWidget(hero)

        # 2. Theme Gallery
        theme_sec = QWidget()
        tl = QVBoxLayout(theme_sec); tl.setContentsMargins(0, 0, 0, 0); tl.setSpacing(16)
        tl.addWidget(QLabel("Interface Themes", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        theme_grid = QGridLayout(); theme_grid.setSpacing(16)
        theme_grid.addWidget(ThemeCard("Light Pro", ["#F8FAFC", "#FFFFFF", "#38BDF8"]), 0, 0)
        theme_grid.addWidget(ThemeCard("Midnight", ["#0F172A", "#1E293B", "#38BDF8"]), 0, 1)
        theme_grid.addWidget(ThemeCard("Glassmorphic", ["#F1F5F9", "#E2E8F0", "#BAE6FD"]), 1, 0)
        theme_grid.addWidget(ThemeCard("Cyber", ["#020617", "#1E1B4B", "#8B5CF6"]), 1, 1)
        tl.addLayout(theme_grid)
        cl.addWidget(theme_sec)

        # 3. Visual Controls
        studio_card = QFrame()
        studio_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        sl = QVBoxLayout(studio_card); sl.setContentsMargins(24, 24, 24, 24); sl.setSpacing(24)
        
        sl.addWidget(QLabel("Studio Controls", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        # Color Studio
        color_h = QHBoxLayout(); color_h.setSpacing(12)
        color_h.addWidget(QLabel("Accent Color", styleSheet="font-size: 13px; font-weight: 600; color: #475569; border: none;"))
        color_h.addStretch()
        for c in ["#38BDF8", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444"]:
            btn = QPushButton(); btn.setFixedSize(20, 20)
            btn.setStyleSheet(f"background: {c}; border-radius: 10px; border: 2px solid white;")
            color_h.addWidget(btn)
        sl.addLayout(color_h)
        
        # Sliders
        def add_slider(label, val):
            row = QVBoxLayout(); row.setSpacing(8)
            hl = QHBoxLayout()
            hl.addWidget(QLabel(label, styleSheet="font-size: 13px; font-weight: 600; color: #475569; border: none;"))
            hl.addStretch()
            hl.addWidget(QLabel(val, styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;"))
            row.addLayout(hl)
            s = QSlider(Qt.Orientation.Horizontal)
            s.setStyleSheet("QSlider::groove:horizontal { height: 4px; background: #F1F5F9; border-radius: 2px; } QSlider::handle:horizontal { background: #38BDF8; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }")
            row.addWidget(s); sl.addLayout(row)
            
        add_slider("Animation Intensity", "Balanced")
        add_slider("Glass Blur Depth", "Medium")
        add_slider("Interface Scaling", "100%")
        
        # Density
        density_h = QHBoxLayout(); density_h.setSpacing(12)
        density_h.addWidget(QLabel("UI Density", styleSheet="font-size: 13px; font-weight: 600; color: #475569; border: none;"))
        density_h.addStretch()
        cb_density = QComboBox(); cb_density.addItems(["Compact", "Comfortable", "Spacious"])
        cb_density.setFixedWidth(140); cb_density.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding-left: 8px;")
        density_h.addWidget(cb_density)
        sl.addLayout(density_h)
        
        cl.addWidget(studio_card)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
