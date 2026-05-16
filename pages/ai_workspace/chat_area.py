from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor
from .message_widgets import AIMessageWidget, UserMessageWidget
from .typing_indicator import TypingIndicator
from .input_widget import ChatInputWidget

class ChatArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F8FAFC;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self._setup_header(layout)
        
        # Chat Messages Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_layout.setContentsMargins(40, 30, 40, 30)
        self.history_layout.setSpacing(10)
        
        # Empty State
        self.empty_container = QWidget()
        el = QVBoxLayout(self.empty_container)
        el.setContentsMargins(0, 100, 0, 0)
        el.setSpacing(20)
        el.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo = QLabel("✦")
        logo.setStyleSheet("font-size: 64px; color: #BAE6FD; border: none; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        el.addWidget(logo)
        
        welcome = QLabel("How can I help you today?")
        welcome.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        el.addWidget(welcome)
        
        sub = QLabel("Your AI Career Copilot is ready to assist with resumes, roadmaps, and interview prep.")
        sub.setStyleSheet("font-size: 14px; color: #64748B; border: none;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        el.addWidget(sub)
        
        # Prompts
        prompts_layout = QHBoxLayout()
        prompts_layout.setSpacing(12)
        prompts_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        prompts = [
            "Analyze my Resume",
            "Create Study Plan",
            "Mock Interview",
            "Career Advice"
        ]
        
        for p in prompts:
            btn = QPushButton(p)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
                    padding: 10px 16px; font-size: 13px; font-weight: 600; color: #475569;
                }
                QPushButton:hover { background-color: #F8FAFC; border-color: #38BDF8; color: #38BDF8; }
            """)
            btn.clicked.connect(lambda ch, t=p: self.add_user_message(t))
            prompts_layout.addWidget(btn)
            
        el.addLayout(prompts_layout)
        self.history_layout.addWidget(self.empty_container)
        self.history_layout.addStretch()
        
        self.scroll.setWidget(self.history_widget)
        layout.addWidget(self.scroll)
        
        # Typing Indicator
        self.typing_container = QWidget()
        self.typing_layout = QHBoxLayout(self.typing_container)
        self.typing_layout.setContentsMargins(40, 0, 40, 10)
        self.typing_indicator = TypingIndicator()
        self.typing_layout.addWidget(self.typing_indicator)
        self.typing_layout.addStretch()
        self.typing_container.hide()
        layout.addWidget(self.typing_container)
        
        # Chat Input
        self.input_container = QWidget()
        ic_layout = QVBoxLayout(self.input_container)
        ic_layout.setContentsMargins(40, 0, 40, 30)
        
        self.chat_input = ChatInputWidget()
        self.chat_input.send_requested.connect(self.add_user_message)
        ic_layout.addWidget(self.chat_input)
        
        layout.addWidget(self.input_container)

    def _setup_header(self, layout):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(32, 0, 32, 0)
        h_layout.setSpacing(16)
        
        # AI Info
        avatar = QLabel("✦")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #F0F9FF; color: #38BDF8; border-radius: 20px;
            font-size: 20px; font-weight: bold; border: 1px solid #BAE6FD;
        """)
        h_layout.addWidget(avatar)
        
        info = QVBoxLayout()
        info.setSpacing(0)
        info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title = QLabel("Career Copilot")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A; border: none;")
        status = QLabel("●  Always Active")
        status.setStyleSheet("font-size: 11px; font-weight: 700; color: #10B981; border: none;")
        info.addWidget(title)
        info.addWidget(status)
        h_layout.addLayout(info)
        
        h_layout.addStretch()
        
        # Model Selector
        self.model_selector = QComboBox()
        self.model_selector.addItems(["GPT-4o (Career)", "Claude 3.5 Sonnet", "DeepSeek-V3"])
        self.model_selector.setFixedWidth(160)
        self.model_selector.setStyleSheet("""
            QComboBox {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                padding: 6px 12px; font-size: 12px; font-weight: 600; color: #475569;
            }
            QComboBox::drop-down { border: none; }
        """)
        h_layout.addWidget(self.model_selector)
        
        # Action Buttons
        for icon in ["🗑️", "📤", "⚙️"]:
            btn = QPushButton(icon)
            btn.setFixedSize(36, 36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; border: none; font-size: 16px; color: #64748B;
                }
                QPushButton:hover { background-color: #F1F5F9; color: #0F172A; border-radius: 10px; }
            """)
            h_layout.addWidget(btn)
            
        layout.addWidget(header)

    def add_user_message(self, text):
        if hasattr(self, 'empty_container') and self.empty_container.isVisible():
            self.empty_container.hide()
            
        import datetime
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        msg = UserMessageWidget(text, time_str)
        # Add before the stretch
        self.history_layout.insertWidget(self.history_layout.count() - 1, msg)
        self.scroll_to_bottom()
        
        # Simulate AI Thinking
        QTimer.singleShot(500, self.show_typing)
        QTimer.singleShot(2000, lambda: self.add_ai_response(text))

    def add_ai_response(self, user_text):
        self.hide_typing()
        import datetime
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        
        response_text = f"I've analyzed your request about '{user_text}'. Here is how I can help:"
        msg = AIMessageWidget(response_text, time_str)
        
        # Example: Add code block if user asks for code
        if "python" in user_text.lower() or "code" in user_text.lower():
            msg.add_code_block("def career_success():\n    skills = ['Python', 'AI', 'Soft Skills']\n    return '🚀' if all(skills) else '📈'", "python")
            
        msg.add_suggestion_chips(["Improve Resume", "Practice Interview", "Learn More"])
        
        self.history_layout.insertWidget(self.history_layout.count() - 1, msg)
        self.scroll_to_bottom()

    def show_typing(self):
        self.typing_container.show()
        self.typing_indicator.start()
        self.scroll_to_bottom()

    def hide_typing(self):
        self.typing_container.hide()
        self.typing_indicator.stop()

    def scroll_to_bottom(self):
        QTimer.singleShot(10, lambda: self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum()))
