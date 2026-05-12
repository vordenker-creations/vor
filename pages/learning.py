import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, QProgressBar)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor
from config import *
from components import SaaSCard, AnimationEngine

class LearningPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("LearningPage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.container = QWidget(); self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(35, 35, 35, 35); self.container_layout.setSpacing(15)
        self._setup_header(); self._setup_breadcrumb(); self._setup_content()
        self.scroll.setWidget(self.container); self.main_layout.addWidget(self.scroll)

    def _setup_header(self):
        header = QWidget(); layout = QVBoxLayout(header); layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("AI Art Creation Studio"); title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold;")
        layout.addWidget(title); sub = QLabel("Nâng cao kỹ năng - Tiếp tục học tập"); sub.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 14px;")
        layout.addWidget(sub); self.container_layout.addWidget(header)

    def _setup_breadcrumb(self):
        bread = QWidget(); layout = QHBoxLayout(bread); layout.setContentsMargins(0, 0, 0, 20)
        btn_dash = QPushButton("Dashboard"); btn_dash.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_dash.setStyleSheet(f"QPushButton {{ background: transparent; color: {COLOR_TEXT_SUB}; font-size: 12px; border: none; }} QPushButton:hover {{ color: {COLOR_PRIMARY}; }}")
        btn_dash.clicked.connect(lambda: self.controller and self.controller.show_page("DashboardPage"))
        layout.addWidget(btn_dash); layout.addWidget(QLabel(" > Khóa học"))
        layout.addStretch(); self.container_layout.addWidget(bread)

    def _setup_content(self):
        grid_widget = QWidget(); grid_layout = QGridLayout(grid_widget); grid_layout.setContentsMargins(0, 0, 0, 0); grid_layout.setSpacing(10)
        grid_layout.setColumnStretch(0, 7); grid_layout.setColumnStretch(1, 3)
        left_col = QWidget(); left_layout = QVBoxLayout(left_col); left_layout.setContentsMargins(0, 0, 0, 0)
        lbl_mine = QLabel("Học phần của bạn"); lbl_mine.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        left_layout.addWidget(lbl_mine); course_grid = QWidget(); c_layout = QGridLayout(course_grid); c_layout.setSpacing(15)
        self._add_course_card(c_layout, 0, 0, "Lập trình Python Nâng cao", 0.8, "80%", [("Pandas", True), ("TensorFlow", False)])
        self._add_course_card(c_layout, 0, 1, "Tạo Ảnh Nghệ Thuật với AI", 0.35, "35%", [("Prompt Eng", True), ("ControlNet", False)])
        left_layout.addWidget(course_grid); left_layout.addStretch(); grid_layout.addWidget(left_col, 0, 0)
        right_col = QWidget(); right_layout = QVBoxLayout(right_col); right_layout.setContentsMargins(0, 0, 0, 0)
        deadline_card = SaaSCard(); d_layout = deadline_card.internal_layout
        lbl_d = QLabel("Sự kiện & Deadline"); lbl_d.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        d_layout.addWidget(lbl_d); self._add_event_item(d_layout, "12", "Th4", "Workshop AI"); self._add_event_item(d_layout, "15", "Th4", "Nộp đồ án")
        right_layout.addWidget(deadline_card); creativity_card = SaaSCard(); crea_layout = creativity_card.internal_layout
        lbl_c = QLabel("Mức độ sáng tạo"); lbl_c.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        crea_layout.addWidget(lbl_c); pb = QProgressBar(); pb.setFixedHeight(8); pb.setValue(75); pb.setTextVisible(False)
        pb.setStyleSheet(f"QProgressBar {{ background: {COLOR_BORDER}; border-radius: 4px; border: none; }} QProgressBar::chunk {{ background: {COLOR_SUCCESS}; border-radius: 4px; }}")
        crea_layout.addWidget(pb); right_layout.addWidget(creativity_card); right_layout.addStretch(); grid_layout.addWidget(right_col, 0, 1)
        self.container_layout.addWidget(grid_widget)

    def _add_course_card(self, layout, r, c, title, val, txt, tasks):
        card = SaaSCard(); c_layout = card.internal_layout
        img = QFrame(); img.setFixedHeight(120); img.setStyleSheet(f"background: {COLOR_BG_APP}; border-radius: 6px;")
        img_l = QVBoxLayout(img); lbl_icon = QLabel("📷"); lbl_icon.setStyleSheet("font-size: 40px;"); img_l.addWidget(lbl_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        c_layout.addWidget(img); lbl_t = QLabel(title); lbl_t.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        c_layout.addWidget(lbl_t); pb = QProgressBar(); pb.setFixedHeight(6); pb.setValue(int(val * 100)); pb.setTextVisible(False)
        pb.setStyleSheet(f"QProgressBar {{ background: {COLOR_BORDER}; border-radius: 3px; border: none; }} QProgressBar::chunk {{ background: {COLOR_PRIMARY}; border-radius: 3px; }}")
        c_layout.addWidget(pb); lbl_p = QLabel(f"{txt} Hoàn thành"); lbl_p.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 11px;"); c_layout.addWidget(lbl_p)
        for t_name, done in tasks:
            t_layout = QHBoxLayout(); lbl_check = QLabel("✓" if done else "🔵"); lbl_check.setStyleSheet(f"color: {COLOR_PRIMARY if done else COLOR_TEXT_SUB}; font-weight: bold;")
            t_layout.addWidget(lbl_check); lbl_task = QLabel(t_name); lbl_task.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 11px;"); t_layout.addWidget(lbl_task); t_layout.addStretch(); c_layout.addLayout(t_layout)
        btn_row = QHBoxLayout(); btn_cont = QPushButton("Tiếp tục"); btn_cont.setFixedHeight(32); btn_cont.setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY}; color: white; font-weight: bold; border-radius: 6px; }}")
        btn_cont.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cont.clicked.connect(lambda: self.controller and self.controller.show_page("CourseDetailPage"))
        btn_row.addWidget(btn_cont); c_layout.addLayout(btn_row); layout.addWidget(card, r, c)

    def _add_event_item(self, layout, day, month, title):
        item = QWidget(); i_layout = QHBoxLayout(item); i_layout.setContentsMargins(0, 5, 0, 5)
        date_box = QFrame(); date_box.setFixedSize(45, 50); date_box.setStyleSheet(f"background: {COLOR_PRIMARY_LIGHT}; border-radius: 6px;")
        d_layout = QVBoxLayout(date_box); d_layout.setContentsMargins(0, 5, 0, 5); lbl_d = QLabel(day); lbl_d.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 16px; font-weight: bold;")
        d_layout.addWidget(lbl_d, alignment=Qt.AlignmentFlag.AlignCenter); lbl_m = QLabel(month); lbl_m.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 10px;")
        d_layout.addWidget(lbl_m, alignment=Qt.AlignmentFlag.AlignCenter); i_layout.addWidget(date_box); lbl_title = QLabel(title); lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        i_layout.addWidget(lbl_title); i_layout.addStretch(); layout.addWidget(item)
