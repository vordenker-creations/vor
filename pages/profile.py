import customtkinter as ctk
import tkinter as tk
from config import *
from components import SaaSCard, AnimatedCircularProgress, AnimationEngine, CountUpLabel
import i18n
from i18n import _

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Header Title
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(35, 10))
        self.title_label = ctk.CTkLabel(header_frame, text=_("prof_title"), 
                                        font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), 
                                        text_color=COLOR_TEXT_MAIN)
        self.title_label.pack(side="left")

        # Tabs Navigation
        self.tab_nav = ctk.CTkFrame(self, fg_color="transparent", height=45)
        self.tab_nav.pack(fill="x", padx=35, pady=(0, 15))
        
        self.tab_buttons = {}
        tabs = [
            ("OVERVIEW", _("prof_tab_overview"), self.show_overview),
            ("CV ANALYSIS", _("prof_tab_cv_analysis"), self.show_cv_analysis),
            ("CV BUILDER", _("prof_tab_cv_builder"), self.show_cv_builder)
        ]

        for key, text, command in tabs:
            btn = ctk.CTkButton(self.tab_nav, text=text, fg_color="transparent", text_color=COLOR_TEXT_SUB,
                                font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"),
                                width=120, height=35, hover_color=COLOR_BG_CARD, corner_radius=6,
                                command=command)
            btn.pack(side="left", padx=(0, 10))
            self.tab_buttons[key] = btn

        # Main Content Container (Scrollable)
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=15, pady=5)

        self.show_overview()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        for btn in self.tab_buttons.values():
            btn.configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)

    def set_active_tab(self, tab_key):
        self.tab_buttons[tab_key].configure(fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY)
        titles = {
            "OVERVIEW": _("prof_title"),
            "CV ANALYSIS": _("prof_sub_analysis"),
            "CV BUILDER": _("prof_sub_builder")
        }
        self.title_label.configure(text=titles[tab_key])

    def show_overview(self):
        self.clear_container()
        self.set_active_tab("OVERVIEW")
        
        card = SaaSCard(self.container, border_color=COLOR_PRIMARY_LIGHT, border_width=1)
        card.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Avatar with glowing border
        avatar_frame = ctk.CTkFrame(card, fg_color="transparent", width=200, height=200)
        avatar_frame.pack(pady=(50, 20))
        avatar_frame.pack_propagate(False)
        
        cvs = tk.Canvas(avatar_frame, width=180, height=180, bg=get_color(COLOR_BG_CARD), highlightthickness=0)
        cvs.place(relx=0.5, rely=0.5, anchor="center")
        # Gold/Cyan glowing rings
        cvs.create_oval(10, 10, 170, 170, outline=get_color(COLOR_PRIMARY), width=2)
        cvs.create_oval(18, 18, 162, 162, outline="#FBBF24", width=4) # Gold inner ring
        
        ctk.CTkLabel(avatar_frame, text="👤", font=ctk.CTkFont(size=80), text_color=COLOR_PRIMARY).place(relx=0.5, rely=0.5, anchor="center")
        
        # Info
        ctk.CTkLabel(card, text="KHANG NGUYEN HOANG DANG", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack()
        ctk.CTkLabel(card, text=_("prof_student_info"), font=ctk.CTkFont(size=14), text_color=COLOR_TEXT_SUB).pack(pady=(5, 15))
        
        btn = ctk.CTkButton(card, text=_("prof_active_path"), fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, corner_radius=15, height=30, hover=False)
        btn.pack(pady=5)
        
        bio = "Aspiring AI engineer with a strong foundation in Python and a passion for deep learning.\nDedicated to developing innovative solutions and mastering modern AI techniques."
        ctk.CTkLabel(card, text=bio, font=ctk.CTkFont(size=13), text_color=COLOR_TEXT_MAIN, justify="center").pack(pady=(20, 50), padx=50)

    def show_cv_analysis(self):
        self.clear_container()
        self.set_active_tab("CV ANALYSIS")
        
        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=15)
        grid.grid_columnconfigure((0, 1), weight=1)
        grid.grid_rowconfigure(0, weight=1)

        # Left Col: My Resumes
        left_card = SaaSCard(grid)
        left_card.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        header_left = ctk.CTkFrame(left_card, fg_color="transparent")
        header_left.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header_left, text=_("prof_my_resumes"), font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        btn_frame = ctk.CTkFrame(left_card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkButton(btn_frame, text=_("prof_create_resume"), fg_color=COLOR_PRIMARY, text_color="#000000", font=ctk.CTkFont(weight="bold")).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text=_("prof_upload_resume"), fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(side="left", fill="x", expand=True, padx=(5, 0))

        resumes = [
            ("📄", "Core Resume - Applied AI", _("prof_create_resume")),
            ("📄", "General CV - Software Engineering", _("prof_view_resume", "View CV"))
        ]
        for i, (icon, title, sub) in enumerate(resumes):
            item = ctk.CTkFrame(left_card, fg_color="transparent")
            AnimationEngine.fade_in_widget(item, delay_ms=i*150)
            
            icon_box = ctk.CTkFrame(item, fg_color=COLOR_BG_APP, corner_radius=6, width=40, height=40)
            icon_box.pack(side="left", padx=(0, 15))
            icon_box.pack_propagate(False)
            ctk.CTkLabel(icon_box, text=icon, font=ctk.CTkFont(size=20)).place(relx=0.5, rely=0.5, anchor="center")
            
            txt = ctk.CTkFrame(item, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(txt, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
            ctk.CTkLabel(txt, text=sub, font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_SUB).pack(anchor="w")
            ctk.CTkLabel(item, text=">", font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_TEXT_SUB).pack(side="right")
            
            ctk.CTkFrame(left_card, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=20, pady=(5,0))

        # Right Col: AI Feedback
        right_card = SaaSCard(grid, border_color=COLOR_SUCCESS, border_width=1)
        right_card.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        header_right = ctk.CTkFrame(right_card, fg_color="transparent")
        header_right.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header_right, text=_("prof_ai_feedback"), font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkLabel(header_right, text="⋮", font=ctk.CTkFont(size=18)).pack(side="right")
        
        match_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        match_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(match_frame, text=_("prof_job_match"), font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", pady=(0,10))
        
        ring_box = ctk.CTkFrame(match_frame, fg_color="transparent")
        ring_box.pack(fill="x")
        
        # Use new AnimatedCircularProgress
        ring = AnimatedCircularProgress(ring_box, size=120)
        ring.pack(side="left", padx=(0, 20))
        # Trigger animation after a slight delay
        self.after(300, lambda: ring.set_target(0.92))
        
        # Network graph placeholder
        net = ctk.CTkFrame(ring_box, fg_color="transparent", height=120)
        net.pack(side="right", fill="both", expand=True)
        net.pack_propagate(False)
        cvs_net = tk.Canvas(net, width=150, height=120, bg=get_color(COLOR_BG_CARD), highlightthickness=0)
        cvs_net.pack(fill="both", expand=True)
        cx, cy = 75, 60
        cvs_net.create_line(cx, cy, cx-40, cy-30, fill=get_color(COLOR_SUCCESS))
        cvs_net.create_line(cx, cy, cx+40, cy-30, fill=get_color(COLOR_SUCCESS))
        cvs_net.create_line(cx, cy, cx, cy+40, fill=get_color(COLOR_PRIMARY))
        
        cvs_net.create_oval(cx-15, cy-15, cx+15, cy+15, fill=get_color(COLOR_BG_APP), outline=get_color(COLOR_SUCCESS), width=2)
        cvs_net.create_text(cx, cy, text="85", fill=get_color(COLOR_TEXT_MAIN), font=("Segoe UI", 10, "bold"))
        for x, y, c in [(cx-40, cy-30, COLOR_SUCCESS), (cx+40, cy-30, COLOR_SUCCESS), (cx, cy+40, COLOR_PRIMARY)]:
            cvs_net.create_oval(x-12, y-10, x+12, y+10, fill=get_color(COLOR_BG_CARD), outline=get_color(c), width=1)
            cvs_net.create_text(x, y, text="JOB", fill=get_color(COLOR_TEXT_SUB), font=("Segoe UI", 6))

        
        ctk.CTkLabel(right_card, text=_("prof_ai_sug"), font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        
        def add_suggestion(parent, title, text, color, delay=0):
            box = ctk.CTkFrame(parent, fg_color="transparent")
            AnimationEngine.fade_in_widget(box, delay_ms=delay)
            ctk.CTkFrame(box, width=3, fg_color=color).pack(side="left", fill="y")
            txt_box = ctk.CTkFrame(box, fg_color="transparent")
            txt_box.pack(side="left", fill="x", expand=True, padx=10)
            ctk.CTkLabel(txt_box, text=f"{title}: {text}", justify="left", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=12), wraplength=250).pack(anchor="w")

        add_suggestion(right_card, "SUGGESTION" if i18n.CURRENT_LANG=="en" else "GỢI Ý", _("prof_sug_1"), COLOR_SUCCESS, delay=400)
        add_suggestion(right_card, "IMPROVEMENT" if i18n.CURRENT_LANG=="en" else "CẢI THIỆN", _("prof_sug_2"), COLOR_WARNING, delay=550)
        
        btn_box = ctk.CTkFrame(right_card, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(25, 20))
        ctk.CTkButton(btn_box, text=_("prof_btn_cover"), fg_color=COLOR_PRIMARY, text_color="#000000", font=ctk.CTkFont(weight="bold"), height=35).pack(fill="x", pady=5)
        ctk.CTkButton(btn_box, text=_("prof_btn_interview"), fg_color=COLOR_PRIMARY, text_color="#000000", font=ctk.CTkFont(weight="bold"), height=35).pack(fill="x", pady=5)

    def show_cv_builder(self):
        self.clear_container()
        self.set_active_tab("CV BUILDER")
        
        grid = ctk.CTkFrame(self.container, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=15)
        grid.grid_columnconfigure(0, weight=6)
        grid.grid_columnconfigure(1, weight=4)
        grid.grid_rowconfigure(0, weight=1)
        
        # Left: Form
        form = SaaSCard(grid)
        form.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(form, text=_("prof_auto_fill"), font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=20)
        
        # Form Fields
        ctk.CTkLabel(form, text=_("prof_edu"), font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=20, pady=(10, 5))
        for p in ["University Name", "Major/Focus", "Current GPA"]:
            entry = ctk.CTkEntry(form, height=35, fg_color=COLOR_BG_APP, border_color=COLOR_BORDER, corner_radius=6, text_color=COLOR_TEXT_MAIN, placeholder_text=p)
            entry.pack(fill="x", padx=20, pady=5)
            
        ctk.CTkLabel(form, text="CONTACT", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=20, pady=(15, 5))
        for p in ["Email Address", "Location"]:
            entry = ctk.CTkEntry(form, height=35, fg_color=COLOR_BG_APP, border_color=COLOR_BORDER, corner_radius=6, text_color=COLOR_TEXT_MAIN, placeholder_text=p)
            entry.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(form, text=_("prof_exp"), font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=20, pady=(15, 5))
        ex = ctk.CTkEntry(form, height=35, fg_color=COLOR_BG_APP, border_color=COLOR_BORDER, corner_radius=6, text_color=COLOR_TEXT_MAIN, placeholder_text="Enter your work experience...")
        ex.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(form, text=_("prof_skills"), font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=20, pady=(15, 5))
        skill_frame = ctk.CTkFrame(form, fg_color="transparent")
        skill_frame.pack(fill="x", padx=20, pady=(5, 20))
        for s in ["Machine Learning", "Python", "Data Analysis"]:
            ctk.CTkLabel(skill_frame, text=s, fg_color=COLOR_BG_APP, text_color=COLOR_TEXT_MAIN, corner_radius=6, padx=12, pady=6).pack(side="left", padx=(0, 10))

        # Right: Preview
        preview = ctk.CTkFrame(grid, fg_color="transparent")
        preview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(preview, text=_("prof_preview"), font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 20))
        
        # Theme-aware paper color (Light: Off-white, Dark: Slightly lighter than BG_CARD)
        paper_color = ("#F8FAFC", "#2D3748")
        paper = ctk.CTkFrame(preview, fg_color=paper_color, width=340, height=520, corner_radius=2)
        paper.pack(anchor="n")
        paper.pack_propagate(False)
        
        # Giả lập CV đơn giản trên giấy trắng
        hdr = ctk.CTkFrame(paper, fg_color="transparent")
        hdr.pack(fill="x", padx=15, pady=25)
        ctk.CTkLabel(hdr, text="🧑", font=ctk.CTkFont(size=40)).pack(side="left", padx=(0, 15))
        info = ctk.CTkFrame(hdr, fg_color="transparent")
        info.pack(side="left")
        ctk.CTkLabel(info, text="KHANG NGUYEN HOANG DANG", font=ctk.CTkFont(size=11, weight="bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(info, text=_("prof_student_info").upper(), font=ctk.CTkFont(size=8), text_color="#64748B", wraplength=200, justify="left").pack(anchor="w")
        
        # Nội dung CV
        body = ctk.CTkFrame(paper, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=15)
        
        col_l = ctk.CTkFrame(body, fg_color="transparent", width=100)
        col_l.pack(side="left", fill="y", padx=(0, 15))
        col_l.pack_propagate(False)
        
        ctk.CTkLabel(col_l, text="CONTACT", font=ctk.CTkFont(size=9, weight="bold"), text_color="#3B82F6", fg_color="#E0F2FE", corner_radius=4, padx=5).pack(anchor="w", pady=5)
        for t in ["Vietnam", "+84 123 456 789", "khang@vku.edu"]:
            ctk.CTkLabel(col_l, text=t, font=ctk.CTkFont(size=7), text_color="#475569", justify="left", wraplength=90).pack(anchor="w", pady=5)
            
        col_r = ctk.CTkFrame(body, fg_color="transparent")
        col_r.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(col_r, text="Developing machine learning models and AI solutions to solve complex problems and drive innovation...", font=ctk.CTkFont(size=7), text_color="#475569", justify="left", wraplength=180).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(col_r, text="EDUCATION", font=ctk.CTkFont(size=9, weight="bold"), text_color="#1E293B").pack(anchor="w")
        edu_frame = ctk.CTkFrame(col_r, fg_color="transparent")
        edu_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(edu_frame, text="GPA\n3.8", font=ctk.CTkFont(size=8, weight="bold"), text_color="#10B981").pack(side="left", padx=(0,15))
        ctk.CTkLabel(edu_frame, text="PROGRESS\n85%", font=ctk.CTkFont(size=8, weight="bold"), text_color="#3B82F6").pack(side="left", padx=15)
        
        ctk.CTkLabel(col_r, text="EXPERIENCE", font=ctk.CTkFont(size=9, weight="bold"), text_color="#1E293B").pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(col_r, text="Discrete Math Project\n• Applied discrete structures to algorithmic problems.\n• Optimized logic for complex data processing.", font=ctk.CTkFont(size=7), text_color="#475569", justify="left", wraplength=180).pack(anchor="w")
        ctk.CTkLabel(col_r, text="AI Research Intern\n• Researched deep learning architectures.", font=ctk.CTkFont(size=7), text_color="#475569", justify="left", wraplength=180).pack(anchor="w", pady=5)
