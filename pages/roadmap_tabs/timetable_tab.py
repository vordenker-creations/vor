import customtkinter as ctk
from config import *
from components import SaaSCard

class TimetableTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 15))
        
        ctk.CTkLabel(header, text="SMART TIMETABLE", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=22, weight="bold"),
                     text_color=COLOR_TEXT_MAIN).pack(side="left")
        
        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.pack(side="right")
        ctk.CTkLabel(nav, text="OCT 14 - OCT 20, 2026", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(side="left", padx=15)
        
        for btn_text in ["<", ">"]:
            ctk.CTkButton(nav, text=btn_text, width=32, height=32, corner_radius=8,
                          fg_color=COLOR_BG_CARD, text_color=COLOR_TEXT_MAIN, 
                          border_width=1, border_color=COLOR_BORDER,
                          hover_color=COLOR_BG_APP).pack(side="left", padx=3)

        # Main Layout with scrolling capability for long schedule
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)

        main_grid = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        main_grid.pack(fill="both", expand=True)
        main_grid.grid_columnconfigure(0, weight=8)
        main_grid.grid_columnconfigure(1, weight=3)

        # --- Bảng lịch (Left) ---
        sheet = SaaSCard(main_grid)
        sheet.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Header: Days
        days = ["TIME", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i, day in enumerate(days):
            sticky = "w" if i == 0 else ""
            padx = 20 if i == 0 else 5
            ctk.CTkLabel(sheet, text=day, font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), 
                         text_color=COLOR_TEXT_SUB).grid(row=0, column=i, pady=15, padx=padx, sticky=sticky)
        
        # Time Range: 6 AM to 11 PM
        times = [f"{h:02d}:00" for h in range(6, 24)]
        self.time_row_map = {}
        for i, t in enumerate(times):
            row_idx = i + 1
            self.time_row_map[t] = row_idx
            # Time Label
            ctk.CTkLabel(sheet, text=t, font=ctk.CTkFont(family=FONT_MAIN, size=11), 
                         text_color=COLOR_TEXT_SUB).grid(row=row_idx, column=0, pady=12, padx=20, sticky="w")
            
            # Grid separators (Horizontal lines)
            if row_idx < len(times):
                ctk.CTkFrame(sheet, height=1, fg_color=COLOR_BORDER).grid(row=row_idx, column=0, columnspan=8, sticky="sew", padx=10)

        # Add sample blocks
        self.add_block(sheet, "09:00", 1, "COURSES\nCS101", COLOR_PRIMARY)
        self.add_block(sheet, "09:00", 4, "COURSES\nCS101", COLOR_PRIMARY)
        self.add_block(sheet, "10:00", 5, "EVENTS\nAI WORKSHOP", COLOR_PRIMARY_LIGHT, txt_color=COLOR_PRIMARY)
        self.add_block(sheet, "14:00", 1, "PYTHON\nPRACTICE", COLOR_SUCCESS)
        self.add_block(sheet, "14:00", 2, "PYTHON\nPRACTICE", COLOR_SUCCESS)
        self.add_block(sheet, "14:00", 4, "PYTHON\nPRACTICE", COLOR_SUCCESS)
        self.add_block(sheet, "18:00", 5, "NETWORKING\nMEETUP", "#8B5CF6")
        self.add_block(sheet, "22:00", 1, "DEADLINE\nLAB 2", COLOR_WARNING)
        self.add_block(sheet, "22:00", 7, "REVIEW\nWEEKLY", COLOR_PRIMARY)

        # --- Sidebar Reminders (Right) ---
        sidebar = SaaSCard(main_grid)
        sidebar.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(sidebar, text="UPCOMING REMINDERS", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"),
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(25, 20))
        
        reminders = [
            ("ASSIGNMENT 2 DEADLINE", "Today @ 23:59", COLOR_WARNING),
            ("AI WORKSHOP PREP", "Oct 15 @ 08:30", COLOR_PRIMARY),
            ("RESEARCH PAPER SYNC", "Oct 16 @ 14:00", COLOR_SUCCESS),
            ("ALGORITHM CHALLENGE", "Oct 18 @ 20:00", "#EC4899"),
        ]
        
        for text, time_str, color in reminders:
            r = ctk.CTkFrame(sidebar, fg_color=COLOR_BG_APP, height=85, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            r.pack(fill="x", padx=15, pady=6)
            r.pack_propagate(False)
            
            # Color strip
            ctk.CTkFrame(r, width=4, fg_color=color, corner_radius=2).pack(side="left", fill="y", padx=2, pady=10)
            
            txt_box = ctk.CTkFrame(r, fg_color="transparent")
            txt_box.pack(side="left", padx=10, fill="both", expand=True)
            ctk.CTkLabel(txt_box, text=text, font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), 
                         justify="left", text_color=COLOR_TEXT_MAIN, wraplength=140).pack(anchor="w", pady=(15, 0))
            ctk.CTkLabel(txt_box, text=time_str, font=ctk.CTkFont(family=FONT_MAIN, size=10), 
                         text_color=COLOR_TEXT_SUB).pack(anchor="w")
            
            ctk.CTkLabel(r, text="🔔", text_color=color, font=(FONT_MAIN, 14)).pack(side="right", padx=12)

    def add_block(self, parent, time_str, col, text, bg_color, txt_color="white"):
        row = self.time_row_map.get(time_str)
        if row:
            block = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=6)
            block.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            ctk.CTkLabel(block, text=text, font=ctk.CTkFont(family=FONT_MAIN, size=9, weight="bold"), 
                         text_color=txt_color, justify="center").pack(expand=True, padx=5, pady=5)