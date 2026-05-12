from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard

class ResultsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Helper function to create items
        def create_item(title, desc):
            w = QWidget()
            l = QVBoxLayout(w)
            l.setContentsMargins(0, 5, 0, 5)
            t = QLabel(title)
            t.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold;")
            d = QLabel(desc)
            d.setStyleSheet(f"color: {COLOR_TEXT_SUB};")
            d.setWordWrap(True)
            l.addWidget(t)
            l.addWidget(d)
            return w

        # Column 1
        c1 = SaaSCard()
        c1.setStyleSheet(f"SaaSCard {{ background-color: {COLOR_BG_CARD}; border: 2px solid #A855F7; border-radius: 16px; }}")
        l1 = c1.internal_layout
        l1.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        t1 = QLabel("Tắm: nay thọt giáp:\n9.2/10")
        t1.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: bold;")
        t1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l1.addWidget(t1)
        
        g1 = QGridLayout()
        g1.addWidget(QLabel("Bài tập: 9.5", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 0, 0)
        g1.addWidget(QLabel("Đồ án: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 0, 1)
        g1.addWidget(QLabel("Bồi án: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 1, 0)
        g1.addWidget(QLabel("Bài tập: 9.5\nKết quả: 9.0", styleSheet=f"color:{COLOR_TEXT_MAIN}"), 1, 1)
        l1.addLayout(g1)
        
        l1.addWidget(QFrame(frameShape=QFrame.Shape.HLine, styleSheet=f"color: {COLOR_BORDER}; margin: 10px 0;"))
        
        l1.addWidget(create_item("Bài tập: viên mano 3.1", "Năm phu báp oo chúng nhận thuật, event haong ập bì rn, un..."))
        l1.addWidget(create_item("Bài tập: viên mano 3.2", "Năm phu hạp con nìrn thạnh, hãn gặc nập chốt custom widget tấu dider."))
        l1.addWidget(create_item("Bài tập: viên mano 3.3", "Năm phu cướp sóng thiểm sở thôi tập van koát."))
        
        s1 = QScrollArea()
        s1.setWidgetResizable(True)
        s1.setWidget(c1)
        s1.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        layout.addWidget(s1, 1)
        
        # Column 2
        c2 = SaaSCard()
        c2.setStyleSheet(f"SaaSCard {{ background-color: {COLOR_BG_CARD}; border: 1px solid {COLOR_BORDER}; border-radius: 16px; }}")
        l2 = c2.internal_layout
        l2.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        l2.addWidget(QLabel("Instructor notes", styleSheet=f"color:{COLOR_TEXT_MAIN}; font-weight: bold; font-size: 14px;"))
        l2.addWidget(create_item("Bài 1: Tổng quan", "Năm phu cáp cao cạo thợ dpaint xa thủi on, pờ khl nọi ccớ rnd chong aren. Mép. lãng lăng chùng nguồn tuyết zờ sự cắt cặng lể tạy fraco giản và hồi olmal gã."))
        l2.addWidget(create_item("BT 3.2: viên mann 5.1", "Năm phu bap báo chứng nhận thuật, event tháng rag tở hòe kon dào mệt, event hanno ấp bỉ rn, un, nâng màn tập event nouse many annát custom widget."))
        l2.addWidget(create_item("BT 5.3: viên mann 3.8", "Năm phu hạp con nìển thạnh, hãn gặc viãn nạng tập. exent hanng nụt nnon tập nẹp chốt custom wiidget the chiler tnun tập the chưer."))
        l2.addWidget(create_item("BT 3.4: viên mann 3.3", "Năm phu hạp căn càn cũng thèm tát, liếp só dọc phủ cặp nập chột custom mạp làm thai hdet."))
        
        s2 = QScrollArea()
        s2.setWidgetResizable(True)
        s2.setWidget(c2)
        s2.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        layout.addWidget(s2, 1)
        
        # Column 3
        c3 = SaaSCard()
        c3.setStyleSheet(f"SaaSCard {{ background-color: {COLOR_BG_CARD}; border: 1px solid {COLOR_BORDER}; border-radius: 16px; }}")
        l3 = c3.internal_layout
        l3.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        l3.addWidget(QLabel("Nutt reviews", styleSheet=f"color:{COLOR_TEXT_MAIN}; font-weight: bold; font-size: 14px;"))
        l3.addWidget(create_item("Bài tập: viên mano 5.1", "Năm phu bap con xàm chên thuật."))
        l3.addWidget(create_item("Bài tập: viên mano 3.3", "Năm phu báp con chống nhận thuật, bant thình nàng hós mănn tập, event atũng, viêuc nnết custom widget.\n\nNăm phu báp con nlim tham hanh kusa, hãn ciắt tiệm kiãng mù tập và từ tấy việt custom thảnh tập nãe roãi."))
        
        l3.addWidget(QFrame(frameShape=QFrame.Shape.HLine, styleSheet=f"color: {COLOR_BORDER}; margin: 10px 0;"))
        
        l3.addWidget(QLabel("Peer reviews", styleSheet=f"color:{COLOR_TEXT_MAIN}; font-weight: bold; font-size: 14px;"))
        l3.addWidget(QLabel("Tide in a peer reviews...", styleSheet=f"color:{COLOR_TEXT_SUB};"))
        
        s3 = QScrollArea()
        s3.setWidgetResizable(True)
        s3.setWidget(c3)
        s3.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        layout.addWidget(s3, 1)
