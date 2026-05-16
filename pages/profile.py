import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, 
                             QLineEdit, QGraphicsDropShadowEffect, QSpacerItem, 
                             QSizePolicy)
from PyQt6.QtCore import Qt, QSize, QRectF, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QFont, QLinearGradient, QIcon

from config import *
from components import SaaSCard, AnimatedCircularProgress, AnimatedProgressBar, AnimationEngine, CollapsiblePanel
from i18n import _
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
        
        # 1. Main Workspace (Scrollable)
        self.workspace_scroll = QScrollArea()
        self.workspace_scroll.setWidgetResizable(True)
        self.workspace_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.workspace_scroll.setStyleSheet("background: transparent;")
        
        self.workspace_widget = QWidget()
        self.workspace_widget.setStyleSheet("background: transparent;")
        self.workspace_layout = QVBoxLayout(self.workspace_widget)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(24)
        
        self.init_hero_section()
        self.init_skills_achievements()
        self.init_portfolio()
        self.init_timelines()
        self.init_activity()
        
        self.workspace_scroll.setWidget(self.workspace_widget)
        self.content_layout.addWidget(self.workspace_scroll, 1)
        
        # 2. Right Insights Panel (Collapsible)
        self.insights_content = self._setup_insights_panel()
        self.insights_content.setFixedWidth(320)
        self.right_panel = CollapsiblePanel(self.insights_content, orientation="right")
        self.content_layout.addWidget(self.right_panel)
        
        self.main_layout.addWidget(content_container, 1)

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
        
        search_container = QFrame()
        search_container.setFixedSize(260, 40)
        search_container.setStyleSheet("background: #FFFFFF; border-radius: 12px; border: 1px solid #E2E8F0;")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(12, 0, 12, 0)
        search_layout.setSpacing(8)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("color: #94A3B8; font-size: 13px;")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search items...")
        search_input.setStyleSheet("background: transparent; border: none; color: #0F172A; font-size: 13px;")

        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_input)
        layout.addWidget(search_container)        
        edit_btn = QPushButton("Edit Profile")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #E2E8F0; border-radius: 10px;
                color: #0F172A; font-weight: 700; font-size: 13px; height: 40px; padding: 0 16px;
            }
            QPushButton:hover { background: #F8FAFC; }
        """)
        
        export_btn = QPushButton("Export Resume")
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background: #0F172A; border-radius: 10px;
                color: white; font-weight: 700; font-size: 13px; height: 40px; padding: 0 16px;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        
        layout.addWidget(edit_btn)
        layout.addWidget(export_btn)
        
        mini_avatar = QLabel()
        mini_avatar.setFixedSize(40, 40)
        mini_avatar.setStyleSheet("background: #38BDF8; border-radius: 22px;")
        layout.addWidget(mini_avatar)
        
        self.main_layout.addWidget(toolbar)

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
        name = student.get("full_name", "Student Name") if student else "Guest User"
        major = student.get("major", "AI Engineering Student") if student else "Web Developer"
        bio = student.get("context", {}).get("bio", "Passionate about creating elegant solutions through code.") if student else "Building the future of AI."
        
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(32, 0, 32, 32)
        
        top_row = QHBoxLayout()
        top_row.setSpacing(24)
        
        avatar = QLabel()
        avatar.setFixedSize(120, 120)
        avatar.setStyleSheet("background: white; border: 6px solid white; border-radius: 60px; margin-top: -60px;")
        avatar_shadow = QGraphicsDropShadowEffect()
        avatar_shadow.setBlurRadius(30); avatar_shadow.setColor(QColor(18, 55, 105, 20)); avatar_shadow.setOffset(0,4)
        avatar.setGraphicsEffect(avatar_shadow)
        top_row.addWidget(avatar)
        
        info_v = QVBoxLayout()
        info_v.addSpacing(10)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: #0F172A; font-size: 32px; font-weight: 800; letter-spacing: -0.5px;")
        
        title_lbl = QLabel(major)
        title_lbl.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: 700;")
        
        info_v.addWidget(name_lbl)
        info_v.addWidget(title_lbl)
        top_row.addLayout(info_v)
        
        top_row.addStretch()
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(32)
        
        for val, label in [("12", "Projects"), ("05", "Certs"), ("94%", "Ready")]:
            stat_v = QVBoxLayout()
            v_lbl = QLabel(val)
            v_lbl.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 800; text-align: center;")
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
        st_lbl = QLabel("Professional Skills")
        st_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        h_layout.addWidget(st_lbl)
        h_layout.addStretch()
        skills_card.layout.addLayout(h_layout)
        
        skills_flow = QGridLayout()
        skills_flow.setSpacing(10)
        
        skills = [("Python", "Advanced"), ("PyQt6", "Advanced"), ("AI/ML", "Intermediate"), ("UI/UX", "Expert"), ("Git", "Advanced")]
        for i, (name, lvl) in enumerate(skills):
            row, col = divmod(i, 2)
            skills_flow.addWidget(SkillChip(name, lvl), row, col)
            
        skills_card.layout.addLayout(skills_flow)
        layout.addWidget(skills_card, 1)
        
        ach_card = ShadowCard()
        ach_card.layout.setSpacing(20)
        ach_lbl = QLabel("Achievements")
        ach_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        ach_card.layout.addWidget(ach_lbl)
        
        for icon, title, sub in [("🏆", "Hackathon Winner", "2023 National AI Challenge"), ("📜", "AWS Certified", "Solutions Architect Associate")]:
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
        section_lbl = QLabel("Featured Portfolio Projects")
        section_lbl.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800; margin-top: 12px;")
        self.workspace_layout.addWidget(section_lbl)
        
        grid = QGridLayout()
        grid.setSpacing(24)
        
        projects = [
            ("AI Research Assistant", ["Python", "OpenAI", "PyQt6"]),
            ("Neuromorphic UI Kit", ["CSS", "PyQt6", "Design"]),
            ("Cloud Sync Worker", ["Go", "Redis", "Docker"])
        ]
        
        for i, (title, tags) in enumerate(projects):
            grid.addWidget(ProjectCard(title, tags), 0, i)
            
        self.workspace_layout.addLayout(grid)

    def init_timelines(self):
        layout = QHBoxLayout()
        layout.setSpacing(24)
        
        aca_card = ShadowCard()
        aca_card.layout.addWidget(QLabel("Academic Milestones", styleSheet="color: #0F172A; font-size: 18px; font-weight: 700;"))
        aca_card.layout.addWidget(TimelineItem("B.Sc in AI & Data Science", "VKU University", "2021 - Present"))
        aca_card.layout.addWidget(TimelineItem("High School Diploma", "Specialized Science School", "2018 - 2021", is_last=True))
        layout.addWidget(aca_card, 1)
        
        car_card = ShadowCard()
        car_card.layout.addWidget(QLabel("Career Journey", styleSheet="color: #0F172A; font-size: 18px; font-weight: 700;"))
        car_card.layout.addWidget(TimelineItem("AI Software Intern", "Google Tech Hub", "Jun 2023 - Aug 2023"))
        car_card.layout.addWidget(TimelineItem("Open Source Contributor", "GitHub Community", "2022 - Present", is_last=True))
        layout.addWidget(car_card, 1)
        
        self.workspace_layout.addLayout(layout)

    def init_activity(self):
        act_card = ShadowCard()
        h_box = QHBoxLayout()
        h_box.addWidget(QLabel("Recent Activity", styleSheet="color: #0F172A; font-size: 18px; font-weight: 700;"))
        h_box.addStretch()
        act_card.layout.addLayout(h_box)
        
        for text, time in [("Pushed 12 commits to 'vku-ai-portal'", "2 hours ago"), ("Updated profile skills with 'PyQt6'", "Yesterday")]:
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
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        ai_card = ShadowCard()
        ai_card.setStyleSheet(ai_card.styleSheet() + " #ShadowCard { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0F172A, stop:1 #1E293B); border: none; }")
        ai_card.layout.setSpacing(12)
        
        ai_title = QLabel("AI Recommendations")
        ai_title.setStyleSheet("color: #38BDF8; font-size: 14px; font-weight: 800; text-transform: uppercase;")
        ai_card.layout.addWidget(ai_title)
        
        tip = QLabel("Your portfolio is 85% complete. Adding a 'Live Demo' could increase views.")
        tip.setWordWrap(True)
        tip.setStyleSheet("color: #E2E8F0; font-size: 13px; line-height: 1.5;")
        ai_card.layout.addWidget(tip)
        
        opt_btn = QPushButton("Optimize Now")
        opt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        opt_btn.setStyleSheet("background: #38BDF8; color: #0F172A; border-radius: 8px; height: 36px; font-weight: 700; font-size: 12px;")
        ai_card.layout.addWidget(opt_btn)
        
        layout.addWidget(ai_card)
        
        goals_card = ShadowCard()
        goals_card.layout.addWidget(QLabel("Upcoming Goals", styleSheet="color: #0F172A; font-size: 16px; font-weight: 700;"))
        
        for goal, date in [("AWS Certification", "Oct 24"), ("Portfolio V2 Launch", "Nov 12")]:
            g_row = QHBoxLayout()
            g_lbl = QLabel(goal)
            g_lbl.setStyleSheet("color: #475569; font-size: 13px; font-weight: 600;")
            d_lbl = QLabel(date)
            d_lbl.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: 700; background: #F0F9FF; padding: 2px 6px; border-radius: 4px;")
            g_row.addWidget(g_lbl); g_row.addStretch(); g_row.addWidget(d_lbl)
            goals_card.layout.addLayout(g_row)
            
        layout.addWidget(goals_card)
        
        ana_card = ShadowCard()
        ana_card.layout.addWidget(QLabel("Profile Analytics", styleSheet="color: #0F172A; font-size: 16px; font-weight: 700;"))
        
        chart_mock = QFrame()
        chart_mock.setFixedHeight(120)
        chart_mock.setStyleSheet("background: #F8FAFC; border: 1px dashed #E2E8F0; border-radius: 12px;")
        ana_card.layout.addWidget(chart_mock)
        
        ana_row = QHBoxLayout()
        for v, l in [("1.2k", "Views"), ("48", "Search")]:
            v_v = QVBoxLayout()
            v_l = QLabel(v); v_l.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800;"); v_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l_l = QLabel(l); l_l.setStyleSheet("color: #64748B; font-size: 11px;"); l_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v_v.addWidget(v_l); v_v.addWidget(l_l)
            ana_row.addLayout(v_v)
        ana_card.layout.addLayout(ana_row)
        
        layout.addWidget(ana_card)
        layout.addStretch()
        
        return panel

    def init_insights_panel(self):
        # This was replaced by _setup_insights_panel and CollapsiblePanel in __init__
        pass
