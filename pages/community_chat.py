from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor


# ==========================================
# GLOBAL SCROLLBAR QSS (ultra-thin, hover-only)
# ==========================================
_SCROLLBAR_QSS = """
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 4px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background: rgba(148, 163, 184, 0);
        min-height: 30px;
        border-radius: 2px;
    }
    QScrollBar::handle:vertical:hover {
        background: rgba(148, 163, 184, 0.5);
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
"""


# ==========================================
# COMPONENT: LEFT SIDEBAR (Channels)
# ==========================================
class ChatLeftSidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.setFixedWidth(230)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Workspace header card
        header_card = QFrame()
        header_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: none;
            }
        """)
        h_shadow = QGraphicsDropShadowEffect()
        h_shadow.setBlurRadius(24)
        h_shadow.setColor(QColor(15, 23, 42, 8))
        h_shadow.setOffset(0, 4)
        header_card.setGraphicsEffect(h_shadow)

        hc_layout = QVBoxLayout(header_card)
        hc_layout.setContentsMargins(20, 20, 20, 20)
        hc_layout.setSpacing(16)

        # Logo row
        logo_row = QHBoxLayout()
        logo_row.setSpacing(12)
        logo_icon = QLabel("V")
        logo_icon.setFixedSize(38, 38)
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_icon.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2563EB, stop:1 #7C3AED);
            color: white; border-radius: 12px; font-weight: 900; font-size: 16px; border: none;
        """)
        logo_text = QVBoxLayout()
        logo_text.setSpacing(1)
        lt1 = QLabel("Vor Community")
        lt1.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A; border: none;")
        lt2 = QLabel("AI Hub")
        lt2.setStyleSheet("font-size: 12px; font-weight: 600; color: #94A3B8; border: none;")
        logo_text.addWidget(lt1)
        logo_text.addWidget(lt2)
        logo_row.addWidget(logo_icon)
        logo_row.addLayout(logo_text)
        logo_row.addStretch()
        hc_layout.addLayout(logo_row)

        # Channels title
        ch_title = QLabel("CHANNELS")
        ch_title.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1.2px; border: none; padding-left: 4px;")
        hc_layout.addWidget(ch_title)

        # Channel list (pill-shaped buttons)
        self.channel_list = QListWidget()
        self.channel_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
                outline: none;
            }
            QListWidget::item {
                border-radius: 12px;
                padding: 10px 14px;
                margin-bottom: 3px;
                color: #64748B;
                font-weight: 600;
                font-size: 14px;
                border: none;
            }
            QListWidget::item:hover {
                background-color: #E2E8F0;
                color: #0F172A;
            }
            QListWidget::item:selected {
                background-color: #EFF6FF;
                color: #2563EB;
                font-weight: 800;
            }
        """ + _SCROLLBAR_QSS)

        for ch in ["# general", "# ai-mentors", "# job-hunting", "# code-review"]:
            self.channel_list.addItem(QListWidgetItem(ch))

        self.channel_list.setCurrentRow(0)
        hc_layout.addWidget(self.channel_list)

        layout.addWidget(header_card)


# ==========================================
# COMPONENT: CHAT MESSAGE BUBBLE
# ==========================================
class ChatMessageBubble(QWidget):
    def __init__(self, text, sender, is_user=False, timestamp="10:00 AM"):
        super().__init__()
        self.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(10)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(460)
        bubble.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        if is_user:
            # --- Own message (right-aligned, brand color) ---
            bubble.setStyleSheet("""
                background-color: #2563EB;
                color: #FFFFFF;
                border-radius: 18px;
                border-bottom-right-radius: 4px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 500;
            """)

            # Avatar
            av = QLabel(sender[0].upper())
            av.setFixedSize(32, 32)
            av.setAlignment(Qt.AlignmentFlag.AlignCenter)
            av.setStyleSheet("""
                background-color: #2563EB; color: #FFFFFF;
                border-radius: 16px; font-weight: 900; font-size: 12px; border: none;
            """)

            time_lbl = QLabel(timestamp)
            time_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 600; border: none;")

            col = QVBoxLayout()
            col.setContentsMargins(0, 0, 0, 0)
            col.setSpacing(4)
            col.addWidget(bubble)
            col.addWidget(time_lbl, alignment=Qt.AlignmentFlag.AlignRight)

            layout.addStretch()
            layout.addLayout(col)
            layout.addWidget(av, alignment=Qt.AlignmentFlag.AlignBottom)

        else:
            # --- Other message (left-aligned, white card) ---
            av = QLabel(sender[0].upper())
            av.setFixedSize(32, 32)
            av.setAlignment(Qt.AlignmentFlag.AlignCenter)
            av.setStyleSheet("""
                background-color: #E2E8F0; color: #475569;
                border-radius: 16px; font-weight: 900; font-size: 12px; border: none;
            """)

            bubble.setStyleSheet("""
                background-color: #FFFFFF;
                color: #1E293B;
                border-radius: 18px;
                border-bottom-left-radius: 4px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 500;
            """)
            bubble_shadow = QGraphicsDropShadowEffect()
            bubble_shadow.setBlurRadius(12)
            bubble_shadow.setColor(QColor(15, 23, 42, 8))
            bubble_shadow.setOffset(0, 2)
            bubble.setGraphicsEffect(bubble_shadow)

            header = QHBoxLayout()
            header.setSpacing(8)
            name_lbl = QLabel(sender)
            name_lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #0F172A; border: none;")
            time_lbl = QLabel(timestamp)
            time_lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #94A3B8; border: none;")
            header.addWidget(name_lbl)
            header.addWidget(time_lbl)
            header.addStretch()

            col = QVBoxLayout()
            col.setContentsMargins(0, 0, 0, 0)
            col.setSpacing(5)
            col.addLayout(header)
            col.addWidget(bubble)

            layout.addWidget(av, alignment=Qt.AlignmentFlag.AlignBottom)
            layout.addLayout(col)
            layout.addStretch()


# ==========================================
# COMPONENT: MAIN CHAT AREA
# ==========================================
class MainChatArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # ---- Header Card ----
        header = QFrame()
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 16px; border: none; }")
        h_shadow = QGraphicsDropShadowEffect()
        h_shadow.setBlurRadius(20)
        h_shadow.setColor(QColor(15, 23, 42, 6))
        h_shadow.setOffset(0, 3)
        header.setGraphicsEffect(h_shadow)

        hl = QHBoxLayout(header)
        hl.setContentsMargins(26, 18, 26, 18)

        self.title_lbl = QLabel("# general")
        self.title_lbl.setStyleSheet("font-size: 18px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px; border: none;")
        self.status_lbl = QLabel("1,204 members · 42 online")
        self.status_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #94A3B8; border: none;")

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title_col.addWidget(self.title_lbl)
        title_col.addWidget(self.status_lbl)
        hl.addLayout(title_col)
        hl.addStretch()

        layout.addWidget(header)

        # ---- Messages Feed ----
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
        """ + _SCROLLBAR_QSS)

        self.chat_content = QWidget()
        self.chat_content.setStyleSheet("background: transparent; border: none;")
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setContentsMargins(8, 16, 8, 16)
        self.chat_layout.setSpacing(6)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._add_dummy_msgs()

        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_content)
        layout.addWidget(self.scroll_area)

        # ---- Floating Input Bar ----
        input_wrapper = QWidget()
        input_wrapper.setStyleSheet("background: transparent; border: none;")
        iw_layout = QHBoxLayout(input_wrapper)
        iw_layout.setContentsMargins(8, 0, 8, 0)  # Side margins so it doesn't stretch edge-to-edge

        input_card = QFrame()
        input_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 24px;
                border: 1px solid #E2E8F0;
            }
        """)
        i_shadow = QGraphicsDropShadowEffect()
        i_shadow.setBlurRadius(24)
        i_shadow.setColor(QColor(15, 23, 42, 10))
        i_shadow.setOffset(0, 4)
        input_card.setGraphicsEffect(i_shadow)

        ic_layout = QHBoxLayout(input_card)
        ic_layout.setContentsMargins(20, 10, 10, 10)
        ic_layout.setSpacing(12)

        btn_attach = QPushButton("📎")
        btn_attach.setFixedSize(34, 34)
        btn_attach.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_attach.setStyleSheet("background: transparent; font-size: 17px; border: none; color: #94A3B8;")

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Message #general...")
        self.msg_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #0F172A;
                font-size: 15px;
                font-weight: 500;
            }
            QLineEdit::placeholder {
                color: #94A3B8;
            }
        """)

        self.btn_send = QPushButton("↑")
        self.btn_send.setFixedSize(38, 38)
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_send.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border-radius: 19px;
                font-size: 18px;
                font-weight: 900;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        ic_layout.addWidget(btn_attach)
        ic_layout.addWidget(self.msg_input)
        ic_layout.addWidget(self.btn_send)

        iw_layout.addWidget(input_card)
        layout.addWidget(input_wrapper)

    def _add_dummy_msgs(self):
        msgs = [
            ("Has anyone tried the new LLM models released today? The benchmarks look insane.", "Sarah", False, "09:45 AM"),
            ("Yes! I've been running inference tests all morning. Latency dropped by 40% compared to last gen.", "Michael", False, "09:48 AM"),
            ("That's incredible. UI/UX is 90% done on our end — just need the API integration and we ship. 🚀", "You", True, "09:50 AM"),
            ("Perfect. I'll push the backend endpoints this afternoon. Check the repo around 3 PM.", "Michael", False, "09:55 AM"),
            ("Quick reminder: our Robotics demo is next Tuesday. Let's sync on Monday to finalize.", "Sarah", False, "10:02 AM"),
        ]
        for t, s, u, ts in msgs:
            self.chat_layout.addWidget(ChatMessageBubble(t, s, u, ts))


# ==========================================
# COMPONENT: RIGHT PANEL (Members)
# ==========================================
class ChatRightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.setFixedWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        card = QFrame()
        card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 16px; border: none; }")
        c_shadow = QGraphicsDropShadowEffect()
        c_shadow.setBlurRadius(24)
        c_shadow.setColor(QColor(15, 23, 42, 8))
        c_shadow.setOffset(0, 4)
        card.setGraphicsEffect(c_shadow)

        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 24, 20, 24)
        cl.setSpacing(20)
        cl.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("MEMBERS")
        title.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1.2px; border: none;")
        cl.addWidget(title)

        members = [
            ("Công Hậu", "#2563EB"),
            ("Sarah J.", "#8B5CF6"),
            ("Michael C.", "#059669"),
            ("David K.", "#EA580C"),
            ("Emma L.", "#DB2777"),
        ]

        for name, color in members:
            row = QHBoxLayout()
            row.setSpacing(12)

            av = QLabel(name[0])
            av.setFixedSize(30, 30)
            av.setAlignment(Qt.AlignmentFlag.AlignCenter)
            av.setStyleSheet(f"""
                background-color: {color}; color: white;
                border-radius: 15px; font-weight: 900; font-size: 11px; border: none;
            """)

            n = QLabel(name)
            n.setStyleSheet("font-size: 13px; font-weight: 700; color: #334155; border: none;")

            # Online dot
            dot = QLabel("●")
            dot.setStyleSheet("color: #22C55E; font-size: 8px; border: none;")

            row.addWidget(av)
            row.addWidget(n)
            row.addStretch()
            row.addWidget(dot)
            cl.addLayout(row)

        cl.addStretch()
        layout.addWidget(card)


# ==========================================
# MAIN PAGE: COMMUNITY CHAT
# ==========================================
class CommunityChatPage(QWidget):
    def __init__(self, controller=None):
        super().__init__(parent=None)
        self.controller = controller

        self.setStyleSheet("background-color: #F8FAFC; border: none;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        self.left_panel = ChatLeftSidebar()
        self.middle_panel = MainChatArea()
        self.right_panel = ChatRightPanel()

        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.middle_panel, 1)  # Stretch to fill
        main_layout.addWidget(self.right_panel)

        # Connections
        self.left_panel.channel_list.currentItemChanged.connect(self._change_channel)
        self.middle_panel.btn_send.clicked.connect(self._send_msg)
        self.middle_panel.msg_input.returnPressed.connect(self._send_msg)

    def _change_channel(self, current, previous):
        if current:
            ch = current.text()
            self.middle_panel.title_lbl.setText(ch)
            self.middle_panel.msg_input.setPlaceholderText(f"Message {ch}...")

    def _send_msg(self):
        text = self.middle_panel.msg_input.text().strip()
        if text:
            from datetime import datetime
            now = datetime.now().strftime("%I:%M %p")
            msg = ChatMessageBubble(text, "You", True, now)
            self.middle_panel.chat_layout.insertWidget(
                self.middle_panel.chat_layout.count() - 1, msg
            )
            self.middle_panel.msg_input.clear()

            QTimer.singleShot(50, lambda: self.middle_panel.scroll_area.verticalScrollBar().setValue(
                self.middle_panel.scroll_area.verticalScrollBar().maximum()
            ))
