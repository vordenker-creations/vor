import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QWidget, QProgressBar, QCheckBox, QScrollArea, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QGuiApplication
from database import portfolio_db

class ProjectDetailDialog(QDialog):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.project_data = project_data
        self.action_requested = None  # None, 'edit', or 'delete'

        self.setWindowTitle(f"Project Details: {project_data.get('title')}")
        self.resize(500, 560)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                color: #0F172A;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 900;
                color: #0F172A;
                letter-spacing: -0.5px;
            }
            QLabel#tech {
                color: #2563EB;
                font-size: 13px;
                font-weight: 700;
            }
            QLabel#labelHeader {
                color: #64748B;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1px;
            }
            QLabel#desc {
                color: #0F172A;
                font-size: 13px;
                line-height: 1.4;
            }
            QFrame#card {
                background-color: #F8FAFC;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
            QCheckBox {
                color: #0F172A;
                font-size: 12px;
            }
            QPushButton {
                background-color: #F1F5F9;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 10px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
            QPushButton#btnGitHub {
                background-color: #2563EB;
                color: white;
                border: none;
            }
            QPushButton#btnGitHub:hover {
                background-color: #1D4ED8;
            }
            QPushButton#btnDelete {
                background-color: transparent;
                color: #EF4444;
                border: 1px solid rgba(239, 68, 68, 0.4);
            }
            QPushButton#btnDelete:hover {
                background-color: rgba(239, 68, 68, 0.1);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Title
        layout.addWidget(QLabel(project_data.get("title"), objectName="title"))

        # Tech stack
        layout.addWidget(QLabel(f"🛠 {project_data.get('technologies')}", objectName="tech"))

        # Scrollable area to handle overflow nicely
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        content_lay = QVBoxLayout(scroll_content)
        content_lay.setContentsMargins(0, 0, 0, 0)
        content_lay.setSpacing(14)

        # Description Frame
        desc_frame = QFrame(objectName="card")
        desc_lay = QVBoxLayout(desc_frame)
        desc_lay.setContentsMargins(12, 12, 12, 12)
        desc_lay.setSpacing(4)
        
        desc_lay.addWidget(QLabel("DESCRIPTION", objectName="labelHeader"))
        desc_lbl = QLabel(project_data.get("description"))
        desc_lbl.setWordWrap(True)
        desc_lbl.setObjectName("desc")
        desc_lay.addWidget(desc_lbl)
        content_lay.addWidget(desc_frame)

        # Linked Skills Frame
        skills_str = project_data.get("skills", "")
        if skills_str:
            skills_frame = QFrame(objectName="card")
            skills_lay = QVBoxLayout(skills_frame)
            skills_lay.setContentsMargins(12, 12, 12, 12)
            skills_lay.setSpacing(4)
            
            skills_lay.addWidget(QLabel("ASSOCIATED SKILLS", objectName="labelHeader"))
            skills_lbl = QLabel(skills_str)
            skills_lbl.setStyleSheet("color: #0F172A; font-size: 12px; font-weight: 600;")
            skills_lbl.setWordWrap(True)
            skills_lay.addWidget(skills_lbl)
            content_lay.addWidget(skills_frame)

        # Milestones / Task checklist
        self.tasks = portfolio_db.get_project_tasks(project_data["id"])
        if self.tasks:
            tasks_frame = QFrame(objectName="card")
            tasks_lay = QVBoxLayout(tasks_frame)
            tasks_lay.setContentsMargins(12, 12, 12, 12)
            tasks_lay.setSpacing(8)
            
            tasks_lay.addWidget(QLabel("MILESTONES / SUB-TASKS", objectName="labelHeader"))
            
            for t in self.tasks:
                chk = QCheckBox(t["task_name"])
                chk.setChecked(bool(t["completed"]))
                chk.setCursor(Qt.CursorShape.PointingHandCursor)
                chk.setStyleSheet("color: #0F172A; font-size: 12px;")
                
                # Connect check box toggle event using default arg
                chk.stateChanged.connect(lambda state, tid=t["id"], c=chk: self._on_task_toggled(tid, c))
                tasks_lay.addWidget(chk)
                
            content_lay.addWidget(tasks_frame)

        # Progress Frame
        prog_frame = QFrame(objectName="card")
        prog_lay = QVBoxLayout(prog_frame)
        prog_lay.setContentsMargins(12, 12, 12, 12)
        prog_lay.setSpacing(8)
        
        prog_title_lay = QHBoxLayout()
        prog_title_lay.addWidget(QLabel("PROGRESS", objectName="labelHeader"))
        prog_title_lay.addStretch()
        
        prog_val = int(project_data.get("progress", 0))
        self.prog_lbl = QLabel(f"{prog_val}%")
        self.prog_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #2563EB;")
        prog_title_lay.addWidget(self.prog_lbl)
        prog_lay.addLayout(prog_title_lay)

        self.bar = QProgressBar()
        self.bar.setFixedHeight(8)
        self.bar.setRange(0, 100)
        self.bar.setValue(prog_val)
        self.bar.setTextVisible(False)
        color = "#10B981" if prog_val == 100 else "#2563EB"
        self.bar.setStyleSheet(f"QProgressBar {{ background: #E2E8F0; border-radius: 4px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}")
        prog_lay.addWidget(self.bar)
        content_lay.addWidget(prog_frame)

        # Requirements Checklist
        self.reqs_frame = QFrame(objectName="card")
        self.reqs_lay = QVBoxLayout(self.reqs_frame)
        self.reqs_lay.setContentsMargins(12, 12, 12, 12)
        self.reqs_lay.setSpacing(8)
        
        self.reqs_lay.addWidget(QLabel("📋 YÊU CẦU ĐỀ BÀI (REQUIREMENTS)", objectName="labelHeader"))
        
        self.reqs_list_widget = QWidget()
        self.reqs_list_lay = QVBoxLayout(self.reqs_list_widget)
        self.reqs_list_lay.setContentsMargins(0, 0, 0, 0)
        self.reqs_list_lay.setSpacing(6)
        self.reqs_lay.addWidget(self.reqs_list_widget)
        
        # Inline Add Form
        add_req_lay = QHBoxLayout()
        self.edit_new_req = QLineEdit()
        self.edit_new_req.setPlaceholderText("Thêm yêu cầu mới (ví dụ: Đăng nhập JWT)...")
        self.edit_new_req.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 6px;
                color: #0F172A; padding: 4px 8px; font-size: 11px;
            }
        """)
        btn_add_req = QPushButton("+ Thêm")
        btn_add_req.setFixedSize(60, 24)
        btn_add_req.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_req.setStyleSheet("""
            QPushButton {
                background: #2563EB; color: white; font-size: 11px; font-weight: bold;
                border-radius: 6px; padding: 2px; border: none;
            }
            QPushButton:hover { background: #1D4ED8; }
        """)
        btn_add_req.clicked.connect(self._add_requirement)
        add_req_lay.addWidget(self.edit_new_req, 3)
        add_req_lay.addWidget(btn_add_req, 1)
        self.reqs_lay.addLayout(add_req_lay)
        
        content_lay.addWidget(self.reqs_frame)
        self._refresh_requirements_list()

        content_lay.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        # GitHub URL Open Link
        self.btn_github = QPushButton("🌐 Open Link", objectName="btnGitHub")
        self.btn_github.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_github.clicked.connect(self._open_url)
        if not project_data.get("github_url"):
            self.btn_github.setEnabled(False)
        btn_layout.addWidget(self.btn_github)

        self.btn_export = QPushButton("📋 Copy MD")
        self.btn_export.setToolTip("Copy project details in Markdown portfolio format")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.clicked.connect(self._export_markdown)
        btn_layout.addWidget(self.btn_export)

        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.clicked.connect(self._request_edit)
        btn_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("🗑️ Delete", objectName="btnDelete")
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete.clicked.connect(self._request_delete)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)

        # Close button
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        from core.config import apply_theme
        apply_theme(self)

    def _on_task_toggled(self, task_id, chk):
        val = 1 if chk.isChecked() else 0
        portfolio_db.update_project_task(task_id, val)
        
        # Load tasks again to keep self.tasks updated
        self.tasks = portfolio_db.get_project_tasks(self.project_data["id"])
        
        # Fetch updated project details (progress is updated by trigger inside portfolio_db)
        projects = portfolio_db.get_all_projects()
        fresh_proj = next((p for p in projects if p["id"] == self.project_data["id"]), None)
        if fresh_proj:
            self.project_data = fresh_proj
            new_prog = int(fresh_proj["progress"])
            
            # Update progress UI elements
            self.prog_lbl.setText(f"{new_prog}%")
            self.bar.setValue(new_prog)
            
            color = "#10B981" if new_prog == 100 else "#2563EB"
            self.bar.setStyleSheet(f"QProgressBar {{ background: #E2E8F0; border-radius: 4px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}")

    def _open_url(self):
        url = self.project_data.get("github_url", "").strip()
        if url:
            try:
                webbrowser.open(url)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open link: {e}")

    def _export_markdown(self):
        text = f"### 💼 {self.project_data['title']}\n\n"
        text += f"- **Technologies**: {self.project_data['technologies']}\n"
        text += f"- **Progress**: {self.project_data['progress']}%\n"
        text += f"- **Skills Associated**: {self.project_data.get('skills', 'None')}\n"
        text += f"- **GitHub/Demo Link**: {self.project_data.get('github_url', 'N/A')}\n\n"
        text += f"**Description**:\n{self.project_data['description']}\n"
        
        if self.tasks:
            text += "\n**Milestones**:\n"
            for t in self.tasks:
                status = "[x]" if t["completed"] else "[ ]"
                text += f"- {status} {t['task_name']}\n"
                
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Export Portfolio", "Project details copied to clipboard as Markdown!")

    def _request_edit(self):
        self.action_requested = "edit"
        self.accept()

    def _request_delete(self):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete project '{self.project_data.get('title')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            portfolio_db.delete_project(self.project_data["id"])
            QMessageBox.information(self, "Success", "Project deleted successfully.")
            self.action_requested = "delete"
            self.accept()

    def _refresh_requirements_list(self):
        while self.reqs_list_lay.count():
            item = self.reqs_list_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        reqs = portfolio_db.get_project_requirements(self.project_data["id"])
        
        for r in reqs:
            row_widget = QWidget()
            row_lay = QHBoxLayout(row_widget)
            row_lay.setContentsMargins(0, 0, 0, 0)
            row_lay.setSpacing(6)
            
            chk = QCheckBox(r["requirement_text"])
            chk.setChecked(bool(r["completed"]))
            chk.setCursor(Qt.CursorShape.PointingHandCursor)
            chk.setStyleSheet("color: #0F172A; font-size: 12px;")
            chk.stateChanged.connect(lambda state, rid=r["id"], c=chk: self._on_requirement_toggled(rid, c))
            row_lay.addWidget(chk, 4)
            
            btn_sug = QPushButton("💡 Gợi ý")
            btn_sug.setFixedSize(65, 20)
            btn_sug.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sug.setStyleSheet("""
                QPushButton {
                    background: #F1F5F9; color: #2563EB; border: 1px solid rgba(37, 99, 235, 0.4);
                    border-radius: 4px; font-size: 10px; font-weight: bold; padding: 1px;
                }
                QPushButton:hover { background: #E2E8F0; }
            """)
            btn_sug.clicked.connect(lambda checked, rid=r["id"], rtxt=r["requirement_text"], sug=r["detailed_suggestion"]: self._show_suggestion(rid, rtxt, sug))
            row_lay.addWidget(btn_sug, 1)

            btn_del = QPushButton("🗑️")
            btn_del.setFixedSize(20, 20)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet("QPushButton { color: #EF4444; border: none; background: transparent; font-size: 11px; }")
            btn_del.clicked.connect(lambda checked, rid=r["id"]: self._delete_requirement(rid))
            row_lay.addWidget(btn_del)
            
            self.reqs_list_lay.addWidget(row_widget)

    def _add_requirement(self):
        txt = self.edit_new_req.text().strip()
        if not txt:
            return
        portfolio_db.add_project_requirement(self.project_data["id"], txt)
        self.edit_new_req.clear()
        self._refresh_requirements_list()

    def _delete_requirement(self, req_id):
        portfolio_db.delete_project_requirement(req_id)
        self._refresh_requirements_list()

    def _on_requirement_toggled(self, req_id, chk):
        val = 1 if chk.isChecked() else 0
        portfolio_db.update_project_requirement_status(req_id, val)

    def _show_suggestion(self, req_id, requirement_text, current_suggestion):
        if current_suggestion:
            self._display_suggestion_dialog(requirement_text, current_suggestion)
        else:
            # Query AI or generate fallback
            prompt = f"Hãy viết hướng dẫn gợi ý lập trình ngắn gọn (dưới 5 câu) bằng tiếng Việt cho yêu cầu dự án sau: '{requirement_text}' trong dự án sử dụng các công nghệ: '{self.project_data.get('technologies', '')}'."
            
            import json, urllib.request
            ai_text = None
            try:
                url = "http://localhost:11434/api/generate"
                payload = json.dumps({
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }).encode("utf-8")
                
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=3.0) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    ai_text = res_data.get("response", "")
            except Exception:
                pass
                
            if not ai_text:
                ai_text = self._generate_suggestion_fallback(requirement_text, self.project_data.get('technologies'))
                
            portfolio_db.update_project_requirement_suggestion(req_id, ai_text)
            self._display_suggestion_dialog(requirement_text, ai_text)
            self._refresh_requirements_list()

    def _display_suggestion_dialog(self, title, text):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"💡 Hướng Dẫn: {title}")
        dlg.resize(400, 300)
        dlg.setStyleSheet("""
            QDialog { background-color: #FFFFFF; color: #0F172A; }
            QLabel { font-size: 13px; line-height: 1.4; color: #0F172A; }
            QPushButton { background-color: #2563EB; color: white; font-weight: bold; border-radius: 8px; height: 32px; font-size: 12px; }
            QPushButton:hover { background-color: #1D4ED8; }
        """)
        lay = QVBoxLayout(dlg)
        
        from PyQt6.QtWidgets import QTextBrowser
        browser = QTextBrowser()
        # Simple Markdown parsing to HTML for headings and bullet points
        html = text.replace("\n", "<br>")
        if "###" in html:
            html = html.replace("### ", "<h3>").replace("<br>", "</h3>", 1)
        browser.setHtml(html)
        browser.setStyleSheet("QTextBrowser { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 10px; }")
        lay.addWidget(browser)
        
        btn = QPushButton("Đóng")
        btn.clicked.connect(dlg.accept)
        lay.addWidget(btn)
        dlg.exec()

    def _generate_suggestion_fallback(self, requirement_text, technologies):
        req_lower = requirement_text.lower()
        tips = []
        if "jwt" in req_lower or "auth" in req_lower or "login" in req_lower or "đăng nhập" in req_lower:
            tips.append("- Sử dụng thư viện bảo mật (như PyJWT) để mã hóa JSON Web Token.")
            tips.append("- Lưu trữ token trong cookie HttpOnly hoặc LocalStorage của trình duyệt.")
            tips.append("- Định cấu hình thời gian hết hạn ngắn cho token (15-30 phút) để tránh rủi ro bảo mật.")
        elif "database" in req_lower or "cơ sở dữ liệu" in req_lower or "db" in req_lower or "sqlite" in req_lower or "postgresql" in req_lower:
            tips.append("- Sử dụng ORM (như SQLAlchemy) hoặc truy vấn tham số hóa (parameterized query) để ngăn chặn lỗi SQL Injection.")
            tips.append("- Thiết kế các bảng có khóa chính, khóa ngoại rõ ràng để bảo toàn ràng buộc dữ liệu.")
            tips.append("- Tạo chỉ mục (INDEX) cho các cột thường xuyên truy vấn như email, project_id để cải thiện tốc độ.")
        elif "api" in req_lower or "rest" in req_lower or "endpoint" in req_lower:
            tips.append("- Thiết kế URL chuẩn RESTful: dùng danh từ số nhiều (ví dụ: /api/v1/jobs) và các phương thức GET, POST, PUT, DELETE phù hợp.")
            tips.append("- Trả về dữ liệu chuẩn JSON thống nhất: `{\"success\": true, \"data\": ...}`.")
            tips.append("- Sử dụng mã trạng thái HTTP phù hợp (200 OK, 201 Created, 400 Bad Request, 404 Not Found).")
        elif "ui" in req_lower or "css" in req_lower or "giao diện" in req_lower or "style" in req_lower or "đẹp" in req_lower:
            tips.append("- Sử dụng CSS variables (biến màu) để dễ quản lý bảng màu đồng bộ.")
            tips.append("- Thiết kế giao diện tương thích responsive với nhiều kích thước màn hình bằng Media Queries.")
            tips.append("- Thêm các hiệu ứng hover, transition mượt mà để tăng trải nghiệm người dùng.")
        else:
            tips.append("- Chia nhỏ yêu cầu này thành các hàm nhỏ hơn để dễ kiểm thử.")
            tips.append("- Viết các trường hợp kiểm thử (test cases) cho cả đầu vào hợp lệ và không hợp lệ.")
            tips.append(f"- Sử dụng các mẫu thiết kế (design patterns) phổ biến phù hợp với công nghệ {technologies or 'dự án'}.")
            
        return "### 💡 Gợi ý thực hiện:\n\n" + "\n".join(tips)
