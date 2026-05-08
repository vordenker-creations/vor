import customtkinter as ctk
from config import *
from components import SaaSCard

class SkillTreeTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        main_card = SaaSCard(self)
        main_card.pack(fill="both", expand=True)
        
        ctk.CTkLabel(main_card, text="AI ENGINEER SKILL TREE", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        canvas_area = ctk.CTkFrame(main_card, fg_color=COLOR_BG_APP, corner_radius=15)
        canvas_area.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Vẽ các Node kỹ năng theo vị trí tọa độ
        nodes = [
            (100, 200, "C++ Core", "#10B981"),
            (250, 100, "OOP", "#10B981"),
            (250, 300, "SQL Server", "#10B981"),
            (450, 200, "Python AI", COLOR_PRIMARY),
            (650, 200, "Deep Learning", COLOR_BORDER),
            (850, 200, "Thesis", COLOR_BORDER)
        ]

        for x, y, name, color in nodes:
            node = ctk.CTkButton(canvas_area, text=name, width=120, height=50, corner_radius=25,
                                 fg_color=color, text_color="white" if color != COLOR_BORDER else COLOR_TEXT_SUB,
                                 font=ctk.CTkFont(size=12, weight="bold"), hover=False)
            node.place(x=x, y=y)