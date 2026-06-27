import base64
import json
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QFileDialog, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QByteArray, QCoreApplication
from PyQt6.QtGui import QColor, QFont, QLinearGradient, QPalette, QPixmap, QPainter, QPageSize
from modules.local_storage import local_data
from core.config import SERVER_URL

class CVBuilderPage(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        
        self.certificates = []
        self.avatar_base64 = ""
        self.avatar_path = None
        
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
            lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; border: none; margin-top: 10px;")
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
                    border: 2px solid #2563EB;
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
                    border: 2px solid #2563EB;
                }
            """)
            return txt
 
        # Personal Info
        add_section("Thông Tin Cá Nhân")
        self.name_input = create_input("Bùi Lê Công Hậu", "Họ và tên")
        self.email_input = create_input("hau.bui@example.com", "Email liên hệ")
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.email_input)
        
        # Biography
        add_section("Tiểu Sử / Giới thiệu")
        self.bio_input = create_textarea("Lập trình viên nhiệt huyết với đam mê AI và Web...", height=70)
        form_layout.addWidget(self.bio_input)

        # Personal Photo
        add_section("Ảnh Đại Diện")
        photo_row = QHBoxLayout()
        self.lbl_avatar_preview = QLabel("Chưa chọn ảnh")
        self.lbl_avatar_preview.setStyleSheet("color: #64748B; font-size: 12px; font-weight: bold;")
        self.btn_avatar = QPushButton("Tải ảnh")
        self.btn_avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_avatar.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 8px;
                padding: 6px 12px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        self.btn_avatar.clicked.connect(self._upload_avatar)
        photo_row.addWidget(self.lbl_avatar_preview, 3)
        photo_row.addWidget(self.btn_avatar, 1)
        form_layout.addLayout(photo_row)

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
        
        # Certificates list
        add_section("Chứng Chỉ & Giải Thưởng")
        
        cert_form = QVBoxLayout()
        cert_form.setSpacing(6)
        
        self.edit_cert_name = QLineEdit()
        self.edit_cert_name.setPlaceholderText("Tên chứng chỉ (ví dụ: IELTS 8.0)...")
        self.edit_cert_name.setStyleSheet("QLineEdit { background: #F1F5F9; border-radius: 8px; padding: 8px; font-size: 12px; }")
        
        cert_row2 = QHBoxLayout()
        self.edit_cert_year = QLineEdit()
        self.edit_cert_year.setPlaceholderText("Năm (ví dụ: 2024)")
        self.edit_cert_year.setStyleSheet("QLineEdit { background: #F1F5F9; border-radius: 8px; padding: 8px; font-size: 12px; }")
        
        self.btn_cert_img = QPushButton("Tải ảnh")
        self.btn_cert_img.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cert_img.setStyleSheet("""
            QPushButton {
                background: #64748B; color: white; border-radius: 8px;
                padding: 6px 12px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background: #475569; }
        """)
        self.btn_cert_img.clicked.connect(self._upload_cert_image)
        
        cert_row2.addWidget(self.edit_cert_year, 2)
        cert_row2.addWidget(self.btn_cert_img, 1)
        
        self.btn_add_cert = QPushButton("+ Thêm chứng chỉ")
        self.btn_add_cert.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_cert.setStyleSheet("""
            QPushButton {
                background: #2563EB; color: white; border-radius: 8px;
                padding: 8px; font-size: 12px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #1D4ED8; }
        """)
        self.btn_add_cert.clicked.connect(self._add_certificate)
        
        cert_form.addWidget(self.edit_cert_name)
        cert_form.addLayout(cert_row2)
        cert_form.addWidget(self.btn_add_cert)
        form_layout.addLayout(cert_form)
        
        self.certs_list_widget = QWidget()
        self.certs_list_lay = QVBoxLayout(self.certs_list_widget)
        self.certs_list_lay.setContentsMargins(0, 0, 0, 0)
        self.certs_list_lay.setSpacing(6)
        form_layout.addWidget(self.certs_list_widget)
        
        form_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        left_layout.addWidget(scroll_area)

        # Restore saved draft from local storage
        self._restore_draft()
        
        # AI Auto-Generate Button
        self.btn_ai_generate = QPushButton("✨ AI Auto-Generate")
        self.btn_ai_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ai_generate.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #3B82F6);
                color: #FFFFFF;
                font-weight: 800;
                border-radius: 16px;
                padding: 14px;
                font-size: 14px;
                border: none;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #2563EB);
            }
        """)
        
        btn_ai_shadow = QGraphicsDropShadowEffect()
        btn_ai_shadow.setBlurRadius(24)
        btn_ai_shadow.setColor(QColor(139, 92, 246, 80))
        btn_ai_shadow.setOffset(0, 6)
        self.btn_ai_generate.setGraphicsEffect(btn_ai_shadow)
        
        # Export Button
        self.btn_export = QPushButton("Export to PDF")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC;
                color: #475569;
                font-weight: 700;
                border-radius: 16px;
                border: 2px solid #E2E8F0;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
                color: #0F172A;
                border-color: #CBD5E1;
            }
        """)

        # Sync Button
        self.btn_sync = QPushButton("Sync to Web Recruiter Portal")
        self.btn_sync.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sync.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 800;
                border-radius: 16px;
                padding: 14px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        
        left_layout.addWidget(self.btn_ai_generate)
        left_layout.addWidget(self.btn_export)
        left_layout.addWidget(self.btn_sync)
        
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
        
        paper_shadow = QGraphicsDropShadowEffect()
        paper_shadow.setBlurRadius(50)
        paper_shadow.setColor(QColor(15, 23, 42, 25))
        paper_shadow.setOffset(0, 15)
        self.a4_paper.setGraphicsEffect(paper_shadow)
        
        paper_layout = QVBoxLayout(self.a4_paper)
        paper_layout.setContentsMargins(60, 60, 60, 60)
        paper_layout.setSpacing(0)
        paper_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Typography Hierarchy with Avatar
        header_lay = QHBoxLayout()
        header_text_lay = QVBoxLayout()
        
        self.cv_name = QLabel(self.name_input.text())
        self.cv_name.setStyleSheet("font-size: 30px; font-weight: 900; color: #0F172A; border: none; letter-spacing: -1px; background: transparent;")
        
        self.cv_contact = QLabel(self.email_input.text())
        self.cv_contact.setStyleSheet("font-size: 13px; color: #64748B; border: none; margin-top: 5px; margin-bottom: 15px; font-weight: 500; background: transparent;")
        
        header_text_lay.addWidget(self.cv_name)
        header_text_lay.addWidget(self.cv_contact)
        header_lay.addLayout(header_text_lay, 4)
        
        self.cv_avatar = QLabel()
        self.cv_avatar.setFixedSize(80, 80)
        self.cv_avatar.setStyleSheet("border-radius: 40px; background-color: #E2E8F0; border: 1px solid #CBD5E1;")
        self.cv_avatar.setScaledContents(True)
        header_lay.addWidget(self.cv_avatar, 1, alignment=Qt.AlignmentFlag.AlignRight)
        
        paper_layout.addLayout(header_lay)
        
        def add_cv_section_title(title):
            lbl = QLabel(title)
            lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #2563EB; text-transform: uppercase; letter-spacing: 1.5px; border: none; margin-top: 20px; margin-bottom: 8px; background: transparent;")
            paper_layout.addWidget(lbl)

        # Bio
        add_cv_section_title("Giới Thiệu Bản Thân")
        self.cv_bio = QLabel(self.bio_input.toPlainText())
        self.cv_bio.setWordWrap(True)
        self.cv_bio.setStyleSheet("font-size: 14px; font-weight: 500; color: #334155; border: none; line-height: 1.5; background: transparent;")
        paper_layout.addWidget(self.cv_bio)
        
        # Education
        add_cv_section_title("Học Vấn")
        self.cv_major = QLabel(self.major_input.text())
        self.cv_major.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        self.cv_uni = QLabel(self.uni_input.text())
        self.cv_uni.setStyleSheet("font-size: 14px; font-weight: 500; color: #475569; border: none; margin-top: 4px; background: transparent;")
        paper_layout.addWidget(self.cv_major)
        paper_layout.addWidget(self.cv_uni)
        
        # Skills
        add_cv_section_title("Kỹ Năng")
        self.cv_skills = QLabel(self.skills_input.toPlainText())
        self.cv_skills.setWordWrap(True)
        self.cv_skills.setStyleSheet("font-size: 14px; font-weight: 500; color: #334155; border: none; line-height: 1.5; background: transparent;")
        paper_layout.addWidget(self.cv_skills)
        
        # Projects
        add_cv_section_title("Dự Án Từng Tham Gia")
        self.cv_projects = QLabel(self.projects_input.toPlainText())
        self.cv_projects.setWordWrap(True)
        self.cv_projects.setStyleSheet("font-size: 14px; font-weight: 500; color: #334155; border: none; line-height: 1.5; background: transparent;")
        paper_layout.addWidget(self.cv_projects)

        # Certificates
        add_cv_section_title("Chứng Chỉ & Giải Thưởng")
        self.cv_certs_lay = QVBoxLayout()
        self.cv_certs_lay.setSpacing(6)
        paper_layout.addLayout(self.cv_certs_lay)
        
        paper_layout.addStretch()
        
        r_content_layout.addWidget(self.a4_paper)
        right_scroll.setWidget(right_scroll_content)
        right_layout.addWidget(right_scroll)
        
        # Splitter Layout separating Form and Preview
        self.cv_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.cv_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #E2E8F0;
                width: 4px;
                margin: 0 8px;
            }
            QSplitter::handle:hover {
                background-color: #2563EB;
            }
        """)
        self.cv_splitter.addWidget(left_panel)
        self.cv_splitter.addWidget(right_panel)
        self.cv_splitter.setSizes([450, 650])
        
        main_layout.addWidget(self.cv_splitter)
        
        # Connections
        self.name_input.textChanged.connect(self._update_preview)
        self.email_input.textChanged.connect(self._update_preview)
        self.major_input.textChanged.connect(self._update_preview)
        self.uni_input.textChanged.connect(self._update_preview)
        self.skills_input.textChanged.connect(self._update_preview)
        self.projects_input.textChanged.connect(self._update_preview)
        self.bio_input.textChanged.connect(self._update_preview)
        
        self.btn_ai_generate.clicked.connect(self._on_ai_generate)
        self.btn_export.clicked.connect(self._export_pdf)
        self.btn_sync.clicked.connect(self._sync_to_web)
        
        from core.config import apply_theme
        apply_theme(self)
        
    def _export_pdf(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Export PDF", "My_CV.pdf", "PDF Files (*.pdf)")
        if not filepath:
            return
            
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filepath)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        
        painter = QPainter(printer)
        rect = printer.pageRect(QPrinter.Unit.DevicePixel)
        xscale = rect.width() / self.a4_paper.width()
        yscale = rect.height() / self.a4_paper.height()
        scale = min(xscale, yscale)
        painter.scale(scale, scale)
        self.a4_paper.render(painter)
        painter.end()
        
        QMessageBox.information(self, "Thành công", f"Đã xuất CV ra file PDF tại:\n{filepath}")

    def _upload_avatar(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh đại diện", "", "Image Files (*.png *.jpg *.jpeg)")
        if filepath:
            self.avatar_path = filepath
            self.lbl_avatar_preview.setText(filepath.split("/")[-1])
            
            with open(filepath, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                self.avatar_base64 = encoded_string
                
            self._update_preview()

    def _upload_cert_image(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh chứng chỉ", "", "Image Files (*.png *.jpg *.jpeg)")
        if filepath:
            self.temp_cert_image_path = filepath
            self.btn_cert_img.setText("Đã chọn")
            
            with open(filepath, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                self.temp_cert_base64 = encoded_string

    def _add_certificate(self):
        name = self.edit_cert_name.text().strip()
        year = self.edit_cert_year.text().strip()
        if not name or not year:
            return
            
        cert_img_path = getattr(self, 'temp_cert_image_path', None)
        cert_img_b64 = getattr(self, 'temp_cert_base64', "")
        
        self.certificates.append({
            "name": name,
            "year": year,
            "image_path": cert_img_path,
            "image_base64": cert_img_b64
        })
        
        self.edit_cert_name.clear()
        self.edit_cert_year.clear()
        self.btn_cert_img.setText("Tải ảnh")
        self.temp_cert_image_path = None
        self.temp_cert_base64 = ""
        
        self._refresh_certs_list()
        self._update_preview()

    def _refresh_certs_list(self):
        while self.certs_list_lay.count():
            item = self.certs_list_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        for idx, cert in enumerate(self.certificates):
            row = QWidget()
            row.setStyleSheet("QWidget { background: #F1F5F9; border-radius: 8px; }")
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(8, 4, 8, 4)
            
            lbl = QLabel(f"{cert['name']} ({cert['year']})")
            lbl.setStyleSheet("font-size: 12px; color: #0F172A; font-weight: bold; border: none; background: transparent;")
            row_lay.addWidget(lbl, 3)
            
            btn_del = QPushButton("🗑️")
            btn_del.setFixedSize(20, 20)
            btn_del.setStyleSheet("QPushButton { color: #EF4444; border: none; background: transparent; font-size: 12px; }")
            btn_del.clicked.connect(lambda checked, i=idx: self._delete_certificate(i))
            row_lay.addWidget(btn_del)
            
            self.certs_list_lay.addWidget(row)
            
    def _delete_certificate(self, idx):
        if 0 <= idx < len(self.certificates):
            self.certificates.pop(idx)
            self._refresh_certs_list()
            self._update_preview()

    def _update_preview(self):
        self.cv_name.setText(self.name_input.text().strip() or "Họ và Tên")
        self.cv_contact.setText(self.email_input.text().strip() or "email@example.com")
        self.cv_major.setText(self.major_input.text().strip() or "Chuyên ngành")
        self.cv_uni.setText(self.uni_input.text().strip() or "Tên trường đại học")
        self.cv_skills.setText(self.skills_input.toPlainText().strip() or "Kỹ năng của bạn")
        self.cv_projects.setText(self.projects_input.toPlainText().strip() or "Dự án của bạn")
        self.cv_bio.setText(self.bio_input.toPlainText().strip() or "Giới thiệu bản thân...")

        # Update avatar
        if getattr(self, 'avatar_path', None):
            self.cv_avatar.setPixmap(QPixmap(self.avatar_path))
        else:
            self.cv_avatar.clear()
            self.cv_avatar.setText("No Photo")
            self.cv_avatar.setStyleSheet("border-radius: 40px; background-color: #E2E8F0; border: 1px solid #CBD5E1; color: #64748B; font-size: 10px; font-weight: bold; qproperty-alignment: AlignCenter;")

        # Update certificates list in A4 preview
        while self.cv_certs_lay.count():
            item = self.cv_certs_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        for cert in self.certificates:
            row = QWidget()
            row.setStyleSheet("background: transparent; border: none;")
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(0, 0, 0, 0)
            
            lbl_title = QLabel(f"• {cert['name']} ({cert['year']})")
            lbl_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #334155; border: none; background: transparent;")
            row_lay.addWidget(lbl_title, 4)
            
            if cert.get("image_path"):
                lbl_thumb = QLabel()
                lbl_thumb.setFixedSize(40, 25)
                lbl_thumb.setScaledContents(True)
                lbl_thumb.setPixmap(QPixmap(cert["image_path"]))
                row_lay.addWidget(lbl_thumb, 1, alignment=Qt.AlignmentFlag.AlignRight)
                
            self.cv_certs_lay.addWidget(row)

        # Auto-save draft to local storage
        local_data.save("cv_draft.name", self.name_input.text())
        local_data.save("cv_draft.email", self.email_input.text())
        local_data.save("cv_draft.major", self.major_input.text())
        local_data.save("cv_draft.uni", self.uni_input.text())
        local_data.save("cv_draft.skills", self.skills_input.toPlainText())
        local_data.save("cv_draft.projects", self.projects_input.toPlainText())
        local_data.save("cv_draft.bio", self.bio_input.toPlainText())

    def _restore_draft(self):
        name = local_data.get("cv_draft.name")
        if name is not None:
            self.name_input.setText(name)
            self.email_input.setText(local_data.get("cv_draft.email", ""))
            self.major_input.setText(local_data.get("cv_draft.major", ""))
            self.uni_input.setText(local_data.get("cv_draft.uni", ""))
            self.skills_input.setText(local_data.get("cv_draft.skills", ""))
            self.projects_input.setText(local_data.get("cv_draft.projects", ""))
            self.bio_input.setText(local_data.get("cv_draft.bio", ""))
            self._update_preview()

    def _on_ai_generate(self):
        pass

    def _sync_to_web(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        major = self.major_input.text().strip()
        uni = self.uni_input.text().strip()
        skills = self.skills_input.toPlainText().strip()
        projects = self.projects_input.toPlainText().strip()
        bio = self.bio_input.toPlainText().strip()
        avatar = getattr(self, 'avatar_base64', "")
        
        certs_list = []
        for c in self.certificates:
            certs_list.append({
                "name": c["name"],
                "year": c["year"],
                "image_base64": c.get("image_base64", "")
            })
            
        payload = {
            "name": name,
            "email": email,
            "major": major,
            "university": uni,
            "gpa": 3.8,
            "skills": skills,
            "languages": "English, Vietnamese",
            "bio": bio,
            "avatar": avatar,
            "certificates": json.dumps(certs_list)
        }
        
        self.btn_sync.setText("Syncing...")
        self.btn_sync.setEnabled(False)
        QCoreApplication.processEvents()
        
        try:
            r = requests.post("http://127.0.0.1:8000/cvs", json=payload, timeout=5)
            r.raise_for_status()
            res = r.json()
            if res.get("success"):
                QMessageBox.information(self, "Đồng bộ thành công", "CV của bạn đã được đồng bộ trực tiếp lên Web Recruiter Portal!")
            else:
                QMessageBox.warning(self, "Thất bại", f"Đồng bộ không thành công: {res.get('message')}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Web Recruiter Portal:\n{str(e)}\n\nVui lòng kiểm tra xem server web portal (port 8000) đã khởi động chưa.")
        finally:
            self.btn_sync.setText("Sync to Web Recruiter Portal")
            self.btn_sync.setEnabled(True)
