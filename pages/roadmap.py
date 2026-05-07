import customtkinter as ctk
from config import *
from components import SaaSCard

class RoadmapPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(35, 15))
        ctk.CTkLabel(header, text="Lộ Trình & AI Mentor", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=0)
        container.grid_columnconfigure(0, weight=5)
        container.grid_columnconfigure(1, weight=5)

        left_card = SaaSCard(container)
        left_card.grid(row=0, column=0, sticky="nsew", padx=5)
        ctk.CTkLabel(left_card, text="Cây Kỹ năng Học thuật", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=30, pady=25)
        
        nodes = [
            ("Năm 1: Cơ sở", "Hoàn thành", "#10B981", "Nhập môn Lập trình, Toán Cao Cấp"),
            ("Năm 2: Cốt lõi", "Hoàn thành", "#10B981", "Cấu trúc dữ liệu, Mạng máy tính"),
            ("Năm 3: Chuyên ngành", "Đang diễn ra", COLOR_PRIMARY, "Trí tuệ Nhân tạo, Phân tích dữ liệu"),
            ("Năm 4: Ra trường", "Chưa mở", COLOR_TEXT_SUB, "Khóa luận tốt nghiệp, Thực tập")
        ]

        for i, (title, status, color, detail) in enumerate(nodes):
            row_frame = ctk.CTkFrame(left_card, fg_color="transparent")
            row_frame.pack(fill="x", padx=30, pady=0)
            line_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=30)
            line_frame.pack(side="left", fill="y", padx=(0, 15))
            ctk.CTkLabel(line_frame, text="●", text_color=color, font=ctk.CTkFont(size=18)).pack(pady=(5, 0))
            if i < len(nodes) - 1:
                ctk.CTkFrame(line_frame, width=2, fg_color=COLOR_BORDER).pack(fill="y", expand=True, pady=5)
            content_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            content_frame.pack(side="left", fill="x", expand=True, pady=(0, 20))
            ctk.CTkLabel(content_frame, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
            ctk.CTkLabel(content_frame, text=f"Trạng thái: {status}", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=color).pack(anchor="w")
            ctk.CTkLabel(content_frame, text=detail, font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB, justify="left").pack(anchor="w", pady=(2,0))

        right_card = SaaSCard(container)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5)
        chat_header = ctk.CTkFrame(right_card, fg_color="transparent", border_width=1, border_color=COLOR_BORDER)
        chat_header.pack(fill="x")
        ctk.CTkLabel(chat_header, text="✨  AI Mentor (Gemini)", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left", padx=20, pady=20)
        
        chat_area = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        chat_area.pack(fill="both", expand=True, padx=10, pady=10)
        self.add_bubble(chat_area, "Đề xuất cho mình lộ trình AI Engineer.", True)
        self.add_bubble(chat_area, "Mình đã cập nhật lộ trình. Bạn nên học 'Deep Learning' vào kỳ này.", False)

        entry_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        entry_frame.pack(fill="x", padx=20, pady=20)
        entry = ctk.CTkEntry(entry_frame, placeholder_text="Hỏi Mentor...", height=40, corner_radius=6, fg_color=COLOR_BG_APP, border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(entry_frame, text="Gửi", width=60, height=40, fg_color=COLOR_PRIMARY, text_color="white", corner_radius=6, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")).pack(side="right")

    def add_bubble(self, parent, text, is_user):
        bg = COLOR_PRIMARY_LIGHT if is_user else COLOR_BG_APP
        border = COLOR_PRIMARY_LIGHT if is_user else COLOR_BORDER
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", pady=8)
        bubble = ctk.CTkFrame(container, fg_color=bg, corner_radius=8, border_width=1, border_color=border)
        bubble.pack(side="right" if is_user else "left", padx=10)
        ctk.CTkLabel(bubble, text=text, text_color=COLOR_TEXT_MAIN, justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=13), wraplength=250).pack(padx=15, pady=10)