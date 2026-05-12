from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard

class TimetableTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        c = QWidget(); scroll.setWidget(c); cl = QVBoxLayout(c)
        
        h = QHBoxLayout(); h.addWidget(QLabel("SMART TIMETABLE")); h.addStretch(); cl.addLayout(h)
        
        grid_widget = QWidget(); grid = QGridLayout(grid_widget); grid.setColumnStretch(0, 8); grid.setColumnStretch(1, 3)
        
        sheet = SaaSCard()
        inner_sheet = QWidget()
        sl = QGridLayout(inner_sheet); sl.setContentsMargins(10,10,10,10)
        days = ["TIME", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i, d in enumerate(days): sl.addWidget(QLabel(d), 0, i)
        
        for h in range(6, 24):
            sl.addWidget(QLabel(f"{h:02d}:00"), h-5, 0)
        sheet.internal_layout.addWidget(inner_sheet)
            
        grid.addWidget(sheet, 0, 0)
        
        sidebar = SaaSCard()
        sidebar.internal_layout.addWidget(QLabel("REMINDERS"))
        grid.addWidget(sidebar, 0, 1)
        
        cl.addWidget(grid_widget)
        l.addWidget(scroll)

