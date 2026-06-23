from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout,
    QProgressBar, QLineEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QGuiApplication
from database import portfolio_db

class ModernCard(QFrame):
    def __init__(self, project_data, on_click=None, parent=None):
        super().__init__(parent)
        self.project_data = project_data
        self.on_click = on_click
        self.setObjectName("ModernCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            #ModernCard {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 16px;
            }
            #ModernCard:hover {
                border: 1px solid #38BDF8;
                background-color: #243249;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)
        self.internal_layout.setSpacing(12)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.project_data)
        super().mousePressEvent(event)

class StatsBox(QFrame):
    def __init__(self, title, icon, value, color_accent, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        self.setFixedHeight(75)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(15, 10, 15, 10)
        lay.setSpacing(12)
        
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 24px; color: {color_accent}; background: transparent; border: none;")
        lay.addWidget(icon_lbl)
        
        text_lay = QVBoxLayout()
        text_lay.setSpacing(2)
        text_lay.setContentsMargins(0, 0, 0, 0)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 800; background: transparent; border: none; letter-spacing: 0.5px;")
        
        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet("color: #F1F5F9; font-size: 18px; font-weight: 800; background: transparent; border: none;")
        
        text_lay.addWidget(title_lbl)
        text_lay.addWidget(self.val_lbl)
        
        lay.addLayout(text_lay)
        lay.addStretch()
        
    def set_value(self, val):
        self.val_lbl.setText(str(val))

class ProjectPortfolioPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #0F172A;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: transparent; border-bottom: 1px solid rgba(148, 163, 184, 0.1);")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(16)
        
        title_lbl = QLabel("💼 Project Portfolio")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: 900; color: #F1F5F9; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)
        
        sub_lbl = QLabel("Display and track your engineering work")
        sub_lbl.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 600; border: none; background: transparent;")
        header_layout.addWidget(sub_lbl)
        
        header_layout.addStretch()
        
        self.btn_add = QPushButton("+ Add Project")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: #0F172A; font-weight: 800; font-size: 13px;
                border-radius: 18px; padding: 0 20px; height: 36px; border: none;
            }
            QPushButton:hover { background: #0EA5E9; }
        """)
        self.btn_add.clicked.connect(self._on_add_project)
        header_layout.addWidget(self.btn_add)
        
        main_layout.addWidget(header)
        
        # Content Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(20)
        
        # 1. Dashboard Stats Panel
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(16)
        
        self.stat_total = StatsBox("TOTAL PROJECTS", "💼", "0", "#38BDF8")
        self.stat_completed = StatsBox("COMPLETED", "✅", "0", "#10B981")
        self.stat_in_progress = StatsBox("IN PROGRESS", "⚡", "0", "#F59E0B")
        self.stat_avg_progress = StatsBox("AVG PROGRESS", "📈", "0%", "#A78BFA")
        
        self.stats_layout.addWidget(self.stat_total)
        self.stats_layout.addWidget(self.stat_completed)
        self.stats_layout.addWidget(self.stat_in_progress)
        self.stats_layout.addWidget(self.stat_avg_progress)
        self.content_layout.addLayout(self.stats_layout)
        
        # 2. Search & Filters Panel
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setSpacing(12)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search projects by title, tech stack, description, or skills...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
            }
        """)
        self.search_input.textChanged.connect(self._apply_filters)
        self.filter_layout.addWidget(self.search_input, 4)
        
        self.filter_status = QComboBox()
        self.filter_status.addItems(["All Statuses", "Completed (100%)", "In Progress (1-99%)", "Planned (0%)"])
        self.filter_status.setStyleSheet("""
            QComboBox {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #38BDF8;
            }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: #F1F5F9;
                selection-background-color: #38BDF8;
                selection-color: #0F172A;
                border: 1px solid #334155;
            }
        """)
        self.filter_status.currentTextChanged.connect(self._apply_filters)
        self.filter_layout.addWidget(self.filter_status, 2)
        
        self.filter_skill = QComboBox()
        self.filter_skill.addItem("All Skills")
        self.filter_skill.setStyleSheet("""
            QComboBox {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #38BDF8;
            }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: #F1F5F9;
                selection-background-color: #38BDF8;
                selection-color: #0F172A;
                border: 1px solid #334155;
            }
        """)
        self.filter_skill.currentTextChanged.connect(self._apply_filters)
        self.filter_layout.addWidget(self.filter_skill, 2)
        
        self.content_layout.addLayout(self.filter_layout)
        
        # 3. Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.content_layout.addLayout(self.grid)
        self.content_layout.addStretch()
        
        scroll.setWidget(self.content_widget)
        main_layout.addWidget(scroll)

        # Initial data holders
        self.projects = []

        # Initial load
        self.refresh()

    def refresh(self):
        # Fetch projects from SQLite DB
        self.projects = portfolio_db.get_all_projects()
        
        # Update statistics dashboard
        self._update_stats()
        
        # Populate skill filter dropdown
        current_skill_filter = self.filter_skill.currentText()
        self.filter_skill.blockSignals(True)
        self.filter_skill.clear()
        self.filter_skill.addItem("All Skills")
        
        unique_skills = set()
        for p in self.projects:
            if p.get("skills"):
                for s in p["skills"].split(","):
                    val = s.strip()
                    if val:
                        unique_skills.add(val)
        for skill in sorted(unique_skills):
            self.filter_skill.addItem(skill)
            
        # Restore selected skill index if still valid
        idx = self.filter_skill.findText(current_skill_filter)
        if idx >= 0:
            self.filter_skill.setCurrentIndex(idx)
        else:
            self.filter_skill.setCurrentIndex(0)
        self.filter_skill.blockSignals(False)
        
        # Apply filters to render cards
        self._apply_filters()

    def _update_stats(self):
        total = len(self.projects)
        completed = sum(1 for p in self.projects if int(p["progress"]) == 100)
        in_progress = sum(1 for p in self.projects if 0 < int(p["progress"]) < 100)
        
        if total > 0:
            avg = sum(int(p["progress"]) for p in self.projects) // total
        else:
            avg = 0
            
        self.stat_total.set_value(total)
        self.stat_completed.set_value(completed)
        self.stat_in_progress.set_value(in_progress)
        self.stat_avg_progress.set_value(f"{avg}%")

    def _apply_filters(self):
        # Clear existing items in grid
        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                
        search_text = self.search_input.text().lower().strip()
        status_filter = self.filter_status.currentText()
        skill_filter = self.filter_skill.currentText()
        
        row, col = 0, 0
        for project in self.projects:
            # 1. Search term match
            title = project["title"].lower()
            tech = project["technologies"].lower()
            desc = project["description"].lower()
            skills = project.get("skills", "").lower()
            
            match_search = (not search_text) or (search_text in title) or (search_text in tech) or (search_text in desc) or (search_text in skills)
            
            # 2. Status match
            prog = int(project["progress"])
            if status_filter == "Completed (100%)":
                match_status = (prog == 100)
            elif status_filter == "In Progress (1-99%)":
                match_status = (0 < prog < 100)
            elif status_filter == "Planned (0%)":
                match_status = (prog == 0)
            else:
                match_status = True
                
            # 3. Skill match
            if skill_filter != "All Skills":
                skills_list = [s.strip().lower() for s in project.get("skills", "").split(",") if s.strip()]
                match_skill = (skill_filter.lower() in skills_list)
            else:
                match_skill = True
                
            if match_search and match_status and match_skill:
                card = ModernCard(project, on_click=self._on_card_clicked)
                
                # Card Header
                c_header = QHBoxLayout()
                c_t = QLabel(project["title"])
                c_t.setStyleSheet("color: #F1F5F9; font-size: 16px; font-weight: 800; background: transparent; border: none;")
                c_header.addWidget(c_t)
                c_header.addStretch()
                
                # Copy Markdown button
                copy_btn = QPushButton("📋")
                copy_btn.setFixedSize(24, 24)
                copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                copy_btn.setStyleSheet("color: #64748B; border: none; background: transparent; font-size: 14px;")
                copy_btn.setToolTip("Copy details in Markdown format")
                # Stop mouse click event propagation to card click
                copy_btn.clicked.connect(lambda checked, p=project: self._copy_markdown(p))
                c_header.addWidget(copy_btn)
                
                # Options button
                opts = QPushButton("⋮")
                opts.setFixedSize(24, 24)
                opts.setStyleSheet("color: #64748B; font-weight: 800; border: none; background: transparent; font-size: 16px;")
                opts.setCursor(Qt.CursorShape.PointingHandCursor)
                # Option click also triggers card detail view
                opts.clicked.connect(lambda checked, p=project: self._on_card_clicked(p))
                c_header.addWidget(opts)
                
                card.internal_layout.addLayout(c_header)
                
                # Badge + Tech tags row
                badge_tech_lay = QHBoxLayout()
                badge_tech_lay.setSpacing(6)
                
                # Status Badge
                badge = QLabel()
                if prog == 100:
                    status_text = "Completed"
                    badge_style = "color: #10B981; background-color: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3);"
                elif prog > 0:
                    status_text = "In Progress"
                    badge_style = "color: #38BDF8; background-color: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3);"
                else:
                    status_text = "Planned"
                    badge_style = "color: #94A3B8; background-color: rgba(148, 163, 184, 0.1); border: 1px solid rgba(148, 163, 184, 0.3);"
                badge.setText(status_text)
                badge.setStyleSheet(badge_style + "font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 4px;")
                badge_tech_lay.addWidget(badge)
                
                # Render first 2 technology buttons
                tech_list = [t.strip() for t in project["technologies"].split(",") if t.strip()]
                for tech in tech_list[:2]:
                    btn_tech = QPushButton(tech)
                    btn_tech.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_tech.setStyleSheet("""
                        QPushButton {
                            background: rgba(56, 189, 248, 0.05);
                            color: #38BDF8;
                            border: 1px solid rgba(56, 189, 248, 0.15);
                            border-radius: 4px;
                            font-size: 10px;
                            padding: 2px 6px;
                        }
                        QPushButton:hover {
                            background: rgba(56, 189, 248, 0.15);
                            border: 1px solid #38BDF8;
                        }
                    """)
                    btn_tech.clicked.connect(lambda checked, t=tech: self.search_input.setText(t))
                    badge_tech_lay.addWidget(btn_tech)
                badge_tech_lay.addStretch()
                card.internal_layout.addLayout(badge_tech_lay)
                
                # Description
                c_desc = QLabel(project["description"])
                c_desc.setStyleSheet("color: #94A3B8; font-size: 13px; line-height: 1.4; background: transparent; border: none;")
                c_desc.setWordWrap(True)
                c_desc.setFixedHeight(40)  # clamp height for alignment
                card.internal_layout.addWidget(c_desc)
                
                # Skills tag
                skills_str = project.get("skills", "")
                if skills_str:
                    skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]
                    skills_flow = QHBoxLayout()
                    skills_flow.setSpacing(4)
                    skills_flow.addWidget(QLabel("🔗 Skills:", styleSheet="color: #64748B; font-size: 11px; background: transparent; border: none; font-weight: 700;"))
                    for skill in skills_list[:2]:
                        btn_skill = QPushButton(skill)
                        btn_skill.setCursor(Qt.CursorShape.PointingHandCursor)
                        btn_skill.setStyleSheet("""
                            QPushButton {
                                background: rgba(167, 139, 250, 0.08);
                                color: #A78BFA;
                                border: 1px solid rgba(167, 139, 250, 0.15);
                                border-radius: 4px;
                                font-size: 10px;
                                padding: 1px 4px;
                            }
                            QPushButton:hover {
                                background: rgba(167, 139, 250, 0.2);
                                border: 1px solid #A78BFA;
                            }
                        """)
                        btn_skill.clicked.connect(lambda checked, s=skill: self.search_input.setText(s))
                        skills_flow.addWidget(btn_skill)
                    skills_flow.addStretch()
                    card.internal_layout.addLayout(skills_flow)
                else:
                    card.internal_layout.addSpacing(10)
                    
                card.internal_layout.addStretch()
                
                # Progress bar footer
                c_foot = QHBoxLayout()
                c_foot.addWidget(QLabel("Completion:", styleSheet="color: #64748B; font-size: 11px; background: transparent; border: none;"))
                
                bar = QProgressBar()
                bar.setFixedHeight(6)
                bar.setRange(0, 100)
                bar.setValue(prog)
                bar.setTextVisible(False)
                color = "#10B981" if prog == 100 else "#38BDF8"
                bar.setStyleSheet(f"QProgressBar {{ background: #0F172A; border-radius: 3px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}")
                
                c_foot.addWidget(bar)
                c_foot.addWidget(QLabel(f"{prog}%", styleSheet="color: #F1F5F9; font-size: 11px; font-weight: 700; background: transparent; border: none;"))
                
                card.internal_layout.addLayout(c_foot)
                
                self.grid.addWidget(card, row, col)
                col += 1
                if col > 1:
                    col = 0
                    row += 1

    def _copy_markdown(self, project):
        text = f"### 💼 {project['title']}\n\n"
        text += f"- **Technologies**: {project['technologies']}\n"
        text += f"- **Progress**: {project['progress']}%\n"
        text += f"- **Skills Associated**: {project.get('skills', 'None')}\n"
        text += f"- **GitHub/Demo Link**: {project.get('github_url', 'N/A')}\n\n"
        text += f"**Description**:\n{project['description']}\n"
        
        # Get tasks
        tasks = portfolio_db.get_project_tasks(project["id"])
        if tasks:
            text += "\n**Milestones**:\n"
            for t in tasks:
                status = "[x]" if t["completed"] else "[ ]"
                text += f"- {status} {t['task_name']}\n"
                
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Export Portfolio", "Project details copied to clipboard as Markdown!")

    def _on_card_clicked(self, project_data):
        from pages.project_detail_dialog import ProjectDetailDialog
        dlg = ProjectDetailDialog(project_data, parent=self)
        dlg.exec()
        
        # Refresh screen to update progress and stats
        self.refresh()
        
        # Handle edit or delete request callbacks
        if dlg.action_requested == "edit":
            self._on_edit_project(project_data)
        elif dlg.action_requested == "delete":
            self.refresh()

    def _on_add_project(self):
        from pages.project_dialog import ProjectDialog
        dlg = ProjectDialog(parent=self)
        if dlg.exec():
            self.refresh()

    def _on_edit_project(self, project_data):
        from pages.project_dialog import ProjectDialog
        # Fetch fresh data in case tasks updated progress
        projects = portfolio_db.get_all_projects()
        fresh_data = next((p for p in projects if p["id"] == project_data["id"]), project_data)
        dlg = ProjectDialog(project_data=fresh_data, parent=self)
        if dlg.exec():
            self.refresh()
