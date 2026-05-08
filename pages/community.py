import customtkinter as ctk
from config import *
from components import SaaSCard
from i18n import _

class CommunityPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # ==========================================
        # HEADER: COMMUNITY DISCUSSION & WORKFLOW
        # ==========================================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(35, 10))
        
        ctk.CTkLabel(header, text=_("comm_title"), 
                     font=ctk.CTkFont(family=FONT_MAIN, size=22, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(side="left")
        
        target_job_frame = ctk.CTkFrame(header, fg_color="transparent")
        target_job_frame.pack(side="right")
        ctk.CTkLabel(target_job_frame, text=_("comm_target_job"), font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_SUB).pack(side="left", padx=10)
        
        job_dropdown = ctk.CTkOptionMenu(target_job_frame, values=["ML Engineer", "Data Scientist", "Full-Stack Dev", "AI Researcher"], 
                                         fg_color=COLOR_BG_CARD, text_color=COLOR_TEXT_MAIN, button_color=COLOR_PRIMARY, font=ctk.CTkFont(family=FONT_MAIN, weight="bold"))
        job_dropdown.pack(side="left")

        # ==========================================
        # SECTION 1: JOIN GROUPS & CHANNELS (Lưới Nhóm)
        # ==========================================
        ctk.CTkLabel(self, text=_("comm_join_groups"), font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(15, 5))

        groups_grid = ctk.CTkFrame(self, fg_color="transparent")
        groups_grid.pack(fill="x", padx=30, pady=5)
        groups_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="group")

        # Dữ liệu mô phỏng các nhóm (tương tự thiết kế)
        groups_data = [
            ("ML Engineers", f"660 {_('comm_members')}", "2 hours ago", COLOR_PRIMARY, "🤖"),
            ("Full-Stack Devs", f"125 {_('comm_members')}", "2 hours ago", "#F59E0B", "💻"),
            ("Python Foundations", f"157 {_('comm_members')}", "2 hours ago", "#10B981", "🐍"),
            ("Job Match Discussion", f"737 {_('comm_members')}", "2 hours ago", "#3B82F6", "💼"),
            ("AI Research", f"500 {_('comm_members')}", "2 hours ago", "#8B5CF6", "🔬"),
            ("Project Feedback", f"320 {_('comm_members')}", "1 hours ago", "#EC4899", "📝")
        ]

        for i, (title, members, time, color, icon) in enumerate(groups_data):
            # Tạo card với viền màu đặc trưng
            card = SaaSCard(groups_grid, border_color=color, border_width=1)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            top_card = ctk.CTkFrame(card, fg_color="transparent")
            top_card.pack(fill="x", padx=15, pady=(15, 5))
            
            icon_lbl = ctk.CTkLabel(top_card, text=icon, font=ctk.CTkFont(size=24))
            icon_lbl.pack(side="left")
            
            # Nút "Tham gia" thu nhỏ ở góc (giả lập icon X hoặc tick)
            ctk.CTkLabel(top_card, text="↗", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=14)).pack(side="right")
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(5, 0))
            ctk.CTkLabel(card, text=f"👥 {members}", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=15, pady=(2, 10))
            
            ctk.CTkFrame(card, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=15, pady=(5, 5))
            ctk.CTkLabel(card, text=f"{_('comm_recent')} {time}", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=15, pady=(5, 15))

        # ==========================================
        # SECTION 2: COMMUNITY ENGAGEMENT WORKFLOW 
        # ==========================================
        ctk.CTkLabel(self, text=_("comm_workflow"), font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 10))
        
        workflow_grid = ctk.CTkFrame(self, fg_color="transparent")
        workflow_grid.pack(fill="both", expand=True, padx=30, pady=5)
        workflow_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="wf")

        # CỘT 1: Nhóm đã tham gia
        col1 = SaaSCard(workflow_grid)
        col1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(col1, text=_("comm_step1"), font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 10))
        self.add_mini_group(col1, "ML Engineers", "2 mins ago")
        self.add_mini_group(col1, "Python Foundations", "1 hour ago")
        self.add_mini_group(col1, "Full-Stack Devs", "1 month ago")

        # CỘT 2: Đăng bài & Chia sẻ
        col2 = SaaSCard(workflow_grid)
        col2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(col2, text=_("comm_step2"), font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 10))
        
        entry_title = ctk.CTkEntry(col2, placeholder_text=_("comm_post_title"), height=35, fg_color=COLOR_BG_APP, border_width=1, border_color=COLOR_BORDER)
        entry_title.pack(fill="x", padx=15, pady=(0, 10))
        
        entry_content = ctk.CTkTextbox(col2, height=100, fg_color=COLOR_BG_APP, border_width=1, border_color=COLOR_BORDER)
        entry_content.pack(fill="x", padx=15, pady=(0, 10))
        entry_content.insert("0.0", "Content and snippets...\n\ncode_snippet = 'AI Model';\nprint(code_snippet)")
        
        # Dropdown Category
        cat_frame = ctk.CTkFrame(col2, fg_color="transparent")
        cat_frame.pack(fill="x", padx=15, pady=(0, 15))
        ctk.CTkLabel(cat_frame, text=_("comm_category"), font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(side="left", padx=(0, 10))
        ctk.CTkOptionMenu(cat_frame, values=["Interview Help", "Project Feedback", "General QA"], fg_color=COLOR_BG_APP, text_color=COLOR_TEXT_MAIN).pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(col2, text=_("comm_btn_post"), fg_color=COLOR_PRIMARY, text_color="white", font=ctk.CTkFont(family=FONT_MAIN, weight="bold"), height=35).pack(fill="x", padx=15, pady=(0, 15))

        # CỘT 3: Nhận phản hồi & Mạng lưới
        col3 = SaaSCard(workflow_grid)
        col3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(col3, text=_("comm_step3"), font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.add_feedback_item(col3, "✨ AI GENERATED SUGGESTIONS", "AI has framed alternative questions for optimizing your post reach.", COLOR_PRIMARY)
        self.add_feedback_item(col3, "👥 FIND MENTORS!", "Find mentors tailored to your suggested questions.", "#F59E0B")
        self.add_feedback_item(col3, "📚 RESOURCE MATCH", "Recommended articles based on your code snippet.", "#10B981")

        # ==========================================
        # BOTTOM ACTION BUTTONS
        # ==========================================
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=35, pady=(15, 35))
        
        # 3 nút bấm phân bổ đều
        ctk.CTkButton(btn_frame, text=_("comm_btn_mentor"), fg_color=COLOR_PRIMARY, text_color="white", height=42, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text=_("comm_btn_ai"), fg_color=COLOR_PRIMARY, text_color="white", height=42, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")).pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(btn_frame, text=_("comm_btn_join"), fg_color=COLOR_PRIMARY, text_color="white", height=42, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def add_mini_group(self, parent, title, time):
        """Hàm tạo các khối nhóm nhỏ trong cột 1"""
        frame = ctk.CTkFrame(parent, fg_color=COLOR_BG_APP, corner_radius=6, border_width=1, border_color=COLOR_BORDER)
        frame.pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=12, pady=(10, 0))
        
        bot_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bot_frame.pack(fill="x", padx=12, pady=(2, 10))
        ctk.CTkLabel(bot_frame, text="👥 " + _("comm_members"), font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(side="left")
        ctk.CTkLabel(bot_frame, text=time, font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(side="right")

    def add_feedback_item(self, parent, title, desc, color):
        """Hàm tạo các khối AI thông báo trong cột 3"""
        frame = ctk.CTkFrame(parent, fg_color="transparent", border_width=1, border_color=COLOR_BORDER, corner_radius=6)
        frame.pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=color).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(frame, text=desc, font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB, wraplength=220, justify="left").pack(anchor="w", padx=12, pady=(0, 10))