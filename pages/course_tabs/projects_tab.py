from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from config import *
from components import SaaSCard

class ProjectsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        card = SaaSCard(); cl = card.internal_layout
        cl.addWidget(QLabel("COURSE PROJECTS"))
        projs = [("Project 1: Personal Website", "Submitted", COLOR_SUCCESS), ("Project 2: Data Dashboard", "Draft", COLOR_WARNING)]
        for name, status, color in projs:
            row = QWidget(); rl = QHBoxLayout(row)
            rl.addWidget(QLabel(name)); rl.addStretch()
            st = QLabel(status); st.setStyleSheet(f"color: {color}; font-weight: bold;")
            rl.addWidget(st); rl.addWidget(QPushButton("View"))
            cl.addWidget(row)
        l.addWidget(card)
