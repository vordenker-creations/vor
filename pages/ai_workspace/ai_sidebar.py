from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class NavButton(QPushButton):
    def __init__(self, text, icon="○", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 10px 16px;
                color: #64748B;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                color: #0F172A;
            }
            QPushButton:checked {
                background-color: #E0F2FE;
                color: #0284C7;
                font-weight: 600;
            }
        """)

class ConversationCard(QPushButton):
    def __init__(self, title, time, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 14px;
                text-align: left;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #F8FAFC;
            }
            QPushButton:checked {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #1E293B; border: none; background: transparent;")
        
        self.time_lbl = QLabel(time)
        self.time_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; border: none; background: transparent;")
        
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.time_lbl)

class AICareerSidebar(QFrame):
    navigation_requested = pyqtSignal(str)
    conversation_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 24, 16, 24)
        self.main_layout.setSpacing(24)

        # 1. Header & New Chat
        header_layout = QVBoxLayout()
        header_layout.setSpacing(16)
        
        title = QLabel("AI Career Coach")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        header_layout.addWidget(title)
        
        self.btn_new_chat = QPushButton("+  New Conversation")
        self.btn_new_chat.setFixedHeight(48)
        self.btn_new_chat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_chat.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 14px;
                font-weight: 700; font-size: 13px; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        header_layout.addWidget(self.btn_new_chat)
        self.main_layout.addLayout(header_layout)

        # 2. Search
        search_container = QFrame()
        search_container.setFixedHeight(44)
        search_container.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px;")
        sl = QHBoxLayout(search_container)
        sl.setContentsMargins(12, 0, 12, 0)
        search_icon = QLabel("🔍")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search conversations...")
        self.search_input.setStyleSheet("border: none; background: transparent; font-size: 13px; color: #0F172A;")
        sl.addWidget(search_icon)
        sl.addWidget(self.search_input)
        self.main_layout.addWidget(search_container)

        # 3. Main Navigation Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        self.scroll_layout = QVBoxLayout(container)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(20)

        # Navigation Sections
        nav_v = QVBoxLayout()
        nav_v.setSpacing(4)
        nav_items = ["Career Chat", "Resume Coaching", "Interview Practice", "Learning Plans", "Job Guidance"]
        self.nav_btns = []
        for item in nav_items:
            btn = NavButton(item)
            btn.clicked.connect(lambda ch, x=item: self._handle_nav_click(x))
            nav_v.addWidget(btn)
            self.nav_btns.append(btn)
            if item == "Career Chat": btn.setChecked(True)
        self.scroll_layout.addLayout(nav_v)

        # History Section
        history_v = QVBoxLayout()
        history_v.setSpacing(8)
        lbl_history = QLabel("RECENT HISTORY")
        lbl_history.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; margin-left: 12px;")
        history_v.addWidget(lbl_history)
        
        self.history_group = QWidget()
        self.history_layout = QVBoxLayout(self.history_group)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_layout.setSpacing(4)
        
        mock_history = [
            ("Optimizing AWS Skills", "2h ago"),
            ("Mock Interview: Tesla", "Yesterday"),
            ("Resume Content Rewrite", "2 days ago")
        ]
        self.history_btns = []
        for title, time in mock_history:
            btn = ConversationCard(title, time)
            btn.clicked.connect(lambda ch, t=title: self._handle_history_click(t))
            self.history_layout.addWidget(btn)
            self.history_btns.append(btn)
            
        history_v.addWidget(self.history_group)
        self.scroll_layout.addLayout(history_v)

        self.scroll_layout.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 4. Footer
        footer = QFrame()
        footer.setFixedHeight(70)
        footer.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0;")
        fl = QHBoxLayout(footer)
        
        avatar = QFrame()
        avatar.setFixedSize(36, 36)
        avatar.setStyleSheet("background: #38BDF8; border-radius: 18px;")
        
        stats_v = QVBoxLayout()
        stats_v.setSpacing(2)
        lbl_user = QLabel("John Doe")
        lbl_user.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none;")
        lbl_usage = QLabel("AI Usage: 85%")
        lbl_usage.setStyleSheet("font-size: 11px; color: #64748B; border: none;")
        stats_v.addWidget(lbl_user)
        stats_v.addWidget(lbl_usage)
        
        fl.addWidget(avatar)
        fl.addLayout(stats_v)
        fl.addStretch()
        
        self.main_layout.addWidget(footer)

    def _handle_nav_click(self, name):
        for btn in self.nav_btns:
            btn.setChecked(btn.text() == name)
        for btn in self.history_btns:
            btn.setChecked(False)
        self.navigation_requested.emit(name)

    def _handle_history_click(self, title):
        for btn in self.history_btns:
            btn.setChecked(btn.title_lbl.text() == title)
        for btn in self.nav_btns:
            btn.setChecked(False)
        self.conversation_selected.emit(title)
