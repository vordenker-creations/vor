import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from config import *

# Import Tabs
from pages.course_tabs.roadmap_tab import RoadmapTab
from pages.course_tabs.documents_tab import DocumentsTab
from pages.course_tabs.exercises_tab import ExercisesTab
from pages.course_tabs.projects_tab import ProjectsTab
from pages.course_tabs.results_tab import ResultsTab
from pages.course_tabs.analytics_tab import AnalyticsTab

class CourseDetailPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("CourseDetailPage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.container = QWidget(); self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(24, 24, 24, 24)
        self.container_layout.setSpacing(16)
        
        self._setup_header(); self._setup_tabs(); self._setup_content()
        self.scroll.setWidget(self.container); self.main_layout.addWidget(self.scroll)

    def _setup_header(self):
        btn_back = QPushButton("⬅ Quay lại Dashboard")
        btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_back.setStyleSheet("QPushButton { background: transparent; color: #475569; font-weight: 600; border: none; text-align: left; font-size: 14px; } QPushButton:hover { color: #0f172a; }")
        btn_back.clicked.connect(lambda: self.controller and self.controller.show_page("DashboardPage"))
        self.container_layout.addWidget(btn_back)
        lbl_t = QLabel("CHI TIẾT: LẬP TRÌNH PYTHON NÂNG CAO")
        lbl_t.setStyleSheet("color: #0f172a; font-size: 22px; font-weight: 700; letter-spacing: -0.3px; margin: 8px 0;")
        self.container_layout.addWidget(lbl_t)

    def _setup_tabs(self):
        row = QHBoxLayout(); row.setSpacing(8); self.tab_btns = {}
        tabs = [("Đường lộ trình", 0), ("Tài liệu", 1), ("Bài tập", 2), ("Đồ án", 3), ("Kết quả", 4), ("Phân tích", 5)]
        for text, idx in tabs:
            btn = QPushButton(text); btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("QPushButton { background: white; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-weight: 600; height: 36px; padding: 0 16px; } QPushButton:hover { background: #f8fafc; }")
            btn.clicked.connect(lambda ch, i=idx: self.show_tab(i))
            row.addWidget(btn); self.tab_btns[idx] = btn
        row.addStretch()
        self.container_layout.addLayout(row)
        line = QFrame(); line.setFixedHeight(1); line.setStyleSheet("background: #e2e8f0;"); self.container_layout.addWidget(line)

    def _setup_content(self):
        self.tab_stack = QStackedWidget()
        self.tab_stack.addWidget(RoadmapTab())   # 0
        self.tab_stack.addWidget(DocumentsTab()) # 1
        self.tab_stack.addWidget(ExercisesTab()) # 2
        self.tab_stack.addWidget(ProjectsTab())  # 3
        self.tab_stack.addWidget(ResultsTab())   # 4
        self.tab_stack.addWidget(AnalyticsTab()) # 5
        self.container_layout.addWidget(self.tab_stack)
        self.show_tab(0)

    def show_tab(self, index):
        self.tab_stack.setCurrentIndex(index)
        for idx, btn in self.tab_btns.items():
            if idx == index:
                btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f172a, stop:1 #334155); color: white; border-radius: 8px; font-weight: 600; border: none; height: 36px; padding: 0 16px; }")
            else:
                btn.setStyleSheet("QPushButton { background: white; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-weight: 600; height: 36px; padding: 0 16px; } QPushButton:hover { background: #f8fafc; }")
