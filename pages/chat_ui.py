from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QTextEdit, QGraphicsDropShadowEffect, QSizePolicy,
                             QSplitter, QProgressBar)
from PyQt6.QtCore import Qt, QSize, QTimer, QPoint
from PyQt6.QtGui import QColor, QFont, QCursor, QIcon, QPainter, QBrush, QPen

from components import CollapsiblePanel

def apply_shadow(widget, blur=15, offset=(0, 4), opacity=0.08):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(offset[0])
    shadow.setYOffset(offset[1])
    shadow.setColor(QColor(15, 23, 42, int(255 * opacity)))
    widget.setGraphicsEffect(shadow)
    return shadow

class ModernCard(QFrame):
    def __init__(self, parent=None, radius=16, bg_color="#FFFFFF", border_color="#E2E8F0"):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: {radius}px;
            }}
        """)
        apply_shadow(self, blur=10, offset=(0, 2), opacity=0.05)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)

class ConversationItem(QFrame):
    def __init__(self, name, last_msg, time_str, unread=0, is_active=False, is_online=False, avatar_color="#38BDF8", is_group=False):
        super().__init__()
        self.setFixedHeight(72)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        bg = "#F8FAFC" if is_active else "transparent"
        border = "#E2E8F0" if is_active else "transparent"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 12px;
                margin: 0px 4px;
            }}
            QFrame:hover {{
                background-color: #F1F5F9;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # Avatar
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(44, 44)
        avatar_frame.setStyleSheet(f"background-color: {avatar_color}; border-radius: 22px; border: none;")
        avatar_layout = QVBoxLayout(avatar_frame)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        initial = name[:2].upper() if is_group else name[:1].upper()
        avatar_lbl = QLabel(initial)
        avatar_lbl.setStyleSheet("color: white; font-weight: 700; font-size: 14px; border: none; background: transparent;")
        avatar_layout.addWidget(avatar_lbl)
        
        layout.addWidget(avatar_frame)
        
        # Status Indicator
        if is_online:
            status = QFrame(avatar_frame)
            status.setFixedSize(12, 12)
            status.setStyleSheet("background-color: #10B981; border-radius: 6px; border: 2px solid #FFFFFF;")
            status.move(32, 32)
            
        # Text details
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 2, 0, 2)
        text_layout.setSpacing(2)
        
        top_row = QHBoxLayout()
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 13px; border: none; background: transparent;")
        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet("color: #94A3B8; font-weight: 500; font-size: 10px; border: none; background: transparent;")
        top_row.addWidget(name_lbl)
        top_row.addStretch()
        top_row.addWidget(time_lbl)
        
        bottom_row = QHBoxLayout()
        msg_lbl = QLabel(last_msg)
        msg_lbl.setStyleSheet(f"color: {'#0F172A' if unread > 0 else '#64748B'}; font-weight: {'600' if unread > 0 else '400'}; font-size: 12px; border: none; background: transparent;")
        msg_lbl.setWordWrap(False)
        
        bottom_row.addWidget(msg_lbl)
        bottom_row.addStretch()
        
        if unread > 0:
            badge = QLabel(str(unread))
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedSize(18, 18)
            badge.setStyleSheet("background-color: #38BDF8; color: white; border-radius: 9px; font-size: 10px; font-weight: 700; border: none;")
            bottom_row.addWidget(badge)
            
        text_layout.addLayout(top_row)
        text_layout.addLayout(bottom_row)
        
        layout.addLayout(text_layout)

class MessageBubble(QWidget):
    def __init__(self, text, time_str, sender_name=None, is_outgoing=False, has_avatar=True):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(8)
        
        if is_outgoing:
            layout.addStretch()
            
        bubble_layout = QVBoxLayout()
        bubble_layout.setSpacing(4)
        
        if sender_name and not is_outgoing:
            sender_lbl = QLabel(sender_name)
            sender_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; margin-left: 12px;")
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
        if not is_outgoing:
            apply_shadow(msg_frame, blur=8, offset=(0, 2), opacity=0.04)
        
        msg_layout = QVBoxLayout(msg_frame)
        msg_layout.setContentsMargins(0, 0, 0, 0)
        msg_layout.setSpacing(4)
        
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color: {text_color}; font-size: 13px; line-height: 1.5; border: none; background: transparent;")
        lbl.setMaximumWidth(400) # prevent super wide bubbles
        msg_layout.addWidget(lbl)
        
        time_layout = QHBoxLayout()
        time_layout.addStretch()
        t_lbl = QLabel(time_str)
        t_color = "rgba(255, 255, 255, 0.7)" if is_outgoing else "#94A3B8"
        t_lbl.setStyleSheet(f"color: {t_color}; font-size: 10px; border: none; background: transparent;")
        time_layout.addWidget(t_lbl)
        
        if is_outgoing:
            read_status = QLabel("✓✓")
            read_status.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 10px; border: none; background: transparent;")
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
        
        # Initialize sub-widgets
        self.sidebar_content = self._setup_conversation_sidebar()
        self.main_chat_content = self._setup_main_chat_area()
        self.details_content = self._setup_right_details_panel()
        
        # Set fixed widths for collapsibles
        self.sidebar_content.setFixedWidth(280)
        self.details_content.setFixedWidth(280)
        
        # Create Collapsible Panels
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        self.right_panel = CollapsiblePanel(self.details_content, orientation="right")
        
        # Main Layout Assembly
        self.main_layout.addWidget(self.left_panel)
        self.main_layout.addWidget(self.main_chat_content, 1) # Chat stretches
        self.main_layout.addWidget(self.right_panel)

    def _setup_conversation_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #FFFFFF; border: none; border-right: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 0)
        layout.setSpacing(16)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Messages")
        title.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800; border: none;")
        header.addWidget(title)
        header.addStretch()
        
        btn_new = QPushButton("+")
        btn_new.setFixedSize(36, 36)
        btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_new.setStyleSheet("""
            QPushButton {
                background: #F1F5F9; border: none; border-radius: 18px; color: #0F172A; font-size: 18px; font-weight: bold;
            }
            QPushButton:hover { background: #E2E8F0; }
        """)
        header.addWidget(btn_new)
        layout.addLayout(header)
        
        # Search
        search = QLineEdit()
        search.setPlaceholderText("Search...")
        search.setFixedHeight(36)
        search.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 18px;
                padding: 0 16px; color: #0F172A; font-size: 13px;
            }
            QLineEdit:focus { border: 1px solid #38BDF8; background-color: #FFFFFF; }
        """)
        layout.addWidget(search)
        
        # Tabs
        tabs = QHBoxLayout()
        tabs.setSpacing(16)
        
        btn_all = QPushButton("All")
        btn_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_all.setStyleSheet("color: #38BDF8; font-weight: 700; font-size: 13px; border: none; border-bottom: 2px solid #38BDF8; padding-bottom: 6px; border-radius: 0; background: transparent;")
        btn_unread = QPushButton("Unread")
        btn_unread.setStyleSheet("color: #64748B; font-weight: 600; font-size: 13px; border: none; padding-bottom: 6px; background: transparent;")
        btn_unread.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        tabs.addWidget(btn_all)
        tabs.addWidget(btn_unread)
        tabs.addStretch()
        layout.addLayout(tabs)
        
        # List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { width: 6px; background: transparent; }
            QScrollBar::handle:vertical { background: #E2E8F0; border-radius: 3px; }
            QScrollBar::handle:vertical:hover { background: #CBD5E1; }
        """)
        
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 8, 0, 24)
        list_layout.setSpacing(4)
        
        list_layout.addWidget(ConversationItem("AI Assistant", "Here are the suggested topics...", "10:24 AM", 2, True, True, "#8B5CF6"))
        list_layout.addWidget(ConversationItem("Math Study Group", "Alex: I'll share the notes later.", "09:15 AM", 0, False, False, "#F59E0B", True))
        list_layout.addWidget(ConversationItem("Prof. Sarah Jenkins", "Your assignment looks great.", "Yesterday", 0, False, True, "#10B981"))
        list_layout.addWidget(ConversationItem("Recruitment Team", "Interview scheduled for Friday.", "Tuesday", 1, False, False, "#3B82F6"))
        list_layout.addWidget(ConversationItem("Design Project", "You: Updated the Figma file.", "Monday", 0, False, False, "#EC4899", True))
        
        list_layout.addStretch()
        scroll.setWidget(list_widget)
        layout.addWidget(scroll)
        
        return sidebar

    def _setup_main_chat_area(self):
        main_area = QFrame()
        main_area.setStyleSheet("background-color: #F8FAFC; border: none;")
        layout = QVBoxLayout(main_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(24, 0, 24, 0)
        t_layout.setSpacing(12)
        
        # Active Chat Info
        avatar = QLabel("AI")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet("background-color: #8B5CF6; color: white; font-weight: 700; border-radius: 20px; font-size: 14px;")
        t_layout.addWidget(avatar)
        
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        info_layout.setSpacing(2)
        name_lbl = QLabel("AI Assistant")
        name_lbl.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 800; border: none;")
        status_lbl = QLabel("● Online")
        status_lbl.setStyleSheet("color: #10B981; font-size: 11px; font-weight: 700; border: none;")
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(status_lbl)
        t_layout.addLayout(info_layout)
        
        t_layout.addStretch()
        
        # Action Buttons
        for icon in ["📞", "📹", "🔍", "⋯"]:
            btn = QPushButton(icon)
            btn.setFixedSize(36, 36)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; color: #64748B; font-size: 16px; border-radius: 18px; border: none;
                }
                QPushButton:hover { background: #F1F5F9; color: #0F172A; }
            """)
            t_layout.addWidget(btn)
            
        layout.addWidget(toolbar)
        
        # Chat History
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        # Custom scrollbar styling
        scroll.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                min-height: 40px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        
        history_widget = QWidget()
        h_layout = QVBoxLayout(history_widget)
        h_layout.setContentsMargins(24, 24, 24, 24)
        h_layout.setSpacing(12)
        
        # Banner
        banner = QFrame()
        banner.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        apply_shadow(banner, blur=8, opacity=0.03)
        b_layout = QVBoxLayout(banner)
        b_layout.setContentsMargins(16, 12, 16, 12)
        b_title = QLabel("🤖 AI Career Mentor is ready to assist you.")
        b_title.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600; border: none; background: transparent;")
        b_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        b_layout.addWidget(b_title)
        
        h_layout.addWidget(banner, alignment=Qt.AlignmentFlag.AlignCenter)
        h_layout.addSpacing(16)
        
        # Messages
        h_layout.addWidget(MessageBubble("Hello! How can I help you with your coursework today?", "09:00 AM", "AI Assistant", False))
        h_layout.addWidget(MessageBubble("Can you review my thesis introduction?", "09:05 AM", "You", True))
        h_layout.addWidget(MessageBubble("Of course! Please upload the document.", "09:06 AM", "AI Assistant", False))
        
        # Attachment
        attach = QFrame()
        attach.setFixedWidth(240)
        attach.setStyleSheet("background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
        apply_shadow(attach, blur=8, opacity=0.04)
        att_layout = QHBoxLayout(attach)
        att_layout.setContentsMargins(12, 10, 12, 10)
        att_icon = QLabel("📄")
        att_icon.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        att_text = QVBoxLayout()
        att_name = QLabel("Thesis_Intro_v2.pdf")
        att_name.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 12px; border: none;")
        att_size = QLabel("1.2 MB")
        att_size.setStyleSheet("color: #94A3B8; font-size: 10px; border: none;")
        att_text.addWidget(att_name)
        att_text.addWidget(att_size)
        att_layout.addWidget(att_icon)
        att_layout.addLayout(att_text)
        att_layout.addStretch()
        
        att_wrapper = QHBoxLayout()
        att_wrapper.addStretch()
        att_wrapper.addWidget(attach)
        h_layout.addLayout(att_wrapper)
        
        h_layout.addWidget(MessageBubble("I've reviewed the file. Your opening hook is strong.", "10:24 AM", "AI Assistant", False))
        
        h_layout.addStretch()
        scroll.setWidget(history_widget)
        layout.addWidget(scroll)
        
        # Composer
        composer_container = QWidget()
        composer_container.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #E2E8F0;")
        cc_layout = QVBoxLayout(composer_container)
        cc_layout.setContentsMargins(24, 16, 24, 24)
        
        composer = QFrame()
        composer.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 20px;")
        c_layout = QHBoxLayout(composer)
        c_layout.setContentsMargins(8, 6, 8, 6)
        c_layout.setSpacing(8)
        
        btn_add = QPushButton("+")
        btn_add.setFixedSize(32, 32)
        btn_add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_add.setStyleSheet("""
            QPushButton {
                background: #FFFFFF; color: #64748B; font-size: 18px; border-radius: 16px; border: 1px solid #E2E8F0;
            }
            QPushButton:hover { background: #F1F5F9; }
        """)
        c_layout.addWidget(btn_add)
        
        input_box = QTextEdit()
        input_box.setPlaceholderText("Type a message...")
        input_box.setFixedHeight(36)
        input_box.setStyleSheet("""
            QTextEdit {
                background: transparent; border: none;
                padding: 8px 8px; color: #0F172A; font-size: 13px;
            }
        """)
        c_layout.addWidget(input_box)
        
        for icon in ["😀", "🎙️"]:
            btn = QPushButton(icon)
            btn.setFixedSize(32, 32)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("background: transparent; color: #64748B; font-size: 16px; border: none;")
            c_layout.addWidget(btn)
            
        btn_send = QPushButton("➤")
        btn_send.setFixedSize(32, 32)
        btn_send.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_send.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: white; font-size: 14px; border-radius: 16px; border: none;
            }
            QPushButton:hover { background: #0284C7; }
        """)
        c_layout.addWidget(btn_send)
        
        cc_layout.addWidget(composer)
        layout.addWidget(composer_container)
        return main_area

    def _setup_right_details_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: #FFFFFF; border: none; border-left: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 32, 24, 24)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Details
        d_lbl = QLabel("About")
        d_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 800; border: none;")
        layout.addWidget(d_lbl)
        
        desc = QLabel("AI Mentor for academic writing, career prep, and study scheduling.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.5; border: none;")
        layout.addWidget(desc)
        
        # Shared Media
        sm_lbl = QLabel("Shared Files")
        sm_lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 700; border: none;")
        layout.addWidget(sm_lbl)
        
        def create_file_row(icon, name, size):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(12)
            ico = QLabel(icon)
            ico.setStyleSheet("font-size: 18px; background: transparent; border: none;")
            
            texts = QVBoxLayout()
            texts.setSpacing(2)
            n_lbl = QLabel(name)
            n_lbl.setStyleSheet("color: #0F172A; font-size: 12px; font-weight: 600; border: none;")
            s_lbl = QLabel(size)
            s_lbl.setStyleSheet("color: #94A3B8; font-size: 10px; border: none;")
            texts.addWidget(n_lbl)
            texts.addWidget(s_lbl)
            
            l.addWidget(ico)
            l.addLayout(texts)
            l.addStretch()
            return w
            
        layout.addWidget(create_file_row("📄", "Thesis_Intro_v2.pdf", "1.2 MB"))
        layout.addWidget(create_file_row("📊", "Study_Schedule.xlsx", "450 KB"))
        
        # AI Suggestions
        ai_lbl = QLabel("AI Tools")
        ai_lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 700; border: none;")
        layout.addWidget(ai_lbl)
        
        sug_card = ModernCard(radius=12, bg_color="#F8FAFC")
        sug_card.layout.setSpacing(8)
        sug_card.layout.setContentsMargins(12, 12, 12, 12)
        
        for tip in ["Summarize", "Action Items", "Schedule"]:
            btn = QPushButton(tip)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
                    padding: 8px 12px; color: #0F172A; font-size: 12px; font-weight: 600; text-align: center;
                }
                QPushButton:hover { background: #F1F5F9; border-color: #CBD5E1; }
            """)
            sug_card.layout.addWidget(btn)
            
        layout.addWidget(sug_card)
        
        # Bottom Productivity
        layout.addStretch()
        
        bar_card = ModernCard(radius=12, bg_color="#FFFFFF")
        bar_card.layout.setContentsMargins(16, 16, 16, 16)
        
        prod_lbl = QLabel("Activity Goal")
        prod_lbl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 700; border: none;")
        bar_card.layout.addWidget(prod_lbl)
        
        bar = QProgressBar()
        bar.setFixedHeight(6)
        bar.setValue(65)
        bar.setTextVisible(False)
        bar.setStyleSheet("""
            QProgressBar { background: #F1F5F9; border-radius: 3px; border: none; }
            QProgressBar::chunk { background: #38BDF8; border-radius: 3px; }
        """)
        bar_card.layout.addWidget(bar)
        stat = QLabel("65% of daily target")
        stat.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 500; border: none;")
        bar_card.layout.addWidget(stat)
        
        layout.addWidget(bar_card)
        
        return panel
