from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QTextEdit, QMessageBox, QScrollArea, QWidget, QCheckBox
)
from PyQt6.QtCore import Qt
from database import portfolio_db
from database import skill_tree_db

class ProjectDialog(QDialog):
    def __init__(self, project_data=None, parent=None):
        super().__init__(parent)
        self.project_data = project_data
        self.is_edit = project_data is not None

        if self.is_edit:
            self.setWindowTitle(f"Edit Project: {project_data.get('title')}")
        else:
            self.setWindowTitle("Add New Project Portfolio")

        self.resize(480, 680)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                color: #0F172A;
            }
            QLabel {
                color: #475569;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit, QTextEdit, QSpinBox {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 8px 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
                border: 1px solid #2563EB;
            }
            QCheckBox {
                color: #475569;
                font-size: 12px;
            }
            QScrollArea {
                border: 1px solid #E2E8F0;
                background-color: #F8FAFC;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #F1F5F9;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
            QPushButton#btnPrimary {
                background-color: #2563EB;
                color: white;
                border: none;
            }
            QPushButton#btnPrimary:hover {
                background-color: #1D4ED8;
            }
        """)

        # Main Layout in a Scroll Area because dialog has many fields now
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        main_scroll.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 1. Project Title
        self.layout.addWidget(QLabel("Project Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g. AI Interview Simulator")
        if self.is_edit:
            self.title_input.setText(project_data.get("title", ""))
        self.layout.addWidget(self.title_input)

        # 2. Technologies
        self.layout.addWidget(QLabel("Technologies Used (comma separated):"))
        self.tech_input = QLineEdit()
        self.tech_input.setPlaceholderText("e.g. Python, PyQt6, SQLite")
        if self.is_edit:
            self.tech_input.setText(project_data.get("technologies", ""))
        self.layout.addWidget(self.tech_input)

        # 3. Short Description
        self.layout.addWidget(QLabel("Project Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Describe your project's main functionality...")
        self.desc_input.setFixedHeight(70)
        if self.is_edit:
            self.desc_input.setText(project_data.get("description", ""))
        self.layout.addWidget(self.desc_input)

        # 4. GitHub / Demo Link
        self.layout.addWidget(QLabel("GitHub or Demo URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g. https://github.com/username/project")
        if self.is_edit:
            self.url_input.setText(project_data.get("github_url", ""))
        self.layout.addWidget(self.url_input)

        # 5. Milestones / Tasks Planner
        self.layout.addWidget(QLabel("Project Milestones / Sub-Tasks:"))
        
        task_add_lay = QHBoxLayout()
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter milestone name (e.g. Design DB Schema)")
        self.btn_add_task = QPushButton("+ Add Milestone")
        self.btn_add_task.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_task.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        self.btn_add_task.clicked.connect(self._add_task_item)
        task_add_lay.addWidget(self.task_name_input, 3)
        task_add_lay.addWidget(self.btn_add_task, 1)
        self.layout.addLayout(task_add_lay)
        
        tasks_scroll = QScrollArea()
        tasks_scroll.setFixedHeight(120)
        tasks_scroll_content = QWidget()
        tasks_scroll_content.setStyleSheet("background: transparent;")
        self.tasks_layout = QVBoxLayout(tasks_scroll_content)
        self.tasks_layout.setContentsMargins(8, 8, 8, 8)
        self.tasks_layout.setSpacing(6)
        self.tasks_layout.addStretch()
        
        tasks_scroll.setWidget(tasks_scroll_content)
        tasks_scroll.setWidgetResizable(True)
        self.layout.addWidget(tasks_scroll)

        # 6. Completion Progress
        prog_header_lay = QHBoxLayout()
        prog_header_lay.addWidget(QLabel("Completion Progress (0 - 100%):"))
        self.progress_label_info = QLabel("Manual input")
        self.progress_label_info.setStyleSheet("color: #64748B; font-size: 11px;")
        prog_header_lay.addStretch()
        prog_header_lay.addWidget(self.progress_label_info)
        self.layout.addLayout(prog_header_lay)
        
        self.progress_spin = QSpinBox()
        self.progress_spin.setRange(0, 100)
        if self.is_edit:
            self.progress_spin.setValue(int(project_data.get("progress", 0)))
        else:
            self.progress_spin.setValue(0)
        self.layout.addWidget(self.progress_spin)

        # Load existing tasks if editing
        self.tasks = []
        if self.is_edit:
            existing_tasks = portfolio_db.get_project_tasks(project_data["id"])
            self.tasks = [{"task_name": t["task_name"], "completed": t["completed"]} for t in existing_tasks]
            self._refresh_tasks_list()

        # 7. Linked Skills (Checkbox List)
        self.layout.addWidget(QLabel("Associate with Skills (from Tree):"))
        
        skills_scroll = QScrollArea()
        skills_scroll.setFixedHeight(100)
        skills_scroll_content = QWidget()
        skills_scroll_content.setStyleSheet("background: transparent;")
        skills_lay = QVBoxLayout(skills_scroll_content)
        skills_lay.setContentsMargins(10, 10, 10, 10)
        skills_lay.setSpacing(6)
        
        branches = skill_tree_db.load_skill_branches_structured()
        self.checkboxes = []
        
        linked_skills = []
        if self.is_edit and project_data.get("skills"):
            linked_skills = [s.strip() for s in project_data.get("skills", "").split(",") if s.strip()]

        for branch_name, branch in branches.items():
            for node in branch["nodes"]:
                skill_name = node["name"]
                chk = QCheckBox(f"{skill_name} ({branch_name})")
                chk.setProperty("skill_name", skill_name)
                chk.setCursor(Qt.CursorShape.PointingHandCursor)
                if skill_name in linked_skills:
                    chk.setChecked(True)
                skills_lay.addWidget(chk)
                self.checkboxes.append(chk)
                
        skills_scroll.setWidget(skills_scroll_content)
        self.layout.addWidget(skills_scroll)

        # Connect scroll content
        main_scroll.setWidget(scroll_content)
        outer_layout.addWidget(main_scroll)

        # 8. Fixed Footer Action buttons (outside scroll area)
        footer_widget = QWidget()
        footer_widget.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #E2E8F0;")
        btn_box = QHBoxLayout(footer_widget)
        btn_box.setContentsMargins(20, 12, 20, 16)
        btn_box.setSpacing(12)
        
        self.btn_submit = QPushButton("Save Project" if self.is_edit else "Add Project")
        self.btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_submit.setObjectName("btnPrimary")
        self.btn_submit.clicked.connect(self._submit)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        
        outer_layout.addWidget(footer_widget)
        
        from core.config import apply_theme
        apply_theme(self)

    def _add_task_item(self):
        name = self.task_name_input.text().strip()
        if not name:
            return
        if any(t["task_name"].lower() == name.lower() for t in self.tasks):
            QMessageBox.warning(self, "Duplicate Milestone", "A milestone task with this name already exists.")
            return
        self.tasks.append({"task_name": name, "completed": 0})
        self.task_name_input.clear()
        self._refresh_tasks_list()

    def _remove_task_item(self, idx):
        self.tasks.pop(idx)
        self._refresh_tasks_list()

    def _on_dialog_task_toggled(self, idx, checked):
        if 0 <= idx < len(self.tasks):
            self.tasks[idx]["completed"] = 1 if checked else 0
            # Update the progress spinner value preview
            completed = sum(1 for t in self.tasks if t["completed"])
            calc_val = int(completed / len(self.tasks) * 100) if self.tasks else 0
            self.progress_spin.setValue(calc_val)

    def _refresh_tasks_list(self):
        # Clear tasks layout
        for i in reversed(range(self.tasks_layout.count())):
            item = self.tasks_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            else:
                self.tasks_layout.removeItem(item)
                
        # Repopulate
        for idx, task in enumerate(self.tasks):
            item_widget = QWidget()
            item_widget.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 6px;
                }
            """)
            item_lay = QHBoxLayout(item_widget)
            item_lay.setContentsMargins(10, 4, 10, 4)
            
            # Interactive Checkbox
            chk = QCheckBox(task["task_name"])
            chk.setChecked(bool(task["completed"]))
            chk.setCursor(Qt.CursorShape.PointingHandCursor)
            chk.setStyleSheet("color: #0F172A; font-size: 12px; border: none; background: transparent;")
            # Connect toggle using stateChanged and capturing index
            chk.stateChanged.connect(lambda state, i=idx, c=chk: self._on_dialog_task_toggled(i, c.isChecked()))
            item_lay.addWidget(chk)
            item_lay.addStretch()
            
            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(24, 24)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setStyleSheet("color: #EF4444; border: none; background: transparent; font-size: 12px;")
            del_btn.clicked.connect(lambda checked, i=idx: self._remove_task_item(i))
            item_lay.addWidget(del_btn)
            
            self.tasks_layout.addWidget(item_widget)
            
        self.tasks_layout.addStretch()
            
        # Update progress spinner and info labels
        if self.tasks:
            self.progress_spin.setEnabled(False)
            completed = sum(1 for t in self.tasks if t["completed"])
            calc_val = int(completed / len(self.tasks) * 100) if self.tasks else 0
            self.progress_spin.setValue(calc_val)
            self.progress_label_info.setText("Progress auto-calculated from milestones")
            self.progress_label_info.setStyleSheet("color: #10B981; font-size: 11px; font-weight: bold;")
        else:
            self.progress_spin.setEnabled(True)
            self.progress_label_info.setText("Manual input (no milestones defined)")
            self.progress_label_info.setStyleSheet("color: #64748B; font-size: 11px; font-weight: normal;")

    def _submit(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation Error", "Project Title cannot be empty.")
            return

        technologies = self.tech_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        github_url = self.url_input.text().strip()

        if self.tasks:
            completed = sum(1 for t in self.tasks if t["completed"])
            progress = int(completed / len(self.tasks) * 100)
        else:
            progress = self.progress_spin.value()

        # Collect checked skills
        selected_skills = []
        for chk in self.checkboxes:
            if chk.isChecked():
                selected_skills.append(chk.property("skill_name"))
        skills_str = ", ".join(selected_skills)

        if self.is_edit:
            project_id = self.project_data["id"]
            portfolio_db.update_project(project_id, title, technologies, description, github_url, progress, skills_str)
            portfolio_db.set_project_tasks(project_id, self.tasks)
            QMessageBox.information(self, "Success", f"Project '{title}' updated successfully.")
        else:
            project_id = portfolio_db.add_project(title, technologies, description, github_url, progress, skills_str)
            portfolio_db.set_project_tasks(project_id, self.tasks)
            QMessageBox.information(self, "Success", f"Project '{title}' added successfully.")

        self.accept()
