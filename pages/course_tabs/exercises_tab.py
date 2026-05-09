import customtkinter as ctk
from config import *
from components import SaaSCard, AnimatedProgressBar, AnimationEngine, CountUpLabel

class ExercisesTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=6)
        grid.grid_columnconfigure(1, weight=4)

        # Left: Exercises Grid
        left_frame = ctk.CTkFrame(grid, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        left_frame.grid_columnconfigure((0, 1), weight=1)

        exercises = [
            ("BT 3.1. Viết custom widget cho Slider", "Nộp ngày 12/07/2022"),
            ("BT 3.1. Viết custom widget cho Slider", "Nộp ngày 15/07/2022"),
            ("BT 3.2. Viết custom widget cho Slider", "Nộp ngày 12/12/2022"),
            ("BT 3.2. Viết custom widget cho Slider", "Nộp ngày 12/03/2022"),
            ("BT 3.1. Viết custom widget cho Slider", "Nộp ngày 11/10/2022"),
            ("BT 3.3. Viết custom widget cho Slider", "Nộp ngày 12/13/2022"),
            ("BT 3.4. Viết custom widget cho Slider", "Nộp ngày 11/10/2022"),
            ("BT 3.4. Viết custom widget cho Slider", "Nộp ngày 11/10/2022")
        ]
        
        for i, (title, date) in enumerate(exercises):
            r = i // 2
            c = i % 2
            card = SaaSCard(left_frame, border_color="#10B981") # Green
            card.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
            AnimationEngine.fade_in_widget(card, delay_ms=i*50)
            
            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=15, pady=(15, 5))
            ctk.CTkLabel(top, text="✓", text_color="#10B981", font=(FONT_MAIN, 16, "bold")).pack(side="left", anchor="n")
            txt_box = ctk.CTkFrame(top, fg_color="transparent")
            txt_box.pack(side="left", fill="x", expand=True, padx=10)
            ctk.CTkLabel(txt_box, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), wraplength=200, justify="left").pack(anchor="w")
            ctk.CTkLabel(txt_box, text=date, font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w")
            
            ctk.CTkButton(card, text="Nộp bài", fg_color=COLOR_BG_APP, text_color=COLOR_TEXT_MAIN, border_width=1, border_color=COLOR_BORDER, height=28, width=80).pack(anchor="e", padx=15, pady=(0, 15))

        # Right: Statistics
        right_card = SaaSCard(grid, border_color=COLOR_PRIMARY)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(right_card, delay_ms=400)
        
        ctk.CTkLabel(right_card, text="Statistics", font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), text_color="#10B981").pack(anchor="w", padx=20, pady=20)
        
        stat_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        stat_frame.pack(fill="x", padx=20)
        
        def add_stat_row(parent, label, val):
            r = ctk.CTkFrame(parent, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=label, text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(side="left")
            c_lbl = CountUpLabel(r, format_str="{}", suffix="", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"))
            c_lbl.pack(side="right")
            c_lbl.set_target(val)
            
        add_stat_row(stat_frame, "Assignment 1:", "3")
        add_stat_row(stat_frame, "Assignment 2:", "4")
        add_stat_row(stat_frame, "Bài án:", "9.5")
        
        r = ctk.CTkFrame(stat_frame, fg_color="transparent")
        r.pack(fill="x", pady=2)
        ctk.CTkLabel(r, text="Kết quả:", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(side="left")
        ctk.CTkLabel(r, text="6k quá", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold")).pack(side="right")

        ctk.CTkLabel(right_card, text="Team lại:\n• Nguyễn Nhì, Nguyễn Tú\n• Nguyễn Long, Nguyễn Tú", justify="left", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(anchor="w", padx=20, pady=(20, 10))
        
        add_stat_row(right_card, "Statistics:", "66")
        p1 = AnimatedProgressBar(right_card, color=COLOR_PRIMARY, height=6)
        p1.pack(fill="x", padx=20, pady=(5, 15))
        p1.set_target(0.66)
        
        add_stat_row(right_card, "Chặng stats:", "10")
        p2 = AnimatedProgressBar(right_card, color=COLOR_PRIMARY, height=6)
        p2.pack(fill="x", padx=20, pady=(5, 15))
        p2.set_target(0.8)
        
        add_stat_row(right_card, "Milestone s:", "2.5")
