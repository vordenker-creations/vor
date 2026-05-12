from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from config import *
from components import SaaSCard

class ExercisesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        card = SaaSCard(); cl = card.internal_layout
        cl.addWidget(QLabel("EXERCISES & QUIZZES"))
        exs = [("Ex 1: Python Basics", "Completed", COLOR_SUCCESS), ("Ex 2: Data Structures", "In Progress", COLOR_WARNING), ("Ex 3: Web Scraping", "Not Started", COLOR_TEXT_SUB)]
        for name, status, color in exs:
            row = QWidget(); rl = QHBoxLayout(row)
            rl.addWidget(QLabel(name)); rl.addStretch()
            st = QLabel(status); st.setStyleSheet(f"color: {color}; font-weight: bold;")
            rl.addWidget(st); rl.addWidget(QPushButton("Open"))
            cl.addWidget(row)
        l.addWidget(card)
