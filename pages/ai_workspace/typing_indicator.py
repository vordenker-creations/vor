from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

class TypingIndicator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setFixedWidth(100)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 15px; border-bottom-left-radius: 4px;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(6)
        
        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet("color: #CBD5E1; font-size: 10px;")
            layout.addWidget(dot)
            self.dots.append(dot)
            
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(400)
        self.counter = 0

    def _animate(self):
        for i, dot in enumerate(self.dots):
            if i == self.counter % 3:
                dot.setStyleSheet("color: #38BDF8; font-size: 10px;")
            else:
                dot.setStyleSheet("color: #CBD5E1; font-size: 10px;")
        self.counter += 1
