from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QTextEdit, QGraphicsDropShadowEffect, QSizePolicy,
                             QSplitter, QProgressBar)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor, QIcon, QPainter, QBrush, QPen

class ModernCard(QFrame):
    def __init__(self, parent=None, radius=12, bg_color="#FFFFFF", border_color="#E2E8F0"):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: {radius}px;
            }}
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)

class ConversationItem(QFrame):
    def __init__(self, name, last_msg, time_str, unread=0, is_active=False, is_online=False, avatar_color="#38BDF8", is_group=False):
        super().__init__()
        self.setFixedHeight(72)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        bg = "#E0F2FE" if is_active else "transparent"
        border = "#38BDF8" if is_active else "transparent"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 12px;
            }}
            QFrame:hover {{
                background-color: #F1F5F9;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(12)
        
        # Avatar
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(48, 48)
        avatar_frame.setStyleSheet(f"background-color: {avatar_color}; border-radius: 24px; border: none;")
        avatar_layout = QVBoxLayout(avatar_frame)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        initial = name[:2].upper() if is_group else name[:1].upper()
        avatar_lbl = QLabel(initial)
        avatar_lbl.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none; background: transparent;")
        avatar_layout.addWidget(avatar_lbl)
        
        layout.addWidget(avatar_frame)
        
        # Status Indicator
        if is_online:
            status = QFrame(avatar_frame)
            status.setFixedSize(14, 14)
            status.setStyleSheet("background-color: #10B981; border-radius: 7px; border: 2px solid #FFFFFF;")
            status.move(34, 34)
            
        # Text details
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 14, 0, 14)
        text_layout.setSpacing(2)
        
        top_row = QHBoxLayout()
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px; border: none; background: transparent;")
        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet("color: #94A3B8; font-weight: 500; font-size: 11px; border: none; background: transparent;")
        top_row.addWidget(name_lbl)
        top_row.addStretch()
        top_row.addWidget(time_lbl)
        
        bottom_row = QHBoxLayout()
        msg_lbl = QLabel(last_msg)
        msg_lbl.setStyleSheet(f"color: {'#0F172A' if unread > 0 else '#64748B'}; font-weight: {'600' if unread > 0 else '400'}; font-size: 13px; border: none; background: transparent;")
        msg_lbl.setFixedWidth(180)
        msg_lbl.setWordWrap(False)
        
        bottom_row.addWidget(msg_lbl)
        bottom_row.addStretch()
        
        if unread > 0:
            badge = QLabel(str(unread))
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedSize(20, 20)
            badge.setStyleSheet("background-color: #EF4444; color: white; border-radius: 10px; font-size: 11px; font-weight: 700; border: none;")
            bottom_row.addWidget(badge)
            
        text_layout.addLayout(top_row)
        text_layout.addLayout(bottom_row)
        
        layout.addLayout(text_layout)

class MessageBubble(QWidget):
    def __init__(self, text, time_str, sender_name=None, is_outgoing=False, has_avatar=True):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        
        if is_outgoing:
            layout.addStretch()
            
        bubble_layout = QVBoxLayout()
        bubble_layout.setSpacing(4)
        
        if sender_name and not is_outgoing:
            sender_lbl = QLabel(sender_name)
            sender_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600;")
            bubble_layout.addWidget(sender_lbl)
            
        msg_frame = QFrame()
        bg_color = "#38BDF8" if is_outgoing else "#FFFFFF"
        text_color = "#FFFFFF" if is_outgoing else "#0F172A"
        border = "none" if is_outgoing else "1px solid #E2E8F0"
        
        msg_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                border-radius: 16px;
                padding: 10px 14px;
            }}
        """)
        
        msg_layout = QVBoxLayout(msg_frame)
        msg_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color: {text_color}; font-size: 14px; line-height: 1.5; border: none; background: transparent;")
        msg_layout.addWidget(lbl)
        
        time_layout = QHBoxLayout()
        time_layout.addStretch()
        t_lbl = QLabel(time_str)
        t_color = "#E0F2FE" if is_outgoing else "#94A3B8"
        t_lbl.setStyleSheet(f"color: {t_color}; font-size: 11px; border: none; background: transparent;")
        time_layout.addWidget(t_lbl)
        
        if is_outgoing:
            read_status = QLabel("✓✓")
            read_status.setStyleSheet("color: #E0F2FE; font-size: 12px; border: none; background: transparent;")
            time_layout.addWidget(read_status)
            
        msg_layout.addLayout(time_layout)
        bubble_layout.addWidget(msg_frame)
        
        layout.addLayout(bubble_layout)
        
        if not is_outgoing:
            layout.addStretch()

class ChatPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_conversation_sidebar()
        self._setup_main_chat_area()
        self._setup_right_details_panel()

    def _setup_conversation_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(320)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 0)
        layout.setSpacing(16)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Messages")
        title.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 700; border: none;")
        header.addWidget(title)
        header.addStretch()
        
        btn_new = QPushButton("✏️")
        btn_new.setFixedSize(36, 36)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.setStyleSheet("""
            QPushButton {
                background: #F1F5F9; border: none; border-radius: 18px; color: #475569; font-size: 16px;
            }
            QPushButton:hover { background: #E2E8F0; color: #0F172A; }
        """)
        header.addWidget(btn_new)
        layout.addLayout(header)
        
        # Search
        search = QLineEdit()
        search.setPlaceholderText("Search messages, people, groups...")
        search.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 10px 36px 10px 16px; color: #0F172A; font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #38BDF8; }
        """)
        
        # Search icon mock
        search_container = QWidget()
        sc_layout = QHBoxLayout(search_container)
        sc_layout.setContentsMargins(0, 0, 0, 0)
        sc_layout.addWidget(search)
        layout.addWidget(search_container)
        
        # Tabs
        tabs = QHBoxLayout()
        tabs.setSpacing(16)
        
        btn_all = QPushButton("All Chats")
        btn_all.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px; border: none; border-bottom: 2px solid #38BDF8; padding-bottom: 4px;")
        btn_unread = QPushButton("Unread")
        btn_unread.setStyleSheet("color: #64748B; font-weight: 500; font-size: 14px; border: none; padding-bottom: 4px;")
        btn_unread.setCursor(Qt.CursorShape.PointingHandCursor)
        
        tabs.addWidget(btn_all)
        tabs.addWidget(btn_unread)
        tabs.addStretch()
        layout.addLayout(tabs)
        
        # List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 8, 0, 24)
        list_layout.setSpacing(4)
        
        list_layout.addWidget(ConversationItem("AI Assistant", "Here are the suggested topics for your next session.", "10:24 AM", 2, True, True, "#8B5CF6"))
        list_layout.addWidget(ConversationItem("Study Group: Math 201", "Alex: I'll share the notes later.", "09:15 AM", 0, False, False, "#F59E0B", True))
        list_layout.addWidget(ConversationItem("Prof. Sarah Jenkins", "Your assignment looks great. Just one minor adjustment needed.", "Yesterday", 0, False, True, "#10B981"))
        list_layout.addWidget(ConversationItem("Tech Recruitment Team", "We would like to schedule an interview.", "Tuesday", 1, False, False, "#3B82F6"))
        list_layout.addWidget(ConversationItem("Design System Project", "You: I updated the Figma file.", "Monday", 0, False, False, "#EC4899", True))
        
        list_layout.addStretch()
        scroll.setWidget(list_widget)
        layout.addWidget(scroll)
        
        self.main_layout.addWidget(sidebar)

    def _setup_main_chat_area(self):
        main_area = QWidget()
        layout = QVBoxLayout(main_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(24, 0, 24, 0)
        t_layout.setSpacing(16)
        
        # Active Chat Info
        avatar = QLabel("AI")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet("background-color: #8B5CF6; color: white; font-weight: bold; border-radius: 20px; font-size: 16px;")
        t_layout.addWidget(avatar)
        
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        info_layout.setSpacing(2)
        name_lbl = QLabel("AI Assistant")
        name_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        status_lbl = QLabel("Online • Always here to help")
        status_lbl.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 500; border: none;")
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(status_lbl)
        t_layout.addLayout(info_layout)
        
        t_layout.addStretch()
        
        # Action Buttons
        for icon in ["📞", "📹", "🔍", "⋯"]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; color: #64748B; font-size: 18px; border-radius: 20px; border: none;
                }
                QPushButton:hover { background: #F1F5F9; color: #0F172A; }
            """)
            t_layout.addWidget(btn)
            
        layout.addWidget(toolbar)
        
        # Chat History
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        history_widget = QWidget()
        h_layout = QVBoxLayout(history_widget)
        h_layout.setContentsMargins(32, 24, 32, 24)
        h_layout.setSpacing(16)
        
        # Banner
        banner = QFrame()
        banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E0F2FE, stop:1 #F0F9FF);
                border: 1px solid #BAE6FD; border-radius: 12px;
            }
        """)
        b_layout = QVBoxLayout(banner)
        b_layout.setContentsMargins(16, 12, 16, 12)
        b_title = QLabel("🤖 This is the beginning of your conversation with AI Assistant.")
        b_title.setStyleSheet("color: #0284C7; font-size: 13px; font-weight: 600; border: none; background: transparent;")
        b_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        b_layout.addWidget(b_title)
        h_layout.addWidget(banner)
        
        h_layout.addSpacing(16)
        
        # Messages
        h_layout.addWidget(MessageBubble("Hello! How can I help you with your coursework today?", "09:00 AM", "AI Assistant", False))
        h_layout.addWidget(MessageBubble("Can you review my thesis introduction?", "09:05 AM", "You", True))
        h_layout.addWidget(MessageBubble("Of course! Please upload the document, and I'll analyze the structure, clarity, and academic tone.", "09:06 AM", "AI Assistant", False))
        
        # Attachment Mock
        attach = QFrame()
        attach.setFixedWidth(240)
        attach.setStyleSheet("background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
        att_layout = QHBoxLayout(attach)
        att_icon = QLabel("📄")
        att_icon.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        att_text = QVBoxLayout()
        att_name = QLabel("Thesis_Intro_v2.pdf")
        att_name.setStyleSheet("color: #0F172A; font-weight: 600; font-size: 13px; border: none;")
        att_size = QLabel("1.2 MB")
        att_size.setStyleSheet("color: #64748B; font-size: 11px; border: none;")
        att_text.addWidget(att_name)
        att_text.addWidget(att_size)
        att_layout.addWidget(att_icon)
        att_layout.addLayout(att_text)
        att_layout.addStretch()
        
        att_wrapper = QHBoxLayout()
        att_wrapper.addStretch()
        att_wrapper.addWidget(attach)
        h_layout.addLayout(att_wrapper)
        
        h_layout.addWidget(MessageBubble("I've reviewed the file. Your opening hook is strong, but you might want to clarify your methodology earlier in the text.", "10:24 AM", "AI Assistant", False))
        
        h_layout.addStretch()
        scroll.setWidget(history_widget)
        layout.addWidget(scroll)
        
        # Composer
        composer = QWidget()
        composer.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #E2E8F0;")
        c_layout = QHBoxLayout(composer)
        c_layout.setContentsMargins(24, 16, 24, 24)
        c_layout.setSpacing(12)
        
        btn_add = QPushButton("➕")
        btn_add.setFixedSize(40, 40)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton {
                background: #F1F5F9; color: #475569; font-size: 16px; border-radius: 20px; border: none;
            }
            QPushButton:hover { background: #E2E8F0; }
        """)
        c_layout.addWidget(btn_add)
        
        input_box = QTextEdit()
        input_box.setPlaceholderText("Type a message...")
        input_box.setFixedHeight(44)
        input_box.setStyleSheet("""
            QTextEdit {
                background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 22px;
                padding: 10px 16px; color: #0F172A; font-size: 14px;
            }
            QTextEdit:focus { border: 1px solid #38BDF8; background: #FFFFFF; }
        """)
        c_layout.addWidget(input_box)
        
        for icon in ["😀", "🎙️"]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("background: transparent; color: #64748B; font-size: 18px; border: none;")
            c_layout.addWidget(btn)
            
        btn_send = QPushButton("➤")
        btn_send.setFixedSize(40, 40)
        btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_send.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: white; font-size: 16px; border-radius: 20px; border: none;
            }
            QPushButton:hover { background: #0284C7; }
        """)
        c_layout.addWidget(btn_send)
        
        layout.addWidget(composer)
        self.main_layout.addWidget(main_area)

    def _setup_right_details_panel(self):
        panel = QFrame()
        panel.setFixedWidth(320)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Details
        d_lbl = QLabel("Conversation Details")
        d_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        layout.addWidget(d_lbl)
        
        desc = QLabel("AI Mentor for academic writing, career prep, and study scheduling.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.5; border: none;")
        layout.addWidget(desc)
        
        # Shared Media
        sm_lbl = QLabel("Shared Media & Files")
        sm_lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600; border: none;")
        layout.addWidget(sm_lbl)
        
        def create_file_row(icon, name, size):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(12)
            ico = QLabel(icon)
            ico.setStyleSheet("font-size: 20px; background: transparent; border: none;")
            
            texts = QVBoxLayout()
            texts.setSpacing(2)
            n_lbl = QLabel(name)
            n_lbl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 500; border: none;")
            s_lbl = QLabel(size)
            s_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; border: none;")
            texts.addWidget(n_lbl)
            texts.addWidget(s_lbl)
            
            l.addWidget(ico)
            l.addLayout(texts)
            l.addStretch()
            return w
            
        layout.addWidget(create_file_row("📄", "Thesis_Intro_v2.pdf", "1.2 MB"))
        layout.addWidget(create_file_row("📊", "Study_Schedule.xlsx", "450 KB"))
        layout.addWidget(create_file_row("🖼️", "Design_System.png", "2.4 MB"))
        
        layout.addSpacing(16)
        
        # AI Suggestions
        ai_lbl = QLabel("AI Chat Assistant")
        ai_lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600; border: none;")
        layout.addWidget(ai_lbl)
        
        sug_card = ModernCard(radius=8, bg_color="#F8FAFC")
        sug_card.layout.setSpacing(8)
        sug_title = QLabel("✨ Suggested Actions")
        sug_title.setStyleSheet("color: #8B5CF6; font-size: 13px; font-weight: 700; border: none;")
        sug_card.layout.addWidget(sug_title)
        
        for tip in ["Summarize Conversation", "Extract Action Items", "Schedule Study Session"]:
            btn = QPushButton(tip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px;
                    padding: 8px 12px; color: #0F172A; font-size: 12px; font-weight: 500; text-align: left;
                }
                QPushButton:hover { background: #F1F5F9; border-color: #CBD5E1; }
            """)
            sug_card.layout.addWidget(btn)
            
        layout.addWidget(sug_card)
        
        # Bottom Productivity
        layout.addStretch()
        prod_lbl = QLabel("Communication Activity")
        prod_lbl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 600; border: none;")
        layout.addWidget(prod_lbl)
        
        bar = QProgressBar()
        bar.setFixedHeight(6)
        bar.setValue(65)
        bar.setTextVisible(False)
        bar.setStyleSheet("""
            QProgressBar { background: #E2E8F0; border-radius: 3px; border: none; }
            QProgressBar::chunk { background: #38BDF8; border-radius: 3px; }
        """)
        layout.addWidget(bar)
        stat = QLabel("65% daily interaction goal")
        stat.setStyleSheet("color: #64748B; font-size: 11px; border: none;")
        layout.addWidget(stat)
        
        self.main_layout.addWidget(panel)
