from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QTextEdit, 
                             QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
                             QStackedWidget)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor
from .typing_indicator import TypingIndicator
from .input_widget import ChatInputWidget

class MessageBubble(QFrame):
    def __init__(self, text, is_ai=True, parent=None):
        super().__init__(parent)
        self.is_ai = is_ai
        self.setup_ui(text)

    def setup_ui(self, text):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        if not self.is_ai: layout.addStretch()
        self.bubble = QFrame()
        self.bubble.setObjectName("Bubble")
        if self.is_ai:
            self.bubble.setStyleSheet("QFrame#Bubble { background: white; border: 1px solid #E2E8F0; border-radius: 20px; border-bottom-left-radius: 4px; }")
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15); shadow.setColor(QColor(15, 23, 42, 12)); shadow.setOffset(0, 2)
            self.bubble.setGraphicsEffect(shadow)
        else:
            self.bubble.setStyleSheet("QFrame#Bubble { background: #0F172A; border-radius: 20px; border-bottom-right-radius: 4px; }")
        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(16, 12, 16, 12)
        self.text_lbl = QLabel(text)
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        if self.is_ai: self.text_lbl.setStyleSheet("color: #1E293B; font-size: 14px; line-height: 1.5; border: none; background: transparent;")
        else: self.text_lbl.setStyleSheet("color: white; font-size: 14px; line-height: 1.5; border: none; background: transparent;")
        bubble_layout.addWidget(self.text_lbl)
        layout.addWidget(self.bubble)
        if self.is_ai: layout.addStretch()

class QuickActionCard(QPushButton):
    def __init__(self, icon, title, desc, parent=None):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("QPushButton { background-color: white; border: 1px solid #E2E8F0; border-radius: 16px; text-align: left; } QPushButton:hover { border-color: #38BDF8; background-color: #F0F9FF; }")
        layout = QVBoxLayout(self); layout.setContentsMargins(16, 16, 16, 16); layout.setSpacing(4)
        self.icon_lbl = QLabel(icon); self.icon_lbl.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        self.title_lbl = QLabel(title); self.title_lbl.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none; background: transparent;")
        self.desc_lbl = QLabel(desc); self.desc_lbl.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        layout.addWidget(self.icon_lbl); layout.addWidget(self.title_lbl); layout.addWidget(self.desc_lbl)

class AIChatCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Header
        self.header = QFrame()
        self.header.setFixedHeight(72)
        self.header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(self.header); hl.setContentsMargins(32, 0, 32, 0)
        
        title_v = QVBoxLayout(); title_v.setSpacing(2); title_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.mode_lbl = QLabel("Career Chat"); self.mode_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A; border: none;")
        self.status_lbl = QLabel("● AI Coach is active"); self.status_lbl.setStyleSheet("font-size: 11px; color: #10B981; font-weight: 600; border: none;")
        title_v.addWidget(self.mode_lbl); title_v.addWidget(self.status_lbl)
        hl.addLayout(title_v); hl.addStretch()
        
        self.tab_group = QFrame()
        self.tab_group.setStyleSheet("background: #F1F5F9; border-radius: 10px; padding: 2px;")
        tl = QHBoxLayout(self.tab_group); tl.setContentsMargins(2, 2, 2, 2); tl.setSpacing(2)
        self.tab_btns = []
        for i, t in enumerate(["Chat", "Plans", "Analysis", "Simulation"]):
            btn = QPushButton(t)
            btn.setCheckable(True); btn.setChecked(i == 0)
            btn.setFixedSize(80, 30)
            btn.setStyleSheet("QPushButton { border: none; border-radius: 8px; font-size: 12px; font-weight: 600; color: #64748B; } QPushButton:checked { background: white; color: #0F172A; }")
            btn.clicked.connect(lambda ch, idx=i: self._switch_tab(idx))
            tl.addWidget(btn); self.tab_btns.append(btn)
        hl.addWidget(self.tab_group); hl.addStretch()
        
        self.btn_sum = QPushButton("Summarize")
        self.btn_sum.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 6px 12px; font-weight: 600; font-size: 12px;")
        hl.addWidget(self.btn_sum); self.main_layout.addWidget(self.header)

        # 2. Main Stack
        self.stack = QStackedWidget()
        
        # Tab 0: Chat View
        self.chat_view = QWidget()
        cvl = QVBoxLayout(self.chat_view); cvl.setContentsMargins(0, 0, 0, 0); cvl.setSpacing(0)
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.chat_container = QWidget(); self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(40, 32, 40, 32); self.chat_layout.setSpacing(12); self.chat_layout.addStretch()
        self.scroll.setWidget(self.chat_container); cvl.addWidget(self.scroll, 1)
        
        # Input Area
        self.input_area = QFrame(); self.input_area.setStyleSheet("background: transparent;")
        il = QVBoxLayout(self.input_area); il.setContentsMargins(40, 0, 40, 40); il.setSpacing(16)
        
        qa_row = QHBoxLayout(); qa_row.setSpacing(12)
        qa_row.addWidget(QuickActionCard("📝", "Resume Tips", "Optimize your bullet points"))
        qa_row.addWidget(QuickActionCard("🎙️", "Mock Interview", "Practice for your next role"))
        qa_row.addWidget(QuickActionCard("🎯", "Skill Gap", "Identify what's missing"))
        il.addLayout(qa_row)
        
        # Redesigned Modern AI Input Bar
        self.chat_input = ChatInputWidget()
        self.chat_input.send_requested.connect(self._handle_send_text)
        il.addWidget(self.chat_input)
        
        cvl.addWidget(self.input_area)
        self.stack.addWidget(self.chat_view)

        # Other Tabs (Placeholders)
        for t in ["Plans", "Analysis", "Simulation"]:
            w = QWidget(); l = QVBoxLayout(w); l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.addWidget(QLabel(f"{t} Workspace Coming Soon", styleSheet="color: #94A3B8; font-size: 16px; font-weight: 600;"))
            self.stack.addWidget(w)

        self.main_layout.addWidget(self.stack)

    def _switch_tab(self, idx):
        for i, btn in enumerate(self.tab_btns): btn.setChecked(i == idx)
        self.stack.setCurrentIndex(idx)
        titles = ["Career Chat", "Action Plans", "Career Analysis", "Interview Simulation"]
        self.mode_lbl.setText(titles[idx])

    def append_message(self, text, is_ai=True):
        bubble = MessageBubble(text, is_ai)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        QTimer.singleShot(50, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))

    def _handle_send_text(self, text):
        if not text: return
        self.append_message(text, is_ai=False)
        
        # Show Typing Indicator
        self.typing = TypingIndicator()
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.typing)
        QTimer.singleShot(50, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))
        
        # Simulated AI Response
        QTimer.singleShot(1500, self._ai_respond)

    def _ai_respond(self):
        self.typing.deleteLater()
        self.append_message("That's a great question! Based on your target role as a Senior Software Engineer, I recommend focusing on distributed systems and cloud architecture patterns. Would you like me to generate a study plan for you?", is_ai=True)
