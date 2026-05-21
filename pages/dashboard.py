import json
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QProgressBar, QFrame, QScrollArea, 
                             QGraphicsDropShadowEffect, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QCursor, QFont
from config import COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB, COLOR_BORDER
from components import SaaSCard, StatusPulse, CollapsiblePanel
from database import crud
from i18n import _
from .dashboard_analytics.dashboard_analytics_overview import DashboardAnalyticsOverview
from .dashboard_operations.workspace_activity_operations_center import WorkspaceActivityOperationsCenter

def create_shadow():
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(6)
    shadow.setColor(QColor(15, 23, 42, 12))
    return shadow

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """)
        self.setGraphicsEffect(create_shadow())
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)

class IconButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(36, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F1F5F9;
            }
        """)

class SearchBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 36)
        self.setStyleSheet("background: #F1F5F9; border-radius: 10px; border: none;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)
        
        icon = QLabel("🔍")
        icon.setStyleSheet("color: #64748B; font-size: 12px;")
        layout.addWidget(icon)
        
        self.input = QLabel("Search workspace...")
        self.input.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500;")
        layout.addWidget(self.input)
        layout.addStretch()

class KPICard(ModernCard):
    def __init__(self, title, value, change, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.internal_layout.setSpacing(4)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase;")
        self.internal_layout.addWidget(lbl_title)
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 800;")
        self.internal_layout.addWidget(lbl_val)
        
        lbl_change = QLabel(change)
        lbl_change.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 600;")
        self.internal_layout.addWidget(lbl_change)
        self.internal_layout.addStretch()

class DashboardOverviewView(QWidget):
    """The original dashboard content, now fully dynamic based on AI status."""
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # Master layout (QHBoxLayout)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Left Workspace Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        
        # Central Stacked Workspace (Switching between EMPTY, PENDING, COMPLETED, FAILED states)
        self.central_stack = QStackedWidget()
        
        # State Widgets
        self.empty_widget = QWidget()
        self.pending_widget = QWidget()
        self.completed_widget = QWidget()
        self.failed_widget = QWidget()
        
        self.central_stack.addWidget(self.empty_widget)      # Index 0
        self.central_stack.addWidget(self.pending_widget)    # Index 1
        self.central_stack.addWidget(self.completed_widget)  # Index 2
        self.central_stack.addWidget(self.failed_widget)     # Index 3
        
        self.scroll_area.setWidget(self.central_stack)
        layout.addWidget(self.scroll_area, stretch=1)
        
        # Right Assistant Panel (Collapsible)
        self.right_content = self._build_right_panel()
        self.right_content.setFixedWidth(320)
        self.right_panel = CollapsiblePanel(self.right_content, orientation="right")
        layout.addWidget(self.right_panel)
        
        self.poll_worker = None
        self.gen_worker = None
        
        # Initial load
        self.refresh()

    def refresh(self):
        """Reloads the dashboard overview state from SQLite."""
        student = crud.get_current_student()
        if not student:
            self.central_stack.setCurrentIndex(0)
            self._populate_empty_view(None)
            return
            
        context = student.get("context", {})
        status = context.get("ai_status", "EMPTY")
        
        if status == "EMPTY":
            self._populate_empty_view(student)
            self.central_stack.setCurrentIndex(0)
        elif status == "PENDING":
            if self.central_stack.currentIndex() != 1:
                self._populate_pending_view()
                self.central_stack.setCurrentIndex(1)
            if not self.poll_worker or not self.poll_worker.isRunning():
                self.start_polling()
        elif status == "COMPLETED":
            self._populate_completed_view(student)
            self.central_stack.setCurrentIndex(2)
        elif status == "FAILED":
            self._populate_failed_view(student)
            self.central_stack.setCurrentIndex(3)

    def _clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())

    # --- STATE POPULATION METHODS ---

    def _populate_empty_view(self, student):
        self._clear_layout(self.empty_widget.layout())
        
        layout = QVBoxLayout(self.empty_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Check if they have set up any context profile
        has_raw_input = False
        if student and student.get("context"):
            raw_input = student["context"].get("raw_input")
            if raw_input and isinstance(raw_input, dict) and len(raw_input) > 0:
                has_raw_input = True
                
        # Banner
        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setStyleSheet("""
            #BannerFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E293B, stop:1 #0F172A);
                border-radius: 16px;
            }
        """)
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(32, 32, 32, 32)
        
        text_layout = QVBoxLayout()
        greeting = QLabel("Welcome to your Academic Portal")
        greeting.setStyleSheet("color: white; font-size: 24px; font-weight: 800;")
        desc = QLabel("Let the AI analyze your strengths, weaknesses, and courses to generate a personalized study roadmap and weekly task list.")
        desc.setStyleSheet("color: #94A3B8; font-size: 14px; margin-top: 8px;")
        desc.setWordWrap(True)
        text_layout.addWidget(greeting)
        text_layout.addWidget(desc)
        banner_layout.addLayout(text_layout, 1)
        
        emoji = QLabel("✨")
        emoji.setStyleSheet("font-size: 48px; background: transparent;")
        banner_layout.addWidget(emoji)
        layout.addWidget(banner)
        
        # Big prompt card
        prompt_card = ModernCard()
        pc_layout = prompt_card.internal_layout
        pc_layout.setSpacing(16)
        
        prompt_title = QLabel("Ready to generate your study plan?")
        prompt_title.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        pc_layout.addWidget(prompt_title)
        
        if has_raw_input:
            prompt_desc = QLabel("You have successfully set up your profile context! Click the button below to sync with the server and start plan generation.")
            prompt_desc.setStyleSheet("color: #475569; font-size: 14px;")
            prompt_desc.setWordWrap(True)
            pc_layout.addWidget(prompt_desc)
            
            btn_gen = QPushButton("✨ Generate Academic Plan")
            btn_gen.setFixedHeight(44)
            btn_gen.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_gen.setStyleSheet("background: #38BDF8; color: white; font-weight: 700; font-size: 14px; border-radius: 10px;")
            btn_gen.clicked.connect(self.start_generation)
            pc_layout.addWidget(btn_gen)
        else:
            prompt_desc = QLabel("You need to complete your academic profile details first (Display Name, University, Major, courses, skills, and goals) so the AI has context to work with.")
            prompt_desc.setStyleSheet("color: #EF4444; font-size: 14px; font-weight: 600;")
            prompt_desc.setWordWrap(True)
            pc_layout.addWidget(prompt_desc)
            
            btn_profile = QPushButton("👉 Complete Academic Profile")
            btn_profile.setFixedHeight(44)
            btn_profile.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_profile.setStyleSheet("background: #0F172A; color: white; font-weight: 700; font-size: 14px; border-radius: 10px;")
            btn_profile.clicked.connect(self._go_to_profile)
            pc_layout.addWidget(btn_profile)
            
        layout.addWidget(prompt_card)
        layout.addStretch()

    def _populate_pending_view(self):
        self._clear_layout(self.pending_widget.layout())
        
        layout = QVBoxLayout(self.pending_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        pending_card = ModernCard()
        pc_layout = pending_card.internal_layout
        pc_layout.setContentsMargins(40, 40, 40, 40)
        pc_layout.setSpacing(20)
        pc_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        loader_lbl = QLabel("⏳")
        loader_lbl.setStyleSheet("font-size: 64px;")
        loader_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_lbl = QLabel("AI is generating your academic plan...")
        title_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 800;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        desc_lbl = QLabel("Our AI engine is currently analyzing your inputs and drafting a weekly study scheduler and milestones roadmap. This may take a few minutes.\nGeneration is still running locally. You can leave this page and polling will resume.")
        desc_lbl.setStyleSheet("color: #64748B; font-size: 14px; line-height: 1.5;")
        desc_lbl.setWordWrap(True)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        progress = QProgressBar()
        progress.setRange(0, 0)  # Indeterminate
        progress.setFixedHeight(8)
        progress.setStyleSheet("QProgressBar { background: #F1F5F9; border-radius: 4px; } QProgressBar::chunk { background: #38BDF8; border-radius: 4px; }")
        
        btn_refresh = QPushButton("🔄 Refresh Status Now")
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setFixedHeight(36)
        btn_refresh.setFixedWidth(180)
        btn_refresh.setStyleSheet("background: #0284C7; color: white; font-weight: 700; font-size: 13px; border-radius: 8px; border: none;")
        btn_refresh.clicked.connect(self.start_polling)
        
        pc_layout.addWidget(loader_lbl)
        pc_layout.addWidget(title_lbl)
        pc_layout.addWidget(desc_lbl)
        pc_layout.addWidget(progress)
        pc_layout.addWidget(btn_refresh, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(pending_card)
        layout.addStretch()

    def _populate_completed_view(self, student):
        self._clear_layout(self.completed_widget.layout())
        
        layout = QVBoxLayout(self.completed_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        context = student.get("context", {})
        ai_plan = context.get("ai_plan") or {}
        
        # 1. Welcome banner
        banner = QFrame()
        banner.setObjectName("BannerFrame")
        banner.setStyleSheet("""
            #BannerFrame {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0F172A, stop:0.6 #1E293B, stop:1 #0284C7);
                border-radius: 16px;
            }
        """)
        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(32, 24, 32, 24)
        
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)
        
        first_name = student.get("display_name") or student.get("username") or "Student"
        greeting = QLabel(f"Good Morning, {first_name}.")
        greeting.setStyleSheet("color: white; font-size: 26px; font-weight: 800; letter-spacing: -1px; background: transparent;")
        
        summary_text = ai_plan.get("student_summary") or "Your academic plan is ready."
        summary = QLabel(summary_text)
        summary.setStyleSheet("color: #94A3B8; font-size: 14px; margin-top: 6px; margin-bottom: 20px; background: transparent;")
        summary.setWordWrap(True)
        left_layout.addWidget(greeting)
        left_layout.addWidget(summary)
        
        actions = QHBoxLayout()
        actions.setSpacing(10)
        
        btn_regen = QPushButton("✨ Regenerate AI Plan")
        btn_regen.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_regen.setFixedHeight(36)
        btn_regen.setStyleSheet("background: #38BDF8; color: #0F172A; font-weight: 700; font-size: 13px; border-radius: 18px; padding: 0 16px; border: none;")
        btn_regen.clicked.connect(self.start_generation)
        
        btn_profile = QPushButton("🗺️ Update Profile Context")
        btn_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_profile.setFixedHeight(36)
        btn_profile.setStyleSheet("background: rgba(255,255,255,0.1); color: white; font-weight: 600; font-size: 13px; border-radius: 18px; padding: 0 16px; border: 1px solid rgba(255,255,255,0.2);")
        btn_profile.clicked.connect(self._go_to_profile)
        
        actions.addWidget(btn_regen)
        actions.addWidget(btn_profile)
        actions.addStretch()
        
        ac_w = QWidget()
        ac_w.setLayout(actions)
        ac_w.setStyleSheet("background: transparent;")
        left_layout.addWidget(ac_w)
        
        b_layout.addLayout(left_layout, 1)
        
        rocket = QLabel("🚀")
        rocket.setStyleSheet("font-size: 56px; background: transparent;")
        b_layout.addWidget(rocket, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(banner)
        
        # 2. KPI row
        kpi_row = QWidget()
        kpi_layout = QHBoxLayout(kpi_row)
        kpi_layout.setContentsMargins(0, 0, 0, 0)
        kpi_layout.setSpacing(16)
        
        metrics = ai_plan.get("metrics") or {}
        ac_prog = metrics.get("academic_progress", 75)
        career_readiness = metrics.get("career_readiness", 80)
        task_load = metrics.get("task_load", 12)
        
        kpi_layout.addWidget(KPICard("Academic Progress", f"{ac_prog}%", "Based on roadmap", "#10B981"))
        kpi_layout.addWidget(KPICard("Weekly Task Load", f"{task_load} tasks", "Weekly study plan", "#F59E0B"))
        kpi_layout.addWidget(KPICard("Career Readiness", f"{career_readiness}%", "Skill matches", "#38BDF8"))
        
        layout.addWidget(kpi_row)
        
        # 3. Main content row (Roadmap timeline + Weekly Schedule)
        content_row = QWidget()
        cr_layout = QHBoxLayout(content_row)
        cr_layout.setContentsMargins(0, 0, 0, 0)
        cr_layout.setSpacing(20)
        
        # Left Panel: Timeline Milestones (Roadmap)
        roadmap_panel = ModernCard()
        rl = roadmap_panel.internal_layout
        rl.setSpacing(12)
        
        r_title = QLabel("AI Academic Roadmap")
        r_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        rl.addWidget(r_title)
        
        roadmap_list = ai_plan.get("academic_roadmap") or []
        for course in roadmap_list:
            card = ModernCard()
            card.internal_layout.setContentsMargins(12, 12, 12, 12)
            card.internal_layout.setSpacing(6)
            
            title = course.get("title", "Milestone")
            status = course.get("status", "not_started").replace("_", " ").title()
            progress = course.get("progress_pct", 0)
            ai_insight = course.get("ai_insight", "")
            
            color = "#10B981" if "completed" in status.lower() else ("#38BDF8" if "progress" in status.lower() else "#94A3B8")
            
            h_row = QHBoxLayout()
            badge = QLabel(status)
            badge.setStyleSheet(f"color: {color}; background: {color}15; font-size: 10px; font-weight: 700; padding: 3px 6px; border-radius: 4px;")
            h_row.addWidget(badge)
            h_row.addStretch()
            card.internal_layout.addLayout(h_row)
            
            lbl = QLabel(title)
            lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600;")
            card.internal_layout.addWidget(lbl)
            
            bar = QProgressBar()
            bar.setFixedHeight(4)
            bar.setValue(progress)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border: none; border-radius: 2px; }} QProgressBar::chunk {{ background: {color}; border-radius: 2px; }}")
            card.internal_layout.addWidget(bar)
            
            if ai_insight:
                ins = QLabel(ai_insight)
                ins.setWordWrap(True)
                ins.setStyleSheet("color: #64748B; font-size: 11px;")
                card.internal_layout.addWidget(ins)
                
            rl.addWidget(card)
            
        cr_layout.addWidget(roadmap_panel, stretch=1)
        
        # Right Panel: Tasks + Insights
        right_subpanel = QWidget()
        rs_layout = QVBoxLayout(right_subpanel)
        rs_layout.setContentsMargins(0, 0, 0, 0)
        rs_layout.setSpacing(20)
        
        # Tasks Card
        tasks_card = ModernCard()
        tl = tasks_card.internal_layout
        tl.setSpacing(10)
        
        t_header = QLabel("AI Recommended Tasks This Week")
        t_header.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        tl.addWidget(t_header)
        
        weekly_plan = ai_plan.get("weekly_study_plan") or []
        task_count = 0
        for day_plan in weekly_plan:
            day = day_plan.get("day", "Monday")
            tasks = day_plan.get("tasks", [])
            for t in tasks:
                if task_count >= 5:  # Cap display at 5 tasks for clean UI
                    break
                w = QWidget()
                l = QHBoxLayout(w)
                l.setContentsMargins(0, 0, 0, 0)
                l.setSpacing(8)
                
                chk = QFrame()
                chk.setFixedSize(14, 14)
                chk.setStyleSheet("border: 2px solid #CBD5E1; border-radius: 3px;")
                l.addWidget(chk)
                
                lbl = QLabel(f"{day}: {t.get('title')}")
                lbl.setStyleSheet("color: #334155; font-size: 12px; font-weight: 500;")
                lbl.setWordWrap(True)
                l.addWidget(lbl)
                l.addStretch()
                
                badge_type = t.get("type", "study").title()
                badge = QLabel(badge_type)
                badge.setStyleSheet("color: #38BDF8; background: #38BDF815; font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 4px;")
                l.addWidget(badge)
                
                tl.addWidget(w)
                task_count += 1
                
        rs_layout.addWidget(tasks_card)
        
        # Focus/Skills Card
        insights_card = ModernCard()
        il = insights_card.internal_layout
        
        i_title = QLabel("✨ Skills Analysis & Focus Areas")
        i_title.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        il.addWidget(i_title)
        
        skill_analysis = ai_plan.get("skill_analysis") or {}
        focus_areas = skill_analysis.get("recommended_focus", [])
        if focus_areas:
            ins_text = "To achieve your goals, focus on prioritizing these skills:\n" + "\n".join([f"• {f}" for f in focus_areas])
        else:
            ins_text = "Keep studying courses on your roadmap. AI advises maintaining high study hours."
            
        msg = QLabel(ins_text)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.4;")
        il.addWidget(msg)
        il.addStretch()
        
        rs_layout.addWidget(insights_card)
        cr_layout.addWidget(right_subpanel, stretch=1)
        
        layout.addWidget(content_row)

    def _populate_failed_view(self, student):
        self._clear_layout(self.failed_widget.layout())
        
        layout = QVBoxLayout(self.failed_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        context = student.get("context", {})
        err_msg = context.get("ai_last_error") or "Unknown error occurred on AI model server."
        
        # Red warning card
        error_card = QFrame()
        error_card.setStyleSheet("background-color: #FEF2F2; border: 1px solid #FCA5A5; border-radius: 12px;")
        el = QVBoxLayout(error_card)
        el.setContentsMargins(20, 20, 20, 20)
        el.setSpacing(8)
        
        title = QLabel("❌ AI Plan Generation Failed")
        title.setStyleSheet("color: #991B1B; font-size: 16px; font-weight: 700;")
        desc = QLabel(f"The backend server encountered an error while generating your plan: {err_msg}")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #7F1D1D; font-size: 13px;")
        
        btn_retry = QPushButton("🔄 Regenerate / Retry Generation")
        btn_retry.setFixedHeight(36)
        btn_retry.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_retry.setStyleSheet("background: #EF4444; color: white; font-weight: 700; font-size: 13px; border-radius: 8px; border: none;")
        btn_retry.clicked.connect(self.start_generation)
        
        el.addWidget(title)
        el.addWidget(desc)
        el.addWidget(btn_retry)
        layout.addWidget(error_card)
        
        # Render a static fallback dashboard layout beneath it to let user see *something*
        fallback_title = QLabel("Preview (Static Fallback Dashboard)")
        fallback_title.setStyleSheet("color: #64748B; font-size: 14px; font-weight: 700; margin-top: 10px;")
        layout.addWidget(fallback_title)
        
        # Mock/Static Dashboard
        kpi_row = QWidget()
        kpi_layout = QHBoxLayout(kpi_row)
        kpi_layout.setContentsMargins(0, 0, 0, 0)
        kpi_layout.setSpacing(16)
        kpi_layout.addWidget(KPICard("Academic Progress", "75%", "Mock data", "#10B981"))
        kpi_layout.addWidget(KPICard("Tasks Completed", "12", "Mock data", "#F59E0B"))
        kpi_layout.addWidget(KPICard("Career Readiness", "80%", "Mock data", "#38BDF8"))
        layout.addWidget(kpi_row)
        
        prompt_card = ModernCard()
        prompt_card.internal_layout.addWidget(QLabel("Why did this fail?", styleSheet="font-size: 15px; font-weight: 700; color: #0F172A;"))
        prompt_card.internal_layout.addWidget(QLabel("Common causes include backend Ollama service offline or student profile context contains empty fields. Please try updating your context in Profile page and retry.", styleSheet="font-size: 13px; color: #475569;"))
        layout.addWidget(prompt_card)
        
        layout.addStretch()

    # --- ACTION HANDLERS ---

    def _go_to_profile(self):
        main_win = self.window()
        if hasattr(main_win, "show_page"):
            main_win.show_page(11) # Index 11 is ProfilePage

    def start_generation(self):
        session = crud.get_session()
        if not session:
            QMessageBox.warning(self, "Authentication Required", "Please log in to generate an academic plan.")
            return

        token = session["access_token"]
        
        # Update local SQLite immediately to PENDING
        student = crud.get_current_student()
        if student:
            raw_input = student.get("context", {}).get("raw_input", {})
            is_dirty = student.get("context", {}).get("is_dirty", 0)
            crud.save_student_context(
                student_id=student["id"],
                raw_input_dict=raw_input,
                ai_status="PENDING",
                is_dirty=is_dirty
            )
        
        self.refresh()

        from modules.ai_worker import AIGenerateWorker
        self.gen_worker = AIGenerateWorker(token)
        self.gen_worker.success.connect(self._on_gen_success)
        self.gen_worker.error.connect(self._on_gen_error)
        self.gen_worker.start()

    def _on_gen_success(self, res):
        print("Dashboard: Generation triggered successfully on backend.")
        # Start polling
        self.start_polling()

    def _on_gen_error(self, err_msg):
        # Update status back to FAILED locally
        student = crud.get_current_student()
        if student:
            raw_input = student.get("context", {}).get("raw_input", {})
            crud.save_student_context(
                student_id=student["id"],
                raw_input_dict=raw_input,
                ai_status="FAILED",
                ai_last_error=err_msg,
                is_dirty=0
            )
        QMessageBox.critical(self, "Generation Failed", f"Could not trigger AI plan: {err_msg}")
        self.refresh()

    def start_polling(self):
        session = crud.get_session()
        if not session:
            return
        token = session["access_token"]
        
        if self.poll_worker and self.poll_worker.isRunning():
            self.poll_worker.stop()
            self.poll_worker.wait()

        from modules.ai_worker import AIPollWorker
        self.poll_worker = AIPollWorker(token)
        self.poll_worker.status_changed.connect(self._on_poll_status_changed)
        self.poll_worker.finished.connect(self._on_poll_finished)
        self.poll_worker.error.connect(self._on_poll_error)
        self.poll_worker.start()
        
        self.refresh()

    def _on_poll_status_changed(self, status):
        print(f"Dashboard: Polling status check: {status}")
        if status in ("COMPLETED", "FAILED"):
            # Polling is finished
            pass
        else:
            # PENDING or other
            if self.central_stack.currentIndex() != 1:
                self.refresh()

    def _on_poll_finished(self, updated_student):
        print("Dashboard: Poll worker finished. Reloading...")
        self.refresh()
        
        # Trigger profile page reload as well if it is loaded
        main_win = self.window()
        if hasattr(main_win, "pages_container"):
            profile_page = main_win.pages_container.widget(11)
            if profile_page and hasattr(profile_page, "refresh"):
                profile_page.refresh()

    def _on_poll_error(self, err_msg):
        print(f"Dashboard: Poll worker finished with error: {err_msg}")
        self.refresh()

    def _build_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: transparent; border: none;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # AI Assistant
        ai = ModernCard()
        al = ai.internal_layout
        al.setSpacing(12)
        h = QHBoxLayout()
        h.addWidget(StatusPulse(size=8, color="#8B5CF6"))
        t = QLabel("AI Mentor Insights")
        t.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        h.addWidget(t)
        h.addStretch()
        al.addLayout(h)
        
        msg = QLabel("Complete your academic roadmap and tasks to receive daily study tips and milestone recommendations here.")
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.4;")
        al.addWidget(msg)
        layout.addWidget(ai)
        
        # Notifications
        notif = ModernCard()
        nl = notif.internal_layout
        t2 = QLabel("Notifications")
        t2.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700;")
        nl.addWidget(t2)
        
        def add_n(t, time, icon="📌"):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 4, 0, 4)
            l.setSpacing(8)
            i = QLabel(icon)
            i.setStyleSheet("font-size: 14px; background: transparent;")
            l.addWidget(i)
            v = QVBoxLayout()
            v.setSpacing(1)
            txt = QLabel(t)
            txt.setStyleSheet("color: #334155; font-size: 12px; font-weight: 500;")
            txt.setWordWrap(True)
            v.addWidget(txt)
            tm = QLabel(time)
            tm.setStyleSheet("color: #94A3B8; font-size: 10px;")
            v.addWidget(tm)
            l.addLayout(v)
            nl.addWidget(w)
            
        add_n("Welcome to AI Career Bridge!", "Just now", "🎉")
        add_n("Please fill out your context profile.", "10 min ago", "📝")
        layout.addWidget(notif)
        layout.addStretch()
        return panel

class DashboardPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # 1. Top Toolbar (Header)
        self.header = self._build_header()
        root_layout.addWidget(self.header)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #E2E8F0; max-height: 1px; border: none;")
        root_layout.addWidget(line)
        
        # 2. Main Stacked Workspace
        self.view_stack = QStackedWidget()
        
        # View 0: Standard Overview
        self.overview_view = DashboardOverviewView(controller=self.controller)
        self.view_stack.addWidget(self.overview_view)
        
        # View 1: Analytics Overview
        self.analytics_view = DashboardAnalyticsOverview(controller=self.controller)
        self.view_stack.addWidget(self.analytics_view)
        
        # View 2: Workspace Activity & Live Ops
        self.activity_view = WorkspaceActivityOperationsCenter(controller=self.controller)
        self.view_stack.addWidget(self.activity_view)
        
        root_layout.addWidget(self.view_stack)

    def refresh(self):
        """Called automatically on page switch."""
        if hasattr(self, "overview_view") and hasattr(self.overview_view, "refresh"):
            self.overview_view.refresh()

    def _build_header(self):
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)
        
        # Sidebar Toggle
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

        # Logo/Title
        title_lbl = QLabel("Dashboard")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A;")
        layout.addWidget(title_lbl)
        
        # Tab Switcher
        tab_container = QFrame()
        tab_container.setStyleSheet("background: #F1F5F9; border-radius: 12px; padding: 2px;")
        tl = QHBoxLayout(tab_container)
        tl.setContentsMargins(2, 2, 2, 2)
        tl.setSpacing(4)
        
        self.btn_overview = QPushButton("Overview")
        self.btn_analytics = QPushButton("Analytics")
        self.btn_activity = QPushButton("Activity")
        
        tab_style = """
            QPushButton {
                border: none; border-radius: 10px; padding: 8px 16px;
                font-size: 13px; font-weight: 700; color: #64748B;
            }
            QPushButton:checked {
                background: white; color: #0F172A;
            }
        """
        self.btn_overview.setStyleSheet(tab_style)
        self.btn_overview.setCheckable(True)
        self.btn_overview.setChecked(True)
        self.btn_analytics.setStyleSheet(tab_style)
        self.btn_analytics.setCheckable(True)
        self.btn_activity.setStyleSheet(tab_style)
        self.btn_activity.setCheckable(True)
        
        self.btn_overview.clicked.connect(lambda: self._set_view(0))
        self.btn_analytics.clicked.connect(lambda: self._set_view(1))
        self.btn_activity.clicked.connect(lambda: self._set_view(2))
        
        tl.addWidget(self.btn_overview)
        tl.addWidget(self.btn_analytics)
        tl.addWidget(self.btn_activity)
        layout.addWidget(tab_container)
        
        layout.addStretch()
        
        # Search
        layout.addWidget(SearchBar())
        
        # Icons
        layout.addWidget(IconButton("📅"))
        layout.addWidget(IconButton("🔔"))
        
        avatar_btn = IconButton("KH")
        avatar_btn.setStyleSheet("QPushButton { background-color: #2DD4BF; color: white; border: none; border-radius: 18px; font-weight: 800; }")
        layout.addWidget(avatar_btn)
        
        return header

    def _set_view(self, idx):
        self.view_stack.setCurrentIndex(idx)
        self.btn_overview.setChecked(idx == 0)
        self.btn_analytics.setChecked(idx == 1)
        self.btn_activity.setChecked(idx == 2)
