from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class RoadmapNavItem(QPushButton):
    def __init__(self, text, icon="○", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 10px 16px;
                color: #64748B;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                color: #0F172A;
            }
            QPushButton:checked {
                background-color: #E0F2FE;
                color: #0284C7;
                font-weight: 600;
            }
        """)

class RoadmapSidebar(QFrame):
    navigation_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 24, 16, 24)
        self.main_layout.setSpacing(20)

        # 1. Header
        header = QLabel("Skill Graph")
        header.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        self.main_layout.addWidget(header)

        # 2. Search
        search_container = QFrame()
        search_container.setFixedHeight(44)
        search_container.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px;")
        sl = QHBoxLayout(search_container)
        sl.setContentsMargins(12, 0, 12, 0)
        search_icon = QLabel("🔍")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search skills...")
        search_input.setStyleSheet("border: none; background: transparent; font-size: 13px;")
        sl.addWidget(search_icon)
        sl.addWidget(search_input)
        self.main_layout.addWidget(search_container)

        # 3. Navigation
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        nav_layout = QVBoxLayout(container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(4)

        sections = [
            ("ROADMAP", ["Skill Map", "Milestones", "Learning Analytics"]),
            ("INTELLIGENCE", ["Weak Skills", "AI Recommendations"]),
            ("CAREER", ["Certifications", "Career Paths"])
        ]

        self.buttons = []
        for section_title, items in sections:
            lbl = QLabel(section_title)
            lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 800; letter-spacing: 1px; margin: 16px 0 8px 12px; border: none;")
            nav_layout.addWidget(lbl)
            
            for item in items:
                btn = RoadmapNavItem(item)
                btn.clicked.connect(lambda ch, i=item: self._handle_click(i))
                nav_layout.addWidget(btn)
                self.buttons.append(btn)
                if item == "Skill Map": btn.setChecked(True)

        nav_layout.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Progress Stats
        stats_card = QFrame()
        stats_card.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0;")
        stl = QVBoxLayout(stats_card)
        stl.setContentsMargins(16, 16, 16, 16)
        stl.setSpacing(12)
        
        head = QLabel("Current Roadmap")
        head.setStyleSheet("font-weight: 700; font-size: 12px; color: #0F172A; border: none;")
        stl.addWidget(head)
        
        prog_v = QVBoxLayout()
        prog_v.setSpacing(4)
        rl = QHBoxLayout()
        rl.addWidget(QLabel("AI Engineer", styleSheet="font-size: 11px; color: #64748B; border: none;"))
        rl.addStretch()
        rl.addWidget(QLabel("45%", styleSheet="font-size: 11px; font-weight: 700; color: #38BDF8; border: none;"))
        prog_v.addLayout(rl)
        
        pb = QProgressBar()
        pb.setFixedHeight(6)
        pb.setValue(45)
        pb.setTextVisible(False)
        pb.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 3px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 3px; }")
        prog_v.addWidget(pb)
        stl.addLayout(prog_v)
        
        self.main_layout.addWidget(stats_card)

    def _handle_click(self, name):
        for btn in self.buttons:
            btn.setChecked(btn.text() == name)
        self.navigation_requested.emit(name)
