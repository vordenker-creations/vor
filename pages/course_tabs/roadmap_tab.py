from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from config import *
from components import SaaSCard

class RoadmapTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        
        card = SaaSCard(); cl = card.internal_layout
        cl.addWidget(QLabel("COURSE LEARNING PATH"))
        
        steps = [
            ("Week 1: Fundamentals", "Setup environment and basic syntax.", True),
            ("Week 2: Advanced OOP", "Classes, Inheritance, and Decorators.", True),
            ("Week 3: Data Analysis", "Pandas and NumPy foundations.", False),
            ("Week 4: Machine Learning", "Scikit-Learn basics.", False)
        ]
        
        for title, desc, done in steps:
            row = QWidget(); rl = QHBoxLayout(row)
            icon = QLabel("✓" if done else "○")
            icon.setStyleSheet(f"color: {COLOR_PRIMARY if done else COLOR_TEXT_SUB}; font-size: 18px; font-weight: bold;")
            rl.addWidget(icon)
            
            info = QVBoxLayout(); t = QLabel(title)
            t.setStyleSheet("font-weight: bold; color: " + (COLOR_TEXT_MAIN if done else COLOR_TEXT_SUB))
            info.addWidget(t); d = QLabel(desc); d.setStyleSheet("font-size: 11px; color: " + COLOR_TEXT_SUB)
            info.addWidget(d); rl.addLayout(info); rl.addStretch()
            cl.addWidget(row)
            
        l.addWidget(card)
