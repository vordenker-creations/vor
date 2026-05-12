import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from config import *
from components import SaaSCard, AnimatedCircularProgress
from i18n import _

class RecruitmentPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("RecruitmentPage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.container = QWidget(); self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(35, 35, 35, 35)
        lbl_title = QLabel(_("recruit_title"))
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.container_layout.addWidget(lbl_title)
        self.grid_widget = QWidget(); self.grid = QGridLayout(self.grid_widget)
        self.grid.setContentsMargins(0, 0, 0, 0); self.grid.setSpacing(20)
        jobs_data = [
            {"company": "Google Vietnam", "location": "TP. HCM", "title": "AI Research Engineer", "salary": "Thỏa thuận", "match": 92, "skills_has": ["Python", "PyTorch"], "skills_missing": ["C++"]},
            {"company": "Shopee Vietnam", "location": "Hà Nội", "title": "Data Scientist", "salary": "25tr - 40tr VNĐ", "match": 75, "skills_has": ["Python", "SQL"], "skills_missing": ["Spark", "Airflow"]},
            {"company": "VNG Corporation", "location": "TP. HCM", "title": "Machine Learning Engineer", "salary": "30tr - 50tr VNĐ", "match": 85, "skills_has": ["Python", "TensorFlow"], "skills_missing": ["Docker"]},
            {"company": "MoMo", "location": "TP. HCM", "title": "Data Analyst", "salary": "20tr - 35tr VNĐ", "match": 60, "skills_has": ["SQL"], "skills_missing": ["Python", "Tableau"]}
        ]
        for i, job in enumerate(jobs_data):
            self._add_job_card(i // 2, i % 2, job)
        self.container_layout.addWidget(self.grid_widget); self.container_layout.addStretch()
        self.scroll.setWidget(self.container); self.main_layout.addWidget(self.scroll)

    def _add_job_card(self, row, col, job):
        card = SaaSCard(); l = card.internal_layout
        head = QHBoxLayout(); info = QVBoxLayout(); lbl_comp = QLabel(job["company"]); lbl_comp.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
        info.addWidget(lbl_comp); lbl_title = QLabel(job["title"]); lbl_title.setWordWrap(True); lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        info.addWidget(lbl_title); head.addLayout(info)
        match_color = COLOR_SUCCESS if job["match"] >= 80 else COLOR_WARNING if job["match"] >= 60 else COLOR_DANGER
        ring = AnimatedCircularProgress(size=60, color=match_color); head.addWidget(ring); ring.set_target(job["match"] / 100)
        l.addLayout(head); lbl_loc = QLabel(f"📍 {job['location']}   💰 {job['salary']}"); lbl_loc.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 13px; margin-top: 5px;")
        l.addWidget(lbl_loc); skills_box = QFrame(); skills_box.setStyleSheet(f"background: {COLOR_BG_APP}; border-radius: 8px;")
        sl = QVBoxLayout(skills_box); lbl_has = QLabel(f"{_('recruit_has')} {', '.join(job['skills_has'])}"); lbl_has.setStyleSheet(f"color: {COLOR_SUCCESS}; font-size: 12px;")
        sl.addWidget(lbl_has); miss_row = QHBoxLayout(); lbl_miss = QLabel(_("recruit_missing")); lbl_miss.setStyleSheet(f"color: {COLOR_WARNING}; font-size: 12px;"); miss_row.addWidget(lbl_miss)
        for m in job["skills_missing"]:
            btn_m = QPushButton(f"{m} +"); btn_m.setFixedSize(70, 24); btn_m.setStyleSheet(f"background: {COLOR_WARNING}; color: white; border-radius: 12px; font-size: 10px; font-weight: bold;"); miss_row.addWidget(btn_m)
        miss_row.addStretch(); sl.addLayout(miss_row); l.addWidget(skills_box); btn_apply = QPushButton(_("recruit_apply")); btn_apply.setFixedHeight(35)
        btn_apply.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)); btn_apply.setStyleSheet(f"background: {COLOR_PRIMARY_LIGHT}; color: {COLOR_PRIMARY}; font-weight: bold; border-radius: 6px;")
        l.addWidget(btn_apply); self.grid.addWidget(card, row, col)
