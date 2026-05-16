from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor
from .waveform_widget import VoiceWaveformWidget

class AIInterviewerCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            AIInterviewerCard {
                background-color: #FFFFFF;
                border-radius: 24px;
                border: 1px solid #E2E8F0;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(15, 23, 42, 20))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        # AI Avatar
        avatar = QLabel("✦")
        avatar.setFixedSize(64, 64)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #0F172A;
            color: #38BDF8;
            border-radius: 32px;
            font-size: 32px;
            font-weight: bold;
        """)
        layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # AI Status
        status = QLabel("●  AI Interviver Speaking")
        status.setStyleSheet("color: #10B981; font-size: 11px; font-weight: 700; text-transform: uppercase;")
        layout.addWidget(status, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Question Card
        self.question_card = QFrame()
        self.question_card.setStyleSheet("""
            background-color: #F8FAFC;
            border-radius: 20px;
            border: 1px solid #E2E8F0;
            padding: 24px;
        """)
        ql = QVBoxLayout(self.question_card)
        self.question_text = QLabel("Tell me about a time you handled a difficult technical challenge in a team environment. What was your role and the outcome?")
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet("font-size: 18px; font-weight: 600; color: #0F172A; line-height: 1.6; border: none;")
        ql.addWidget(self.question_text)
        
        layout.addWidget(self.question_card)

class InterviewWorkspace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F8FAFC;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self._setup_header(layout)
        
        # Interaction Area
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(40, 32, 40, 40)
        cl.setSpacing(32)
        
        # 1. AI Interviewer Card
        self.ai_card = AIInterviewerCard()
        cl.addWidget(self.ai_card)
        
        # 2. User Response Area
        self.response_area = QFrame()
        self.response_area.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 24px;
                border: 1px solid #E2E8F0;
                padding: 32px;
            }
        """)
        rl = QVBoxLayout(self.response_area)
        rl.setSpacing(20)
        
        # Waveform
        self.waveform = VoiceWaveformWidget()
        rl.addWidget(self.waveform)
        
        # Controls
        ctrl = QHBoxLayout()
        ctrl.setSpacing(16)
        
        self.btn_record = QPushButton("● Start Speaking")
        self.btn_record.setFixedHeight(48)
        self.btn_record.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_record.setStyleSheet("""
            QPushButton {
                background-color: #EF4444; color: white; border-radius: 24px;
                font-size: 15px; font-weight: 700; padding: 0 24px; border: none;
            }
            QPushButton:hover { background-color: #DC2626; }
        """)
        self.btn_record.clicked.connect(self._toggle_recording)
        
        self.btn_skip = QPushButton("Skip Question")
        self.btn_skip.setFixedHeight(48)
        self.btn_skip.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9; color: #475569; border-radius: 24px;
                font-size: 14px; font-weight: 600; padding: 0 20px; border: none;
            }
            QPushButton:hover { background-color: #E2E8F0; }
        """)
        
        ctrl.addStretch()
        ctrl.addWidget(self.btn_skip)
        ctrl.addWidget(self.btn_record)
        ctrl.addStretch()
        rl.addLayout(ctrl)
        
        cl.addWidget(self.response_area)
        
        # 3. Live Transcript
        transcript_lbl = QLabel("Live Transcript")
        transcript_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
        cl.addWidget(transcript_lbl)
        
        self.transcript_box = QLabel("Waiting for your response...")
        self.transcript_box.setWordWrap(True)
        self.transcript_box.setStyleSheet("""
            color: #64748B; font-size: 15px; line-height: 1.5; font-style: italic;
        """)
        cl.addWidget(self.transcript_box)
        
        cl.addStretch()
        layout.addWidget(content)

    def _setup_header(self, layout):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(32, 0, 32, 0)
        hl.setSpacing(20)
        
        # Info
        info = QVBoxLayout()
        info.setSpacing(2)
        info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title = QLabel("AI Mock Interview")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        status = QLabel("●  Recording Session")
        status.setStyleSheet("font-size: 11px; font-weight: 700; color: #EF4444;")
        info.addWidget(title)
        info.addWidget(status)
        hl.addLayout(info)
        
        hl.addStretch()
        
        # Progress
        progress = QHBoxLayout()
        progress.setSpacing(10)
        for i in range(5):
            dot = QFrame()
            dot.setFixedSize(12, 12)
            color = "#38BDF8" if i == 0 else "#E2E8F0"
            dot.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
            progress.addWidget(dot)
        hl.addLayout(progress)
        
        hl.addStretch()
        
        # Actions
        btns = QHBoxLayout()
        btns.setSpacing(12)
        for icon in ["⏸", "🔄", "⚙️"]:
            btn = QPushButton(icon)
            btn.setFixedSize(36, 36)
            btn.setStyleSheet("background-color: #F1F5F9; border-radius: 18px; font-size: 14px; border: none;")
            btns.addWidget(btn)
        hl.addLayout(btns)
        
        layout.addWidget(header)

    def _toggle_recording(self):
        if not self.waveform.is_active:
            self.waveform.start()
            self.btn_record.setText("■ Stop Recording")
            self.transcript_box.setText("Listening... \"In my previous project at Google, I was responsible for refactoring the data pipeline...\"")
            self.transcript_box.setStyleSheet("color: #1E293B; font-size: 15px; line-height: 1.5; font-style: normal;")
        else:
            self.waveform.stop()
            self.btn_record.setText("● Start Speaking")
