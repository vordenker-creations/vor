import customtkinter as ctk
from config import *
from components import SaaSCard, AnimationEngine

class ResultsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1)

        # Left: Scores
        left_card = SaaSCard(grid, border_color="#8B5CF6") # Purple
        left_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(left_card, delay_ms=100)
        
        top = ctk.CTkFrame(left_card, fg_color="transparent")
        top.pack(fill="x", padx=25, pady=25)
        ctk.CTkLabel(top, text="Tóm tắt kết quả:\n9.2/10", font=ctk.CTkFont(family=FONT_MAIN, size=20, weight="bold")).pack(side="left")
        
        r1 = ctk.CTkFrame(top, fg_color="transparent")
        r1.pack(side="right")
        ctk.CTkLabel(r1, text="Bài tập: 9.5\nĐồ án: 9.0", font=ctk.CTkFont(family=FONT_MAIN, size=13), justify="left").pack(side="left", padx=10)
        ctk.CTkLabel(r1, text="Điểm cộng: 0\nKết quả: 9.2", font=ctk.CTkFont(family=FONT_MAIN, size=13), justify="left").pack(side="left", padx=10)

        for i in range(1, 5):
            box = ctk.CTkFrame(left_card, fg_color=COLOR_BG_APP, corner_radius=8)
            box.pack(fill="x", padx=25, pady=5)
            ctk.CTkLabel(box, text=f"Bài tập: viên mann 3.{i}", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
            ctk.CTkLabel(box, text="Năm phụ cấp cao hơn bận học, môn tập custom widget...", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12), justify="left").pack(anchor="w", padx=15, pady=(0, 15))

        # Right: Notes
        right_card = SaaSCard(grid)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(right_card, delay_ms=300)
        
        ctk.CTkLabel(right_card, text="Instructor notes", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold")).pack(anchor="w", padx=25, pady=(25, 10))
        for i in range(1, 4):
            box = ctk.CTkFrame(right_card, fg_color="transparent")
            box.pack(fill="x", padx=25, pady=5)
            ctk.CTkLabel(box, text=f"Bài 1: Tổng quan" if i==1 else f"BT 3.{i}: viên mann", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(box, text="Năm phụ cấp cao hơn bận học, môn tập custom widget...", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12), justify="left").pack(anchor="w", pady=(5, 10))
            ctk.CTkFrame(right_card, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=25)

        ctk.CTkLabel(right_card, text="Peer reviews", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold")).pack(anchor="w", padx=25, pady=(20, 10))
        ctk.CTkLabel(right_card, text="Title in a peer reviews...", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(anchor="w", padx=25, pady=5)
