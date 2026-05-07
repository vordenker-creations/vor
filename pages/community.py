import customtkinter as ctk
from config import *
from components import SaaSCard

class CommunityPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Cộng đồng & Thảo luận", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 15))
        for i in range(3):
            card = SaaSCard(self)
            card.pack(fill="x", padx=35, pady=8)
            ctk.CTkLabel(card, text="[Hỏi đáp] Tài liệu ôn thi Cấu trúc Dữ liệu", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=25, pady=(20, 5))
            ctk.CTkLabel(card, text="Đăng bởi: Học viên A • 2 giờ trước • 15 bình luận", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=25, pady=(0, 20))