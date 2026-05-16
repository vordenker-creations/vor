from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QTextEdit, QFileDialog,
                             QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor

class ApplicationModal(QDialog):
    def __init__(self, job_data, parent=None):
        super().__init__(parent)
        self.job_data = job_data
        self.setWindowTitle("Apply for Job")
        self.setFixedSize(600, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setup_ui()

    def setup_ui(self):
        # Main Container with rounded corners and border
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 24px;
            }
        """)
        
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0; border-top-left-radius: 24px; border-top-right-radius: 24px;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(32, 0, 32, 0)
        
        title_v = QVBoxLayout()
        title_v.setSpacing(2)
        title_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        main_title = QLabel(f"Apply to {self.job_data.get('company', 'Company')}")
        main_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        sub_title = QLabel(self.job_data.get("title", "Job Title"))
        sub_title.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none;")
        
        title_v.addWidget(main_title)
        title_v.addWidget(sub_title)
        hl.addLayout(title_v)
        
        hl.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9; border: none; border-radius: 16px;
                color: #64748B; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #E2E8F0; color: #0F172A; }
        """)
        hl.addWidget(close_btn)
        
        container_layout.addWidget(header)
        
        # Body
        body = QFrame()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(32, 32, 32, 32)
        body_layout.setSpacing(24)
        
        # Resume Selection
        resume_v = QVBoxLayout()
        resume_v.setSpacing(12)
        res_lbl = QLabel("Resume / CV")
        res_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none;")
        resume_v.addWidget(res_lbl)
        
        self.resume_path = QLineEdit()
        self.resume_path.setReadOnly(True)
        self.resume_path.setPlaceholderText("Upload your latest resume...")
        self.resume_path.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 12px;
                padding: 12px 16px; font-size: 13px; color: #475569;
            }
        """)
        
        upload_btn = QPushButton("Choose File")
        upload_btn.setFixedHeight(44)
        upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_btn.clicked.connect(self._upload_resume)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px;
                color: #0F172A; font-size: 13px; font-weight: 600; padding: 0 16px;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #CBD5E1; }
        """)
        
        rh = QHBoxLayout()
        rh.setSpacing(12)
        rh.addWidget(self.resume_path, 1)
        rh.addWidget(upload_btn)
        resume_v.addLayout(rh)
        body_layout.addLayout(resume_v)
        
        # Cover Letter
        cl_v = QVBoxLayout()
        cl_v.setSpacing(12)
        cl_h = QHBoxLayout()
        cl_lbl = QLabel("Cover Letter")
        cl_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none;")
        
        ai_gen_btn = QPushButton("✨ Generate with AI")
        ai_gen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ai_gen_btn.clicked.connect(self._generate_with_ai)
        ai_gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD;
                border-radius: 8px; padding: 4px 12px; font-size: 11px; font-weight: 700;
            }
            QPushButton:hover { background-color: #E0F2FE; }
        """)
        
        cl_h.addWidget(cl_lbl)
        cl_h.addStretch()
        cl_h.addWidget(ai_gen_btn)
        cl_v.addLayout(cl_h)
        
        self.cl_text = QTextEdit()
        self.cl_text.setPlaceholderText("Write why you're a great fit for this role...")
        self.cl_text.setStyleSheet("""
            QTextEdit {
                background-color: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 12px;
                padding: 16px; font-size: 13px; color: #475569; line-height: 1.5;
            }
            QTextEdit:focus { border-color: #38BDF8; }
        """)
        cl_v.addWidget(self.cl_text)
        body_layout.addLayout(cl_v)
        
        container_layout.addWidget(body)
        
        # Footer
        footer = QFrame()
        footer.setFixedHeight(100)
        footer.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #E2E8F0; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;")
        fh = QHBoxLayout(footer)
        fh.setContentsMargins(32, 0, 32, 0)
        fh.setSpacing(16)
        
        self.submit_btn = QPushButton("Submit Application")
        self.submit_btn.setFixedHeight(52)
        self.submit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self._submit)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 16px;
                font-size: 15px; font-weight: 700; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        
        fh.addWidget(self.submit_btn, 1)
        container_layout.addWidget(footer)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.container)

    def _upload_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Resume", "", "PDF Files (*.pdf);;Word Files (*.docx)")
        if file_path:
            self.resume_path.setText(file_path)

    def _generate_with_ai(self):
        self.cl_text.setPlaceholderText("AI is generating your cover letter...")
        self.cl_text.clear()
        
        # Mock AI generation
        def update_text():
            mock_text = f"Dear Hiring Team at {self.job_data.get('company', 'the company')},\n\nI am writing to express my strong interest in the {self.job_data.get('title', 'position')} role. With my background in AI and Software Engineering, I am confident that I can contribute significantly to your team...\n\nThank you for your consideration.\n\nBest regards,\n[Your Name]"
            self.cl_text.setText(mock_text)
            
        QTimer.singleShot(1500, update_text)

    def _submit(self):
        self.submit_btn.setText("Sending...")
        self.submit_btn.setEnabled(False)
        
        QTimer.singleShot(2000, self.accept)
