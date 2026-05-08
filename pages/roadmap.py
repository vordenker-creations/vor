import customtkinter as ctk
from config import *
from components import SaaSCard

class RoadmapPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        
        # Header Page
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(35, 15))
        ctk.CTkLabel(header, text="Lộ Trình & AI Mentor", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        # Container chia 2 cột chính
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=0)
        container.grid_columnconfigure(0, weight=3) # Bên trái chứa Lộ trình
        container.grid_columnconfigure(1, weight=7) # Bên phải mở rộng cho Dashboard Chat

        # ==========================================
        # LEFT PANEL: CÂY KỸ NĂNG HỌC THUẬT
        # ==========================================
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

        # ==========================================
        # RIGHT PANEL: AI ASSISTANCE DASHBOARD
        # ==========================================
        right_card = SaaSCard(container)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5)
        
        # 1. Header & Tabs Navigation
        chat_header = ctk.CTkFrame(right_card, fg_color="transparent", border_width=1, border_color=COLOR_BORDER)
        chat_header.pack(fill="x")
        
        tabs_frame = ctk.CTkFrame(chat_header, fg_color="transparent")
        tabs_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkButton(tabs_frame, text="COMMUNITY CHAT", fg_color="transparent", text_color=COLOR_PRIMARY, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), width=120, hover_color=COLOR_BG_APP).pack(side="left")
        ctk.CTkButton(tabs_frame, text="MENTORING", fg_color="transparent", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), width=100, hover_color=COLOR_BG_APP).pack(side="left")
        ctk.CTkButton(tabs_frame, text="PROJECT PARTNERS", fg_color="transparent", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), width=140, hover_color=COLOR_BG_APP).pack(side="left")
        
        # Đường highlight dưới Tab đang active
        ctk.CTkFrame(chat_header, height=2, fg_color=COLOR_PRIMARY, width=120).place(x=20, y=43)

        # 2. Main Chat Body (Split into Chat Area and AI Sidebar)
        chat_body = ctk.CTkFrame(right_card, fg_color="transparent")
        chat_body.pack(fill="both", expand=True)
        chat_body.grid_columnconfigure(0, weight=7) # Cột chat chính
        chat_body.grid_columnconfigure(1, weight=3) # Cột AI Summarizer

        # -- Chat Area --
        chat_area = ctk.CTkScrollableFrame(chat_body, fg_color="transparent")
        chat_area.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Render tin nhắn mẫu
        self.add_message(chat_area, "Khoa", "AI Engineer Student", "Đề xuất cho mình lộ trình học Machine Learning với.", "Vừa xong", is_ai=False, avatar="👤")
        self.add_message(chat_area, "AI Mentor", "Gemini 1.5 Pro", "Chào Khoa! Dựa trên nền tảng Python và C++ của bạn, mình khuyên bạn nên bắt đầu với các thư viện Pandas và NumPy trước. Bạn có muốn mình tạo một lộ trình chi tiết và đề xuất dự án luôn không?", "2 phút trước", is_ai=True, avatar="✨")
        self.add_message(chat_area, "DiverSo Member", "Computer Science", "Mình cũng đang học Python nâng cao, các bạn có khóa nào hay trên Udemy để tham khảo thêm không?", "5 phút trước", is_ai=False, avatar="👨‍💻")

        # -- AI Sidebar (Summarizer & Matching) --
        ai_sidebar = ctk.CTkFrame(chat_body, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        ai_sidebar.grid(row=0, column=1, sticky="nsew", padx=(5, 15), pady=15)

        # Chat Summarizer
        ctk.CTkLabel(ai_sidebar, text="AI CHAT SUMMARIZER", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(ai_sidebar, text="Tóm tắt: Cuộc thảo luận đang tập trung vào lộ trình phát triển AI, Machine Learning và các thư viện cốt lõi của Python (Pandas, NumPy).\n\nTừ khóa: #MachineLearning, #Python", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB, justify="left", wraplength=200).pack(anchor="w", padx=15)
        
        ctk.CTkFrame(ai_sidebar, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=15, pady=15)
        
        # Mentor Matching
        ctk.CTkLabel(ai_sidebar, text="AI MENTOR MATCHING", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(0, 10))
        self.add_mentor_match(ai_sidebar, "Nguyễn Hoàng", "Data Scientist", "95%")
        self.add_mentor_match(ai_sidebar, "Lê Trần", "ML Engineer", "88%")

        # 3. Message Input Area
        entry_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        entry_frame.pack(fill="x", padx=20, pady=15)
        
        entry_bg = ctk.CTkFrame(entry_frame, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        entry_bg.pack(fill="x", expand=True)
        
        entry = ctk.CTkEntry(entry_bg, placeholder_text="Type a message... (Gõ '/' để gọi AI)", height=45, fg_color="transparent", border_width=0, text_color=COLOR_TEXT_MAIN)
        entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # Nút AI Enhance
        btn_ai = ctk.CTkButton(entry_bg, text="✨ AI", width=40, height=35, fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, corner_radius=6, font=ctk.CTkFont(weight="bold"))
        btn_ai.pack(side="right", padx=(0, 5), pady=5)
        
        # Nút Send
        btn_send = ctk.CTkButton(entry_bg, text="➤", width=40, height=35, fg_color=COLOR_PRIMARY, text_color="white", corner_radius=6, font=ctk.CTkFont(size=16))
        btn_send.pack(side="right", padx=(0, 5), pady=5)

    def add_message(self, parent, name, role, text, time, is_ai, avatar):
        """Hàm render một khối tin nhắn trong khung Chat"""
        msg_container = ctk.CTkFrame(parent, fg_color="transparent")
        msg_container.pack(fill="x", pady=10, padx=5)

        # Cột Avatar
        avatar_col = ctk.CTkFrame(msg_container, fg_color="transparent", width=40)
        avatar_col.pack(side="left", fill="y")
        avatar_bg = COLOR_PRIMARY_LIGHT if is_ai else COLOR_BORDER
        avatar_label = ctk.CTkLabel(avatar_col, text=avatar, font=ctk.CTkFont(size=18), fg_color=avatar_bg, width=38, height=38, corner_radius=19)
        avatar_label.pack(anchor="n")

        # Cột Nội dung tin nhắn
        content_col = ctk.CTkFrame(msg_container, fg_color="transparent")
        content_col.pack(side="left", fill="x", expand=True, padx=(12, 0))

        # Dòng thông tin: Tên | Vai trò | Thời gian
        header_row = ctk.CTkFrame(content_col, fg_color="transparent")
        header_row.pack(fill="x")
        ctk.CTkLabel(header_row, text=name, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header_row, text=f"• {role}", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(side="left", padx=(5, 0))
        ctk.CTkLabel(header_row, text=time, font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(side="right", padx=(0, 10))

        # Khung chứa Text (Bubble)
        bubble_bg = COLOR_PRIMARY_LIGHT if is_ai else COLOR_BG_CARD
        border_col = COLOR_PRIMARY if is_ai else COLOR_BORDER
        
        bubble = ctk.CTkFrame(content_col, fg_color=bubble_bg, corner_radius=6, border_width=1, border_color=border_col)
        bubble.pack(anchor="w", pady=(5, 0), fill="x")
        
        ctk.CTkLabel(bubble, text=text, text_color=COLOR_TEXT_MAIN, justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=13), wraplength=400).pack(padx=15, pady=12, anchor="w")

    def add_mentor_match(self, parent, name, role, match_percent):
        """Hàm render một card mentor được AI đề xuất"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)
        
        avatar_lbl = ctk.CTkLabel(frame, text="👤", font=ctk.CTkFont(size=18), fg_color=COLOR_BORDER, width=32, height=32, corner_radius=16)
        avatar_lbl.pack(side="left", padx=(0, 10))
        
        info = ctk.CTkFrame(frame, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(info, text=name, font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(info, text=f"Thích hợp: {role}", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w")
        
        ctk.CTkLabel(frame, text=match_percent, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_PRIMARY).pack(side="right")