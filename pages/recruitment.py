import customtkinter as ctk
from config import *
from components import SaaSCard

class RecruitmentPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Thị Trường Tuyển Dụng", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 15))
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=30)
        grid.grid_columnconfigure((0, 1), weight=1)
        for i in range(4):
            card = SaaSCard(grid)
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            ctk.CTkLabel(card, text="🏢 Công ty Cổ phần VNG", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=25, pady=(25, 2))
            ctk.CTkLabel(card, text="Thực tập sinh AI Engineer", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=25)
            ctk.CTkButton(card, text="Ứng tuyển ngay", fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, height=35, corner_radius=6, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=25, pady=25)