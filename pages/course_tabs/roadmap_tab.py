import customtkinter as ctk
from config import *
from components import SaaSCard, AnimatedProgressBar, AnimationEngine

class RoadmapTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        main_card = SaaSCard(self)
        main_card.pack(fill="both", expand=True, padx=10, pady=10)

        timeline_container = ctk.CTkFrame(main_card, fg_color="transparent")
        timeline_container.pack(fill="both", expand=True, padx=30, pady=25)

        self._add_timeline_item(timeline_container, "✓", "white", COLOR_PRIMARY, "☑ Module 3: Tkinter Advanced Widgets", 0.8, "80%", "Module 3.1: custom widgets\nModule 3.2: event handling\nModule 3.3: architecture", False, delay=100)
        self._add_timeline_item(timeline_container, "📦", COLOR_TEXT_SUB, COLOR_BG_APP, "📄 Module 4: Data Science Foundations", 0.4, "40%", "", False, delay=200)
        self._add_timeline_item(timeline_container, "🎓", COLOR_TEXT_SUB, COLOR_BG_APP, "📄 Module 5: Data robotics Foundations", 0.2, "20%", "", True, delay=300)

    def _add_timeline_item(self, parent, icon, icon_color, icon_bg, title, progress, progress_text, sub_items, is_last, delay=0):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        AnimationEngine.fade_in_widget(row, delay_ms=delay)

        left_col = ctk.CTkFrame(row, fg_color="transparent", width=40)
        left_col.pack(side="left", fill="y")
        
        icon_btn = ctk.CTkButton(left_col, text=icon, width=30, height=30, corner_radius=15, fg_color=icon_bg, text_color=icon_color, hover=False, font=ctk.CTkFont(size=14, weight="bold"))
        icon_btn.pack(pady=(0, 5))

        if not is_last:
            ctk.CTkFrame(left_col, width=2, fg_color=COLOR_PRIMARY if progress > 0.5 else COLOR_BORDER).pack(fill="y", expand=True)

        right_col = ctk.CTkFrame(row, fg_color="transparent")
        right_col.pack(side="left", fill="x", expand=True, padx=(15, 0), pady=(0, 30))

        header_box = ctk.CTkFrame(right_col, fg_color="transparent")
        header_box.pack(fill="x")
        ctk.CTkLabel(header_box, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header_box, text=progress_text, font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="right")

        progress_bar = AnimatedProgressBar(right_col, color=COLOR_PRIMARY if progress > 0.5 else COLOR_BORDER, height=6)
        progress_bar.pack(fill="x", pady=(10, 10))
        progress_bar.set_target(progress)

        if sub_items:
            ctk.CTkLabel(right_col, text=sub_items, justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20)
