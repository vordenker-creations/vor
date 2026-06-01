from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QLinearGradient, QPalette
from modules.local_storage import local_data

class CVBuilderPage(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        
        # Nền ứng dụng siêu sạch
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)
        
        # ==========================================
        # LEFT PANEL (40%) - Form & Action
        # ==========================================
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
        """)
        
        left_shadow = QGraphicsDropShadowEffect()
        left_shadow.setBlurRadius(30)
        left_shadow.setColor(QColor(15, 23, 42, 10))
        left_shadow.setOffset(0, 5)
        left_panel.setGraphicsEffect(left_shadow)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(30, 30, 30, 30)
        left_layout.setSpacing(24)
        
        title_lbl = QLabel("Tạo CV AI Cao Cấp")
        title_lbl.setStyleSheet("font-size: 24px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px; border: none; background: transparent;")
        left_layout.addWidget(title_lbl)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { border: none; background: transparent; width: 4px; }
            QScrollBar::handle:vertical { background: #CBD5E1; border-radius: 2px; }
        """)
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setContentsMargins(0, 0, 10, 0)
        form_layout.setSpacing(20)
        
        def add_section(title):
            lbl = QLabel(title)
            lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; border: none;")
            form_layout.addWidget(lbl)
            
        def create_input(text, placeholder):
            inp = QLineEdit()
            inp.setText(text)
            inp.setPlaceholderText(placeholder)
            inp.setStyleSheet("""
                QLineEdit {
                    background-color: #F1F5F9;
                    border: 2px solid transparent;
                    border-radius: 12px;
                    padding: 14px 18px;
                    color: #0F172A;
                    font-size: 14px;
                    font-weight: 600;
                }
                QLineEdit:focus {
                    background-color: #FFFFFF;
                    border: 2px solid #38BDF8;
                }
            """)
            return inp

        def create_textarea(text, height=80):
            txt = QTextEdit()
            txt.setText(text)
            txt.setFixedHeight(height)
            txt.setStyleSheet("""
                QTextEdit {
                    background-color: #F1F5F9;
                    border: 2px solid transparent;
                    border-radius: 12px;
                    padding: 14px 18px;
                    color: #0F172A;
                    font-size: 14px;
                    font-weight: 600;
                }
                QTextEdit:focus {
                    background-color: #FFFFFF;
                    border: 2px solid #38BDF8;
                }
            """)
            return txt

        # Personal Info
        add_section("Thông Tin Cá Nhân")
        self.name_input = create_input("Bùi Lê Công Hậu", "Họ và tên")
        self.email_input = create_input("hau.bui@example.com", "Email liên hệ")
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        
        # Education
        add_section("Học Vấn")
        self.major_input = create_input("AI Engineer", "Chuyên ngành")
        self.uni_input = create_input("VKU", "Trường đại học")
        form_layout.addWidget(self.major_input)
        form_layout.addWidget(self.uni_input)
        
        # Skills
        add_section("Kỹ Năng Công Nghệ")
        self.skills_input = create_textarea("Python, C++, Java", height=60)
        form_layout.addWidget(self.skills_input)
        
        # Projects
        add_section("Dự Án Nổi Bật")
        self.projects_input = create_textarea("Robotics FPV\nAI Computer Vision System", height=80)
        form_layout.addWidget(self.projects_input)
        
        form_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        left_layout.addWidget(scroll_area)

        # Restore saved draft from local storage
        self._restore_draft()
        
        # AI Auto-Generate Button (Primary CTA - SaaS Style)
        self.btn_ai_generate = QPushButton("✨ AI Auto-Generate")
        self.btn_ai_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ai_generate.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #3B82F6);
                color: #FFFFFF;
                font-weight: 800;
                border-radius: 16px;
                padding: 18px;
                font-size: 16px;
                border: none;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #2563EB);
            }
        """)
        
        btn_ai_shadow = QGraphicsDropShadowEffect()
        btn_ai_shadow.setBlurRadius(24)
        btn_ai_shadow.setColor(QColor(139, 92, 246, 80)) # Purple/Blue glow
        btn_ai_shadow.setOffset(0, 6)
        self.btn_ai_generate.setGraphicsEffect(btn_ai_shadow)
        
        # Export Button -> Now Secondary
        self.btn_export = QPushButton("Export to PDF")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC;
                color: #475569;
                font-weight: 700;
                border-radius: 16px;
                border: 2px solid #E2E8F0;
                padding: 16px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                color: #0F172A;
                border-color: #CBD5E1;
            }
        """)
        
        left_layout.addWidget(self.btn_ai_generate)
        left_layout.addWidget(self.btn_export)
        
        # ==========================================
        # RIGHT PANEL (60%) - A4 Live Preview
        # ==========================================
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: transparent;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { border: none; background: transparent; width: 0px; }
        """)
        
        right_scroll_content = QWidget()
        right_scroll_content.setStyleSheet("background: transparent;")
        r_content_layout = QVBoxLayout(right_scroll_content)
        r_content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.a4_paper = QFrame()
        self.a4_paper.setFixedSize(620, 877) # A4 ratio
        self.a4_paper.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 4px;
            }
        """)
        
        # Strong shadow to separate from background
        paper_shadow = QGraphicsDropShadowEffect()
        paper_shadow.setBlurRadius(50)
        paper_shadow.setColor(QColor(15, 23, 42, 25))
        paper_shadow.setOffset(0, 15)
        self.a4_paper.setGraphicsEffect(paper_shadow)
        
        paper_layout = QVBoxLayout(self.a4_paper)
        paper_layout.setContentsMargins(60, 70, 60, 70)
        paper_layout.setSpacing(0)
        paper_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Typography Hierarchy
        self.cv_name = QLabel(self.name_input.text())
        self.cv_name.setStyleSheet("font-size: 36px; font-weight: 900; color: #0F172A; border: none; letter-spacing: -1px;")
        
        self.cv_contact = QLabel(self.email_input.text())
        self.cv_contact.setStyleSheet("font-size: 14px; color: #64748B; border: none; margin-top: 5px; margin-bottom: 35px; font-weight: 500;")
        
        paper_layout.addWidget(self.cv_name)
        paper_layout.addWidget(self.cv_contact)
        
        def add_cv_section_title(title):
            lbl = QLabel(title)
            lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 1.5px; border: none; margin-top: 25px; margin-bottom: 12px;")
            paper_layout.addWidget(lbl)
            
        # Education
        add_cv_section_title("Học Vấn")
        
        self.cv_major = QLabel(self.major_input.text())
        self.cv_major.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        self.cv_uni = QLabel(self.uni_input.text())
        self.cv_uni.setStyleSheet("font-size: 15px; font-weight: 500; color: #475569; border: none; margin-top: 4px;")
        
        paper_layout.addWidget(self.cv_major)
        paper_layout.addWidget(self.cv_uni)
        
        # Skills
        add_cv_section_title("Kỹ Năng")
        
        self.cv_skills = QLabel(self.skills_input.toPlainText())
        self.cv_skills.setWordWrap(True)
        self.cv_skills.setStyleSheet("font-size: 15px; font-weight: 500; color: #334155; border: none; line-height: 1.6;")
        
        paper_layout.addWidget(self.cv_skills)
        
        # Projects
        add_cv_section_title("Dự Án Từng Tham Gia")
        
        self.cv_projects = QLabel(self.projects_input.toPlainText())
        self.cv_projects.setWordWrap(True)
        self.cv_projects.setStyleSheet("font-size: 15px; font-weight: 500; color: #334155; border: none; line-height: 1.6;")
        
        paper_layout.addWidget(self.cv_projects)
        
        paper_layout.addStretch()
        
        r_content_layout.addWidget(self.a4_paper)
        right_scroll.setWidget(right_scroll_content)
        right_layout.addWidget(right_scroll)
        
        # Weights
        main_layout.addWidget(left_panel, 4)
        main_layout.addWidget(right_panel, 6)
        
        # Connections
        self.name_input.textChanged.connect(self._update_preview)
        self.email_input.textChanged.connect(self._update_preview)
        self.major_input.textChanged.connect(self._update_preview)
        self.uni_input.textChanged.connect(self._update_preview)
        self.skills_input.textChanged.connect(self._update_preview)
        self.projects_input.textChanged.connect(self._update_preview)
        
        self.btn_ai_generate.clicked.connect(self._on_ai_generate)
        
    def _update_preview(self):
        self.cv_name.setText(self.name_input.text().strip() or "Họ và Tên")
        self.cv_contact.setText(self.email_input.text().strip() or "email@example.com")
        self.cv_major.setText(self.major_input.text().strip() or "Chuyên ngành")
        self.cv_uni.setText(self.uni_input.text().strip() or "Tên trường đại học")
        self.cv_skills.setText(self.skills_input.toPlainText().strip() or "Kỹ năng của bạn")
        self.cv_projects.setText(self.projects_input.toPlainText().strip() or "Dự án của bạn")

        # Auto-save draft to local storage
        local_data.save("cv_draft.name", self.name_input.text())
        local_data.save("cv_draft.email", self.email_input.text())
        local_data.save("cv_draft.major", self.major_input.text())
        local_data.save("cv_draft.uni", self.uni_input.text())
        local_data.save("cv_draft.skills", self.skills_input.toPlainText())
        local_data.save("cv_draft.projects", self.projects_input.toPlainText())

    def _restore_draft(self):
        """Restore CV draft fields from local storage if a saved draft exists."""
        name = local_data.get("cv_draft.name")
        if name is not None:
            self.name_input.setText(name)
            self.email_input.setText(local_data.get("cv_draft.email", ""))
            self.major_input.setText(local_data.get("cv_draft.major", ""))
            self.uni_input.setText(local_data.get("cv_draft.uni", ""))
            self.skills_input.setText(local_data.get("cv_draft.skills", ""))
            self.projects_input.setText(local_data.get("cv_draft.projects", ""))
            self._update_preview()

    def _on_ai_generate(self):
        # Placeholder cho tính năng API Auto-Generate sau này
        pass
