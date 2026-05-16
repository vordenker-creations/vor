from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from .toggle_switch import ToggleSwitch

class ToggleRow(QWidget):
    def __init__(self, title, desc, parent=None):
        super().__init__(parent)
        l = QHBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        
        v = QVBoxLayout()
        v.setSpacing(2)
        t = QLabel(title)
        t.setStyleSheet("font-weight: 600; font-size: 13px; color: #1E293B; border: none;")
        d = QLabel(desc)
        d.setStyleSheet("font-size: 12px; color: #64748B; border: none;")
        v.addWidget(t); v.addWidget(d)
        l.addLayout(v)
        
        l.addStretch()
        self.toggle = ToggleSwitch()
        l.addWidget(self.toggle)
