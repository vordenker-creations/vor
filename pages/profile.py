import customtkinter as ctk
from config import *
from components import SaaSCard

class ProfilePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(
            self, text="Tài khoản & Trình tạo CV", 
            font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w", padx=35, pady=(35, 15))

        main_box = ctk.CTkFrame(self, fg_color="transparent")
        main_box.pack(fill="both", expand=True, padx=30)
        main_box.grid_columnconfigure((0,1), weight=1)

        form = SaaSCard(main_box)
        form.grid(row=0, column=0, sticky="nsew", padx=5)
        header_form = ctk.CTkFrame(form, fg_color="transparent")
        header_form.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(header_form, text="Thiết lập Tài khoản", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        
        avatar_frame = ctk.CTkFrame(form, fg_color="transparent")
        avatar_frame.pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(avatar_frame, text="👤", font=ctk.CTkFont(size=40), text_color=COLOR_PRIMARY).pack(side="left", padx=(0, 15))
        ctk.CTkButton(avatar_frame, text="Tải ảnh lên", fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, font=ctk.CTkFont(family=FONT_MAIN, weight="bold"), height=30).pack(side="left")

        fields = [
            ("Họ và tên", "Bùi Hậu"),
            ("Email liên hệ", "hau.bui@university.edu.vn"),
            ("Chuyên ngành", "Công nghệ Thông tin"),
            ("Kỹ năng chính", "Java, C++, Python, SQL Server"),
            ("Liên kết GitHub", "github.com/hau-workspace")
        ]
        
        for label, placeholder in fields:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=30, pady=(5, 5))
            entry = ctk.CTkEntry(form, height=40, corner_radius=6, fg_color=COLOR_BG_APP, border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN)
            entry.insert(0, placeholder) 
            entry.pack(fill="x", padx=30, pady=(0, 10))
        
        ctk.CTkButton(form, text="Lưu thay đổi", fg_color=COLOR_PRIMARY, text_color="white", corner_radius=6, height=40, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")).pack(pady=(15, 25), padx=30, fill="x")

        preview = SaaSCard(main_box)
        preview.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(preview, text="Bản xem trước CV", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(pady=(25, 15))
        
        paper = ctk.CTkFrame(preview, fg_color=COLOR_BG_CARD, width=340, height=480, corner_radius=0, border_width=1, border_color=COLOR_BORDER)
        paper.pack(pady=10)
        paper.pack_propagate(False)
        
        top_paper = ctk.CTkFrame(paper, fg_color=COLOR_BG_APP, corner_radius=0, height=90)
        top_paper.pack(fill="x")
        ctk.CTkLabel(top_paper, text="BÙI HẬU", font=ctk.CTkFont(family=FONT_MAIN, size=20, weight="bold"), text_color=COLOR_PRIMARY).pack(pady=(20, 2))
        ctk.CTkLabel(top_paper, text="Sinh viên Công nghệ Thông tin", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack()
        
        body_paper = ctk.CTkFrame(paper, fg_color="transparent")
        body_paper.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(body_paper, text="KỸ NĂNG CHUYÊN MÔN", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(body_paper, text="• Ngôn ngữ: Java, C++, Python\n• Cơ sở dữ liệu: SQL Server\n• Công cụ quản lý: Git / GitHub", justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(anchor="w", pady=(5, 15))

        ctk.CTkLabel(body_paper, text="DỰ ÁN NỔI BẬT", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        
        p1_frame = ctk.CTkFrame(body_paper, fg_color="transparent")
        p1_frame.pack(fill="x", pady=(5, 8))
        ctk.CTkLabel(p1_frame, text="Phần mềm Quản lý Truy cập Internet", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(p1_frame, text="- Thiết kế GUI thân thiện bằng Java Swing\n- Xây dựng và tích hợp logic Database SQL Server", justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w")

        p2_frame = ctk.CTkFrame(body_paper, fg_color="transparent")
        p2_frame.pack(fill="x", pady=(5, 0))
        ctk.CTkLabel(p2_frame, text="Dự án web_Edupro", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(p2_frame, text="- Quản lý mã nguồn dự án qua Repository GitHub", justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w")

        ctk.CTkButton(preview, text="Xuất File PDF", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), fg_color=COLOR_PRIMARY, text_color="white", corner_radius=6, height=42).pack(pady=20, padx=40, fill="x")