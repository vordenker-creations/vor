import customtkinter as ctk
from config import *
from components import SaaSCard

class TimetableTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.pack(fill="both", expand=True)
        grid_container.grid_columnconfigure(0, weight=8)
        grid_container.grid_columnconfigure(1, weight=2)

        # Bảng lịch học
        sheet = SaaSCard(grid_container)
        sheet.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"]
        for i, day in enumerate(days):
            ctk.CTkLabel(sheet, text=day, font=ctk.CTkFont(weight="bold")).grid(row=0, column=i+1, pady=15, padx=20)
        
        hours = ["08:00", "10:00", "13:00", "15:00"]
        for i, hour in enumerate(hours):
            ctk.CTkLabel(sheet, text=hour, text_color=COLOR_TEXT_SUB).grid(row=i+1, column=0, pady=25, padx=15)
            
            # Thêm một vài môn học mẫu
            if i % 2 == 0:
                box = ctk.CTkFrame(sheet, fg_color=COLOR_PRIMARY_LIGHT, corner_radius=6, border_width=1, border_color=COLOR_PRIMARY)
                box.grid(row=i+1, column=i+1, sticky="nsew", padx=4, pady=4)
                ctk.CTkLabel(box, text="Lập trình AI", text_color=COLOR_PRIMARY, font=ctk.CTkFont(size=11, weight="bold")).pack(expand=True)

        # Cột Sidebar thông báo
        sidebar = SaaSCard(grid_container)
        sidebar.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(sidebar, text="DEADLINES", font=ctk.CTkFont(weight="bold")).pack(pady=20)
        
        for task in ["Project Python", "Quiz Toán RR"]:
            t = ctk.CTkFrame(sidebar, fg_color="#FEE2E2", height=70, corner_radius=10)
            t.pack(fill="x", padx=15, pady=8)
            ctk.CTkLabel(t, text=task, text_color="#B91C1C", font=ctk.CTkFont(weight="bold")).pack(pady=15)