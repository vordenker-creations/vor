import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, 
                             QProgressBar, QLineEdit, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor, QIcon, QFont
from config import *
from components import AnimationEngine, AnimatedProgressBar, AnimatedCircularProgress, CollapsiblePanel

class ModernCard(QFrame):
    def __init__(self, parent=None, radius=20, border_color="#E2E8F0"):
        super().__init__(parent)
        self.setObjectName("ModernCard")
        self.setStyleSheet(f"""
            QFrame#ModernCard {{
                background-color: #FFFFFF;
                border: 1px solid {border_color};
                border-radius: {radius}px;
            }}
        """)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(8)
        self.shadow.setColor(QColor(18, 55, 105, 20))
        self.setGraphicsEffect(self.shadow)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

class KPICard(ModernCard):
    def __init__(self, title, value, subtext, progress=None, icon=None, color="#38BDF8"):
        super().__init__()
        self.setFixedHeight(140)
        
        h_layout = QHBoxLayout()
        self.layout.addLayout(h_layout)
        h_layout.setContentsMargins(0, 0, 0, 0)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase;")
        info_layout.addWidget(title_lbl)
        
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 700;")
        info_layout.addWidget(val_lbl)
        
        sub_lbl = QLabel(subtext)
        sub_lbl.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500;")
        info_layout.addWidget(sub_lbl)
        
        h_layout.addLayout(info_layout)
        h_layout.addStretch()
        
        if progress is not None:
            circ = AnimatedCircularProgress(size=70, color=color)
            circ.set_target(progress)
            h_layout.addWidget(circ)
        elif icon:
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet(f"font-size: 32px; color: {color};")
            h_layout.addWidget(icon_lbl)

class TaskCard(ModernCard):
    def __init__(self, title, course, deadline, priority, progress=0, ai_tag=None):
        super().__init__(radius=16)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.setSpacing(10)
        
        tag_layout = QHBoxLayout()
        course_lbl = QLabel(course)
        course_lbl.setStyleSheet(f"""
            background: #F1F5F9; color: #475569; 
            padding: 4px 10px; border-radius: 6px; 
            font-size: 11px; font-weight: 700;
        """)
        tag_layout.addWidget(course_lbl)
        tag_layout.addStretch()
        
        p_colors = {"Urgent": "#EF4444", "High": "#F59E0B", "Med": "#3B82F6", "Low": "#10B981"}
        p_color = p_colors.get(priority, "#64748B")
        p_lbl = QLabel(priority)
        p_lbl.setStyleSheet(f"""
            color: {p_color}; background: {p_color}15; 
            padding: 4px 10px; border-radius: 6px; 
            font-size: 11px; font-weight: 700;
        """)
        tag_layout.addWidget(p_lbl)
        self.layout.addLayout(tag_layout)
        
        title_lbl = QLabel(title)
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 600;")
        self.layout.addWidget(title_lbl)
        
        dd_layout = QHBoxLayout()
        dd_icon = QLabel("📅")
        dd_icon.setStyleSheet("font-size: 12px;")
        dd_lbl = QLabel(deadline)
        dd_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 500;")
        dd_layout.addWidget(dd_icon)
        dd_layout.addWidget(dd_lbl)
        dd_layout.addStretch()
        self.layout.addLayout(dd_layout)
        
        pb = QProgressBar()
        pb.setFixedHeight(6)
        pb.setValue(progress)
        pb.setTextVisible(False)
        pb.setStyleSheet(f"""
            QProgressBar {{ background: #F1F5F9; border-radius: 3px; border: none; }}
            QProgressBar::chunk {{ background: {COLOR_PRIMARY}; border-radius: 3px; }}
        """)
        self.layout.addWidget(pb)
        
        if ai_tag:
            ai_layout = QHBoxLayout()
            ai_icon = QLabel("✨")
            ai_lbl = QLabel(ai_tag)
            ai_lbl.setStyleSheet("color: #8B5CF6; font-size: 11px; font-weight: 600; font-style: italic;")
            ai_layout.addWidget(ai_icon)
            ai_layout.addWidget(ai_lbl)
            ai_layout.addStretch()
            self.layout.addLayout(ai_layout)

class KanbanColumn(QWidget):
    def __init__(self, title, count):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(16)
        
        header = QHBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        count_lbl = QLabel(str(count))
        count_lbl.setStyleSheet("background: #E2E8F0; color: #64748B; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: 700;")
        
        header.addWidget(title_lbl)
        header.addWidget(count_lbl)
        header.addStretch()
        
        add_btn = QPushButton("+")
        add_btn.setFixedSize(24, 24)
        add_btn.setStyleSheet("background: transparent; color: #94A3B8; font-size: 18px; border: none;")
        header.addWidget(add_btn)
        
        self.layout.addLayout(header)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(2, 2, 2, 2)
        self.container_layout.setSpacing(12)
        self.container_layout.addStretch()
        
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

    def add_task(self, widget):
        self.container_layout.insertWidget(self.container_layout.count() - 1, widget)

class EnterpriseSearchWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(38)
        self.setMinimumWidth(240)
        self.setMaximumWidth(320)
        self.setObjectName("SearchWidget")
        self.setStyleSheet("""
            QFrame#SearchWidget {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QFrame#SearchWidget:hover {
                border: 1px solid #CBD5E1;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        
        self.icon = QLabel("🔍")
        self.icon.setStyleSheet("color: #94A3B8; font-size: 13px; border: none; background: transparent;")
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Search assignments...")
        self.input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                font-size: 13px;
                color: #0F172A;
                padding: 0;
            }
        """)
        # Override focus events to update parent style
        self.input.focusInEvent = self._on_focus_in
        self.input.focusOutEvent = self._on_focus_out
        
        layout.addWidget(self.icon)
        layout.addWidget(self.input, 1)

    def _on_focus_in(self, event):
        self.setStyleSheet("""
            QFrame#SearchWidget {
                background-color: #FFFFFF;
                border: 1.5px solid #38BDF8;
                border-radius: 12px;
            }
        """)
        QLineEdit.focusInEvent(self.input, event)

    def _on_focus_out(self, event):
        self.setStyleSheet("""
            QFrame#SearchWidget {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QFrame#SearchWidget:hover {
                border: 1px solid #CBD5E1;
            }
        """)
        QLineEdit.focusOutEvent(self.input, event)

class LearningPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("LearningPage")
        self.setStyleSheet(f"background-color: #F8FAFC;")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_top_toolbar()
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.content_container = QWidget()
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(24)
        
        self.left_area = QWidget()
        self.left_layout = QVBoxLayout(self.left_area)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(32)
        
        self._setup_kpi_section()
        self._setup_kanban_section()
        self._setup_calendar_section()
        
        self.content_layout.addWidget(self.left_area, stretch=1)
        
        # Right Productivity Panel (Collapsible)
        self.right_content = QWidget()
        self.right_content.setFixedWidth(320)
        self.right_layout = QVBoxLayout(self.right_content)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(24)
        
        self._setup_right_panel()
        
        self.right_panel = CollapsiblePanel(self.right_content, orientation="right")
        self.content_layout.addWidget(self.right_panel)
        
        self.scroll.setWidget(self.content_container)
        self.main_layout.addWidget(self.scroll)

    def _setup_top_toolbar(self):
        toolbar = QFrame()
        toolbar.setFixedHeight(84)
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E2E8F0;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(15, 23, 42, 10))
        shadow.setOffset(0, 2)
        toolbar.setGraphicsEffect(shadow)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)
        
        # Sidebar Toggle (Prominent & Always Visible)
        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setFixedSize(40, 40)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #000000;
                border-radius: 12px;
                font-size: 19px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(15, 23, 42, 0.08);
            }
            QPushButton:pressed {
                background-color: rgba(15, 23, 42, 0.14);
            }
        """)
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(10)
        btn_shadow.setColor(QColor(15, 23, 42, 15))
        btn_shadow.setOffset(0, 2)
        self.btn_toggle.setGraphicsEffect(btn_shadow)
        
        if self.controller and hasattr(self.controller, 'sidebar'):
             self.btn_toggle.clicked.connect(self.controller.sidebar.toggle_collapse)
        layout.addWidget(self.btn_toggle)

        # 1. Left Area: Breadcrumb & Title
        left_container = QVBoxLayout()
        left_container.setSpacing(1)
        left_container.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        bread = QLabel("STUDY TASKS / PLANNING")
        bread.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")
        
        self.main_title = QLabel("Fall Semester 2024")
        self.main_title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 800; letter-spacing: -0.4px;")
        
        subtitle = QLabel("Track and manage assignments efficiently")
        subtitle.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 500;")
        
        left_container.addWidget(bread)
        left_container.addWidget(self.main_title)
        left_container.addWidget(subtitle)
        layout.addLayout(left_container)
        
        layout.addStretch()
        
        # 2. Right Area: Search & Actions
        right_container = QHBoxLayout()
        right_container.setSpacing(12)
        right_container.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.search_bar = EnterpriseSearchWidget()
        right_container.addWidget(self.search_bar)
        
        # Quick Actions
        ai_btn = QPushButton("✨ AI Plan")
        ai_btn.setFixedSize(100, 38)
        ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ai_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F9FF;
                color: #0284C7;
                border: 1px solid #BAE6FD;
                border-radius: 12px;
                font-weight: 700;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #BAE6FD; }
        """)
        right_container.addWidget(ai_btn)
        
        add_btn = QPushButton("+ Add Task")
        add_btn.setFixedSize(110, 38)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0F172A;
                color: #FFFFFF;
                border-radius: 12px;
                font-weight: 700;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        right_container.addWidget(add_btn)
        
        layout.addLayout(right_container)
        self.main_layout.addWidget(toolbar)

    def _setup_kpi_section(self):
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)
        
        kpi_grid.addWidget(KPICard("Pending Assignments", "12", "4 due this week", progress=0.65, color="#38BDF8"), 0, 0)
        kpi_grid.addWidget(KPICard("Completed Tasks", "48", "+12% from last month", progress=0.85, color="#2DD4BF"), 0, 1)
        kpi_grid.addWidget(KPICard("Upcoming Exams", "3", "Next: Discrete Math", icon="🎯", color="#F59E0B"), 0, 2)
        kpi_grid.addWidget(KPICard("Study Productivity", "92%", "Excellent focus score", progress=0.92, color="#8B5CF6"), 0, 3)
        
        self.left_layout.addLayout(kpi_grid)

    def _setup_kanban_section(self):
        kanban_widget = QWidget()
        k_layout = QVBoxLayout(kanban_widget)
        k_layout.setContentsMargins(0, 0, 0, 0)
        k_layout.setSpacing(20)
        
        header = QHBoxLayout()
        title = QLabel("Study Tasks Board")
        title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()
        
        for btn_text in ["Filter", "Sort", "List View"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("background: #FFFFFF; color: #64748B; border: 1px solid #E2E8F0; border-radius: 8px; padding: 6px 12px; font-size: 12px; font-weight: 600;")
            header.addWidget(btn)
        
        k_layout.addLayout(header)
        
        board_layout = QHBoxLayout()
        board_layout.setSpacing(20)
        
        self.col_todo = KanbanColumn("Todo", 5)
        self.col_todo.add_task(TaskCard("Lab Report: Neural Networks", "AI-101", "Oct 12", "High", 0, "Needs 2h focus"))
        self.col_todo.add_task(TaskCard("Read Chapter 4: Calculus", "MATH-202", "Oct 15", "Low"))
        
        self.col_progress = KanbanColumn("In Progress", 2)
        self.col_progress.add_task(TaskCard("Design System Project", "UX-302", "Oct 10", "Urgent", 65, "Priority for today"))
        
        self.col_review = KanbanColumn("Review", 1)
        self.col_review.add_task(TaskCard("Python Scripting HW", "CS-50", "Tomorrow", "Med", 90))
        
        self.col_done = KanbanColumn("Completed", 12)
        self.col_done.add_task(TaskCard("Midterm Reflection", "EDU-10", "Completed", "Low", 100))
        
        board_layout.addWidget(self.col_todo)
        board_layout.addWidget(self.col_progress)
        board_layout.addWidget(self.col_review)
        board_layout.addWidget(self.col_done)
        
        k_layout.addLayout(board_layout)
        self.left_layout.addWidget(kanban_widget)

    def _setup_calendar_section(self):
        cal_widget = QWidget()
        c_layout = QHBoxLayout(cal_widget)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(24)
        
        cal_card = ModernCard()
        cal_card.layout.setSpacing(20)
        
        header = QHBoxLayout()
        header.addWidget(QLabel("October 2024"))
        header.itemAt(0).widget().setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        header.addStretch()
        header.addWidget(QPushButton("<"))
        header.addWidget(QPushButton(">"))
        cal_card.layout.addLayout(header)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            lbl = QLabel(d)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 700;")
            grid.addWidget(lbl, 0, i)
            
        for day in range(1, 32):
            lbl = QLabel(str(day))
            lbl.setFixedSize(36, 36)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if day == 10: # Current day
                lbl.setStyleSheet(f"background: {COLOR_PRIMARY}; color: white; border-radius: 18px; font-weight: 700;")
            elif day in [12, 15, 20]: # Deadline days
                lbl.setStyleSheet("background: #F1F5F9; color: #0F172A; border-radius: 18px; border: 1px solid #38BDF8; font-weight: 700;")
            else:
                lbl.setStyleSheet("color: #475569; font-size: 13px; font-weight: 500;")
            grid.addWidget(lbl, (day-1)//7 + 1, (day-1)%7)
            
        cal_card.layout.addLayout(grid)
        c_layout.addWidget(cal_card, stretch=2)
        
        dl_panel = ModernCard()
        dl_panel.layout.setSpacing(16)
        
        dl_title = QLabel("Upcoming Deadlines")
        dl_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        dl_panel.layout.addWidget(dl_title)
        
        for icon, title, time, color in [
            ("🔴", "UX Project Final", "In 4 hours", "#EF4444"),
            ("🟠", "AI Ethics Essay", "Tomorrow, 11:59 PM", "#F59E0B"),
            ("🔵", "Math Quiz", "Friday, 10:00 AM", "#3B82F6"),
        ]:
            item = QWidget()
            i_layout = QHBoxLayout(item)
            i_layout.setContentsMargins(0, 0, 0, 0)
            
            indicator = QLabel(icon)
            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600;")
            time_lbl = QLabel(time)
            time_lbl.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 500;")
            text_layout.addWidget(t_lbl)
            text_layout.addWidget(time_lbl)
            
            i_layout.addWidget(indicator)
            i_layout.addLayout(text_layout)
            i_layout.addStretch()
            dl_panel.layout.addWidget(item)
            
        c_layout.addWidget(dl_panel, stretch=1)
        self.left_layout.addWidget(cal_widget)

    def _setup_right_panel(self):
        ai_card = ModernCard(border_color="#8B5CF6")
        ai_card.setStyleSheet(ai_card.styleSheet() + "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F5F3FF, stop:1 #FFFFFF);")
        
        ai_header = QHBoxLayout()
        ai_icon = QLabel("🤖")
        ai_icon.setStyleSheet("font-size: 24px;")
        ai_title = QLabel("AI Assistant")
        ai_title.setStyleSheet("color: #5B21B6; font-size: 16px; font-weight: 700;")
        ai_header.addWidget(ai_icon)
        ai_header.addWidget(ai_title)
        ai_header.addStretch()
        ai_card.layout.addLayout(ai_header)
        
        tip = QLabel("“You've been studying for 3 hours. Take a 15-minute break to avoid burnout.”")
        tip.setWordWrap(True)
        tip.setStyleSheet("color: #6D28D9; font-size: 13px; font-weight: 500; font-style: italic;")
        ai_card.layout.addWidget(tip)
        
        suggest_btn = QPushButton("Generate Study Plan")
        suggest_btn.setStyleSheet("background: #8B5CF6; color: white; border-radius: 8px; padding: 10px; font-weight: 700; font-size: 12px; border: none;")
        ai_card.layout.addWidget(suggest_btn)
        
        self.right_layout.addWidget(ai_card)
        
        activity_card = ModernCard()
        activity_card.layout.setSpacing(16)
        
        act_title = QLabel("Recent Activity")
        act_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        activity_card.layout.addWidget(act_title)
        
        activities = [
            ("✅", "Completed 'SQL Basics'", "2h ago"),
            ("📝", "Added 'Thesis Draft'", "5h ago"),
            ("📅", "Rescheduled 'Meeting'", "Yesterday"),
        ]
        
        for icon, text, time in activities:
            item = QHBoxLayout()
            ico = QLabel(icon)
            info = QVBoxLayout()
            info.setSpacing(2)
            t = QLabel(text)
            t.setStyleSheet("color: #475569; font-size: 13px; font-weight: 600;")
            tm = QLabel(time)
            tm.setStyleSheet("color: #94A3B8; font-size: 11px;")
            info.addWidget(t)
            info.addWidget(tm)
            item.addWidget(ico)
            item.addLayout(info)
            item.addStretch()
            activity_card.layout.addLayout(item)
            
        self.right_layout.addWidget(activity_card)
        
        note_card = ModernCard()
        note_card.setStyleSheet(note_card.styleSheet() + "background: #FEF9C3; border: 1px solid #FDE68A;")
        note_card.layout.setSpacing(10)
        
        note_title = QLabel("📌 Quick Notes")
        note_title.setStyleSheet("color: #854D0E; font-size: 15px; font-weight: 700;")
        note_card.layout.addWidget(note_title)
        
        note_edit = QLineEdit()
        note_edit.setPlaceholderText("Type a quick note...")
        note_edit.setStyleSheet("background: transparent; border: none; color: #713F12; font-size: 13px;")
        note_card.layout.addWidget(note_edit)
        
        mock_note = QLabel("- Don't forget to email Prof. Smith\n- Research Paper deadline is approaching!")
        mock_note.setStyleSheet("color: #713F12; font-size: 13px; line-height: 150%;")
        note_card.layout.addWidget(mock_note)
        
        self.right_layout.addWidget(note_card)
        self.right_layout.addStretch()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LearningPage()
    window.resize(1300, 850)
    window.show()
    sys.exit(app.exec())
