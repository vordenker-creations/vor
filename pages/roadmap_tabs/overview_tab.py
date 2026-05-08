import customtkinter as ctk
from config import *
from components import SaaSCard

class OverviewTab(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Tiêu đề chào mừng
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 20), padx=5)
        
        ctk.CTkLabel(header_frame, text="WELCOME BACK, KHANG! ", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header_frame, text="EXPLORE YOUR JOURNEY.", 
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_SUCCESS).pack(side="left")

        # Grid chính cho các chỉ số
        main_grid = ctk.CTkFrame(self, fg_color="transparent")
        main_grid.pack(fill="x", pady=5)
        main_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # 1. ROADMAP PROGRESS (65%)
        card_progress = SaaSCard(main_grid)
        card_progress.grid(row=0, column=0, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card_progress, text="ROADMAP PROGRESS:", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(card_progress, text="65%", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLOR_PRIMARY).pack(anchor="w", padx=15)
        
        # Giả lập vòng tròn tiến độ
        canvas_progress = tk.Canvas(card_progress, width=120, height=120, bg=get_color(COLOR_BG_CARD), highlightthickness=0)
        canvas_progress.pack(pady=10)
        self.draw_circular_progress(canvas_progress, 65, COLOR_PRIMARY)
        ctk.CTkLabel(card_progress, text="Current semester\nprogress analysis", font=ctk.CTkFont(size=10), text_color=COLOR_TEXT_SUB).pack(pady=(0, 15))

        # 2. CREDITS ACCUMULATED (84/120)
        card_credits = SaaSCard(main_grid)
        card_credits.grid(row=0, column=1, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card_credits, text="CREDITS ACCUMULATED:", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(card_credits, text="84 / 120", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_PRIMARY).pack(anchor="w", padx=15)
        
        # Giả lập biểu đồ cột
        chart_frame = ctk.CTkFrame(card_credits, fg_color="transparent", height=100)
        chart_frame.pack(fill="x", padx=15, pady=20)
        bars = [0.3, 0.5, 0.8, 0.4, 0.6]
        for val in bars:
            bar_bg = ctk.CTkFrame(chart_frame, fg_color=COLOR_BORDER, width=15, height=80)
            bar_bg.pack(side="left", padx=5, anchor="s")
            bar_val = ctk.CTkFrame(bar_bg, fg_color=COLOR_PRIMARY, width=15, height=80*val)
            bar_val.place(relx=0, rely=1.0, anchor="sw")

        # 3. GPA (3.8)
        card_gpa = SaaSCard(main_grid)
        card_gpa.grid(row=0, column=2, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card_gpa, text="GPA:", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(card_gpa, text="3.8", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_SUCCESS).pack(anchor="w", padx=15)
        
        gpa_list = [("Discrete Math", "A", "4.0"), ("Python", "A-", "3.7"), ("AI Basics", "B+", "3.5"), ("Data Struct", "A", "4.0")]
        for i, (label, val, sub) in enumerate(gpa_list):
            row = ctk.CTkFrame(card_gpa, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=9), text_color=COLOR_TEXT_SUB).pack(side="left")
            ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=9, weight="bold")).pack(side="right", padx=(20, 0))
            ctk.CTkLabel(row, text=sub, font=ctk.CTkFont(size=9), text_color=COLOR_TEXT_SUB).pack(side="right")

        # 4. CV JOB MATCH (92%)
        card_cv = SaaSCard(main_grid)
        card_cv.grid(row=0, column=3, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card_cv, text="CV JOB MATCH: 92%", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_SUCCESS).pack(anchor="w", padx=15, pady=(15, 5))
        
        canvas_cv = tk.Canvas(card_cv, width=120, height=120, bg=get_color(COLOR_BG_CARD), highlightthickness=0)
        canvas_cv.pack(pady=10)
        self.draw_radar_match(canvas_cv)

        # Hàng thứ 2: Learning Journey & Events
        bottom_grid = ctk.CTkFrame(self, fg_color="transparent")
        bottom_grid.pack(fill="x", pady=15)
        bottom_grid.grid_columnconfigure(0, weight=3)
        bottom_grid.grid_columnconfigure(1, weight=2)

        # LEARNING JOURNEY UPDATE
        card_journey = SaaSCard(bottom_grid)
        card_journey.grid(row=0, column=0, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card_journey, text="LEARNING JOURNEY UPDATE", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(card_journey, text="ADVANCED PYTHON: 80% COMPLETED", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_SUCCESS).pack(anchor="w", padx=20, pady=5)
        
        bar = ctk.CTkProgressBar(card_journey, height=12, progress_color=COLOR_SUCCESS, fg_color=COLOR_BORDER)
        bar.pack(fill="x", padx=20, pady=10)
        bar.set(0.8)
        
        desc = "Track your learning progress across all courses and skills.\nComplete assignments and modules to advance your career path\nand unlock new opportunities in the AI industry."
        ctk.CTkLabel(card_journey, text=desc, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_SUB, justify="left").pack(anchor="w", padx=20, pady=(10, 20))

        # UPCOMING EVENTS & DEADLINES
        card_events = SaaSCard(bottom_grid)
        card_events.grid(row=0, column=1, padx=5, sticky="nsew")
        
        ctk.CTkLabel(card_events, text="UPCOMING EVENTS & DEADLINES", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        
        events = [
            ("📅", "AI WORKSHOP", "Tomorrow @ 10:00", "Details >"),
            ("📙", "Assignment 2 DUE", "Friday @ 23:59", "Submit >"),
            ("⌛", "LAB SESSION", "Monday @ 15:00", "Details >")
        ]
        
        for icon, title, time, action in events:
            item = ctk.CTkFrame(card_events, fg_color="transparent")
            item.pack(fill="x", padx=20, pady=8)
            
            ctk.CTkLabel(item, text=icon, font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 10))
            
            info = ctk.CTkFrame(item, fg_color="transparent")
            info.pack(side="left", fill="y")
            ctk.CTkLabel(info, text=title, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(info, text=time, font=ctk.CTkFont(size=10), text_color=COLOR_TEXT_SUB).pack(anchor="w")
            
            ctk.CTkLabel(item, text=action, font=ctk.CTkFont(size=10), text_color=COLOR_TEXT_SUB).pack(side="right")

    def draw_circular_progress(self, canvas, percentage, color):
        canvas.delete("all")
        # Vòng nền
        canvas.create_oval(10, 10, 110, 110, outline=get_color(COLOR_BORDER), width=8)
        # Vòng tiến độ
        extent = -(360 * percentage / 100)
        canvas.create_arc(10, 10, 110, 110, start=90, extent=extent, outline=get_color(color), width=10, style="arc")
        # Text ở giữa
        canvas.create_text(60, 60, text=f"{percentage}%", fill=get_color(COLOR_TEXT_MAIN), font=("Segoe UI", 16, "bold"))

    def draw_radar_match(self, canvas):
        canvas.delete("all")
        cx, cy = 60, 60
        r = 45
        # Vẽ các vòng tròn đồng tâm
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=get_color(COLOR_BORDER), width=1)
        canvas.create_oval(cx-r*0.6, cy-r*0.6, cx+r*0.6, cy+r*0.6, outline=get_color(COLOR_BORDER), width=1)
        
        # Vẽ các "node" job giả lập
        points = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
        for x, y in points:
            canvas.create_oval(x-8, y-8, x+8, y+8, fill=get_color(COLOR_BG_CARD), outline=get_color(COLOR_PRIMARY), width=1)
            canvas.create_text(x, y, text="JOB", fill=get_color(COLOR_TEXT_SUB), font=("Segoe UI", 6))
        
        # Center node
        canvas.create_oval(cx-12, cy-12, cx+12, cy+12, fill=get_color(COLOR_BG_APP), outline=get_color(COLOR_SUCCESS), width=2)
        canvas.create_text(cx, cy, text="CV", fill=get_color(COLOR_SUCCESS), font=("Segoe UI", 8, "bold"))
        
        # Connections
        for x, y in points:
            canvas.create_line(cx, cy, x, y, fill=get_color(COLOR_SUCCESS), dash=(2, 2))
import tkinter as tk # Đảm bảo tk được import để dùng Canvas