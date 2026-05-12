import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, QComboBox, QTextEdit, QLineEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor
from config import *
from components import SaaSCard, AnimationEngine
from i18n import _

class CommunityPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("CommunityPage")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.container = QWidget(); self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(35, 35, 35, 35); self.container_layout.setSpacing(15)
        self._setup_header(); self._setup_groups(); self._setup_workflow(); self._setup_actions()
        self.scroll.setWidget(self.container); self.main_layout.addWidget(self.scroll)

    def _setup_header(self):
        header = QWidget(); h_layout = QHBoxLayout(header); h_layout.setContentsMargins(0, 0, 0, 0)
        lbl_title = QLabel(_("comm_title")); lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 22px; font-weight: bold;")
        h_layout.addWidget(lbl_title); h_layout.addStretch()
        target_box = QWidget(); target_layout = QHBoxLayout(target_box)
        target_layout.addWidget(QLabel(_("comm_target_job")))
        job_combo = QComboBox(); job_combo.addItems(["ML Engineer", "Data Scientist", "Full-Stack Dev", "AI Researcher"])
        job_combo.setStyleSheet(f"QComboBox {{ background: {COLOR_BG_CARD}; color: {COLOR_TEXT_MAIN}; border-radius: 6px; padding: 5px; }}")
        target_layout.addWidget(job_combo); h_layout.addWidget(target_box)
        self.container_layout.addWidget(header)

    def _setup_groups(self):
        lbl_groups = QLabel(_("comm_join_groups")); lbl_groups.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        self.container_layout.addWidget(lbl_groups); grid_widget = QWidget(); grid = QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0); grid.setSpacing(15)
        groups = [("ML Engineers", "660", "2 hours ago", COLOR_PRIMARY, "🤖"), ("Full-Stack Devs", "125", "2 hours ago", "#F59E0B", "💻"), ("Python Foundations", "157", "2 hours ago", "#10B981", "🐍")]
        for i, (title, members, time, color, icon) in enumerate(groups):
            card = SaaSCard(border_color=color); card_layout = card.internal_layout
            head = QHBoxLayout(); head.addWidget(QLabel(icon)); head.addStretch(); head.addWidget(QLabel("↗"))
            card_layout.addLayout(head); t_lbl = QLabel(title); t_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;")
            card_layout.addWidget(t_lbl); m_lbl = QLabel(f"👥 {members} members"); m_lbl.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
            card_layout.addWidget(m_lbl); card_layout.addWidget(QLabel(f"Recent: {time}"))
            grid.addWidget(card, 0, i)
        self.container_layout.addWidget(grid_widget)

    def _setup_workflow(self):
        lbl_wf = QLabel(_("comm_workflow")); lbl_wf.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: bold;")
        self.container_layout.addWidget(lbl_wf); grid_widget = QWidget(); grid = QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0); grid.setSpacing(15)
        col1 = SaaSCard(); c1_layout = col1.internal_layout; c1_layout.addWidget(QLabel(_("comm_step1")))
        for g, t in [("ML Engineers", "2 mins ago"), ("Python Found", "1 hour ago")]:
            box = QFrame(); box.setStyleSheet(f"background: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 6px;")
            l = QVBoxLayout(box); l.addWidget(QLabel(g)); l.addWidget(QLabel(t))
            c1_layout.addWidget(box)
        grid.addWidget(col1, 0, 0); col2 = SaaSCard(); c2_layout = col2.internal_layout; c2_layout.addWidget(QLabel(_("comm_step2")))
        title_in = QLineEdit(); title_in.setPlaceholderText(_("comm_post_title")); c2_layout.addWidget(title_in)
        content_in = QTextEdit(); content_in.setPlaceholderText("Content..."); c2_layout.addWidget(content_in)
        btn_post = QPushButton(_("comm_btn_post")); btn_post.setStyleSheet(f"background: {COLOR_PRIMARY}; color: black; font-weight: bold; height: 35px; border-radius: 6px;")
        c2_layout.addWidget(btn_post); grid.addWidget(col2, 0, 1); col3 = SaaSCard(); c3_layout = col3.internal_layout; c3_layout.addWidget(QLabel(_("comm_step3")))
        self._add_feedback(c3_layout, "AI SUGGESTIONS", "Optimize reach.", COLOR_PRIMARY)
        grid.addWidget(col3, 0, 2); self.container_layout.addWidget(grid_widget)

    def _setup_actions(self):
        row = QHBoxLayout(); btns = [(_("comm_btn_mentor"), COLOR_PRIMARY), (_("comm_btn_ai"), COLOR_PRIMARY), (_("comm_btn_join"), COLOR_PRIMARY)]
        for text, color in btns:
            btn = QPushButton(text); btn.setFixedHeight(42); btn.setStyleSheet(f"background: {color}; color: white; font-weight: bold; border-radius: 8px;")
            row.addWidget(btn)
        self.container_layout.addLayout(row)

    def _add_feedback(self, layout, title, desc, color):
        box = QFrame(); box.setStyleSheet(f"border: 1px solid {COLOR_BORDER}; border-radius: 6px;")
        l = QVBoxLayout(box); t = QLabel(title); t.setStyleSheet(f"color: {color}; font-weight: bold;"); l.addWidget(t)
        d = QLabel(desc); d.setWordWrap(True); l.addWidget(d); layout.addWidget(box)
