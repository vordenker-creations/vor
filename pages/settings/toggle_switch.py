from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QBrush, QCursor

class ToggleSwitch(QWidget):
    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self._checked = checked
        self._thumb_pos = 22 if checked else 2
        
        self.animation = QPropertyAnimation(self, b"thumb_pos")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    @pyqtProperty(int)
    def thumb_pos(self):
        return self._thumb_pos
        
    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            self.animation.setStartValue(self._thumb_pos)
            self.animation.setEndValue(22 if self._checked else 2)
            self.animation.start()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bg_color = QColor("#38BDF8") if self._checked else QColor("#E2E8F0")
        painter.setBrush(QBrush(bg_color)); painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        painter.setBrush(QBrush(QColor("#FFFFFF"))); painter.drawEllipse(self._thumb_pos, 2, 20, 20)
