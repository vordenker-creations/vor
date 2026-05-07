import customtkinter as ctk
from config import *
from components import SaaSCard

class CourseDetailPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        content_pad = 35

        # 1. Header & Nút quay lại
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=content_pad, pady=(content_pad, 10))
        
        btn_back = ctk.CTkButton(header_frame, text="⬅ Quay lại Dashboard", 
                                 fg_color="transparent", text_color=COLOR_TEXT_SUB, 
                                 hover_color=COLOR_BG_APP, width=150, font=ctk.CTkFont(family=FONT_MAIN, weight="bold"),
                                 command=lambda: self.controller.show_page("DashboardPage"))
        btn_back.pack(side="left")

        # 2. Card chính chứa Nội dung
        main_card = SaaSCard(self)
        main_card.pack(fill="both", expand=True, padx=content_pad, pady=10)

        # Tiêu đề học phần
        ctk.CTkLabel(main_card, text="CHI TIẾT: LẬP TRÌNH PYTHON NÂNG CAO", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=30, pady=(25, 10))

        # 3. Thanh Tabs điều hướng ngang
        tabs_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        tabs_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        tabs = ["Đường lộ trình", "Tài liệu", "Bài tập", "Đồ án", "Kết quả"]
        for i, tab in enumerate(tabs):
            color = COLOR_PRIMARY if i == 0 else COLOR_TEXT_SUB
            weight = "bold" if i == 0 else "normal"
            btn = ctk.CTkButton(tabs_frame, text=tab, fg_color="transparent", text_color=color, 
                                font=ctk.CTkFont(family=FONT_MAIN, size=14, weight=weight), width=100)
            btn.pack(side="left", padx=(0, 15))
            
        # Đường gạch dưới Tab
        ctk.CTkFrame(main_card, height=2, fg_color=COLOR_PRIMARY, width=120).place(x=30, y=95)
        ctk.CTkFrame(main_card, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=30)

        # 4. Khu vực Timeline (Đường lộ trình chi tiết)
        timeline_container = ctk.CTkFrame(main_card, fg_color="transparent")
        timeline_container.pack(fill="both", expand=True, padx=30, pady=25)

        # Module 3 (Hoàn thành phần lớn)
        self.add_timeline_item(
            parent=timeline_container,
            icon="✓", icon_color="white", icon_bg=COLOR_PRIMARY,
            title="☑ Module 3: Tkinter Advanced Widgets",
            progress=0.8, progress_text="80%",
            sub_items="Module 3.1: custom widgets\nModule 3.2: event handling\nModule 3.3: architecture",
            is_last=False
        )

        # Module 4 (Đang học)
        self.add_timeline_item(
            parent=timeline_container,
            icon="📦", icon_color=COLOR_TEXT_SUB, icon_bg=COLOR_BG_APP,
            title="📄 Module 4: Data Science Foundations",
            progress=0.4, progress_text="40%",
            sub_items="",
            is_last=False
        )

        # Module 5 (Chưa học)
        self.add_timeline_item(
            parent=timeline_container,
            icon="🎓", icon_color=COLOR_TEXT_SUB, icon_bg=COLOR_BG_APP,
            title="📄 Module 5: Data robotics Foundations",
            progress=0.2, progress_text="20%",
            sub_items="",
            is_last=True
        )

    def add_timeline_item(self, parent, icon, icon_color, icon_bg, title, progress, progress_text, sub_items, is_last):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=0)

        # Cột icon & đường kẻ dọc
        left_col = ctk.CTkFrame(row, fg_color="transparent", width=40)
        left_col.pack(side="left", fill="y")
        
        icon_btn = ctk.CTkButton(left_col, text=icon, width=30, height=30, corner_radius=15, 
                                 fg_color=icon_bg, text_color=icon_color, hover=False,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        icon_btn.pack(pady=(0, 5))

        if not is_last:
            ctk.CTkFrame(left_col, width=2, fg_color=COLOR_PRIMARY if progress > 0.5 else COLOR_BORDER).pack(fill="y", expand=True)

        # Cột Nội dung
        right_col = ctk.CTkFrame(row, fg_color="transparent")
        right_col.pack(side="left", fill="x", expand=True, padx=(15, 0), pady=(0, 30))

        # Header của Module (Title + Phần trăm)
        header_box = ctk.CTkFrame(right_col, fg_color="transparent")
        header_box.pack(fill="x")
        ctk.CTkLabel(header_box, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header_box, text=progress_text, font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="right")

       # Thanh tiến trình (Progress Bar)
        progress_bar = ctk.CTkProgressBar(right_col, progress_color=COLOR_PRIMARY if progress > 0.5 else COLOR_BORDER, fg_color=COLOR_BG_APP, height=6)
        progress_bar.pack(fill="x", pady=(10, 10))
        progress_bar.set(progress)

        # Sub-items (nếu có)
        if sub_items:
            ctk.CTkLabel(right_col, text=sub_items, justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=13), 
                         text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20)