from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard

class YearDetailsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        c = QWidget(); scroll.setWidget(c); cl = QVBoxLayout(c)
        
        h = QHBoxLayout(); h.addWidget(QLabel("EXPANDED Y1 DETAILS (Y1 YEAR 1)")); h.addStretch(); cl.addLayout(h)
        
        grid_widget = QWidget(); grid = QGridLayout(grid_widget)
        s1 = SaaSCard(); s1l = s1.internal_layout; s1l.addWidget(QLabel("Y1 SEMESTER 1: FOUNDATIONS"))
        grid.addWidget(s1, 0, 0)
        s2 = SaaSCard(); s2l = s2.internal_layout; s2l.addWidget(QLabel("Y1 SEMESTER 2: CORE CONCEPTS"))
        grid.addWidget(s2, 0, 1)
        cl.addWidget(grid_widget)
        l.addWidget(scroll)

