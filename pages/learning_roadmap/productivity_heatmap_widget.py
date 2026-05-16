from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen

class HeatmapCell(QFrame):
    def __init__(self, intensity, parent=None):
        super().__init__(parent)
        self.setFixedSize(14, 14)
        colors = ["#F1F5F9", "#BAE6FD", "#7DD3FC", "#38BDF8", "#0284C7"]
        color = colors[min(intensity, 4)]
        self.setStyleSheet(f"background: {color}; border-radius: 3px; border: none;")

class ProductivityHeatmapWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        l = QVBoxLayout(self)
        l.setContentsMargins(24, 24, 24, 24)
        l.setSpacing(16)
        
        t_h = QHBoxLayout()
        t = QLabel("Productivity Heatmap")
        t.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; border: none;")
        t_h.addWidget(t)
        t_h.addStretch()
        l.addLayout(t_h)
        
        # Heatmap Grid (Weeks x Days)
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(4)
        grid.setContentsMargins(0, 0, 0, 0)
        
        import random
        for week in range(20):
            for day in range(7):
                intensity = random.randint(0, 4) if random.random() > 0.3 else 0
                cell = HeatmapCell(intensity)
                grid.addWidget(cell, day, week)
                
        l.addWidget(grid_container)
        
        # Legend
        leg_h = QHBoxLayout()
        leg_h.addStretch()
        leg_h.addWidget(QLabel("Less", styleSheet="font-size: 11px; color: #64748B; border: none;"))
        for i in range(5):
            leg_h.addWidget(HeatmapCell(i))
        leg_h.addWidget(QLabel("More", styleSheet="font-size: 11px; color: #64748B; border: none;"))
        l.addLayout(leg_h)
