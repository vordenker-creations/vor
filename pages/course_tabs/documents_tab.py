import customtkinter as ctk
from config import *
from components import SaaSCard, AnimationEngine

class DocumentsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        # Col 1
        c1 = SaaSCard(grid, border_color=COLOR_PRIMARY)
        c1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self._build_doc_list(c1, "Tài liệu 1:", ["Bài 1: Tổng quan", "Slide 3: Tkinter Overview", "Slide 3: Tkinter Handling...", "Slide 4: Tkinter Handling...", "Slide 5: Tkinter Widgets", "Slide 6: Tkinter Computer...", "Slide 7: Tkinter Overview", "Slide 8: Tkinter Display", "Slide 8: Tkinter Function...", "Slide 10: Tkinter Breonm..."], delay=100)

        # Col 2
        c2 = SaaSCard(grid, border_color="#10B981") # Greenish
        c2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self._build_doc_list(c2, "Tài liệu 2:", ["example_custom_widget_final.py", "example_custom_widget_final_ão.py", "example_custom_widget.py", "example_custom_widget.py", "example_custom_widget.py", "example_custom_widget.py", "example_stant_widget.py", "example_custom_widget.py", "example_stant_widget.py", "example_custom_widget.py", "example_event_widget.py"], delay=200)

        # Col 3
        c3 = SaaSCard(grid, border_color="#8B5CF6") # Purple
        c3.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(c3, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Tải xuống tất cả", fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(fill="x", pady=2)
        ctk.CTkButton(btn_frame, text="Tải xuống tất cả", fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(fill="x", pady=2)
        
        self._build_doc_list(c3, "Tài liệu 3:", ["E-book: https://A-book-fuc...", "E-book: https://A-book-fuc...", "E-book: https://A-book-fuc..."], delay=300, include_header=False)

    def _build_doc_list(self, parent, title, items, delay=0, include_header=True):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        AnimationEngine.fade_in_widget(wrapper, delay_ms=delay)
        
        if include_header:
            ctk.CTkLabel(wrapper, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        for item in items:
            row = ctk.CTkFrame(wrapper, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(row, text="📄", text_color=COLOR_TEXT_SUB, font=(FONT_MAIN, 14)).pack(side="left", padx=(0, 5))
            ctk.CTkLabel(row, text=item, text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(side="left")
