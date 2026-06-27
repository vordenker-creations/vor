from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout,
    QProgressBar, QLineEdit, QComboBox, QMessageBox, QStackedWidget, QDialog,
    QCheckBox, QSplitter
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
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            #ModernCard:hover {
                border: 1px solid #2563EB;
                background-color: #F8FAFC;
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
        
        from core.config import apply_theme
        apply_theme(self)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.project_data)
        super().mousePressEvent(event)

class StatsBox(QFrame):
    def __init__(self, title, icon, value, color_accent, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        self.setFixedHeight(75)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        from core.config import apply_theme
        apply_theme(self)
        
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
        self.val_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800; background: transparent; border: none;")
        
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
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.stacked_widget)
        
        # 1. Grid List view
        self.list_view_widget = QWidget()
        self._setup_list_view()
        self.stacked_widget.addWidget(self.list_view_widget)
        
        # 2. Detail view
        self.detail_view_widget = QWidget()
        self._setup_detail_view()
        self.stacked_widget.addWidget(self.detail_view_widget)
        
        self.projects = []
        self.active_project_id = None
        self.active_project_data = None
        
        self.refresh()

    def _setup_list_view(self):
        layout = QVBoxLayout(self.list_view_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: transparent; border-bottom: 1px solid rgba(148, 163, 184, 0.1);")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(16)
        
        title_lbl = QLabel("💼 Project Portfolio")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: 900; color: #0F172A; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)
        
        sub_lbl = QLabel("Display and track your engineering work")
        sub_lbl.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 600; border: none; background: transparent;")
        header_layout.addWidget(sub_lbl)
        
        header_layout.addStretch()
        
        self.btn_add = QPushButton("+ Add Project")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background: #2563EB; color: #F8FAFC; font-weight: 800; font-size: 13px;
                border-radius: 18px; padding: 0 20px; height: 36px; border: none;
            }
            QPushButton:hover { background: #1D4ED8; }
        """)
        self.btn_add.clicked.connect(self._on_add_project)
        header_layout.addWidget(self.btn_add)
        
        layout.addWidget(header)
        
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
        
        self.stat_total = StatsBox("TOTAL PROJECTS", "💼", "0", "#2563EB")
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
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #2563EB;
            }
        """)
        self.search_input.textChanged.connect(self._apply_filters)
        self.filter_layout.addWidget(self.search_input, 4)
        
        self.filter_status = QComboBox()
        self.filter_status.addItems(["All Statuses", "Completed (100%)", "In Progress (1-99%)", "Planned (0%)"])
        self.filter_status.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #2563EB;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #0F172A;
                selection-background-color: #2563EB;
                selection-color: #F8FAFC;
                border: 1px solid #E2E8F0;
            }
        """)
        self.filter_status.currentTextChanged.connect(self._apply_filters)
        self.filter_layout.addWidget(self.filter_status, 2)
        
        self.filter_skill = QComboBox()
        self.filter_skill.addItem("All Skills")
        self.filter_skill.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #2563EB;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #0F172A;
                selection-background-color: #2563EB;
                selection-color: #F8FAFC;
                border: 1px solid #E2E8F0;
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
        layout.addWidget(scroll)

    def _setup_detail_view(self):
        layout = QVBoxLayout(self.detail_view_widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header Row
        header_row = QHBoxLayout()
        header_row.setSpacing(12)
        
        self.btn_back = QPushButton("← Back to Projects")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background: transparent; color: #2563EB; font-weight: 800; font-size: 13px; border: none;
            }
            QPushButton:hover { text-decoration: underline; }
        """)
        self.btn_back.clicked.connect(self._on_back_clicked)
        header_row.addWidget(self.btn_back)
        header_row.addStretch()
        
        self.btn_edit_p = QPushButton("⚙ Edit Project")
        self.btn_edit_p.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_p.setStyleSheet("""
            QPushButton {
                background: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1;
                border-radius: 6px; padding: 6px 14px; font-weight: 600; font-size: 12px;
            }
            QPushButton:hover { background: #E2E8F0; }
        """)
        self.btn_edit_p.clicked.connect(self._on_edit_project_inline)
        header_row.addWidget(self.btn_edit_p)
        
        self.btn_delete_p = QPushButton("🗑 Delete")
        self.btn_delete_p.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete_p.setStyleSheet("""
            QPushButton {
                background: #FEE2E2; color: #EF4444; border: 1px solid #FCA5A5;
                border-radius: 6px; padding: 6px 14px; font-weight: 600; font-size: 12px;
            }
            QPushButton:hover { background: #FEE2E2; border: 1px solid #EF4444; }
        """)
        self.btn_delete_p.clicked.connect(self._on_delete_project_inline)
        header_row.addWidget(self.btn_delete_p)
        
        layout.addLayout(header_row)
        
        # Title & Tech Row
        title_row = QHBoxLayout()
        self.lbl_detail_title = QLabel("Project Title")
        self.lbl_detail_title.setStyleSheet("font-size: 24px; font-weight: 900; color: #0F172A; background: transparent;")
        title_row.addWidget(self.lbl_detail_title)
        
        self.detail_tech_container = QHBoxLayout()
        self.detail_tech_container.setSpacing(6)
        title_row.addLayout(self.detail_tech_container)
        title_row.addStretch()
        layout.addLayout(title_row)
        
        # Split Panel using QSplitter
        self.detail_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.detail_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #E2E8F0;
                width: 4px;
                margin: 0 4px;
            }
            QSplitter::handle:hover {
                background-color: #2563EB;
            }
        """)
        
        # Left Panel (Metadata)
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)
        
        # Description Card
        from ui_core.components import SaaSCard
        self.desc_card = SaaSCard(self)
        dl = self.desc_card.internal_layout
        dl.setSpacing(8)
        dl.addWidget(QLabel("ABOUT THIS PROJECT", styleSheet="color: #64748B; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;"))
        self.lbl_detail_desc = QLabel("Project description goes here.")
        self.lbl_detail_desc.setWordWrap(True)
        self.lbl_detail_desc.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.5; background: transparent;")
        dl.addWidget(self.lbl_detail_desc)
        
        self.lbl_detail_github = QLabel("GitHub: https://github.com")
        self.lbl_detail_github.setWordWrap(True)
        self.lbl_detail_github.setStyleSheet("color: #2563EB; font-size: 12px; background: transparent;")
        dl.addWidget(self.lbl_detail_github)
        left_panel.addWidget(self.desc_card)
        
        # Skills Card
        self.skills_card = SaaSCard(self)
        sl = self.skills_card.internal_layout
        sl.setSpacing(8)
        sl.addWidget(QLabel("ASSOCIATED SKILLS", styleSheet="color: #64748B; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;"))
        self.detail_skills_container = QHBoxLayout()
        self.detail_skills_container.setSpacing(6)
        sl.addLayout(self.detail_skills_container)
        sl.addStretch()
        left_panel.addWidget(self.skills_card)
        
        # Progress Card
        self.progress_card = SaaSCard(self)
        pl = self.progress_card.internal_layout
        pl.setSpacing(10)
        pl.addWidget(QLabel("COMPLETION PROGRESS", styleSheet="color: #64748B; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;"))
        
        p_row = QHBoxLayout()
        self.detail_bar = QProgressBar()
        self.detail_bar.setFixedHeight(8)
        self.detail_bar.setRange(0, 100)
        self.detail_bar.setTextVisible(False)
        self.detail_bar.setStyleSheet("QProgressBar { background: #F1F5F9; border-radius: 4px; border: none; } QProgressBar::chunk { background: #2563EB; border-radius: 4px; }")
        p_row.addWidget(self.detail_bar)
        
        self.lbl_detail_percent = QLabel("0%")
        self.lbl_detail_percent.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 800; background: transparent;")
        p_row.addWidget(self.lbl_detail_percent)
        pl.addLayout(p_row)
        
        self.lbl_progress_status = QLabel("Determined by requirements checklist below.")
        self.lbl_progress_status.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
        pl.addWidget(self.lbl_progress_status)
        left_panel.addWidget(self.progress_card)
        
        left_panel.addStretch()
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        self.detail_splitter.addWidget(left_widget)
        
        # Right Panel (Requirements checklist styled like a task board)
        right_panel = QVBoxLayout()
        right_panel.setSpacing(12)
        
        self.reqs_card = SaaSCard(self)
        rl = self.reqs_card.internal_layout
        rl.setSpacing(12)
        
        rl.addWidget(QLabel("📋 PROJECT REQUIREMENTS / TASKS", styleSheet="color: #0F172A; font-size: 15px; font-weight: 800;"))
        
        # Add requirement input row
        add_req_row = QHBoxLayout()
        add_req_row.setSpacing(8)
        self.edit_new_req = QLineEdit()
        self.edit_new_req.setPlaceholderText("Enter new project requirement...")
        self.edit_new_req.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1;
                border-radius: 6px; padding: 8px 12px; font-size: 13px;
            }
            QLineEdit:focus { border: 1px solid #2563EB; }
        """)
        self.edit_new_req.returnPressed.connect(self._add_requirement_inline)
        add_req_row.addWidget(self.edit_new_req, 4)
        
        btn_add_req = QPushButton("+ Add")
        btn_add_req.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_req.setStyleSheet("""
            QPushButton {
                background: #2563EB; color: white; border-radius: 6px;
                padding: 8px 16px; font-weight: bold; font-size: 12px; border: none;
            }
            QPushButton:hover { background: #1D4ED8; }
        """)
        btn_add_req.clicked.connect(self._add_requirement_inline)
        add_req_row.addWidget(btn_add_req, 1)
        rl.addLayout(add_req_row)
        
        # Scroll area for requirements list
        reqs_scroll = QScrollArea()
        reqs_scroll.setWidgetResizable(True)
        reqs_scroll.setFrameShape(QFrame.Shape.NoFrame)
        reqs_scroll.setStyleSheet("background: transparent;")
        
        self.reqs_list_widget = QWidget()
        self.reqs_list_lay = QVBoxLayout(self.reqs_list_widget)
        self.reqs_list_lay.setContentsMargins(0, 0, 0, 0)
        self.reqs_list_lay.setSpacing(8)
        self.reqs_list_lay.addStretch()
        
        reqs_scroll.setWidget(self.reqs_list_widget)
        rl.addWidget(reqs_scroll, 1)
        
        right_panel.addWidget(self.reqs_card, 1)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        self.detail_splitter.addWidget(right_widget)
        
        self.detail_splitter.setSizes([450, 650])
        layout.addWidget(self.detail_splitter, 1)

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

        # If currently looking at a specific project details, refresh it too
        if self.stacked_widget.currentIndex() == 1 and self.active_project_id is not None:
            updated_p = next((proj for proj in self.projects if proj["id"] == self.active_project_id), None)
            if updated_p:
                self._show_project_detail(updated_p)
            else:
                self._on_back_clicked()

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
                c_t.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 800; background: transparent; border: none;")
                c_header.addWidget(c_t)
                c_header.addStretch()
                
                # Copy Markdown button
                copy_btn = QPushButton("📋")
                copy_btn.setFixedSize(24, 24)
                copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                copy_btn.setStyleSheet("color: #64748B; border: none; background: transparent; font-size: 14px;")
                copy_btn.setToolTip("Copy details in Markdown format")
                copy_btn.clicked.connect(lambda checked, p=project: self._copy_markdown(p))
                c_header.addWidget(copy_btn)
                
                # Options button
                opts = QPushButton("⋮")
                opts.setFixedSize(24, 24)
                opts.setStyleSheet("color: #64748B; font-weight: 800; border: none; background: transparent; font-size: 16px;")
                opts.setCursor(Qt.CursorShape.PointingHandCursor)
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
                    badge_style = "color: #2563EB; background-color: rgba(37, 99, 235, 0.1); border: 1px solid rgba(37, 99, 235, 0.3);"
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
                            background: rgba(37, 99, 235, 0.05);
                            color: #2563EB;
                            border: 1px solid rgba(37, 99, 235, 0.15);
                            border-radius: 4px;
                            font-size: 10px;
                            padding: 2px 6px;
                        }
                        QPushButton:hover {
                            background: rgba(37, 99, 235, 0.15);
                            border: 1px solid #2563EB;
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
                color = "#10B981" if prog == 100 else "#2563EB"
                bar.setStyleSheet(f"QProgressBar {{ background: #F8FAFC; border-radius: 3px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}")
                
                c_foot.addWidget(bar)
                c_foot.addWidget(QLabel(f"{prog}%", styleSheet="color: #0F172A; font-size: 11px; font-weight: 700; background: transparent; border: none;"))
                
                from core.config import apply_theme
                apply_theme(card)
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
        
        # Get tasks (requirements)
        reqs = portfolio_db.get_project_requirements(project["id"])
        if reqs:
            text += "\n**Requirements**:\n"
            for r in reqs:
                status = "[x]" if r["completed"] else "[ ]"
                text += f"- {status} {r['requirement_text']}\n"
                
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Export Portfolio", "Project details copied to clipboard as Markdown!")

    def _on_card_clicked(self, project_data):
        self._show_project_detail(project_data)

    def _show_project_detail(self, project_data):
        self.active_project_id = project_data["id"]
        self.active_project_data = project_data
        
        self.lbl_detail_title.setText(project_data["title"])
        self.lbl_detail_desc.setText(project_data["description"])
        
        github = project_data.get("github_url", "")
        if github:
            self.lbl_detail_github.setText(f"GitHub/Link: <a href='{github}' style='color: #2563EB; text-decoration: none;'>{github}</a>")
            self.lbl_detail_github.setOpenExternalLinks(True)
        else:
            self.lbl_detail_github.setText("No GitHub or Demo Link provided.")
            
        while self.detail_tech_container.count():
            item = self.detail_tech_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        
        techs = [t.strip() for t in project_data.get("technologies", "").split(",") if t.strip()]
        for t in techs:
            lbl = QLabel(t)
            lbl.setStyleSheet("color: #2563EB; background: rgba(37,99,235,0.06); border: 1px solid rgba(37,99,235,0.15); padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;")
            self.detail_tech_container.addWidget(lbl)
            
        while self.detail_skills_container.count():
            item = self.detail_skills_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        skills = [s.strip() for s in project_data.get("skills", "").split(",") if s.strip()]
        if skills:
            for s in skills:
                lbl = QLabel(s)
                lbl.setStyleSheet("color: #A78BFA; background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.15); padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;")
                self.detail_skills_container.addWidget(lbl)
        else:
            self.detail_skills_container.addWidget(QLabel("No skills associated yet.", styleSheet="color: #94A3B8; font-size: 11px;"))
            
        self.detail_skills_container.addStretch()
        self._refresh_requirements_list_inline()
        self.stacked_widget.setCurrentIndex(1)

    def _refresh_requirements_list_inline(self):
        while self.reqs_list_lay.count() > 1:
            item = self.reqs_list_lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        reqs = portfolio_db.get_project_requirements(self.active_project_id)
        
        for r in reqs:
            row_widget = QWidget()
            row_lay = QHBoxLayout(row_widget)
            row_lay.setContentsMargins(0, 4, 0, 4)
            row_lay.setSpacing(8)
            
            chk = QCheckBox(r["requirement_text"])
            chk.setChecked(bool(r["completed"]))
            chk.setCursor(Qt.CursorShape.PointingHandCursor)
            
            if r["completed"]:
                chk.setStyleSheet("QCheckBox { color: #94A3B8; font-size: 13px; text-decoration: line-through; }")
            else:
                chk.setStyleSheet("QCheckBox { color: #0F172A; font-size: 13px; font-weight: 500; }")
                
            chk.stateChanged.connect(lambda state, rid=r["id"], c=chk: self._on_requirement_toggled_inline(rid, c))
            row_lay.addWidget(chk, 1)
            
            btn_sug = QPushButton("💡 Gợi ý")
            btn_sug.setFixedSize(75, 24)
            btn_sug.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_sug.setStyleSheet("""
                QPushButton {
                    background: #F1F5F9; color: #2563EB; border: 1px solid rgba(37, 99, 235, 0.4);
                    border-radius: 4px; font-size: 10px; font-weight: bold;
                }
                QPushButton:hover { background: #E2E8F0; }
            """)
            btn_sug.clicked.connect(lambda checked, rid=r["id"], rtxt=r["requirement_text"], sug=r["detailed_suggestion"]: self._show_suggestion_inline(rid, rtxt, sug))
            row_lay.addWidget(btn_sug)
 
            btn_del = QPushButton("🗑️")
            btn_del.setFixedSize(24, 24)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet("QPushButton { color: #EF4444; border: none; background: transparent; font-size: 12px; }")
            btn_del.clicked.connect(lambda checked, rid=r["id"]: self._delete_requirement_inline(rid))
            row_lay.addWidget(btn_del)
            
            self.reqs_list_lay.insertWidget(self.reqs_list_lay.count() - 1, row_widget)
            
        # Refresh overall project progress and set it to details progress bar
        projects = portfolio_db.get_all_projects()
        p = next((proj for proj in projects if proj["id"] == self.active_project_id), self.active_project_data)
        prog = p["progress"]
        self.detail_bar.setValue(prog)
        self.lbl_detail_percent.setText(f"{prog}%")
        color = "#10B981" if prog == 100 else "#2563EB"
        self.detail_bar.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border-radius: 4px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 4px; }}")
        
        if prog == 100:
            self.lbl_progress_status.setText("🎉 Project is fully completed!")
            self.lbl_progress_status.setStyleSheet("color: #10B981; font-weight: bold; font-size: 11px;")
        else:
            self.lbl_progress_status.setText("Complete all project requirements to achieve 100%.")
            self.lbl_progress_status.setStyleSheet("color: #64748B; font-size: 11px;")

    def _on_requirement_toggled_inline(self, req_id, chk):
        val = 1 if chk.isChecked() else 0
        portfolio_db.update_project_requirement_status(req_id, val)
        self._refresh_requirements_list_inline()

    def _add_requirement_inline(self):
        txt = self.edit_new_req.text().strip()
        if not txt: return
        portfolio_db.add_project_requirement(self.active_project_id, txt)
        self.edit_new_req.clear()
        self._refresh_requirements_list_inline()

    def _delete_requirement_inline(self, req_id):
        portfolio_db.delete_project_requirement(req_id)
        self._refresh_requirements_list_inline()

    def _show_suggestion_inline(self, req_id, requirement_text, current_suggestion):
        if current_suggestion:
            self._display_suggestion_dialog(requirement_text, current_suggestion)
        else:
            # Query AI or generate fallback
            prompt = f"Hãy viết hướng dẫn gợi ý lập trình ngắn gọn (dưới 5 câu) bằng tiếng Việt cho yêu cầu dự án sau: '{requirement_text}' trong dự án sử dụng các công nghệ: '{self.active_project_data.get('technologies', '')}'."
            
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
                ai_text = self._generate_suggestion_fallback(requirement_text, self.active_project_data.get('technologies'))
                
            portfolio_db.update_project_requirement_suggestion(req_id, ai_text)
            self._display_suggestion_dialog(requirement_text, ai_text)
            self._refresh_requirements_list_inline()

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
        elif "db" in req_lower or "database" in req_lower or "cơ sở dữ liệu" in req_lower or "sql" in req_lower:
            tips.append("- Thiết kế schema rõ ràng, sử dụng khóa ngoại để liên kết các bảng.")
            tips.append("- Đảm bảo đánh index ở các cột hay dùng để tìm kiếm (như email, id).")
        elif "api" in req_lower or "websocket" in req_lower or "endpoint" in req_lower:
            tips.append("- Tuân thủ quy chuẩn RESTful API, trả về HTTP status code phù hợp.")
            tips.append("- Áp dụng middleware kiểm tra xác thực đối với các API private.")
        else:
            tips.append(f"- Tìm hiểu tài liệu/API của các công nghệ: {technologies or 'không rõ'}.")
            tips.append("- Phân rã yêu cầu thành các hàm nhỏ, viết unit test trước khi ghép nối.")
        return f"💡 Gợi ý thiết kế cho '{requirement_text}':\n\n" + "\n".join(tips)

    def _on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(0)
        self.refresh()

    def _on_add_project(self):
        from pages.project_dialog import ProjectDialog
        dlg = ProjectDialog(parent=self)
        if dlg.exec():
            self.refresh()

    def _on_edit_project_inline(self):
        from pages.project_dialog import ProjectDialog
        projects = portfolio_db.get_all_projects()
        fresh_data = next((p for p in projects if p["id"] == self.active_project_id), self.active_project_data)
        dlg = ProjectDialog(project_data=fresh_data, parent=self)
        if dlg.exec():
            projects = portfolio_db.get_all_projects()
            updated_data = next((p for p in projects if p["id"] == self.active_project_id), fresh_data)
            self._show_project_detail(updated_data)

    def _on_delete_project_inline(self):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the project '{self.lbl_detail_title.text()}'? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            portfolio_db.delete_project(self.active_project_id)
            QMessageBox.information(self, "Success", "Project deleted successfully.")
            self._on_back_clicked()
