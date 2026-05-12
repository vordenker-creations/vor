from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard

class SkillTreeGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(400)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(COLOR_PRIMARY), 2))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Skill Tree Graph Rendering...")

class SkillTreeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(5,5,5,5)
        card = SaaSCard(); l.addWidget(card)
        cl = card.internal_layout
        cl.addWidget(QLabel("4-YEAR CAREER ROADMAP: SKILL TREE"))
        cl.addWidget(SkillTreeGraph())
