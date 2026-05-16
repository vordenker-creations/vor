import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QLineEdit,
                             QProgressBar, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QColor

class RoadmapPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("RoadmapPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Top Toolbar (Header)
        header = QFrame()
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        header.setFixedHeight(72)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        header_layout.setSpacing(16)
        
        breadcrumbs = QLabel("Academic Roadmap / Fall 2026")
        breadcrumbs.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: bold; border: none;")
        header_layout.addWidget(breadcrumbs)
        
        header_layout.addStretch()
        
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search roadmap... (Ctrl+K)")
        search_bar.setFixedWidth(240)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #F1F5F9;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                color: #0F172A;
            }
        """)
        header_layout.addWidget(search_bar)
        
        btn_add = QPushButton("+ Add Subject")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #38BDF8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0284C7; }
        """)
        header_layout.addWidget(btn_add)
        
        btn_export = QPushButton("Export PDF")
        btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #F8FAFC; }
        """)
        header_layout.addWidget(btn_export)
        
        avatar = QLabel("JD")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #2DD4BF;
            color: white;
            border-radius: 18px;
            font-weight: bold;
        """)
        header_layout.addWidget(avatar)
        
        main_layout.addWidget(header)
        
        # QScrollArea for Central Workspace and Right Panel
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(24, 24, 24, 24)
        scroll_layout.setSpacing(24)
        
        # Central Workspace
        central_workspace = QWidget()
        central_layout = QVBoxLayout(central_workspace)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(32)
        
        # Setup sections in Central Workspace
        self.setup_kpi_cards(central_layout)
        self.setup_roadmap_timeline(central_layout)
        self.setup_study_planner(central_layout)
        self.setup_certification_tracker(central_layout)
        
        central_layout.addStretch()
        
        scroll_layout.addWidget(central_workspace, stretch=1)
        
        # Right Assistant Panel
        right_panel = QFrame()
        right_panel.setFixedWidth(320)
        right_panel.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(24)
        
        self.setup_right_panel(right_layout)
        right_layout.addStretch()
        
        scroll_layout.addWidget(right_panel)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
    def create_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF; 
                border: 1px solid #E2E8F0; 
                border-radius: 22px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        return card

    def setup_kpi_cards(self, parent_layout):
        layout = QHBoxLayout()
        layout.setSpacing(16)
        
        kpis = [
            ("Completed Credits", "84 / 120", "12 this semester", "#38BDF8"),
            ("Current GPA", "3.85", "Top 5% of class", "#2DD4BF"),
            ("Semester Progress", "65%", "Week 10 of 15", "#F59E0B"),
            ("AI Readiness Score", "Advanced", "+15 pts from last month", "#8B5CF6")
        ]
        
        for title, value, sub, color in kpis:
            card = self.create_card()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(8)
            
            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("color: #64748B; font-size: 14px; border: none; background: transparent;")
            
            lbl_value = QLabel(value)
            lbl_value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold; border: none; background: transparent;")
            
            lbl_sub = QLabel(sub)
            lbl_sub.setStyleSheet("color: #94A3B8; font-size: 12px; border: none; background: transparent;")
            
            card_layout.addWidget(lbl_title)
            card_layout.addWidget(lbl_value)
            card_layout.addWidget(lbl_sub)
            layout.addWidget(card)
            
        parent_layout.addLayout(layout)
        
    def setup_roadmap_timeline(self, parent_layout):
        title = QLabel("Roadmap Timeline")
        title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: bold;")
        parent_layout.addWidget(title)
        
        timeline_layout = QVBoxLayout()
        timeline_layout.setSpacing(16)
        
        semesters = [
            ("Semester 5 (Current)", [("CS301", "Algorithms", "Hard", True), ("AI101", "Intro to AI", "Medium", False)]),
            ("Semester 6", [("CS401", "Databases", "Medium", False), ("SE201", "Software Eng", "Hard", False)])
        ]
        
        for sem, subjects in semesters:
            card = self.create_card()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(12)
            
            sem_title = QLabel(sem)
            sem_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: bold; border: none; background: transparent;")
            card_layout.addWidget(sem_title)
            
            for code, name, diff, done in subjects:
                subj_widget = QFrame()
                subj_widget.setStyleSheet("background: transparent; border: none;")
                subj_layout = QHBoxLayout(subj_widget)
                subj_layout.setContentsMargins(0, 4, 0, 4)
                
                chk = QLabel("☑" if done else "☐")
                chk.setStyleSheet(f"color: {'#2DD4BF' if done else '#CBD5E1'}; font-size: 20px; border: none; background: transparent;")
                subj_layout.addWidget(chk)
                
                lbl_name = QLabel(f"<b>{code}</b>: {name}")
                lbl_name.setStyleSheet("color: #334155; font-size: 14px; border: none; background: transparent;")
                subj_layout.addWidget(lbl_name)
                
                subj_layout.addStretch()
                
                badge = QLabel(diff)
                badge_color = "#EF4444" if diff == "Hard" else "#F59E0B"
                badge.setStyleSheet(f"background-color: {badge_color}; color: white; padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: bold; border: none;")
                subj_layout.addWidget(badge)
                
                card_layout.addWidget(subj_widget)
                
            timeline_layout.addWidget(card)
            
        parent_layout.addLayout(timeline_layout)

    def setup_study_planner(self, parent_layout):
        title = QLabel("Study Planner")
        title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: bold;")
        parent_layout.addWidget(title)
        
        layout = QHBoxLayout()
        layout.setSpacing(24)
        
        # Left: Calendar Blocks
        calendar_card = self.create_card()
        cal_layout = QVBoxLayout(calendar_card)
        cal_layout.setContentsMargins(20, 20, 20, 20)
        cal_layout.setSpacing(16)
        
        cal_title = QLabel("Today's Schedule")
        cal_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        cal_layout.addWidget(cal_title)
        
        schedule = [
            ("09:00 AM", "Algorithms Lecture", "#38BDF8"),
            ("11:00 AM", "AI Lab Assignment", "#2DD4BF"),
            ("02:00 PM", "Group Study: DBs", "#8B5CF6")
        ]
        
        for time, task, color in schedule:
            item = QFrame()
            item.setStyleSheet("background: transparent; border: none;")
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 4, 0, 4)
            
            lbl_time = QLabel(time)
            lbl_time.setStyleSheet("color: #64748B; font-size: 13px; border: none; background: transparent;")
            lbl_time.setFixedWidth(70)
            item_layout.addWidget(lbl_time)
            
            line = QFrame()
            line.setFixedWidth(4)
            line.setStyleSheet(f"background-color: {color}; border-radius: 2px; border: none;")
            item_layout.addWidget(line)
            
            lbl_task = QLabel(task)
            lbl_task.setStyleSheet("color: #334155; font-size: 14px; font-weight: bold; border: none; background: transparent;")
            item_layout.addWidget(lbl_task)
            
            cal_layout.addWidget(item)
            
        layout.addWidget(calendar_card, stretch=2)
        
        # Right: Floating Recommendations
        recom_card = self.create_card()
        rec_layout = QVBoxLayout(recom_card)
        rec_layout.setContentsMargins(20, 20, 20, 20)
        rec_layout.setSpacing(12)
        
        rec_title = QLabel("Smart Recommendations")
        rec_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        rec_layout.addWidget(rec_title)
        
        recs = [
            "Review AI Lab notes before 11 AM.",
            "Complete 2 LeetCode Mediums today.",
            "Start drafting DB project proposal."
        ]
        
        for r in recs:
            lbl = QLabel(f"• {r}")
            lbl.setStyleSheet("color: #475569; font-size: 13px; border: none; background: transparent;")
            lbl.setWordWrap(True)
            rec_layout.addWidget(lbl)
            
        rec_layout.addStretch()
        layout.addWidget(recom_card, stretch=1)
        
        parent_layout.addLayout(layout)

    def setup_certification_tracker(self, parent_layout):
        title = QLabel("Certification Tracker")
        title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: bold;")
        parent_layout.addWidget(title)
        
        layout = QHBoxLayout()
        layout.setSpacing(16)
        
        certs = [
            ("AWS Solutions Architect", 75, "Est. Dec 2026"),
            ("Google Data Engineer", 40, "Est. Mar 2027")
        ]
        
        for name, prog, est in certs:
            card = self.create_card()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(12)
            
            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: bold; border: none; background: transparent;")
            card_layout.addWidget(lbl_name)
            
            progress = QProgressBar()
            progress.setValue(prog)
            progress.setFixedHeight(8)
            progress.setTextVisible(False)
            progress.setStyleSheet("""
                QProgressBar {
                    background-color: #E2E8F0;
                    border: none;
                    border-radius: 4px;
                }
                QProgressBar::chunk {
                    background-color: #38BDF8;
                    border-radius: 4px;
                }
            """)
            card_layout.addWidget(progress)
            
            lbl_est = QLabel(est)
            lbl_est.setStyleSheet("color: #64748B; font-size: 12px; border: none; background: transparent;")
            card_layout.addWidget(lbl_est)
            
            layout.addWidget(card)
            
        parent_layout.addLayout(layout)

    def setup_right_panel(self, parent_layout):
        # AI Insights
        ai_card = self.create_card()
        ai_layout = QVBoxLayout(ai_card)
        ai_layout.setContentsMargins(20, 20, 20, 20)
        ai_layout.setSpacing(12)
        
        ai_title = QLabel("✨ AI Insights")
        ai_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        ai_layout.addWidget(ai_title)
        
        ai_desc = QLabel("Based on your performance in Algorithms, consider dedicating an extra 2 hours this week to Dynamic Programming concepts.")
        ai_desc.setWordWrap(True)
        ai_desc.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.5; border: none; background: transparent;")
        ai_layout.addWidget(ai_desc)
        parent_layout.addWidget(ai_card)
        
        # Upcoming Deadlines
        deadlines_card = self.create_card()
        dl_layout = QVBoxLayout(deadlines_card)
        dl_layout.setContentsMargins(20, 20, 20, 20)
        dl_layout.setSpacing(12)
        
        dl_title = QLabel("📅 Upcoming Deadlines")
        dl_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        dl_layout.addWidget(dl_title)
        
        deadlines = [
            ("AI Assignment 3", "Tomorrow, 11:59 PM", "#EF4444"),
            ("DB Milestone 1", "Friday, 5:00 PM", "#F59E0B")
        ]
        
        for task, due, color in deadlines:
            dl_item = QFrame()
            dl_item.setStyleSheet("background: transparent; border: none;")
            item_layout = QVBoxLayout(dl_item)
            item_layout.setContentsMargins(0, 4, 0, 4)
            item_layout.setSpacing(4)
            
            lbl_task = QLabel(task)
            lbl_task.setStyleSheet("color: #334155; font-size: 14px; font-weight: bold; border: none; background: transparent;")
            lbl_due = QLabel(due)
            lbl_due.setStyleSheet(f"color: {color}; font-size: 12px; border: none; background: transparent;")
            
            item_layout.addWidget(lbl_task)
            item_layout.addWidget(lbl_due)
            dl_layout.addWidget(dl_item)
            
        parent_layout.addWidget(deadlines_card)
        
        # Recent Activity
        activity_card = self.create_card()
        act_layout = QVBoxLayout(activity_card)
        act_layout.setContentsMargins(20, 20, 20, 20)
        act_layout.setSpacing(12)
        
        act_title = QLabel("🔄 Recent Activity")
        act_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        act_layout.addWidget(act_title)
        
        activities = [
            "Completed CS301 Quiz 2",
            "Added new goal: AWS Cert",
            "Studied AI for 2 hours"
        ]
        
        for act in activities:
            lbl = QLabel(f"• {act}")
            lbl.setStyleSheet("color: #64748B; font-size: 13px; border: none; background: transparent;")
            act_layout.addWidget(lbl)
            
        parent_layout.addWidget(activity_card)
