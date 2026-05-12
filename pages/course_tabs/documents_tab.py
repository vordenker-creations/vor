from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from config import *
from components import SaaSCard

class DocumentsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        card = SaaSCard(); cl = card.internal_layout
        cl.addWidget(QLabel("RESOURCES & DOCUMENTS"))
        docs = [("Lecture_Notes_01.pdf", "PDF"), ("Advanced_OOP.mp4", "Video"), ("Assignment_Guide.docx", "Doc")]
        for name, type in docs:
            row = QWidget(); rl = QHBoxLayout(row)
            rl.addWidget(QLabel("📄" if type=="PDF" else "🎬" if type=="Video" else "📝"))
            rl.addWidget(QLabel(name)); rl.addStretch(); rl.addWidget(QPushButton("Download"))
            cl.addWidget(row)
        l.addWidget(card)
