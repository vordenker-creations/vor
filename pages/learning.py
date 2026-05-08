import customtkinter as ctk
from config import *
from components import SaaSCard

class LearningPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        content_pad = 35

        # 1. Header Section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=content_pad, pady=(content_pad, 10))
        
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(title_box, text="AI Art Creation Studio", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Nâng cao kỹ năng - Tiếp tục học tập", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=14), 
                     text_color=COLOR_TEXT_SUB).pack(anchor="w")
        
        # 2. Breadcrumb
        breadcrumb_frame = ctk.CTkFrame(self, fg_color="transparent")
        breadcrumb_frame.pack(fill="x", padx=content_pad, pady=(0, 20))
        
        ctk.CTkButton(breadcrumb_frame, text="Dashboard", fg_color="transparent", text_color=COLOR_TEXT_SUB, 
                      hover_color=COLOR_BG_APP, width=60, font=ctk.CTkFont(size=12),
                      command=lambda: self.controller.show_page("DashboardPage")).pack(side="left")
        ctk.CTkLabel(breadcrumb_frame, text=" > Khóa học", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=12), 
                     text_color=COLOR_TEXT_SUB).pack(side="left")

        # 3. Main Content Area (Grid)
        content_grid = ctk.CTkFrame(self, fg_color="transparent")
        content_grid.pack(fill="both", expand=True, padx=content_pad-5)
        content_grid.grid_columnconfigure(0, weight=7)
        content_grid.grid_columnconfigure(1, weight=3)

        left_col = ctk.CTkFrame(content_grid, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=5)
        
        right_col = ctk.CTkFrame(content_grid, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=5)

        # Left Column: "Học phần của bạn"
        ctk.CTkLabel(left_col, text="Học phần của bạn", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 15))

        course_grid = ctk.CTkFrame(left_col, fg_color="transparent")
        course_grid.pack(fill="both", expand=True)
        course_grid.grid_columnconfigure((0, 1), weight=1)

        # Course Card 1
        self.create_course_card(course_grid, 0, 0, "Lập trình Python Nâng cao", "80% Hoàn thành", 0.8, 
                                [("Xử lý dữ liệu với Pandas", "Đã xong"), 
                                 ("Mô hình học máy với TensorFlow", "Đang học, Bài 12/15"),
                                 ("Thực hành Tạo thành", "Đã xong")])

        # Course Card 2
        self.create_course_card(course_grid, 0, 1, "Tạo Ảnh Nghệ Thuật với AI", "35% Hoàn thành", 0.35,
                                [("Prompt Engineering Cơ bản", "Đã xong"),
                                 ("Điều khiển Kiểu dáng & Tỷ lệ", "Đang học, Bài 4/10"),
                                 ("Thực hành Tạo Ảnh", "Sẵn sàng")])
        
        # Course Card 3 (Architecture)
        self.create_course_card(course_grid, 1, 0, "Kiến trúc Bền vững với AI", "55% Hoàn thành", 0.55,
                                [("Mô phỏng Năng lượng", "Đã xong"),
                                 ("Lựa chọn Vật liệu thông minh", "Đang học, Bài 7/12")])

        # Right Column: "Sự kiện & Deadline"
        deadline_card = SaaSCard(right_col)
        deadline_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(deadline_card, text="Sự kiện & Deadline", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 15))
        
        self.add_event_item(deadline_card, "12", "Th4", "Workshop AI", ["Ras Sàng", "Anime", "Abstract"])
        self.add_event_item(deadline_card, "15", "Th4", "Nộp đồ án Cơ 2", ["1:1", "4:3"])

        # Creativity Level Card
        creativity_card = SaaSCard(right_col)
        creativity_card.pack(fill="x")
        ctk.CTkLabel(creativity_card, text="Mức độ sáng tạo", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        
        creativity_pb = ctk.CTkProgressBar(creativity_card, height=8, progress_color="#10B981")
        creativity_pb.pack(fill="x", padx=20, pady=10)
        creativity_pb.set(0.75)

    def create_course_card(self, parent, row, col, title, progress_text, progress_val, tasks):
        card = SaaSCard(parent)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Image placeholder
        img_placeholder = ctk.CTkFrame(card, height=120, fg_color=COLOR_BG_APP, corner_radius=6)
        img_placeholder.pack(fill="x", padx=15, pady=(15, 10))
        ctk.CTkLabel(img_placeholder, text="📷", font=ctk.CTkFont(size=40)).place(relx=0.5, rely=0.5, anchor="center")

        # Title and menu
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15)
        ctk.CTkLabel(header, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header, text="⋮", font=ctk.CTkFont(size=16), text_color=COLOR_TEXT_SUB).pack(side="right")

        # Progress bar
        progress_frame = ctk.CTkFrame(card, fg_color="transparent")
        progress_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        pb = ctk.CTkProgressBar(progress_frame, height=6, progress_color=COLOR_PRIMARY)
        pb.pack(fill="x")
        pb.set(progress_val)
        
        ctk.CTkLabel(progress_frame, text=progress_text, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w", pady=(2, 0))

        # Tasks
        for task_name, status in tasks:
            task_frame = ctk.CTkFrame(card, fg_color="transparent")
            task_frame.pack(fill="x", padx=15, pady=2)
            icon = "✓" if "Đã xong" in status else "🔵"
            color = COLOR_PRIMARY if "Đã xong" in status else COLOR_TEXT_SUB
            ctk.CTkLabel(task_frame, text=icon, text_color=color, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 5))
            ctk.CTkLabel(task_frame, text=f"{task_name} - {status}", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MAIN, wraplength=180, justify="left").pack(side="left")

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(15, 15))
        
        primary_btn_text = "Tiếp tục bài học"
        if "Studio" in title or "Tạo Ảnh" in title: primary_btn_text = "Đến Studio"
        if "Kiến trúc" in title: primary_btn_text = "Mở đồ án"

        secondary_btn_text = "Xem chi tiết"
        if "Tạo Ảnh" in title: secondary_btn_text = "Tải nguyên liệu"
        if "Kiến trúc" in title: secondary_btn_text = "Xem tài liệu"

        ctk.CTkButton(btn_frame, text=primary_btn_text, 
                      fg_color=COLOR_PRIMARY, text_color="white", height=32, font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"),
                      command=lambda: self.controller.show_page("CourseDetailPage")).pack(side="left", expand=True, padx=(0, 5))
        
        ctk.CTkButton(btn_frame, text=secondary_btn_text, 
                      fg_color=COLOR_BG_APP, text_color=COLOR_TEXT_MAIN, height=32, font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold")).pack(side="left", expand=True, padx=(5, 0))

    def add_event_item(self, parent, day, month, title, tags):
        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.pack(fill="x", padx=20, pady=10)
        
        date_box = ctk.CTkFrame(item, width=45, height=50, fg_color=COLOR_PRIMARY_LIGHT, corner_radius=6)
        date_box.pack(side="left")
        date_box.pack_propagate(False)
        ctk.CTkLabel(date_box, text=day, font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_PRIMARY).pack(pady=(5, 0))
        ctk.CTkLabel(date_box, text=month, font=ctk.CTkFont(size=10), text_color=COLOR_PRIMARY).pack()

        info_box = ctk.CTkFrame(item, fg_color="transparent")
        info_box.pack(side="left", padx=10, fill="both", expand=True)
        ctk.CTkLabel(info_box, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        
        tag_frame = ctk.CTkFrame(info_box, fg_color="transparent")
        tag_frame.pack(fill="x", pady=(2, 0))
        for tag in tags:
            ctk.CTkButton(tag_frame, text=tag, height=22, width=60, fg_color=COLOR_BG_APP, text_color=COLOR_TEXT_SUB, 
                          font=ctk.CTkFont(family=FONT_MAIN, size=10), corner_radius=4).pack(side="left", padx=(0, 4))
