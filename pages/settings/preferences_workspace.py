from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor
from .toggle_switch import ToggleSwitch
from .common_widgets import ToggleRow

class ModeCard(QFrame):
    def __init__(self, title, icon, desc, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #E2E8F0;
                border-radius: 20px;
            }
            QFrame:hover {
                border-color: #38BDF8;
                background-color: #F8FAFC;
            }
            QFrame[selected="true"] {
                border-color: #38BDF8;
                background-color: #F0F9FF;
            }
        """)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(4)
        
        h = QHBoxLayout()
        ico = QLabel(icon); ico.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        h.addWidget(ico); h.addStretch()
        l.addLayout(h)
        
        t = QLabel(title)
        t.setStyleSheet("font-weight: 700; font-size: 14px; color: #0F172A; border: none; background: transparent;")
        l.addWidget(t)
        
        d = QLabel(desc)
        d.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        l.addWidget(d)

    def set_selected(self, selected):
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

class PreferencesWorkspace(QWidget):
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

        # 1. Hero Summary
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(40)
        
        info = QVBoxLayout(); info.setSpacing(8)
        tag = QLabel("✨ WORKSPACE OPTIMIZATION")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("Personalized Experience")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your workspace is currently set to <b>Productivity Mode</b>. AI has optimized your interaction patterns for maximum focus.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        stats = QGridLayout(); stats.setSpacing(12)
        def add_stat(val, label, r, c):
            v = QVBoxLayout(); v.setSpacing(2); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l1 = QLabel(val); l1.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
            l2 = QLabel(label); l2.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
            v.addWidget(l1); v.addWidget(l2); stats.addLayout(v, r, c)
            
        add_stat("94%", "Optimized", 0, 0); add_stat("Active", "Sync", 0, 1)
        add_stat("Elite", "Plan", 1, 0); add_stat("High", "Density", 1, 1)
        hl.addLayout(stats)
        cl.addWidget(hero)

        # 2. Workspace Modes
        mode_sec = QWidget()
        ml = QVBoxLayout(mode_sec); ml.setContentsMargins(0, 0, 0, 0); ml.setSpacing(16)
        ml.addWidget(QLabel("Workspace Modes", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        mode_grid = QGridLayout(); mode_grid.setSpacing(16)
        mode_grid.addWidget(ModeCard("Focus Mode", "🎯", "Minimize distractions and UI density."), 0, 0)
        mode_grid.addWidget(ModeCard("Productivity", "⚡", "High information density and quick actions."), 0, 1)
        mode_grid.addWidget(ModeCard("Minimal", "❄️", "Clean interface with essential tools only."), 1, 0)
        mode_grid.addWidget(ModeCard("Enterprise", "🏢", "Multi-user collaboration and tracking."), 1, 1)
        ml.addLayout(mode_grid)
        cl.addWidget(mode_sec)

        # 3. Behavior Sections
        behavior_sec = QFrame()
        behavior_sec.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        bl = QVBoxLayout(behavior_sec); bl.setContentsMargins(24, 24, 24, 24); bl.setSpacing(20)
        
        bl.addWidget(QLabel("Navigation & Interaction", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        bl.addWidget(ToggleRow("Auto-Collapse Sidebar", "Automatically hide the sidebar when focusing on content."))
        bl.addWidget(ToggleRow("Smooth Transitions", "Enable fluid animations when switching between workspaces."))
        bl.addWidget(ToggleRow("Tab Persistence", "Restore previously opened tabs on startup."))
        bl.addWidget(ToggleRow("Smart Quick-Actions", "Show AI-powered action suggestions based on context."))
        
        cl.addWidget(behavior_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
