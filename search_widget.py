from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QFrame, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QColor, QIcon, QFont, QCursor

class PremiumSearchWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(38)
        self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.is_collapsed = False
        
        # Smooth Opacity Effect for collapse
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.setObjectName("PremiumSearch")
        self.setStyleSheet("""
            QFrame#PremiumSearch {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QFrame#PremiumSearch:hover {
                border: 1px solid #CBD5E1;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        
        self.icon_label = QLabel("🔍") 
        self.icon_label.setStyleSheet("font-size: 13px; color: #94A3B8; border: none; background: transparent;")
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Search anything...")
        self.input.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                color: #0F172A;
                font-size: 13px;
                font-weight: 500;
                padding: 0;
            }
        """)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.input, 1)
        
        self.input.focusInEvent = self._handle_focus_in
        self.input.focusOutEvent = self._handle_focus_out

    def _handle_focus_in(self, event):
        self.setStyleSheet("""
            QFrame#PremiumSearch {
                background-color: #FFFFFF;
                border: 1.5px solid #38BDF8;
                border-radius: 12px;
            }
        """)
        QLineEdit.focusInEvent(self.input, event)

    def _handle_focus_out(self, event):
        self.setStyleSheet("""
            QFrame#PremiumSearch {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QFrame#PremiumSearch:hover {
                border: 1px solid #CBD5E1;
            }
        """)
        QLineEdit.focusOutEvent(self.input, event)

    def setCollapsed(self, collapsed):
        if self.is_collapsed == collapsed:
            return
        self.is_collapsed = collapsed
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        if collapsed:
            self.anim.setStartValue(1.0)
            self.anim.setEndValue(0.0)
            self.anim.finished.connect(self.hide)
        else:
            self.show()
            self.anim.setStartValue(0.0)
            self.anim.setEndValue(1.0)
            try:
                self.anim.finished.disconnect(self.hide)
            except Exception:
                pass
            
        self.anim.start()
