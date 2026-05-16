from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QLineEdit, QTextEdit, 
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class SectionCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            SectionCard {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #E2E8F0;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(15, 23, 42, 20))
        self.setGraphicsEffect(shadow)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)
        
        # Header
        header = QHBoxLayout()
        header.setSpacing(12)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 18px; font-weight: 700; color: #0F172A;")
        header.addWidget(title_lbl)
        header.addStretch()
        
        ai_btn = QPushButton("✨ AI Improve")
        ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ai_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F9FF; color: #0284C7; border-radius: 8px;
                font-size: 12px; font-weight: 600; padding: 6px 12px; border: 1px solid #BAE6FD;
            }
            QPushButton:hover { background-color: #BAE6FD; }
        """)
        header.addWidget(ai_btn)
        
        self.main_layout.addLayout(header)

    def add_field(self, label, placeholder, is_multiline=False):
        row = QVBoxLayout()
        row.setSpacing(6)
        l_lbl = QLabel(label)
        l_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #64748B;")
        row.addWidget(l_lbl)
        
        if is_multiline:
            field = QTextEdit()
            field.setPlaceholderText(placeholder)
            field.setFixedHeight(100)
            field.setStyleSheet("""
                QTextEdit {
                    background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
                    padding: 10px; color: #1E293B; font-size: 13px;
                }
                QTextEdit:focus { border: 1px solid #38BDF8; background-color: white; }
            """)
        else:
            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            field.setFixedHeight(40)
            field.setStyleSheet("""
                QLineEdit {
                    background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;
                    padding: 0 12px; color: #1E293B; font-size: 13px;
                }
                QLineEdit:focus { border: 1px solid #38BDF8; background-color: white; }
            """)
            
        row.addWidget(field)
        self.main_layout.addLayout(row)

class ResumeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F8FAFC;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self._setup_header(layout)
        
        # Editor Workspace
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(32, 24, 32, 40)
        self.content_layout.setSpacing(24)
        
        # Personal Info Card
        pi_card = SectionCard("Personal Information")
        pi_card.add_field("Full Name", "e.g. John Doe")
        pi_card.add_field("Professional Title", "e.g. Senior Software Engineer")
        
        contact_row = QHBoxLayout()
        contact_row.setSpacing(16)
        
        email_v = QVBoxLayout()
        email_v.addWidget(QLabel("Email", styleSheet="font-size: 12px; font-weight: 600; color: #64748B;"))
        email_field = QLineEdit()
        email_field.setPlaceholderText("e.g. john@example.com")
        email_field.setFixedHeight(40)
        email_field.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 0 12px;")
        email_v.addWidget(email_field)
        
        phone_v = QVBoxLayout()
        phone_v.addWidget(QLabel("Phone", styleSheet="font-size: 12px; font-weight: 600; color: #64748B;"))
        phone_field = QLineEdit()
        phone_field.setPlaceholderText("e.g. +1 234 567 890")
        phone_field.setFixedHeight(40)
        phone_field.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 0 12px;")
        phone_v.addWidget(phone_field)
        
        contact_row.addLayout(email_v)
        contact_row.addLayout(phone_v)
        pi_card.main_layout.addLayout(contact_row)
        
        self.content_layout.addWidget(pi_card)
        
        # Summary Card
        summary_card = SectionCard("Professional Summary")
        summary_card.add_field("Summary", "Briefly describe your professional background and key achievements...", is_multiline=True)
        self.content_layout.addWidget(summary_card)
        
        # Experience Card
        exp_card = SectionCard("Work Experience")
        exp_card.add_field("Company Name", "e.g. Google")
        exp_card.add_field("Job Title", "e.g. Software Engineer")
        exp_card.add_field("Description", "Describe your responsibilities and achievements...", is_multiline=True)
        
        add_exp = QPushButton("+ Add another experience")
        add_exp.setStyleSheet("color: #38BDF8; font-weight: 700; font-size: 13px; text-align: left; border: none; background: transparent; padding: 0;")
        add_exp.setCursor(Qt.CursorShape.PointingHandCursor)
        exp_card.main_layout.addWidget(add_exp)
        
        self.content_layout.addWidget(exp_card)
        
        self.content_layout.addStretch()
        
        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)

    def _setup_header(self, layout):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(32, 0, 32, 0)
        hl.setSpacing(20)
        
        # Left: Info
        info = QVBoxLayout()
        info.setSpacing(2)
        info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        name = QLabel("My Resume 2026")
        name.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        status = QLabel("✓ Saved to cloud")
        status.setStyleSheet("font-size: 11px; font-weight: 600; color: #10B981;")
        info.addWidget(name)
        info.addWidget(status)
        hl.addLayout(info)
        
        hl.addStretch()
        
        # Center: Zoom/Layout
        controls = QHBoxLayout()
        controls.setSpacing(8)
        for btn_text in ["-", "100%", "+"]:
            btn = QPushButton(btn_text)
            btn.setFixedSize(36, 32)
            btn.setStyleSheet("background-color: #F1F5F9; border-radius: 8px; font-size: 11px; font-weight: 700; border: none;")
            controls.addWidget(btn)
        hl.addLayout(controls)
        
        hl.addStretch()
        
        # Right: Actions
        btns = QHBoxLayout()
        btns.setSpacing(12)
        
        preview_btn = QPushButton("Preview")
        preview_btn.setStyleSheet("background-color: #F1F5F9; color: #0F172A; border-radius: 10px; font-weight: 700; font-size: 12px; height: 38px; padding: 0 16px; border: none;")
        
        export_btn = QPushButton("Export PDF")
        export_btn.setStyleSheet("background-color: #38BDF8; color: white; border-radius: 10px; font-weight: 700; font-size: 12px; height: 38px; padding: 0 16px; border: none;")
        
        btns.addWidget(preview_btn)
        btns.addWidget(export_btn)
        hl.addLayout(btns)
        
        layout.addWidget(header)
