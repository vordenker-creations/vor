import customtkinter as ctk
from config import *
from components import SaaSCard

class TimetableTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 20))
        
        ctk.CTkLabel(header, text="SMART TIMETABLE: WEEKLY VIEW (Oct 14 - Oct 20)", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.pack(side="right")
        ctk.CTkLabel(nav, text="Oct 14 - Oct 20", font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        ctk.CTkButton(nav, text="<", width=30, height=30, fg_color=COLOR_BG_CARD).pack(side="left", padx=2)
        ctk.CTkButton(nav, text=">", width=30, height=30, fg_color=COLOR_BG_CARD).pack(side="left", padx=2)

        # Main Grid
        main_grid = ctk.CTkFrame(self, fg_color="transparent")
        main_grid.pack(fill="both", expand=True)
        main_grid.grid_columnconfigure(0, weight=8)
        main_grid.grid_columnconfigure(1, weight=2)

        # Bảng lịch (Left)
        sheet = SaaSCard(main_grid)
        sheet.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ctk.CTkLabel(sheet, text=day, font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT_SUB).grid(row=0, column=i+1, pady=15, padx=10)
        
        times = ["9:00", "10:00", "14:00", "18:00", "23:00", "23:30"]
        for i, t in enumerate(times):
            ctk.CTkLabel(sheet, text=t, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_SUB).grid(row=i+1, column=0, pady=20, padx=15)

        # Thêm các block mẫu (Course, Event, Practice, Deadline)
        self.add_block(sheet, 1, 1, "COURSES\nCS101 @ 9:00", COLOR_PRIMARY)
        self.add_block(sheet, 1, 4, "COURSES\nCS101 @ 9:00", COLOR_PRIMARY)
        self.add_block(sheet, 1, 5, "EVENTS\nAI WORKSHOP\n@ 10:00", COLOR_ACCENT)
        
        self.add_block(sheet, 3, 1, "PYTHON\nPRACTICE\n@ 14:00", COLOR_SUCCESS)
        self.add_block(sheet, 3, 2, "PYTHON\nPRACTICE\n@ 14:00", COLOR_SUCCESS)
        self.add_block(sheet, 3, 4, "PYTHON\nPRACTICE\n@ 14:00", COLOR_SUCCESS)
        self.add_block(sheet, 3, 5, "PYTHON\nPRACTICE\n@ 14:00", COLOR_SUCCESS)
        
        self.add_block(sheet, 5, 1, "DEADLINES\nAssignment 2\ndue @ 23:59", COLOR_WARNING)
        self.add_block(sheet, 5, 4, "DEADLINES\nAssignment 2\ndue @ 23:59", COLOR_WARNING)

        # Sidebar Reminders (Right)
        sidebar = SaaSCard(main_grid)
        sidebar.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(sidebar, text="REMINDERS", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=20, pady=20)
        
        reminders = [
            ("URGENT: ASSIGNMENT 2\nDEADLINE", "(Tom @ 23:59)", COLOR_WARNING),
            ("URGENT: ASSIGNMENT 2\nDEADLINE", "(Tom @ 23:59)", COLOR_WARNING),
            ("URGENT: ASSIGNMENT 2.1\nDEADLINE COONG", "(Tom @ 23:59)", COLOR_WARNING),
        ]
        
        for text, time, color in reminders:
            r = ctk.CTkFrame(sidebar, fg_color=COLOR_BG_APP, height=80, corner_radius=8)
            r.pack(fill="x", padx=15, pady=8)
            r.pack_propagate(False)
            
            # Thanh màu bên trái
            ctk.CTkFrame(r, width=5, fg_color=color).pack(side="left", fill="y")
            
            txt_box = ctk.CTkFrame(r, fg_color="transparent")
            txt_box.pack(side="left", padx=10, fill="both")
            ctk.CTkLabel(txt_box, text=text, font=ctk.CTkFont(size=10, weight="bold"), justify="left", text_color=color).pack(anchor="w", pady=(10, 0))
            ctk.CTkLabel(txt_box, text=time, font=ctk.CTkFont(size=9), text_color=COLOR_TEXT_SUB).pack(anchor="w")
            
            ctk.CTkLabel(r, text="⭐", text_color=color).pack(side="right", padx=10)

    def add_block(self, parent, row, col, text, color):
        block = ctk.CTkFrame(parent, fg_color=color, corner_radius=4)
        block.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        ctk.CTkLabel(block, text=text, font=ctk.CTkFont(size=9, weight="bold"), text_color="white", justify="left").pack(expand=True, padx=5)