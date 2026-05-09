import customtkinter as ctk
from config import *
from components import SaaSCard, AnimatedProgressBar, AnimationEngine

class ProjectsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=7)
        grid.grid_columnconfigure(1, weight=3)

        # Left: Project Details
        left_card = SaaSCard(grid, border_color="#F59E0B") # Yellow
        left_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(left_card, delay_ms=100)
        
        ctk.CTkLabel(left_card, text="Đồ án cuối khóa: Ứng dụng Quản lý Nhân sự", font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold")).pack(anchor="w", padx=25, pady=(25, 10))
        
        ctk.CTkLabel(left_card, text="Dự án outline:\n• Milestone 1: Training\n• Milestone 2: Train\n• Milestone 3: Train\n• Milestone 4: Training", justify="left", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(anchor="w", padx=25, pady=5)
        
        ctk.CTkLabel(left_card, text="Team lại:\n• Nguyễn Nhì, FTuyen\n• Nguyễn Lòng, ATuyen", justify="left", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(anchor="w", padx=25, pady=5)
        
        ctk.CTkLabel(left_card, text="Timeline:", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w", padx=25, pady=(15, 5))
        p_bar = AnimatedProgressBar(left_card, color=COLOR_PRIMARY, height=8)
        p_bar.pack(fill="x", padx=25, pady=(0, 20))
        p_bar.set_target(0.6)
        
        r = ctk.CTkFrame(left_card, fg_color="transparent")
        r.pack(fill="x", padx=25)
        ctk.CTkLabel(r, text="Chặng status", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(side="left")
        ctk.CTkLabel(r, text="Current status", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(side="right")
        
        ctk.CTkLabel(left_card, text="Outline:\n• Milestone 1:\n• Milestone 2:\n• Milestone 3:\n• Milestone 4:\n• Nguồn hắng", justify="left", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(anchor="w", padx=25, pady=10)

        # Right: Group Chat
        right_card = SaaSCard(grid)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(right_card, delay_ms=300)
        
        chat_area = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        chat_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        def add_msg(name, text):
            msg = ctk.CTkFrame(chat_area, fg_color="transparent")
            msg.pack(fill="x", pady=10)
            ctk.CTkLabel(msg, text="👤", font=(FONT_MAIN, 20)).pack(side="left", anchor="n")
            b = ctk.CTkFrame(msg, fg_color="transparent")
            b.pack(side="left", fill="x", expand=True, padx=10)
            ctk.CTkLabel(b, text=name, font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(b, text=text, font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB, wraplength=200, justify="left").pack(anchor="w")
            
        add_msg("Việt mann 0.1", "Năm phụ cấp cao hơn bận học, môn tập custom widget.")
        add_msg("Việt mann 02", "Năm phụ cấp cho môn này, bài nạp chất button...")

        ctk.CTkLabel(right_card, text="Group chat", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        inp = ctk.CTkEntry(right_card, placeholder_text="Chat ...", height=40, fg_color=COLOR_BG_APP, border_color=COLOR_BORDER)
        inp.pack(fill="x", padx=20, pady=(0, 10))
        
        btn_box = ctk.CTkFrame(right_card, fg_color="transparent")
        btn_box.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(btn_box, text="😀 📎", text_color=COLOR_TEXT_SUB, font=(FONT_MAIN, 16)).pack(side="left")
        ctk.CTkButton(btn_box, text="Send", width=60, height=30, fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY).pack(side="right")
