from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from config import *
from components import SaaSCard

class ResultsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        card = SaaSCard(); cl = card.internal_layout
        cl.addWidget(QLabel("GRADES & RESULTS"))
        res = [("Midterm Exam", "8.5 / 10", COLOR_SUCCESS), ("Assignment 1", "9.0 / 10", COLOR_SUCCESS), ("Quiz 1", "7.0 / 10", COLOR_WARNING)]
        for name, score, color in res:
            row = QWidget(); rl = QHBoxLayout(row)
            rl.addWidget(QLabel(name)); rl.addStretch()
            sc = QLabel(score); sc.setStyleSheet(f"color: {color}; font-weight: bold;")
            rl.addWidget(sc)
            cl.addWidget(row)
        l.addWidget(card)
