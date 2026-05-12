from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QWidget, QLabel, QProgressBar, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRectF, QTimer
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor
from config import COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY, COLOR_BG_APP, COLOR_TEXT_MAIN, COLOR_TEXT_SUB, COLOR_PRIMARY_LIGHT

class SaaSCard(QFrame):
    def __init__(self, parent=None, border_color=COLOR_BORDER):
        super().__init__(parent)
        self.border_color = border_color
        self._update_style(self.border_color)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)
    def _update_style(self, b_color):
        self.setStyleSheet(f"SaaSCard {{ background-color: {COLOR_BG_CARD}; border: 1px solid {b_color}; border-radius: 16px; }}")
    def enterEvent(self, event):
        self._update_style(COLOR_PRIMARY)
        super().enterEvent(event)
    def leaveEvent(self, event):
        self._update_style(self.border_color)
        super().leaveEvent(event)

class AnimatedProgressBar(QProgressBar):
    def __init__(self, color=COLOR_PRIMARY, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setFixedHeight(6)
        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {COLOR_BORDER};
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        self._value = 0
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(1000)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(int)
    def value(self): return self._value
    
    @value.setter
    def value(self, val):
        self._value = val
        super().setValue(val)

    def set_target(self, progress_float):
        self.animation.setEndValue(int(progress_float * 100))
        self.animation.start()

class StatusPulse(QWidget):
    def __init__(self, color=COLOR_PRIMARY, size=8, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

class ChipButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(32)
        self.setStyleSheet(f"""
            QPushButton {{ 
                background: {COLOR_BG_APP}; 
                color: {COLOR_PRIMARY}; 
                border: 1px solid {COLOR_BORDER}; 
                border-radius: 16px; 
                padding: 0 15px; 
                font-weight: bold; 
                font-size: 12px; 
            }} 
            QPushButton:hover {{ 
                background: {COLOR_PRIMARY_LIGHT}; 
            }}
        """)

class AnimatedCircularProgress(QWidget):
    def __init__(self, parent=None, size=100, color=COLOR_PRIMARY):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._value = 0
        self.color = color
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(1500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    @pyqtProperty(float)
    def value(self): return self._value
    @value.setter
    def value(self, val):
        self._value = val
        self.update()
    def set_target(self, val):
        self.animation.setEndValue(val)
        self.animation.start()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(10, 10, self.width()-20, self.height()-20)
        painter.setPen(QPen(QColor(COLOR_BORDER), 8))
        painter.drawEllipse(rect)
        painter.setPen(QPen(QColor(self.color), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(rect, 90 * 16, int(-self._value * 360 * 16))
        painter.setPen(QColor(COLOR_TEXT_MAIN))
        font = painter.font(); font.setBold(True); font.setPointSize(int(self.width() * 0.15)); painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(self._value * 100)}%")

class AnimationEngine:
    @staticmethod
    def fade_in_widget(widget, delay_ms=0, duration=600):
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)
        anim = QPropertyAnimation(opacity_effect, b"opacity")
        anim.setStartValue(0.0); anim.setEndValue(1.0); anim.setDuration(duration)
        if delay_ms > 0: QTimer.singleShot(delay_ms, anim.start)
        else: anim.start()
        if not hasattr(widget, '_anims'): widget._anims = []
        widget._anims.append(anim)

class CountUpLabel(QLabel):
    def __init__(self, format_str="{}", suffix="", parent=None):
        super().__init__(parent)
        self.format_str = format_str; self.suffix = suffix
        self._curr = 0; self._target = 0
        self.timer = QTimer(self); self.timer.timeout.connect(self._upd)
    def set_target(self, val):
        try:
            self._target = float(val)
            if not self.timer.isActive():
                self.timer.start(30)
        except: self.setText(str(val) + self.suffix)
    def _upd(self):
        if abs(self._curr - self._target) < 0.1:
            self._curr = self._target; self.timer.stop()
        else: self._curr += (self._target - self._curr) / 10
        self.setText(self.format_str.format(int(self._curr)) + self.suffix)
