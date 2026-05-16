from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen, QRadialGradient

class NeuralNode(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(10, 10)
        self.color = QColor("#38BDF8")
        self.opacity = 0.5
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = self.color
        c.setAlphaF(self.opacity)
        painter.setBrush(c)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

class AIMetricsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #0F172A; border-radius: 22px; border: 1px solid #1E293B;")
        self.setMinimumHeight(240)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header
        head = QHBoxLayout()
        t = QLabel("AI Interaction Intelligence")
        t.setStyleSheet("font-size: 15px; font-weight: 800; color: #38BDF8; border: none;")
        head.addWidget(t); head.addStretch()
        
        badge = QLabel("GPT-4 Omni")
        badge.setStyleSheet("font-size: 10px; font-weight: 800; color: white; background: #38BDF833; padding: 2px 8px; border-radius: 6px; border: 1px solid #38BDF8;")
        head.addWidget(badge)
        layout.addLayout(head)
        
        # Metrics
        grid = QGridLayout()
        grid.setSpacing(20)
        
        def add_metric(label, val, r, c):
            v = QVBoxLayout(); v.setSpacing(4)
            l1 = QLabel(label); l1.setStyleSheet("font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
            l2 = QLabel(val); l2.setStyleSheet("font-size: 22px; font-weight: 800; color: white;")
            v.addWidget(l1); v.addWidget(l2); grid.addLayout(v, r, c)
            
        add_metric("Requests", "1,240", 0, 0)
        add_metric("Avg. Latency", "1.2s", 0, 1)
        add_metric("Token Usage", "452k", 1, 0)
        add_metric("Productivity Lift", "32%", 1, 1)
        
        layout.addLayout(grid)
        
        # Simulated Neural Visual
        self.visual_frame = QFrame()
        self.visual_frame.setFixedHeight(60)
        self.visual_frame.setStyleSheet("background: rgba(56, 189, 248, 0.05); border-radius: 12px;")
        vl = QHBoxLayout(self.visual_frame); vl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        for _ in range(8):
            node = NeuralNode()
            vl.addWidget(node)
            
        layout.addWidget(self.visual_frame)
