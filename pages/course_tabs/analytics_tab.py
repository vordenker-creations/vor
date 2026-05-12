from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, AnimatedProgressBar

class AnalyticsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Side - Bar Chart
        left_card = SaaSCard()
        ll = left_card.internal_layout
        ll.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        top_ly = QHBoxLayout()
        top_ly.addWidget(QLabel("Overal course trong trem khán các", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold;"))
        top_ly.addStretch()
        
        legend_ly = QHBoxLayout()
        lg1 = QLabel("■ Giảng")
        lg1.setStyleSheet("color: #718096;")
        lg2 = QLabel("■ Strong")
        lg2.setStyleSheet("color: #A0AEC0;")
        legend_ly.addWidget(lg1)
        legend_ly.addWidget(lg2)
        top_ly.addLayout(legend_ly)
        
        ll.addLayout(top_ly)
        
        # Simulated Bar Chart
        chart_area = QWidget()
        chart_layout = QHBoxLayout(chart_area)
        chart_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart_layout.setSpacing(20)
        
        y_axis = QVBoxLayout()
        for v in ["120%", "100%", "80%", "60%", "40%", "20%", "0%"]:
            y_axis.addWidget(QLabel(v, styleSheet=f"color: {COLOR_TEXT_SUB}; font-size: 10px;"))
        chart_layout.addLayout(y_axis)
        
        bars = [0.4, 0.6, 0.5, 0.9, 0.8]
        labels = ["Toàn", "Toàn", "Nguyên", "Thống iến", "Mán"]
        
        bars_layout = QHBoxLayout()
        bars_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        for h, lbl in zip(bars, labels):
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
            bar = QFrame()
            bar.setStyleSheet("background-color: #A0AEC0;")
            bar.setFixedSize(30, int(h * 200)) # Simple height
            col.addWidget(bar, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
            col.addWidget(QLabel(lbl, styleSheet=f"color: {COLOR_TEXT_SUB}; font-size: 10px;"), alignment=Qt.AlignmentFlag.AlignHCenter)
            bars_layout.addLayout(col)
            
        chart_layout.addLayout(bars_layout)
        ll.addWidget(chart_area)
        
        # Bottom text
        ll.addWidget(QFrame(frameShape=QFrame.Shape.HLine, styleSheet=f"color: {COLOR_BORDER}; margin: 10px 0;"))
        
        bl1 = QHBoxLayout()
        bl1.addWidget(QLabel("Key nung giáp:", styleSheet=f"color:{COLOR_TEXT_MAIN}; font-weight: bold;"))
        bl1.addStretch()
        ll.addLayout(bl1)
        
        bl2 = QHBoxLayout()
        bl2.addWidget(QLabel("Bài tập: 9.0\nĐồ án: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN};"))
        bl2.addWidget(QLabel("Bài tập: 9.0\nBiết quả: 9.5", styleSheet=f"color:{COLOR_TEXT_MAIN};"))
        bl2.addWidget(QLabel("Bài tập: 9.0\nthinpoont", styleSheet=f"color:{COLOR_TEXT_MAIN};"))
        ll.addLayout(bl2)
        
        layout.addWidget(left_card, 2)
        
        # Right Side - KPIs
        right_card = SaaSCard()
        rl = right_card.internal_layout
        rl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        rl.addWidget(QLabel("Key nung giáp:", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold;"))
        
        g1 = QGridLayout()
        g1.addWidget(QLabel("Bài tập: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 0, 0)
        g1.addWidget(QLabel("Bài tập: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 0, 1)
        g1.addWidget(QLabel("Bồi án: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 1, 0)
        g1.addWidget(QLabel("Biết quả: 9.5", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 1, 1)
        rl.addLayout(g1)
        
        rl.addWidget(QLabel("Comparison", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 15px;"))
        
        for k, v in [("112ph", 0.95), ("12qn", 0.32), ("12qn", 0.67), ("12qn", 0.65)]:
            h = QHBoxLayout()
            h.addWidget(QLabel(k, styleSheet=f"color:{COLOR_TEXT_SUB}; font-size: 10px;"))
            pb = AnimatedProgressBar(color="#CBD5E0")
            pb.set_target(v)
            h.addWidget(pb)
            h.addWidget(QLabel(f"{int(v*100)}%", styleSheet=f"color:{COLOR_TEXT_SUB}; font-size: 10px;"))
            rl.addLayout(h)
            
        rl.addWidget(QLabel("Key skills gap", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 15px;"))
        
        tbl = QGridLayout()
        tbl.addWidget(QLabel("Vã cg", styleSheet=f"color:{COLOR_TEXT_SUB}; font-size: 10px;"), 0, 1)
        tbl.addWidget(QLabel("Sloàng", styleSheet=f"color:{COLOR_TEXT_SUB}; font-size: 10px;"), 0, 2)
        
        skills = [("Tdan", "9.0", "5.0"), ("Tim-long", "9.0", "5.5"), ("Thông", "9.0", "5.5"), ("Trỏan", "9.0", "5.5")]
        for i, (k, v1, v2) in enumerate(skills):
            tbl.addWidget(QLabel(k, styleSheet=f"color:{COLOR_TEXT_MAIN}; font-size: 11px;"), i+1, 0)
            tbl.addWidget(QLabel(v1, styleSheet=f"color:{COLOR_TEXT_MAIN}; font-size: 11px;"), i+1, 1)
            tbl.addWidget(QLabel(v2, styleSheet=f"color:{COLOR_TEXT_MAIN}; font-size: 11px;"), i+1, 2)
        rl.addLayout(tbl)
        
        layout.addWidget(right_card, 1)
