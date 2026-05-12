import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, QLineEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor

from config import *
from components import SaaSCard, AnimatedCircularProgress, AnimationEngine
from i18n import _

class ProfilePage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("ProfilePage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        header_frame = QWidget()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(35, 35, 35, 10)
        self.title_label = QLabel(_("prof_title"))
        self.title_label.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(self.title_label)
        self.main_layout.addWidget(header_frame)
        self.tab_nav = QWidget()
        self.tab_nav.setFixedHeight(45)
        self.tab_layout = QHBoxLayout(self.tab_nav)
        self.tab_layout.setContentsMargins(35, 0, 35, 15)
        self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tab_buttons = {}
        tabs = [("OVERVIEW", _("prof_tab_overview"), self.show_overview), ("CV ANALYSIS", _("prof_tab_cv_analysis"), self.show_cv_analysis), ("CV BUILDER", _("prof_tab_cv_builder"), self.show_cv_builder)]
        for key, text, command in tabs:
            btn = QPushButton(text)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setFixedHeight(35); btn.setMinimumWidth(120)
            btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {COLOR_TEXT_SUB}; font-weight: bold; border-radius: 6px; padding: 0 10px; }} QPushButton:hover {{ background: {COLOR_BG_CARD}; }}")
            btn.clicked.connect(command)
            self.tab_layout.addWidget(btn); self.tab_buttons[key] = btn
        self.main_layout.addWidget(self.tab_nav)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 5, 15, 5)
        self.scroll.setWidget(self.container)
        self.main_layout.addWidget(self.scroll)
        self.show_overview()

    def clear_container(self):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget: 
                widget.deleteLater()
            elif item.layout():
                self._clear_sub_layout(item.layout())
        
        for btn in self.tab_buttons.values():
            btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {COLOR_TEXT_SUB}; font-weight: bold; border-radius: 6px; padding: 0 10px; }} QPushButton:hover {{ background: {COLOR_BG_CARD}; }}")

    def _clear_sub_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_sub_layout(item.layout())

    def set_active_tab(self, tab_key):
        self.tab_buttons[tab_key].setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY_LIGHT}; color: {COLOR_PRIMARY}; font-weight: bold; border-radius: 6px; padding: 0 10px; }}")
        titles = {"OVERVIEW": _("prof_title"), "CV ANALYSIS": _("prof_sub_analysis"), "CV BUILDER": _("prof_sub_builder")}
        self.title_label.setText(titles.get(tab_key, _("prof_title")))

    def show_overview(self):
        self.clear_container(); self.set_active_tab("OVERVIEW")
        card = SaaSCard(); card_layout = card.internal_layout
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        from database import crud
        student = crud.get_current_student()
        
        name_text = "Guest User"
        major_text = _("prof_student_info")
        bio_text = "Aspiring AI engineer with a strong foundation in Python and a passion for deep learning.\nDedicated to developing innovative solutions and mastering modern AI techniques."
        
        if student:
            name_text = student.get("full_name", "Student")
            major_text = student.get("major", _("prof_student_info"))
            bio_text = student.get("context", {}).get("bio", bio_text)

        avatar_lbl = QLabel("👤")
        avatar_lbl.setStyleSheet(f"font-size: 80px; color: {COLOR_PRIMARY}; margin-top: 50px;")
        card_layout.addWidget(avatar_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        name_lbl = QLabel(name_text)
        name_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold;")
        card_layout.addWidget(name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        info_lbl = QLabel(major_text)
        info_lbl.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 14px;")
        card_layout.addWidget(info_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_active = QPushButton(_("prof_active_path"))
        btn_active.setFixedSize(120, 30); btn_active.setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY_LIGHT}; color: {COLOR_PRIMARY}; border-radius: 15px; font-size: 11px; font-weight: bold; }}")
        card_layout.addWidget(btn_active, alignment=Qt.AlignmentFlag.AlignCenter)
        bio_lbl = QLabel(bio_text); bio_lbl.setWordWrap(True); bio_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bio_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 13px; margin: 20px 50px 50px 50px;")
        card_layout.addWidget(bio_lbl)
        self.container_layout.addWidget(card)

    def show_cv_analysis(self):
        self.clear_container(); self.set_active_tab("CV ANALYSIS")
        grid_widget = QWidget(); grid = QGridLayout(grid_widget); grid.setContentsMargins(0, 0, 0, 0); grid.setSpacing(20)
        left_card = SaaSCard(); left_layout = left_card.internal_layout
        lbl_resumes = QLabel(_("prof_my_resumes")); lbl_resumes.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: bold;"); left_layout.addWidget(lbl_resumes)
        btn_row = QHBoxLayout(); btn_create = QPushButton(_("prof_create_resume")); btn_create.setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY}; color: black; font-weight: bold; border-radius: 8px; height: 35px; }}"); btn_row.addWidget(btn_create)
        btn_upload = QPushButton(_("prof_upload_resume")); btn_upload.setStyleSheet(f"QPushButton {{ background: {COLOR_BG_CARD}; color: {COLOR_TEXT_MAIN}; border: 1px solid {COLOR_BORDER}; font-weight: bold; border-radius: 8px; height: 35px; }}"); btn_row.addWidget(btn_upload); left_layout.addLayout(btn_row)
        resumes = [("📄", "Core Resume - Applied AI", _("prof_create_resume")), ("📄", "General CV - Software Engineering", "View CV")]
        for icon, title, sub in resumes:
            item = QWidget(); item_layout = QHBoxLayout(item)
            icon_lbl = QLabel(icon); icon_lbl.setStyleSheet("font-size: 20px;"); item_layout.addWidget(icon_lbl)
            txt_layout = QVBoxLayout(); t_lbl = QLabel(title); t_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold;"); txt_layout.addWidget(t_lbl)
            s_lbl = QLabel(sub); s_lbl.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;"); txt_layout.addWidget(s_lbl); item_layout.addLayout(txt_layout)
            item_layout.addStretch(); item_layout.addWidget(QLabel(">")); left_layout.addWidget(item)
        grid.addWidget(left_card, 0, 0); right_card = SaaSCard(border_color=COLOR_SUCCESS); right_layout = right_card.internal_layout
        lbl_feedback = QLabel(_("prof_ai_feedback")); lbl_feedback.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;"); right_layout.addWidget(lbl_feedback)
        match_box = QHBoxLayout(); ring = AnimatedCircularProgress(size=120, color=COLOR_SUCCESS); match_box.addWidget(ring); ring.set_target(0.92)
        match_info = QVBoxLayout(); lbl_match = QLabel(_("prof_job_match")); lbl_match.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px; font-weight: bold;"); match_info.addWidget(lbl_match); match_box.addLayout(match_info); right_layout.addLayout(match_box)
        grid.addWidget(right_card, 0, 1); self.container_layout.addWidget(grid_widget)

    def show_cv_builder(self):
        self.clear_container(); self.set_active_tab("CV BUILDER")
        grid_widget = QWidget(); grid = QGridLayout(grid_widget); grid.setColumnStretch(0, 6); grid.setColumnStretch(1, 4)
        form_card = SaaSCard(); form_layout = form_card.internal_layout; lbl_auto = QLabel(_("prof_auto_fill")); lbl_auto.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;"); form_layout.addWidget(lbl_auto)
        for p in ["University Name", "Major/Focus", "Current GPA"]:
            entry = QLineEdit(); entry.setPlaceholderText(p); entry.setFixedHeight(35); entry.setStyleSheet(f"QLineEdit {{ background: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 6px; color: {COLOR_TEXT_MAIN}; padding: 0 10px; }}"); form_layout.addWidget(entry)
        grid.addWidget(form_card, 0, 0); preview_area = QVBoxLayout(); lbl_prev = QLabel(_("prof_preview")); lbl_prev.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;"); preview_area.addWidget(lbl_prev)
        paper = QFrame(); paper.setFixedSize(340, 520); paper.setStyleSheet("background: #F8FAFC; border-radius: 2px;"); preview_area.addWidget(paper); grid.addLayout(preview_area, 0, 1); self.container_layout.addWidget(grid_widget)
