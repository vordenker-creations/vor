import customtkinter as ctk
from config import *
from components import SaaSCard

class DashboardPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        content_pad = 35

        hero_banner = ctk.CTkFrame(self, fg_color="#1E3A8A", corner_radius=12) 
        hero_banner.pack(fill="x", padx=content_pad, pady=(content_pad, 15))
        
        hero_text = ctk.CTkFrame(hero_banner, fg_color="transparent")
        hero_text.pack(side="left", padx=40, pady=35)
        ctk.CTkLabel(hero_text, text="HỆ THỐNG AI MENTOR ĐÃ KÍCH HOẠT", font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), text_color="#93C5FD").pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(hero_text, text="Tối ưu hóa Lộ trình Học tập\nKiến tạo Tương lai Kỹ sư.", font=ctk.CTkFont(family=FONT_MAIN, size=28, weight="bold"), text_color="white", justify="left").pack(anchor="w")
        ctk.CTkButton(hero_text, text="Tiếp tục Học tập  ➔", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), 
                      fg_color=COLOR_PRIMARY, text_color="white", height=40, corner_radius=6,
                      command=lambda: self.controller.show_page("LearningPage")).pack(anchor="w", pady=(20, 0))

        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=content_pad-5, pady=10) 
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1, uniform="stat_cols")

        self.create_stat_card(stats_frame, 0, "Tiến độ Lộ trình", "65%", "📈")
        self.create_stat_card(stats_frame, 1, "Tín chỉ Tích lũy", "84 / 120", "📚")
        self.create_stat_card(stats_frame, 2, "Điểm GPA", "3.8", "🎓")
        self.create_stat_card(stats_frame, 3, "Độ khớp CV", "92%", "✨")

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=content_pad-5, pady=15)
        grid_frame.grid_columnconfigure(0, weight=6)
        grid_frame.grid_columnconfigure(1, weight=4)

        left_col = SaaSCard(grid_frame)
        left_col.grid(row=0, column=0, sticky="nsew", padx=5)
        header_l = ctk.CTkFrame(left_col, fg_color="transparent")
        header_l.pack(fill="x", padx=25, pady=(25, 15))
        ctk.CTkLabel(header_l, text="Học phần đang diễn ra", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkButton(header_l, text="Xem tất cả", fg_color="transparent", text_color=COLOR_PRIMARY, font=ctk.CTkFont(weight="bold")).pack(side="right")
        self.add_course_item(left_col, "Lập trình Python Nâng cao", "Tiến độ: 80%", COLOR_PRIMARY, 0.8)
        self.add_course_item(left_col, "Toán rời rạc & Thuật toán", "Tiến độ: 45%", "#F59E0B", 0.45)
        self.add_course_item(left_col, "Kỹ năng Giao tiếp Tiếng Anh", "Tiến độ: 15%", "#10B981", 0.15)

        right_col = SaaSCard(grid_frame)
        right_col.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(right_col, text="Sự kiện & Deadline", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=25, pady=(25, 15))
        self.add_event_item(right_col, "12 Th4", "Workshop Trí tuệ Nhân tạo", "08:00 Sáng - Online")
        self.add_event_item(right_col, "15 Th4", "Nộp Đồ án Cơ sở 2", "14:00 Chiều - Hệ thống")
        self.add_event_item(right_col, "20 Th4", "Ngày hội Việc làm IT", "Cả ngày - Hội trường A")

    def create_stat_card(self, parent, col, title, value, icon):
        card = SaaSCard(parent)
        card.grid(row=0, column=col, padx=5, sticky="nsew")
        top_box = ctk.CTkFrame(card, fg_color="transparent")
        top_box.pack(fill="x", padx=20, pady=(20, 5))
        ctk.CTkLabel(top_box, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(side="left")
        ctk.CTkLabel(top_box, text=icon, font=ctk.CTkFont(size=18)).pack(side="right")
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(0, 20))

    def add_course_item(self, parent, title, status, color, progress):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=10)
        
        # Biến title thành một nút bấm
        title_btn = ctk.CTkButton(
            frame, text=title, text_color=COLOR_TEXT_MAIN, 
            font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"),
            fg_color="transparent", hover_color=COLOR_BG_APP, anchor="w",
            command=lambda: self.controller.show_page("CourseDetailPage") # Lệnh chuyển trang
        )
        title_btn.pack(anchor="w", fill="x")
        
        ctk.CTkLabel(frame, text=status, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(anchor="w", pady=(0, 5), padx=10)
        ctk.CTkProgressBar(frame, progress_color=color, fg_color=COLOR_BG_APP, height=6, corner_radius=3).pack(fill="x", padx=10)
        ctk.CTkFrame(parent, height=1, fg_color=COLOR_BORDER).pack(fill="x", pady=(15, 0))

    def add_event_item(self, parent, date, title, time):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=10)
        date_box = ctk.CTkFrame(frame, fg_color=COLOR_PRIMARY_LIGHT, corner_radius=6, width=50, height=50)
        date_box.pack(side="left", padx=(0, 15))
        date_box.pack_propagate(False)
        ctk.CTkLabel(date_box, text=date.split()[0], font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_PRIMARY).pack(pady=(5,0))
        ctk.CTkLabel(date_box, text=date.split()[1], font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_PRIMARY).pack()
        txt_box = ctk.CTkFrame(frame, fg_color="transparent")
        txt_box.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(txt_box, text=title, text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(txt_box, text=time, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(anchor="w")