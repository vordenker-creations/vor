from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from config import *
from components import SaaSCard

class AnalyticsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        card = SaaSCard(); cl = card.internal_layout
        cl.addWidget(QLabel("LEARNING ANALYTICS"))
        cl.addWidget(QLabel("Activity over time: [Chart Placeholder]"))
        l.addWidget(card)
