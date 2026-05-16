from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath
import random
import math

class VoiceWaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.is_active = False
        self.amplitudes = [0] * 50
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_amplitudes)
        self.timer.start(50)
        
    def start(self):
        self.is_active = True
        
    def stop(self):
        self.is_active = False
        self.amplitudes = [0] * 50
        self.update()
        
    def _update_amplitudes(self):
        if not self.is_active:
            return
            
        # Shift and add new random amplitude
        self.amplitudes.pop(0)
        self.amplitudes.append(random.uniform(0.1, 1.0))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        center_y = h / 2
        
        spacing = w / len(self.amplitudes)
        
        painter.setPen(Qt.PenStyle.NoPen)
        
        for i, amp in enumerate(self.amplitudes):
            x = i * spacing
            bar_h = amp * h * 0.8
            # Gradient-like effect based on index
            alpha = int(255 * (i / len(self.amplitudes)))
            color = QColor(56, 189, 248, alpha) # #38BDF8
            
            painter.setBrush(QBrush(color))
            # Rounded rect bars
            painter.drawRoundedRect(
                int(x + spacing/4), 
                int(center_y - bar_h/2), 
                int(spacing/2), 
                int(bar_h), 
                3, 3
            )
