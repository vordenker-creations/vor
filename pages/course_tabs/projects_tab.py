from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, AnimatedProgressBar

class ProjectsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Side - Project Details
        left_card = SaaSCard()
        ll = left_card.internal_layout
        ll.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = QLabel("Đồ án cuối khóa: Ứng dụng Quản lý Nhân sự")
        title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: bold;")
        ll.addWidget(title)
        
        lbl_outline = QLabel("Dự án outline:")
        lbl_outline.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 10px;")
        ll.addWidget(lbl_outline)
        
        outline_text = "• Milestone 1: Thailing\n• Milestone 2: Truan\n• Milestone 3: Truan\n• Milestone 4: Thailing"
        out_lbl = QLabel(outline_text)
        out_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; margin-left: 10px;")
        ll.addWidget(out_lbl)
        
        lbl_team = QLabel("Team lai:")
        lbl_team.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 10px;")
        ll.addWidget(lbl_team)
        
        team_text = "• Nân nhí hh, Ftuyen\n• Nguồn ling, Atuyen"
        team_lbl = QLabel(team_text)
        team_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; margin-left: 10px;")
        ll.addWidget(team_lbl)
        
        lbl_tl = QLabel("Timeline:")
        lbl_tl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 10px;")
        ll.addWidget(lbl_tl)
        
        pb_tl = AnimatedProgressBar(color="#3b82f6")
        pb_tl.set_target(0.7)
        ll.addWidget(pb_tl)
        
        # Chặng status
        ch_ly = QHBoxLayout()
        ch_ly.addWidget(QLabel("Chặng status:", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 10px;"))
        ch_ly.addStretch()
        ch_ly.addWidget(QLabel("Current status", styleSheet=f"color: {COLOR_TEXT_SUB}; margin-top: 10px;"))
        ll.addLayout(ch_ly)
        
        pb_ch = AnimatedProgressBar(color="#3b82f6")
        pb_ch.set_target(0.5)
        ll.addWidget(pb_ch)
        
        lbl_out2 = QLabel("Outline:")
        lbl_out2.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; margin-top: 10px;")
        ll.addWidget(lbl_out2)
        
        out2_text = "• Milestone 1:\n• Milestone 2:\n• Milestone 3:\n• Milestone 4:\n• Nguồn hãng"
        out2_lbl = QLabel(out2_text)
        out2_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; margin-left: 10px;")
        ll.addWidget(out2_lbl)
        
        scroll_left = QScrollArea()
        scroll_left.setWidgetResizable(True)
        scroll_left.setWidget(left_card)
        scroll_left.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        layout.addWidget(scroll_left, 2)
        
        # Right Side - Chat
        right_layout = QVBoxLayout()
        
        chat_card = SaaSCard()
        cl = chat_card.internal_layout
        cl.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_chat = QLabel("Mọi group chat")
        lbl_chat.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; font-size: 14px;")
        cl.addWidget(lbl_chat)
        
        msg1 = QLabel("<b>Viên mano 0.1</b><br>Năm phuro op bìn slhọc, màn tập custom widget.")
        msg1.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; background-color: {COLOR_BG_APP}; padding: 10px; border-radius: 8px; margin-top: 10px;")
        msg1.setWordWrap(True)
        cl.addWidget(msg1)
        
        msg2 = QLabel("<b>Viên mano 02</b><br>Năm phu cap củo mún thris, bác nập chất build mings ítlá choác")
        msg2.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; background-color: {COLOR_BG_APP}; padding: 10px; border-radius: 8px; margin-top: 10px;")
        msg2.setWordWrap(True)
        cl.addWidget(msg2)
        
        cl.addStretch()
        right_layout.addWidget(chat_card, 1)
        
        input_card = SaaSCard()
        il = input_card.internal_layout
        
        lbl_grp = QLabel("Group chat")
        lbl_grp.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold;")
        il.addWidget(lbl_grp)
        
        input_box = QLineEdit()
        input_box.setPlaceholderText("Com ecat or milestons...")
        input_box.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 4px; padding: 10px; color: {COLOR_TEXT_MAIN}")
        il.addWidget(input_box)
        
        btn_ly = QHBoxLayout()
        btn_ly.addStretch()
        btn_send = QPushButton("Send")
        btn_send.setStyleSheet(f"background-color: {COLOR_PRIMARY}; color: {COLOR_TEXT_MAIN}; border: none; padding: 8px 20px; border-radius: 4px;")
        btn_ly.addWidget(btn_send)
        il.addLayout(btn_ly)
        
        right_layout.addWidget(input_card)
        
        layout.addLayout(right_layout, 1)
