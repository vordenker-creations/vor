from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, AnimatedCircularProgress

class OverviewTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        c = QWidget(); scroll.setWidget(c); cl = QVBoxLayout(c); cl.setContentsMargins(5,5,5,5)
        
        h = QHBoxLayout(); lbl_w = QLabel("WELCOME BACK, KHANG! "); lbl_w.setStyleSheet("font-size: 24px; font-weight: bold;")
        h.addWidget(lbl_w); lbl_s = QLabel("EXPLORE YOUR JOURNEY."); lbl_s.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_SUCCESS};")
        h.addWidget(lbl_s); h.addStretch(); cl.addLayout(h)
        
        grid = QGridLayout(); grid.setSpacing(10)
        c1 = SaaSCard(); c1l = c1.internal_layout; c1l.addWidget(QLabel("ROADMAP PROGRESS:"))
        ring = AnimatedCircularProgress(size=120); c1l.addWidget(ring, alignment=Qt.AlignmentFlag.AlignCenter); ring.set_target(0.65)
        grid.addWidget(c1, 0, 0)
        
        c2 = SaaSCard(); c2l = c2.internal_layout; c2l.addWidget(QLabel("CREDITS ACCUMULATED:"))
        lbl_cr = QLabel("84 / 120"); lbl_cr.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_PRIMARY};"); c2l.addWidget(lbl_cr)
        grid.addWidget(c2, 0, 1)
        
        c3 = SaaSCard(); c3l = c3.internal_layout; c3l.addWidget(QLabel("GPA:")); lbl_gpa = QLabel("3.8")
        lbl_gpa.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_SUCCESS};"); c3l.addWidget(lbl_gpa)
        grid.addWidget(c3, 0, 2)
        
        c4 = SaaSCard(); c4l = c4.internal_layout; c4l.addWidget(QLabel("CV JOB MATCH: 92%"))
        grid.addWidget(c4, 0, 3)
        cl.addLayout(grid)
        
        bot = QHBoxLayout(); cl_j = SaaSCard(); lj = cl_j.internal_layout; lj.addWidget(QLabel("LEARNING JOURNEY UPDATE"))
        pb = QProgressBar(); pb.setValue(80); pb.setStyleSheet(f"QProgressBar::chunk {{ background: {COLOR_SUCCESS}; }}"); lj.addWidget(pb)
        bot.addWidget(cl_j, 3); cl_e = SaaSCard(); le = cl_e.internal_layout; le.addWidget(QLabel("UPCOMING EVENTS"))
        bot.addWidget(cl_e, 2); cl.addLayout(bot)
        l.addWidget(scroll)
