import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from config import *

# Import Tabs
from pages.roadmap_tabs.overview_tab import OverviewTab
from pages.roadmap_tabs.skill_tree_tab import SkillTreeTab
from pages.roadmap_tabs.year_details_tab import YearDetailsTab
from pages.roadmap_tabs.timetable_tab import TimetableTab

class RoadmapPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("RoadmapPage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab Nav
        self.tab_nav = QWidget()
        self.tab_nav.setFixedHeight(60)
        self.nav_layout = QHBoxLayout(self.tab_nav)
        self.nav_layout.setContentsMargins(35, 20, 35, 10)
        self.nav_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.tab_btns = {}
        tabs = [("OVERVIEW", 0), ("SKILL TREE", 1), ("Y1 DETAILS", 2), ("TIMETABLE", 3)]
        for text, idx in tabs:
            btn = QPushButton(text); btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)); btn.setFixedHeight(35)
            btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {COLOR_TEXT_SUB}; font-weight: bold; border-radius: 18px; padding: 0 15px; }}")
            btn.clicked.connect(lambda ch, i=idx: self.show_tab(i))
            self.nav_layout.addWidget(btn); self.tab_btns[idx] = btn
            
        self.main_layout.addWidget(self.tab_nav)
        
        # Tab Container
        self.tab_stack = QStackedWidget()
        self.tab_stack.addWidget(OverviewTab())     # 0
        self.tab_stack.addWidget(SkillTreeTab())    # 1
        self.tab_stack.addWidget(YearDetailsTab()) # 2
        self.tab_stack.addWidget(TimetableTab())   # 3
        
        self.main_layout.addWidget(self.tab_stack)
        self.show_tab(0)

    def show_tab(self, index):
        self.tab_stack.setCurrentIndex(index)
        for idx, btn in self.tab_btns.items():
            if idx == index:
                btn.setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY}; color: white; font-weight: bold; border-radius: 18px; padding: 0 15px; }}")
            else:
                btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {COLOR_TEXT_SUB}; font-weight: bold; border-radius: 18px; padding: 0 15px; }}")
