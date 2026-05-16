from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

class HistoryItem(QFrame):
    clicked = pyqtSignal(int)
    
    def __init__(self, title, timestamp, is_active=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.update_style(is_active)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)
        
        # Icon
        icon_lbl = QLabel("💬")
        icon_lbl.setStyleSheet("font-size: 16px; background: transparent; border: none;")
        layout.addWidget(icon_lbl)
        
        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size: 13px; font-weight: {'700' if is_active else '500'}; color: {'#0284C7' if is_active else '#1E293B'}; border: none; background: transparent;")
        
        time_lbl = QLabel(timestamp)
        time_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; border: none; background: transparent;")
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(time_lbl)
        layout.addLayout(text_layout)
        layout.addStretch()
        
    def update_style(self, is_active):
        if is_active:
            self.setStyleSheet("""
                HistoryItem {
                    background-color: #F0F9FF;
                    border-radius: 12px;
                    border-left: 4px solid #38BDF8;
                }
            """)
        else:
            self.setStyleSheet("""
                HistoryItem {
                    background-color: transparent;
                    border-radius: 12px;
                    border: none;
                }
                HistoryItem:hover {
                    background-color: #F1F5F9;
                }
            """)

    def mousePressEvent(self, event):
        self.clicked.emit(0) # Dummy ID
        super().mousePressEvent(event)

class HistorySidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(20)
        
        # Top Header
        header = QHBoxLayout()
        title = QLabel("AI Assistant")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # New Chat Button
        btn_new = QPushButton("+  New Chat")
        btn_new.setFixedHeight(44)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 12px;
                font-size: 14px; font-weight: 700; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        layout.addWidget(btn_new)
        
        # Search
        search = QLineEdit()
        search.setPlaceholderText("Search conversations...")
        search.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
                padding: 10px 14px; font-size: 13px; color: #1E293B;
            }
            QLineEdit:focus { border: 1px solid #38BDF8; background-color: white; }
        """)
        layout.addWidget(search)
        
        # Chat History List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(4)
        
        chats = [
            ("Resume Optimization", "10:24 AM"),
            ("AI Interview Practice", "Yesterday"),
            ("Python Assignment Help", "Monday"),
            ("Career Roadmap", "May 12"),
            ("Machine Learning Advice", "May 10")
        ]
        
        for i, (chat_title, time) in enumerate(chats):
            item = HistoryItem(chat_title, time, is_active=(i==0))
            self.list_layout.addWidget(item)
            
        self.list_layout.addStretch()
        scroll.setWidget(self.list_widget)
        layout.addWidget(scroll)
        
        # Bottom Section
        bottom = QFrame()
        bottom.setStyleSheet("border-top: 1px solid #E2E8F0; padding-top: 16px;")
        b_layout = QVBoxLayout(bottom)
        b_layout.setContentsMargins(0, 16, 0, 0)
        b_layout.setSpacing(12)
        
        # Credits Info
        credits_card = QFrame()
        credits_card.setStyleSheet("background-color: #F8FAFC; border-radius: 12px; padding: 12px;")
        cl = QVBoxLayout(credits_card)
        cl.setContentsMargins(12, 12, 12, 12)
        cl.setSpacing(8)
        
        cl_top = QHBoxLayout()
        cl_lbl = QLabel("AI Credits")
        cl_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #64748B; border: none;")
        cl_top.addWidget(cl_lbl)
        cl_top.addStretch()
        cl_val = QLabel("850 / 1000")
        cl_val.setStyleSheet("font-size: 11px; font-weight: 700; color: #38BDF8; border: none;")
        cl_top.addWidget(cl_val)
        cl.addLayout(cl_top)
        
        bar = QFrame()
        bar.setFixedHeight(4)
        bar.setStyleSheet("background-color: #E2E8F0; border-radius: 2px;")
        bar_fg = QFrame(bar)
        bar_fg.setFixedHeight(4)
        bar_fg.setFixedWidth(160) # 85%
        bar_fg.setStyleSheet("background-color: #38BDF8; border-radius: 2px;")
        cl.addWidget(bar)
        
        b_layout.addWidget(credits_card)
        
        # User Info
        user = QHBoxLayout()
        user.setSpacing(10)
        avatar = QLabel("JD")
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("background-color: #38BDF8; color: white; border-radius: 16px; font-size: 12px; font-weight: 700;")
        user.addWidget(avatar)
        
        u_info = QVBoxLayout()
        u_info.setSpacing(0)
        u_name = QLabel("John Doe")
        u_name.setStyleSheet("font-size: 13px; font-weight: 700; color: #0F172A; border: none;")
        u_plan = QLabel("Pro Plan")
        u_plan.setStyleSheet("font-size: 11px; color: #64748B; border: none;")
        u_info.addWidget(u_name)
        u_info.addWidget(u_plan)
        user.addLayout(u_info)
        user.addStretch()
        
        b_layout.addLayout(user)
        layout.addWidget(bottom)
