import sys
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, 
                             QLineEdit, QTextEdit, QComboBox, QMessageBox,
                             QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,
                             QTabWidget)
from PyQt6.QtCore import Qt, QSize, QRectF, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QFont, QLinearGradient, QIcon

from core.config import *
from ui_core.components import SaaSCard, AnimatedCircularProgress, AnimatedProgressBar, AnimationEngine, CollapsiblePanel
from core.i18n import _
from database import crud

class ShadowCard(QFrame):
    def __init__(self, parent=None, radius=20):
        super().__init__(parent)
        self.setObjectName("ShadowCard")
        self.setStyleSheet(f"""
            #ShadowCard {{
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: {radius}px;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(18, 55, 105, 20))
        self.setGraphicsEffect(shadow)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

class SkillChip(QWidget):
    def __init__(self, name, level="Advanced"):
        super().__init__()
        self.setFixedHeight(32)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        
        self.setStyleSheet(f"""
            QWidget {{
                background: #F1F5F9;
                border-radius: 16px;
            }}
        """)
        
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: #0F172A; font-weight: 600; font-size: 13px;")
        
        dot = QWidget()
        dot.setFixedSize(6, 6)
        dot_color = "#38BDF8" if level == "Advanced" else "#94A3B8"
        dot.setStyleSheet(f"background: {dot_color}; border-radius: 3px;")
        
        level_lbl = QLabel(level)
        level_lbl.setStyleSheet("color: #64748B; font-size: 11px;")
        
        layout.addWidget(name_lbl)
        layout.addWidget(dot)
        layout.addWidget(level_lbl)

class ProjectCard(ShadowCard):
    def __init__(self, title, tags, description="Modern AI-driven platform for enterprise solutions."):
        super().__init__(radius=20)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        thumb = QFrame()
        thumb.setFixedHeight(140)
        thumb.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F1F5F9, stop:1 #E2E8F0);
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        self.layout.addWidget(thumb)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 16, 20, 20)
        content_layout.setSpacing(12)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        content_layout.addWidget(title_lbl)
        
        desc_lbl = QLabel(description)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.4;")
        content_layout.addWidget(desc_lbl)
        
        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(8)
        for tag in tags:
            t_lbl = QLabel(tag)
            t_lbl.setStyleSheet("background: #F0F9FF; color: #0369A1; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;")
            tags_layout.addWidget(t_lbl)
        tags_layout.addStretch()
        content_layout.addLayout(tags_layout)
        
        btns_layout = QHBoxLayout()
        btns_layout.setSpacing(12)
        
        gh_btn = QPushButton("GitHub")
        gh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gh_btn.setStyleSheet("background: #0F172A; color: white; border-radius: 8px; height: 32px; font-weight: 600; font-size: 12px; padding: 0 12px;")
        
        demo_btn = QPushButton("Live Demo")
        demo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        demo_btn.setStyleSheet("background: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 8px; height: 32px; font-weight: 600; font-size: 12px; padding: 0 12px;")
        
        btns_layout.addWidget(gh_btn)
        btns_layout.addWidget(demo_btn)
        btns_layout.addStretch()
        content_layout.addLayout(btns_layout)
        
        self.layout.addWidget(content)

class TimelineItem(QWidget):
    def __init__(self, title, subtitle, date, is_last=False):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        left_col = QVBoxLayout()
        left_col.setContentsMargins(0, 4, 0, 0)
        dot = QWidget()
        dot.setFixedSize(12, 12)
        dot.setStyleSheet("background: #38BDF8; border: 3px solid #E0F2FE; border-radius: 6px;")
        left_col.addWidget(dot, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        if not is_last:
            line = QFrame()
            line.setFixedWidth(2)
            line.setStyleSheet("background: #E2E8F0; margin-top: 4px; margin-bottom: 4px;")
            left_col.addWidget(line, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        else:
            left_col.addStretch(1)
            
        layout.addLayout(left_col)
        
        right_col = QVBoxLayout()
        right_col.setSpacing(4)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px;")
        
        s_lbl = QLabel(subtitle)
        s_lbl.setStyleSheet("color: #64748B; font-size: 13px;")
        
        d_lbl = QLabel(date)
        d_lbl.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500;")
        
        right_col.addWidget(t_lbl)
        right_col.addWidget(s_lbl)
        right_col.addWidget(d_lbl)
        right_col.addSpacing(16)
        
        layout.addLayout(right_col, 1)

class TimetableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
        
        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)
        
        add_btn = QPushButton("+ Add Class")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("background: #38BDF8; color: white; border-radius: 4px; padding: 6px 12px; font-weight: bold;")
        add_btn.clicked.connect(lambda: self.add_row())
        self.layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.rows = []

    def add_row(self, data=None):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(4)
        
        day_cb = QComboBox()
        day_cb.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        start_cb = QComboBox()
        start_cb.addItems([str(i) for i in range(1, 11)])
        end_cb = QComboBox()
        end_cb.addItems([str(i) for i in range(1, 11)])
        
        title_le = QLineEdit()
        title_le.setPlaceholderText("Title")
        group_le = QLineEdit()
        group_le.setPlaceholderText("Group")
        group_le.setFixedWidth(60)
        room_le = QLineEdit()
        room_le.setPlaceholderText("Room")
        room_le.setFixedWidth(60)
        
        type_cb = QComboBox()
        type_cb.addItems(["class", "makeup", "self_study", "exam", "other"])
        
        del_btn = QPushButton("X")
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet("background: #EF4444; color: white; border-radius: 4px; padding: 4px 8px; font-weight: bold;")
        del_btn.clicked.connect(lambda: self.remove_row(row_widget))
        
        row_layout.addWidget(day_cb)
        row_layout.addWidget(QLabel("Tiết:"))
        row_layout.addWidget(start_cb)
        row_layout.addWidget(QLabel("-"))
        row_layout.addWidget(end_cb)
        row_layout.addWidget(title_le)
        row_layout.addWidget(group_le)
        row_layout.addWidget(room_le)
        row_layout.addWidget(type_cb)
        row_layout.addWidget(del_btn)
        
        if data:
            day_cb.setCurrentText(data.get("day", "Monday"))
            start_cb.setCurrentText(str(data.get("period_start", 1)))
            end_cb.setCurrentText(str(data.get("period_end", 4)))
            title_le.setText(data.get("title", ""))
            group_le.setText(data.get("group", ""))
            room_le.setText(data.get("room", ""))
            type_cb.setCurrentText(data.get("type", "class"))
            
        self.rows_layout.addWidget(row_widget)
        self.rows.append({
            "widget": row_widget,
            "day": day_cb, "start": start_cb, "end": end_cb,
            "title": title_le, "group": group_le, "room": room_le, "type": type_cb
        })

    def remove_row(self, widget):
        for row in self.rows:
            if row["widget"] == widget:
                self.rows.remove(row)
                widget.deleteLater()
                break

    def get_data(self):
        data = []
        for row in self.rows:
            title = row["title"].text().strip()
            if not title:
                continue
            data.append({
                "day": row["day"].currentText(),
                "period_start": int(row["start"].currentText()),
                "period_end": int(row["end"].currentText()),
                "title": title,
                "group": row["group"].text().strip(),
                "room": row["room"].text().strip(),
                "type": row["type"].currentText()
            })
        return data

    def clear(self):
        for row in self.rows:
            row["widget"].deleteLater()
        self.rows.clear()

class ProfilePage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("ProfilePage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.init_toolbar()
        
        content_container = QWidget()
        self.content_layout = QHBoxLayout(content_container)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(24)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: transparent;
                color: #64748B;
                font-weight: 600;
                font-size: 14px;
                padding: 12px 24px;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected {
                color: #0F172A;
                border-bottom: 2px solid #38BDF8;
                font-weight: 700;
            }
            QTabBar::tab:hover {
                color: #0F172A;
            }
        """)
        
        # 1. Tab 1: Academic Profile Form
        self.form_tab = QWidget()
        self.init_form_tab()
        self.tabs.addTab(self.form_tab, "Academic Profile Form")
        
        # 2. Tab 2: Portfolio View (Scrollable workspace)
        self.portfolio_tab = QWidget()
        self.init_portfolio_tab()
        self.tabs.addTab(self.portfolio_tab, "Portfolio View")
        
        self.content_layout.addWidget(self.tabs, 1)
        
        # 3. Right Insights Panel (Collapsible)
        self.insights_content = self._setup_insights_panel()
        self.insights_content.setFixedWidth(320)
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        self.content_layout.addWidget(self.right_panel)
        
        self.main_layout.addWidget(content_container, 1)
        
        self.refresh()

    def init_toolbar(self):
        toolbar = QWidget()
        toolbar.setFixedHeight(80)
        toolbar.setStyleSheet("background: white; border-bottom: 1px solid #E2E8F0;")
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(20)
        
        breadcrumbs = QLabel("My Profile / Portfolio")
        breadcrumbs.setStyleSheet("color: #64748B; font-weight: 600; font-size: 14px;")
        layout.addWidget(breadcrumbs)
        
        layout.addStretch()
        
        edit_btn = QPushButton("Academic Form")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #E2E8F0; border-radius: 10px;
                color: #0F172A; font-weight: 700; font-size: 13px; height: 40px; padding: 0 16px;
            }
            QPushButton:hover { background: #F8FAFC; }
        """)
        edit_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        
        export_btn = QPushButton("View Portfolio")
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background: #0F172A; border-radius: 10px;
                color: white; font-weight: 700; font-size: 13px; height: 40px; padding: 0 16px;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        export_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        
        layout.addWidget(edit_btn)
        layout.addWidget(export_btn)
        
        self.mini_avatar = QLabel()
        self.mini_avatar.setFixedSize(40, 40)
        self.mini_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mini_avatar.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38BDF8, stop:1 #0284C7);
            color: white;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        """)
        layout.addWidget(self.mini_avatar)
        
        self.main_layout.addWidget(toolbar)

    def init_form_tab(self):
        layout = QVBoxLayout(self.form_tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setFrameShape(QFrame.Shape.NoFrame)
        form_scroll.setStyleSheet("background: transparent;")
        
        form_widget = QWidget()
        form_widget.setStyleSheet("background: transparent;")
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(24)
        
        self.form_card = ShadowCard(radius=24)
        fc_layout = self.form_card.layout
        
        form_title = QLabel("Edit Academic Profile")
        form_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A;")
        fc_layout.addWidget(form_title)
        
        def create_group(title):
            group = QFrame()
            group.setStyleSheet("""
                QFrame {
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
            """)
            layout = QVBoxLayout(group)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(16)
            
            lbl = QLabel(title)
            lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
            layout.addWidget(lbl)
            
            grid = QGridLayout()
            grid.setSpacing(12)
            layout.addLayout(grid)
            return group, grid
            
        def add_field(grid, row, label_text, widget):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #475569; border: none;")
            grid.addWidget(lbl, row, 0)
            grid.addWidget(widget, row, 1)
            widget.setStyleSheet("""
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    color: #0F172A;
                    font-size: 13px;
                }
                QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                    border: 1px solid #38BDF8;
                    background-color: #FFFFFF;
                }
            """)

        # Personal Information
        g_personal, grid_personal = create_group("Personal Information")
        self.edit_display_name = QLineEdit()
        self.edit_display_name.setPlaceholderText("e.g. John Doe")
        add_field(grid_personal, 0, "Display Name:", self.edit_display_name)
        
        self.combo_student_year = QComboBox()
        self.combo_student_year.addItems(["1st Year", "2nd Year", "3rd Year", "4th Year"])
        add_field(grid_personal, 1, "Student Year:", self.combo_student_year)
        
        self.edit_major = QLineEdit()
        self.edit_major.setPlaceholderText("e.g. Computer Science")
        add_field(grid_personal, 2, "Major / Field:", self.edit_major)
        fc_layout.addWidget(g_personal)

        # Academic Background
        g_academic, grid_academic = create_group("Academic Background")
        self.edit_gpa = QLineEdit()
        self.edit_gpa.setPlaceholderText("e.g. 3.8")
        add_field(grid_academic, 0, "Current GPA:", self.edit_gpa)
        
        self.edit_courses = QTextEdit()
        self.edit_courses.setPlaceholderText("e.g. Data Structures, Intro to AI")
        self.edit_courses.setFixedHeight(60)
        add_field(grid_academic, 1, "Current Courses:", self.edit_courses)
        
        self.edit_skills = QTextEdit()
        self.edit_skills.setPlaceholderText("e.g. Python, PyQt6, Machine Learning")
        self.edit_skills.setFixedHeight(60)
        add_field(grid_academic, 2, "Professional Skills:", self.edit_skills)
        fc_layout.addWidget(g_academic)

        # Career Goals
        g_career, grid_career = create_group("Career Goals")
        self.edit_interests = QTextEdit()
        self.edit_interests.setPlaceholderText("e.g. Web Development, Robotics")
        self.edit_interests.setFixedHeight(60)
        add_field(grid_career, 0, "Interests & Goals:", self.edit_interests)
        fc_layout.addWidget(g_career)

        # Class Schedule
        g_schedule, grid_schedule = create_group("Class Schedule")
        self.timetable_editor = TimetableEditor()
        add_field(grid_schedule, 0, "Manual Timetable:", self.timetable_editor)
        fc_layout.addWidget(g_schedule)
        
        # Save & Sync Button
        self.btn_save_sync = QPushButton("Save & Sync Profile")
        self.btn_save_sync.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save_sync.setFixedHeight(48)
        self.btn_save_sync.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: white;
                border-radius: 12px;
                font-weight: 700;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1E293B;
            }
        """)
        self.btn_save_sync.clicked.connect(self._handle_save_sync)
        fc_layout.addWidget(self.btn_save_sync)
        
        form_layout.addWidget(self.form_card)
        form_layout.addStretch()
        
        form_scroll.setWidget(form_widget)
        layout.addWidget(form_scroll)

    def init_portfolio_tab(self):
        layout = QVBoxLayout(self.portfolio_tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.workspace_scroll = QScrollArea()
        self.workspace_scroll.setWidgetResizable(True)
        self.workspace_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.workspace_scroll.setStyleSheet("background: transparent;")
        
        self.workspace_widget = QWidget()
        self.workspace_widget.setStyleSheet("background: transparent;")
        self.workspace_layout = QVBoxLayout(self.workspace_widget)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(24)
        
        self.workspace_scroll.setWidget(self.workspace_widget)
        layout.addWidget(self.workspace_scroll)

    def init_hero_section(self):
        hero = ShadowCard(radius=28)
        hero.layout.setContentsMargins(0, 0, 0, 0)
        hero.layout.setSpacing(0)
        
        banner = QFrame()
        banner.setFixedHeight(120)
        banner.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:1 #38BDF8);
            border-top-left-radius: 28px;
            border-top-right-radius: 28px;
        """)
        hero.layout.addWidget(banner)
        
        student = crud.get_current_student()
        display_name = student.get("display_name", "Student Name") if student else "Guest User"
        major = student.get("major", "AI Engineering Student") if student else "Undecided"
        
        ai_plan = None
        if student:
            ai_plan = student.get("context", {}).get("ai_plan")
            
        if ai_plan and isinstance(ai_plan, dict):
            bio = ai_plan.get("student_summary", "Passionate about creating elegant solutions through code.")
        else:
            bio = "Save your profile context and click Generate Plan to build your dynamic AI Portfolio timeline."
            
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(32, 0, 32, 32)
        
        top_row = QHBoxLayout()
        top_row.setSpacing(24)
        
        avatar = QLabel()
        avatar.setFixedSize(120, 120)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        parts = display_name.strip().split()
        if len(parts) >= 2:
            initials = parts[0][0].upper() + parts[-1][0].upper()
        elif len(parts) == 1 and parts[0]:
            initials = parts[0][:2].upper()
        else:
            initials = "ST"
            
        avatar.setText(initials)
        avatar.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38BDF8, stop:1 #0284C7);
            color: white;
            border: 6px solid white;
            border-radius: 60px;
            font-weight: bold;
            font-size: 28px;
            margin-top: -60px;
        """)
        avatar_shadow = QGraphicsDropShadowEffect()
        avatar_shadow.setBlurRadius(30)
        avatar_shadow.setColor(QColor(18, 55, 105, 20))
        avatar_shadow.setOffset(0, 4)
        avatar.setGraphicsEffect(avatar_shadow)
        top_row.addWidget(avatar)
        
        info_v = QVBoxLayout()
        info_v.addSpacing(10)
        name_lbl = QLabel(display_name)
        name_lbl.setStyleSheet("color: #0F172A; font-size: 32px; font-weight: 800; letter-spacing: -0.5px;")
        
        title_lbl = QLabel(major)
        title_lbl.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: 700;")
        
        info_v.addWidget(name_lbl)
        info_v.addWidget(title_lbl)
        top_row.addLayout(info_v)
        
        top_row.addStretch()
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(32)
        
        proj_count = "0"
        readiness = "0%"
        status_text = "EMPTY"
        
        if student:
            raw_input = student.get("context", {}).get("raw_input", {})
            proj_count = str(len(raw_input.get("academic_context", {}).get("current_courses", [])))
            status_text = student.get("context", {}).get("ai_status", "EMPTY")
            if ai_plan and isinstance(ai_plan, dict):
                readiness = f"{ai_plan.get('metrics', {}).get('career_readiness', 0)}%"
                
        for val, label in [(proj_count, "Courses"), (status_text, "AI Status"), (readiness, "Ready")]:
            stat_v = QVBoxLayout()
            v_lbl = QLabel(val)
            v_lbl.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800;")
            v_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l_lbl = QLabel(label)
            l_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600; text-transform: uppercase;")
            l_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stat_v.addWidget(v_lbl)
            stat_v.addWidget(l_lbl)
            stats_layout.addLayout(stat_v)
            
        top_row.addLayout(stats_layout)
        c_layout.addLayout(top_row)
        
        bio_lbl = QLabel(bio)
        bio_lbl.setWordWrap(True)
        bio_lbl.setStyleSheet("color: #475569; font-size: 15px; margin-top: 16px; line-height: 1.6;")
        c_layout.addWidget(bio_lbl)
        
        hero.layout.addWidget(content)
        self.workspace_layout.addWidget(hero)

    def init_skills_achievements(self):
        layout = QHBoxLayout()
        layout.setSpacing(24)
        
        skills_card = ShadowCard()
        skills_card.layout.setSpacing(20)
        
        h_layout = QHBoxLayout()
        st_lbl = QLabel("Academic & Professional Skills")
        st_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        h_layout.addWidget(st_lbl)
        h_layout.addStretch()
        skills_card.layout.addLayout(h_layout)
        
        skills_flow = QGridLayout()
        skills_flow.setSpacing(10)
        
        student = crud.get_current_student()
        skills_list = []
        if student:
            ai_plan = student.get("context", {}).get("ai_plan")
            if ai_plan and isinstance(ai_plan, dict):
                strengths = ai_plan.get("skill_analysis", {}).get("strengths", [])
                skills_list = [(s, "AI Verified") for s in strengths]
                
            if not skills_list:
                raw_skills = student.get("context", {}).get("raw_input", {}).get("student_info", {}).get("skills", [])
                skills_list = [(s, "Custom") for s in raw_skills]
                
        if not skills_list:
            skills_list = [("Python", "Skill"), ("PyQt6", "Skill"), ("Git", "Skill")]
            
        for i, (name, lvl) in enumerate(skills_list[:8]):
            row, col = divmod(i, 2)
            skills_flow.addWidget(SkillChip(name, lvl), row, col)
            
        skills_card.layout.addLayout(skills_flow)
        layout.addWidget(skills_card, 1)
        
        ach_card = ShadowCard()
        ach_card.layout.setSpacing(20)
        ach_lbl = QLabel("Recommendations / Focus")
        ach_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        ach_card.layout.addWidget(ach_lbl)
        
        focus_items = []
        if student:
            ai_plan = student.get("context", {}).get("ai_plan")
            if ai_plan and isinstance(ai_plan, dict):
                focus_areas = ai_plan.get("skill_analysis", {}).get("recommended_focus", [])
                for f in focus_areas:
                    focus_items.append(("🎯", "Recommended Focus", f))
                    
        if not focus_items:
            focus_items = [
                ("🏆", "Default Goal", "Generate study plan to calculate recommendations"),
                ("📜", "Skill Target", "Add your courses to begin verification")
            ]
            
        for icon, title, sub in focus_items[:3]:
            row = QHBoxLayout()
            row.setSpacing(12)
            ic_lbl = QLabel(icon)
            ic_lbl.setFixedSize(40, 40)
            ic_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ic_lbl.setStyleSheet("background: #F0F9FF; border-radius: 12px; font-size: 20px;")
            
            t_v = QVBoxLayout()
            t_l = QLabel(title)
            t_l.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px;")
            s_l = QLabel(sub)
            s_l.setStyleSheet("color: #64748B; font-size: 12px;")
            t_v.addWidget(t_l); t_v.addWidget(s_l)
            
            row.addWidget(ic_lbl)
            row.addLayout(t_v)
            row.addStretch()
            ach_card.layout.addLayout(row)
            
        layout.addWidget(ach_card, 1)
        self.workspace_layout.addLayout(layout)

    def init_portfolio(self):
        section_lbl = QLabel("Featured Study Tracks & Courses")
        section_lbl.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800; margin-top: 12px;")
        self.workspace_layout.addWidget(section_lbl)
        
        grid = QGridLayout()
        grid.setSpacing(24)
        
        student = crud.get_current_student()
        courses_list = []
        if student:
            raw_input = student.get("context", {}).get("raw_input", {})
            courses_list = raw_input.get("academic_context", {}).get("current_courses", [])
            
        if not courses_list:
            courses_list = ["No Courses Added Yet"]
            
        for i, course_name in enumerate(courses_list[:3]):
            grid.addWidget(ProjectCard(course_name, ["Course", "Academic"], "Part of your active student profile study plan."), 0, i)
            
        self.workspace_layout.addLayout(grid)

    def init_timelines(self):
        layout = QHBoxLayout()
        layout.setSpacing(24)
        
        student = crud.get_current_student()
        roadmap = []
        if student:
            ai_plan = student.get("context", {}).get("ai_plan")
            if ai_plan and isinstance(ai_plan, dict):
                roadmap = ai_plan.get("academic_roadmap", [])
                
        aca_card = ShadowCard()
        aca_card.layout.addWidget(QLabel("AI Academic Roadmap", styleSheet="color: #0F172A; font-size: 18px; font-weight: 700;"))
        
        if roadmap:
            for i, item in enumerate(roadmap[:3]):
                title = item.get("title", "Course Plan")
                status = item.get("status", "planned").replace("_", " ").title()
                insight = item.get("ai_insight", "")
                progress = item.get("progress_pct", 0)
                is_last = (i == len(roadmap[:3]) - 1)
                
                subtitle = f"Status: {status} ({progress}%)"
                if insight:
                    subtitle += f"\nAI Insight: {insight}"
                aca_card.layout.addWidget(TimelineItem(title, subtitle, "Roadmap", is_last=is_last))
        else:
            aca_card.layout.addWidget(TimelineItem("B.Sc in AI & Data Science", "VKU University", "2021 - Present"))
            aca_card.layout.addWidget(TimelineItem("No AI Roadmap Available", "Please trigger plan generation on the Dashboard.", "Planned", is_last=True))
            
        layout.addWidget(aca_card, 1)
        
        car_card = ShadowCard()
        car_card.layout.addWidget(QLabel("Career Journey Plan", styleSheet="color: #0F172A; font-size: 18px; font-weight: 700;"))
        
        target_role = "Software Engineer"
        interests = []
        if student:
            raw_input = student.get("context", {}).get("raw_input", {})
            interests = raw_input.get("career_goals", {}).get("interests", [])
            
        car_card.layout.addWidget(TimelineItem(f"Target: {target_role}", ", ".join(interests) if interests else "AI Developer / Web Architect", "Goal"))
        car_card.layout.addWidget(TimelineItem("Active Learner Profile", "Tracking local sync and academic plan progress", "Current", is_last=True))
        layout.addWidget(car_card, 1)
        
        self.workspace_layout.addLayout(layout)

    def init_activity(self):
        act_card = ShadowCard()
        h_box = QHBoxLayout()
        h_box.addWidget(QLabel("Local Sync Activity Log", styleSheet="color: #0F172A; font-size: 18px; font-weight: 700;"))
        h_box.addStretch()
        act_card.layout.addLayout(h_box)
        
        student = crud.get_current_student()
        is_dirty = 0
        status_text = "EMPTY"
        updated_at = "Unknown"
        if student:
            is_dirty = student.get("context", {}).get("is_dirty", 0) or student.get("is_dirty", 0)
            status_text = student.get("context", {}).get("ai_status", "EMPTY")
            updated_at = student.get("context", {}).get("updated_at", "")[:19].replace("T", " ")
            
        sync_status = "Pending Sync" if is_dirty else "Synchronized with Backend"
        
        for text, time in [
            (f"AI Plan Status: {status_text}", updated_at),
            (f"Local SQLite Sync Status: {sync_status}", "Realtime")
        ]:
            row = QHBoxLayout()
            row.setContentsMargins(0, 8, 0, 8)
            t_lbl = QLabel(text)
            t_lbl.setStyleSheet("color: #475569; font-size: 14px;")
            time_lbl = QLabel(time)
            time_lbl.setStyleSheet("color: #94A3B8; font-size: 12px;")
            row.addWidget(t_lbl)
            row.addStretch()
            row.addWidget(time_lbl)
            act_card.layout.addLayout(row)
            
        self.workspace_layout.addWidget(act_card)

    def _setup_insights_panel(self):
        self.insights_container = QWidget()
        self.insights_content_layout = QVBoxLayout(self.insights_container)
        self.insights_content_layout.setContentsMargins(0, 0, 0, 0)
        self.insights_content_layout.setSpacing(24)
        
        self._populate_insights(self.insights_content_layout)
        return self.insights_container

    def _populate_insights(self, layout):
        student = crud.get_current_student()
        recommendation_text = "Your portfolio is ready. Update your profile info to recalculate insights."
        
        ai_plan = None
        if student:
            ai_plan = student.get("context", {}).get("ai_plan")
            
        if ai_plan and isinstance(ai_plan, dict):
            focus_areas = ai_plan.get("skill_analysis", {}).get("recommended_focus", [])
            if focus_areas:
                recommendation_text = "Recommended Skills to target:\n" + "\n".join([f"• {f}" for f in focus_areas])
            else:
                recommendation_text = "Academic profile successfully generated! View your study roadmap below."
        elif student:
            recommendation_text = "Profile saved locally. Please trigger AI Academic Plan generation to calculate recommendations."
            
        ai_card = ShadowCard()
        ai_card.setStyleSheet(ai_card.styleSheet() + " #ShadowCard { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0F172A, stop:1 #1E293B); border: none; }")
        ai_card.layout.setSpacing(12)
        
        ai_title = QLabel("AI Recommendations")
        ai_title.setStyleSheet("color: #38BDF8; font-size: 14px; font-weight: 800; text-transform: uppercase;")
        ai_card.layout.addWidget(ai_title)
        
        tip = QLabel(recommendation_text)
        tip.setWordWrap(True)
        tip.setStyleSheet("color: #E2E8F0; font-size: 13px; line-height: 1.5;")
        ai_card.layout.addWidget(tip)
        
        opt_btn = QPushButton("Generate/Refresh Plan")
        opt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        opt_btn.setStyleSheet("background: #38BDF8; color: #0F172A; border-radius: 8px; height: 36px; font-weight: 700; font-size: 12px;")
        opt_btn.clicked.connect(self._trigger_ai_plan_from_portfolio)
        ai_card.layout.addWidget(opt_btn)
        
        layout.addWidget(ai_card)
        
        goals_card = ShadowCard()
        goals_card.layout.addWidget(QLabel("Upcoming Goals", styleSheet="color: #0F172A; font-size: 16px; font-weight: 700;"))
        
        goals = []
        if ai_plan and isinstance(ai_plan, dict):
            roadmap = ai_plan.get("academic_roadmap", [])
            for item in roadmap:
                if item.get("status") == "in_progress":
                    goals.append((item.get("title", ""), "Target"))
            
        if not goals:
            goals = [("AWS Certification", "Oct 24"), ("Portfolio V2 Launch", "Nov 12")]
            
        for goal, date in goals:
            g_row = QHBoxLayout()
            g_lbl = QLabel(goal)
            g_lbl.setStyleSheet("color: #475569; font-size: 13px; font-weight: 600;")
            d_lbl = QLabel(date)
            d_lbl.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: 700; background: #F0F9FF; padding: 2px 6px; border-radius: 4px;")
            g_row.addWidget(g_lbl); g_row.addStretch(); g_row.addWidget(d_lbl)
            goals_card.layout.addLayout(g_row)
            
        layout.addWidget(goals_card)
        
        # GPA / Readiness stats
        gpa_val = "0.0"
        readiness_val = "0%"
        if student:
            gpa_raw = student.get("context", {}).get("raw_input", {}).get("student_info", {}).get("gpa", 0.0)
            try:
                gpa_val = f"{float(gpa_raw):.2f}"
            except:
                gpa_val = "0.0"
            if ai_plan and isinstance(ai_plan, dict):
                readiness_val = f"{ai_plan.get('metrics', {}).get('career_readiness', 0)}%"
                
        ana_card = ShadowCard()
        ana_card.layout.addWidget(QLabel("Profile Analytics", styleSheet="color: #0F172A; font-size: 16px; font-weight: 700;"))
        
        ana_row = QHBoxLayout()
        for v, l in [(gpa_val, "GPA"), (readiness_val, "Career Ready")]:
            v_v = QVBoxLayout()
            v_l = QLabel(v); v_l.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800;"); v_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l_l = QLabel(l); l_l.setStyleSheet("color: #64748B; font-size: 11px;"); l_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v_v.addWidget(v_l); v_v.addWidget(l_l)
            ana_row.addLayout(v_v)
        ana_card.layout.addLayout(ana_row)
        
        layout.addWidget(ana_card)
        layout.addStretch()

    def _trigger_ai_plan_from_portfolio(self):
        if self.controller and hasattr(self.controller, "show_page"):
            self.controller.show_page(0)
            dashboard_page = self.controller.pages_container.widget(0)
            if dashboard_page and hasattr(dashboard_page, "start_generation"):
                dashboard_page.start_generation()

    def _handle_save_sync(self):
        student = crud.get_current_student()
        if not student:
            QMessageBox.warning(self, "Error", "No logged-in student session found.")
            return
            
        student_id = student["id"]
        email = student["email"]
        username = student["username"]
        
        display_name = self.edit_display_name.text().strip()
        major = self.edit_major.text().strip()
        student_year = self.combo_student_year.currentData()
        
        # Validate GPA
        try:
            gpa = float(self.edit_gpa.text().strip() or 0.0)
        except ValueError:
            QMessageBox.warning(self, "Invalid GPA", "GPA must be a valid number (e.g. 3.8).")
            return
            
        def parse_list(txt_edit):
            text = txt_edit.toPlainText().strip()
            if not text:
                return []
            return [x.strip() for x in text.split(",") if x.strip()]
            
        courses = parse_list(self.edit_courses)
        skills = parse_list(self.edit_skills)
        interests = parse_list(self.edit_interests)
        
        raw_input = {
            "student_info": {
                "full_name": display_name,
                "major": major,
                "current_semester": student_year * 2 - 1,
                "gpa": gpa,
                "skills": skills
            },
            "academic_context": {
                "current_courses": courses,
                "completed_courses": [],
                "timetable_manual": self.timetable_editor.get_data()
            },
            "career_goals": {
                "target_role": "",
                "interests": interests
            }
        }
        
        # Save to SQLite local database with is_dirty=1 (both profile and context)
        crud.save_student_profile(
            student_id=student_id,
            email=email,
            username=username,
            display_name=display_name,
            major=major,
            student_year=student_year,
            is_dirty=1
        )
        
        context_data = student.get("context", {})
        ai_plan = context_data.get("ai_plan")
        ai_status = context_data.get("ai_status", "EMPTY")
        ai_last_error = context_data.get("ai_last_error")
        
        crud.save_student_context(
            student_id=student_id,
            raw_input_dict=raw_input,
            ai_plan_dict=ai_plan,
            ai_status=ai_status,
            ai_last_error=ai_last_error,
            is_dirty=1
        )
        
        # Update user info in sidebar
        main_win = self.window()
        if main_win and hasattr(main_win, "sidebar"):
            main_win.sidebar.update_user_info(display_name, major)
            
        QMessageBox.information(self, "Profile Saved", "Your academic profile changes have been saved locally. They will sync to the server automatically during plan generation.")
        
        # Switch to dashboard page and start AI generation
        if self.controller and hasattr(self.controller, "show_page"):
            self.controller.show_page(0)
            dashboard_page = self.controller.pages_container.widget(0)
            if dashboard_page and hasattr(dashboard_page, "start_generation"):
                dashboard_page.start_generation()

    def load_data(self):
        student = crud.get_current_student()
        if not student:
            return
            
        display_name = student.get("display_name", "") or ""
        major = student.get("major", "") or ""
        student_year = student.get("student_year", 1) or 1
        
        self.edit_display_name.setText(display_name)
        self.edit_major.setText(major)
        
        idx = self.combo_student_year.findData(student_year)
        if idx >= 0:
            self.combo_student_year.setCurrentIndex(idx)
            
        context_data = student.get("context", {})
        raw_input = context_data.get("raw_input", {})
        
        student_info = raw_input.get("student_info", {})
        gpa = student_info.get("gpa", 0.0)
        skills = student_info.get("skills", [])
        
        academic_context = raw_input.get("academic_context", {})
        courses = academic_context.get("current_courses", [])
        
        career_goals = raw_input.get("career_goals", {})
        interests = career_goals.get("interests", [])
        
        self.edit_gpa.setText(str(gpa))
        self.edit_courses.setText(", ".join(courses))
        self.edit_skills.setText(", ".join(skills))
        self.edit_interests.setText(", ".join(interests))
        
        self.timetable_editor.clear()
        timetable_manual = academic_context.get("timetable_manual", [])
        for row_data in timetable_manual:
            self.timetable_editor.add_row(row_data)
        
        # Update mini avatar initials
        parts = display_name.strip().split()
        if len(parts) >= 2:
            initials = parts[0][0].upper() + parts[-1][0].upper()
        elif len(parts) == 1 and parts[0]:
            initials = parts[0][:2].upper()
        else:
            initials = "ST"
        self.mini_avatar.setText(initials)

    def refresh(self):
        self.load_data()
        
        # Rebuild the portfolio tab
        self._clear_layout(self.workspace_layout)
        
        self.init_hero_section()
        self.init_skills_achievements()
        self.init_portfolio()
        self.init_timelines()
        self.init_activity()
        
        # Rebuild the insights panel
        if hasattr(self, "insights_content_layout"):
            self._clear_layout(self.insights_content_layout)
            self._populate_insights(self.insights_content_layout)

    def _clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())
