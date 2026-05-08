import customtkinter as ctk
from config import *
from components import SaaSCard

class RecruitmentPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        
        # 1. Header Tiêu đề
        ctk.CTkLabel(self, text="Thị Trường Tuyển Dụng", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 20))

        # 2. Khung chứa Grid Lưới các công việc
        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=25)
        # Chia đều 3 cột
        grid_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

        # Dữ liệu mô phỏng giống hệt thiết kế
        jobs_data = [
            ("Công ty Cổ phần VNG", "TP. Hồ Chí Minh", "Thực tập sinh AI Engineer\n(Computer Vision)", "20tr - 35tr VNĐ/tháng", "Python, PyTorch, SQL", None),
            ("FPT Software", "Hà Nội", "Chuyên viên Machine Learning\n(NLP)", "Thỏa thuận", "Python, PyTorch, SQL", None),
            ("MoMo (M-Service)", "TP. HCM, Hà Nội", "Data Analyst - Fintech\n", "Thỏa thuận", "Python, PyTorch, SQL", "new"),
            ("Shopee Vietnam", "TP. HCM, Hà Nội", "Senior AI Researcher -\nE-commerce", "20tr - 35tr VNĐ/tháng", "Python, PyTorch, SQL", "new"),
            ("VNPAY", "TP. HCM, Hà Nội", "Data Scientist - Risk & Fraud\n", "Thỏa thuận", "Python, PyTorch, SQL", "featured"),
            ("VinAI Research", "TP. HCM, Hà Nội", "Generative AI Research\nEngineer", "Thỏa thuận", "Python, PyTorch, Engineer", "new"),
            ("Google Vietnam", "TP. HCM, Hà Nội", "Generative AI Research\nEngineer", "20tr - 35tr VNĐ/tháng", "Python, PyTorch, SQL", "new"),
            ("Công ty Cổ phần VNG", "TP. HCM, Hà Nội", "Thực tập sinh AI Engineer\n", "20tr - 35tr VNĐ/tháng", "Python, PyTorch, SQL", "new"),
            ("VinAI Research", "TP. HCM, Hà Nội", "Generative AI Research\nEngineer", "Thỏa thuận", "Python, PyTorch, SQL", "new")
        ]

        # Render danh sách Card
        for i, job in enumerate(jobs_data):
            row = i // 3
            col = i % 3
            self.create_job_card(grid_container, row, col, *job)

        # 3. Phân trang (Pagination) ở dưới cùng
        pagination_frame = ctk.CTkFrame(self, fg_color="transparent")
        pagination_frame.pack(pady=30)
        
        ctk.CTkButton(pagination_frame, text="|<", width=30, fg_color="transparent", text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(side="left", padx=2)
        ctk.CTkButton(pagination_frame, text="<", width=30, fg_color="transparent", text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(side="left", padx=2)
        ctk.CTkLabel(pagination_frame, text="Trang 1 of 5", font=ctk.CTkFont(family=FONT_MAIN, size=13)).pack(side="left", padx=15)
        ctk.CTkButton(pagination_frame, text=">", width=30, fg_color="transparent", text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(side="left", padx=2)
        ctk.CTkButton(pagination_frame, text=">|", width=30, fg_color="transparent", text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP).pack(side="left", padx=2)

    def create_job_card(self, parent, row, col, company, location, title, salary, skills, badge):
        """Hàm dựng UI cho 1 Card Công việc"""
        card = SaaSCard(parent)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Dòng 1: Tên Công ty + Vị trí + Badge
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        comp_frame = ctk.CTkFrame(header, fg_color="transparent")
        comp_frame.pack(side="left")
        ctk.CTkLabel(comp_frame, text="🏢", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(comp_frame, text=company, font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(side="left")

        # Thiết lập màu sắc cho Badge (new / featured)
        loc_frame = ctk.CTkFrame(header, fg_color="transparent")
        loc_frame.pack(side="right")
        
        if badge == "new":
            badge_bg = "#FFEDD5" # Cam nhạt
            badge_fg = "#EA580C" # Cam đậm
            badge_lbl = ctk.CTkLabel(loc_frame, text=badge, fg_color=badge_bg, text_color=badge_fg, 
                                     corner_radius=4, font=ctk.CTkFont(size=10, weight="bold"), width=35, height=20)
            badge_lbl.pack(side="right", padx=(10, 0))
        elif badge == "featured":
            badge_bg = "#D1FAE5" # Xanh lục nhạt
            badge_fg = "#059669" # Xanh lục đậm
            badge_lbl = ctk.CTkLabel(loc_frame, text=badge, fg_color=badge_bg, text_color=badge_fg, 
                                     corner_radius=4, font=ctk.CTkFont(size=10, weight="bold"), width=50, height=20)
            badge_lbl.pack(side="right", padx=(10, 0))

        ctk.CTkLabel(loc_frame, text=f"📍 {location}", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(side="right")

        # Dòng 2: Tiêu đề công việc
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN, justify="left", anchor="w").pack(fill="x", padx=20, pady=(5, 5))
        
        # Dòng 3: Mức lương
        ctk.CTkLabel(card, text=f"💰 {salary}", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN, anchor="w").pack(fill="x", padx=20, pady=(0, 2))
                     
        # Dòng 4: Kỹ năng yêu cầu
        ctk.CTkLabel(card, text=skills, font=ctk.CTkFont(family=FONT_MAIN, size=13), 
                     text_color=COLOR_TEXT_SUB, anchor="w").pack(fill="x", padx=20, pady=(0, 20))

        # Dòng 5: Nút Ứng tuyển
        btn = ctk.CTkButton(card, text="Ứng tuyển ngay", fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, 
                            font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), corner_radius=6, height=35)
        btn.pack(anchor="w", padx=20, pady=(0, 25))