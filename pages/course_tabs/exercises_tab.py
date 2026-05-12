from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, AnimatedProgressBar

class ExercisesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side - 2 columns for exercises
        exercises_layout = QGridLayout()
        exercises_layout.setSpacing(15)
        
        exercise_data = [
            {"title": "BT 3.1. Việt custom widget cho Slider", "date": "Nộp key 12/07/2022", "done": True},
            {"title": "BT 3.1. Việt custom widget cho Slider", "date": "Nộp key 15/07/2022", "done": True},
            {"title": "BT 3.2. Việt custom widget cho Slider", "date": "Nộp key 12/12/2022", "done": True},
            {"title": "BT 3.2. Việt custom widget cho Slider", "date": "Nộp key 12/03/2022", "done": True},
            {"title": "BT 3.1. Việt custom widget cho Slider", "date": "Nộp key 11/10/2022", "done": True},
            {"title": "BT 3.3. Việt custom widget cho ẩn", "date": "Nộp key 12/13/2022", "done": True},
            {"title": "BT 3.4. Việt custom widget cho ẩn", "date": "Nộp key 13/10/2022", "done": False},
            {"title": "BT 3.4. Việt custom widget cho ẩn", "date": "Nộp key 13/10/2022", "done": False},
        ]
        
        row, col = 0, 0
        for data in exercise_data:
            card = SaaSCard()
            card.setStyleSheet(f"SaaSCard {{ background-color: {COLOR_BG_CARD}; border: 1px solid {COLOR_BORDER}; border-radius: 8px; }}")
            cl = card.internal_layout
            cl.setContentsMargins(15, 15, 15, 15)
            
            top_ly = QHBoxLayout()
            icon_lbl = QLabel("✔️" if data['done'] else "⭕")
            icon_lbl.setStyleSheet(f"color: {COLOR_SUCCESS if data['done'] else COLOR_TEXT_SUB}; font-size: 16px;")
            title_lbl = QLabel(data['title'])
            title_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; font-size: 14px;")
            title_lbl.setWordWrap(True)
            top_ly.addWidget(icon_lbl)
            top_ly.addWidget(title_lbl, 1)
            cl.addLayout(top_ly)
            
            date_lbl = QLabel(data['date'])
            date_lbl.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
            date_lbl.setContentsMargins(25, 0, 0, 0)
            cl.addWidget(date_lbl)
            
            btn_ly = QHBoxLayout()
            btn_ly.addStretch()
            btn = QPushButton("Nộp bài")
            btn.setStyleSheet(f"background-color: {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}; border: none; padding: 5px 15px; border-radius: 4px;")
            btn_ly.addWidget(btn)
            cl.addLayout(btn_ly)
            
            exercises_layout.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        # Main left widget
        left_widget = QWidget()
        left_widget.setLayout(exercises_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(left_widget)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; } QWidget#qt_scrollarea_viewport { background-color: transparent; }")
        layout.addWidget(scroll, 2)
        
        # Right side - Statistics
        stats_card = SaaSCard()
        stats_layout = stats_card.internal_layout
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        stats_title = QLabel("Statistics")
        stats_title.setStyleSheet(f"color: {COLOR_SUCCESS}; font-size: 20px; font-weight: bold;")
        stats_layout.addWidget(stats_title)
        
        sub_title = QLabel("Staiioz stác:")
        sub_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold; margin-top: 10px;")
        stats_layout.addWidget(sub_title)
        
        stats_data = [("Assignment 1:", "3"), ("Bồi án rương:", "4"), ("Bồi án:", "9.5"), ("Biết quá:", "6k qu.á")]
        for k, v in stats_data:
            rl = QHBoxLayout()
            rl.addWidget(QLabel(k, styleSheet=f"color: {COLOR_TEXT_MAIN};"))
            rl.addStretch()
            rl.addWidget(QLabel(v, styleSheet=f"color: {COLOR_TEXT_MAIN};"))
            stats_layout.addLayout(rl)
            
        team_title = QLabel("Team lai:")
        team_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold; margin-top: 15px;")
        stats_layout.addWidget(team_title)
        
        team_lbl = QLabel("• Nân nhí hh, Ftuyen\n• Nguồn ling, Atuyen")
        team_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; margin-left: 10px;")
        stats_layout.addWidget(team_lbl)
        
        stats_label = QLabel("Statistics: 66")
        stats_label.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 15px;")
        stats_layout.addWidget(stats_label)
        
        # Progress Bars for Chặng stats and Milestone S
        ch_ly = QHBoxLayout()
        ch_ly.addWidget(QLabel("Chặng stats:", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold;"))
        ch_ly.addStretch()
        ch_ly.addWidget(QLabel("10", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold;"))
        stats_layout.addLayout(ch_ly)
        
        pb1 = AnimatedProgressBar(color="#00A2FF")
        pb1.set_target(0.6)
        stats_layout.addWidget(pb1)
        
        ml_ly = QHBoxLayout()
        ml_ly.addWidget(QLabel("Milestone s:", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold;"))
        ml_ly.addStretch()
        ml_ly.addWidget(QLabel("2.5", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold;"))
        stats_layout.addLayout(ml_ly)
        
        pb2 = AnimatedProgressBar(color="#00A2FF")
        pb2.set_target(0.4)
        stats_layout.addWidget(pb2)
        
        layout.addWidget(stats_card, 1)
