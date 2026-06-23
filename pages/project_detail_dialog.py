import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QWidget, QProgressBar, QCheckBox, QScrollArea
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
                background-color: #0F172A;
                color: #F1F5F9;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 900;
                color: #F1F5F9;
                letter-spacing: -0.5px;
            }
            QLabel#tech {
                color: #38BDF8;
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
                color: #E2E8F0;
                font-size: 13px;
                line-height: 1.4;
            }
            QFrame#card {
                background-color: #1E293B;
                border-radius: 12px;
                border: 1px solid #334155;
            }
            QCheckBox {
                color: #E2E8F0;
                font-size: 12px;
            }
            QPushButton {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton#btnGitHub {
                background-color: #38BDF8;
                color: #0F172A;
                border: none;
            }
            QPushButton#btnGitHub:hover {
                background-color: #0EA5E9;
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
            skills_lbl.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 600;")
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
                chk.setStyleSheet("color: #E2E8F0; font-size: 12px;")
                
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
        self.prog_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #38BDF8;")
        prog_title_lay.addWidget(self.prog_lbl)
        prog_lay.addLayout(prog_title_lay)

        self.bar = QProgressBar()
        self.bar.setFixedHeight(8)
        self.bar.setRange(0, 100)
        self.bar.setValue(prog_val)
        self.bar.setTextVisible(False)
        color = "#10B981" if prog_val == 100 else "#38BDF8"
        self.bar.setStyleSheet(f"QProgressBar {{ background: #0F172A; border-radius: 4px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}")
        prog_lay.addWidget(self.bar)
        content_lay.addWidget(prog_frame)

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
            
            color = "#10B981" if new_prog == 100 else "#38BDF8"
            self.bar.setStyleSheet(f"QProgressBar {{ background: #0F172A; border-radius: 4px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}")

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
