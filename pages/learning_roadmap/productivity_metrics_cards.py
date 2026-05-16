from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QProgressBar, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen

class AnalyticsMetricCard(QFrame):
    def __init__(self, title, value, trend, subtext, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setFixedHeight(160)
        self.setStyleSheet(f"""
            QFrame {{
                background: white; border: 1px solid #E2E8F0; border-radius: 22px;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(15, 23, 42, 10))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(12)
        
        # Header
        head = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; border: none;")
        head.addWidget(t_lbl)
        head.addStretch()
        
        tr_lbl = QLabel(trend)
        tr_color = "#10B981" if "+" in trend else "#EF4444"
        tr_lbl.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {tr_color}; background: {tr_color}15; padding: 2px 8px; border-radius: 6px; border: none;")
        head.addWidget(tr_lbl)
        l.addLayout(head)
        
        # Value
        v_lbl = QLabel(value)
        v_lbl.setStyleSheet("font-size: 26px; font-weight: 800; color: #0F172A; border: none;")
        l.addWidget(v_lbl)
        
        # Subtext
        s_lbl = QLabel(subtext)
        s_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none; font-weight: 500;")
        l.addWidget(s_lbl)
        
        l.addStretch()

class ProgressMetricCard(QFrame):
    def __init__(self, title, val, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        
        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(8)
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; text-transform: uppercase; border: none;")
        l.addWidget(t)
        
        v_h = QHBoxLayout()
        v_lbl = QLabel(f"{val}%")
        v_lbl.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {color}; border: none;")
        v_h.addWidget(v_lbl)
        v_h.addStretch()
        l.addLayout(v_h)
        
        pb = QProgressBar()
        pb.setFixedHeight(6)
        pb.setValue(val)
        pb.setTextVisible(False)
        pb.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border-radius: 3px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}")
        l.addWidget(pb)
