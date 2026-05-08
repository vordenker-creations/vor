import customtkinter as ctk
from config import *
from components import SaaSCard

class OverviewTab(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Grid cho các thẻ chỉ số
        stats_grid = ctk.CTkFrame(self, fg_color="transparent")
        stats_grid.pack(fill="x", pady=10)
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)

        # Thẻ tiến độ (65%)
        card1 = SaaSCard(stats_grid)
        card1.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkLabel(card1, text="ROADMAP PROGRESS", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT_SUB).pack(pady=(15, 5))
        ctk.CTkLabel(card1, text="65%", font=ctk.CTkFont(size=44, weight="bold"), text_color=COLOR_PRIMARY).pack(pady=10)
        
        # Thẻ GPA (3.8)
        card2 = SaaSCard(stats_grid)
        card2.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(card2, text="CURRENT GPA", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT_SUB).pack(pady=(15, 5))
        ctk.CTkLabel(card2, text="3.8 / 4.0", font=ctk.CTkFont(size=40, weight="bold"), text_color="#10B981").pack(pady=15)

        # Thẻ Độ khớp CV (92%)
        card3 = SaaSCard(stats_grid)
        card3.grid(row=0, column=2, padx=5, sticky="nsew")
        ctk.CTkLabel(card3, text="CV MATCH RATE", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT_SUB).pack(pady=(15, 5))
        ctk.CTkLabel(card3, text="92%", font=ctk.CTkFont(size=44, weight="bold"), text_color="#3B82F6").pack(pady=10)

        # Phần Timeline Học tập bên dưới
        timeline_box = SaaSCard(self)
        timeline_box.pack(fill="x", pady=20)
        ctk.CTkLabel(timeline_box, text="HÀNH TRÌNH CỦA KHOA", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=25, pady=20)
        
        # Giả lập Timeline
        for task in ["Học Python Nâng cao (Vừa xong)", "Dự án AI Mentor (Đang thực hiện)", "Thực tập VNG (Sắp tới)"]:
            item = ctk.CTkFrame(timeline_box, fg_color=COLOR_BG_APP, height=50, corner_radius=8)
            item.pack(fill="x", padx=25, pady=5)
            ctk.CTkLabel(item, text=f"✨ {task}", font=ctk.CTkFont(size=13)).pack(side="left", padx=15)