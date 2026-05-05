import customtkinter as ctk
import tkinter as tk
from datetime import datetime

#cau hinh ht & màu
ctk.set_appearance_mode("light")

FONT_MAIN = "Segoe UI" 

COLOR_BG_APP = "#F1F5F9"      
COLOR_BG_CARD = "#FFFFFF"     
COLOR_PRIMARY = "#2563EB"     
COLOR_PRIMARY_LIGHT = "#EFF6FF"
COLOR_TEXT_MAIN = "#0F172A"    
COLOR_TEXT_SUB = "#64748B"    
COLOR_BORDER = "#E2E8F0"     

class AICareerBridgeEnterprise(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI-Career Bridge - Enterprise Edition")
        self.geometry("1200x700") # vừa màn        self.configure(fg_color=COLOR_BG_APP)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        self.frames = {}
        self.nav_buttons = {}
        self.active_page = None

        self.setup_sidebar()
        self.setup_topbar()
        
        #ndung chính
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_APP)
        self.main_container.grid(row=1, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        #khởi tạo các trang
        for PageClass in (DashboardPage, RoadmapPage, CommunityPage, RecruitmentPage, ProfilePage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
        #trang mặc định
        self.show_page("DashboardPage")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.pack_propagate(False)
        
        # Logo Area
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(35, 40), fill="x", padx=25)
        ctk.CTkLabel(logo_frame, text="🎓", font=ctk.CTkFont(size=32), text_color=COLOR_PRIMARY).pack(side="left", padx=(0, 10))
        
        text_logo_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_logo_frame.pack(side="left")
        ctk.CTkLabel(text_logo_frame, text="BRIDGE", font=ctk.CTkFont(family=FONT_MAIN, size=20, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=0)
        ctk.CTkLabel(text_logo_frame, text="EDUCATION", font=ctk.CTkFont(family=FONT_MAIN, size=10, weight="bold"), text_color=COLOR_PRIMARY).pack(anchor="w", pady=0)
        # Menu Title
        ctk.CTkLabel(self.sidebar, text="MAIN MENU", font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=25, pady=(0, 15))
        #menu Buttons
        self.create_nav_btn("DashboardPage", "📊", "Tổng quan")
        self.create_nav_btn("RoadmapPage", "🧭", "Lộ trình & AI")
        self.create_nav_btn("CommunityPage", "👥", "Cộng đồng")
        self.create_nav_btn("RecruitmentPage", "💼", "Tuyển dụng")
        self.create_nav_btn("ProfilePage", "👤", "Hồ sơ & CV")
        # Bottom Pro Upgrade Card
        upgrade_box = ctk.CTkFrame(self.sidebar, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        upgrade_box.pack(side="bottom", fill="x", padx=20, pady=30)
        ctk.CTkLabel(upgrade_box, text="Gói Pro - 30 Ngày", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(pady=(15, 5))
        ctk.CTkProgressBar(upgrade_box, progress_color=COLOR_PRIMARY, fg_color=COLOR_BORDER, height=6).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(upgrade_box, text="Nâng cấp", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), fg_color=COLOR_PRIMARY, text_color="white", height=30, corner_radius=6).pack(pady=(5, 15), padx=20, fill="x")
    def create_nav_btn(self, page_name, icon, text):
        btn_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_container.pack(fill="x", padx=15, pady=2)
        
        indicator = ctk.CTkFrame(btn_container, width=4, fg_color="transparent", corner_radius=2)
        indicator.pack(side="left", fill="y", pady=5)
        
        btn = ctk.CTkButton(btn_container, text=f"{icon}   {text}", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"),
                            anchor="w", fg_color="transparent", text_color=COLOR_TEXT_SUB,
                            hover_color=COLOR_BG_APP, height=42, corner_radius=6)
        btn.configure(command=lambda p=page_name: self.show_page(p))
        btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        self.nav_buttons[page_name] = {"btn": btn, "indicator": indicator}

    def setup_topbar(self):
        #top Navbar
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER)
        self.topbar.grid(row=0, column=1, sticky="nsew")
        #search Bar
        search_frame = ctk.CTkFrame(self.topbar, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        search_frame.pack(side="left", padx=30, pady=15)
        ctk.CTkLabel(search_frame, text="🔍", text_color=COLOR_TEXT_SUB).pack(side="left", padx=(10, 5))
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm khóa học, kỹ năng...", width=300, height=35, fg_color="transparent", border_width=0, text_color=COLOR_TEXT_MAIN)
        search_entry.pack(side="left", padx=(0, 10))
        # Right Actions
        right_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        right_frame.pack(side="right", padx=30, pady=15)
        
        current_date = datetime.now().strftime("%d %b, %Y")
        ctk.CTkLabel(right_frame, text=f"📅 {current_date}", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(side="left", padx=20)
        
        ctk.CTkButton(right_frame, text="🔔", width=40, height=40, fg_color="transparent", border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN, corner_radius=8).pack(side="left", padx=(0, 15))
        # User Avatar Header
        user_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        user_frame.pack(side="left")
        ctk.CTkLabel(user_frame, text="Nguyễn Văn A", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="e")
        ctk.CTkLabel(user_frame, text="Sinh viên IT", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="e")
        ctk.CTkLabel(right_frame, text="👤", font=ctk.CTkFont(size=24), text_color=COLOR_PRIMARY).pack(side="left", padx=(10, 0))

    def show_page(self, page_name):
        #reset
        for name, elements in self.nav_buttons.items():
            elements["btn"].configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)
            elements["indicator"].configure(fg_color="transparent")
        
        #style active
        active_elements = self.nav_buttons[page_name]
        active_elements["btn"].configure(fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY)
        active_elements["indicator"].configure(fg_color=COLOR_PRIMARY)
        for frame in self.frames.values():
            frame.grid_forget()
        if page_name in self.frames:
            self.frames[page_name].grid(row=0, column=0, sticky="nsew")

#helper
class SaaSCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLOR_BG_CARD, corner_radius=8, border_width=1, border_color=COLOR_BORDER, **kwargs)

# TRANG 1: DASHBOARD
class DashboardPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        
        content_pad = 35
        #hERO BANNER 
        hero_banner = ctk.CTkFrame(self, fg_color="#1E3A8A", corner_radius=12) # Xanh Navy cực sang
        hero_banner.pack(fill="x", padx=content_pad, pady=(content_pad, 15))
        
        hero_text = ctk.CTkFrame(hero_banner, fg_color="transparent")
        hero_text.pack(side="left", padx=40, pady=35)
        
        ctk.CTkLabel(hero_text, text="HỆ THỐNG AI MENTOR ĐÃ KÍCH HOẠT", font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), text_color="#93C5FD").pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(hero_text, text="Tối ưu hóa Lộ trình Học tập\nKiến tạo Tương lai Kỹ sư.", font=ctk.CTkFont(family=FONT_MAIN, size=28, weight="bold"), text_color="white", justify="left").pack(anchor="w")
        ctk.CTkButton(hero_text, text="Tiếp tục Học tập  ➔", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), fg_color=COLOR_PRIMARY, text_color="white", height=40, corner_radius=6).pack(anchor="w", pady=(20, 0))
        # THỐNG KÊ
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=content_pad-5, pady=10) # Bù trừ lề của lưới
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1, uniform="stat_cols")

        self.create_stat_card(stats_frame, 0, "Tiến độ Lộ trình", "65%", "📈")
        self.create_stat_card(stats_frame, 1, "Tín chỉ Tích lũy", "84 / 120", "📚")
        self.create_stat_card(stats_frame, 2, "Điểm GPA", "3.8", "🎓")
        self.create_stat_card(stats_frame, 3, "Độ khớp CV", "92%", "✨")

        # NỘI DUNG CHÍNH
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=content_pad-5, pady=15)
        grid_frame.grid_columnconfigure(0, weight=6)
        grid_frame.grid_columnconfigure(1, weight=4)
        # Cột Trái
        left_col = SaaSCard(grid_frame)
        left_col.grid(row=0, column=0, sticky="nsew", padx=5)
        
        header_l = ctk.CTkFrame(left_col, fg_color="transparent")
        header_l.pack(fill="x", padx=25, pady=(25, 15))
        ctk.CTkLabel(header_l, text="Học phần đang diễn ra", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkButton(header_l, text="Xem tất cả", fg_color="transparent", text_color=COLOR_PRIMARY, font=ctk.CTkFont(weight="bold")).pack(side="right")
        
        self.add_course_item(left_col, "Lập trình Python Nâng cao", "Tiến độ: 80%", COLOR_PRIMARY, 0.8)
        self.add_course_item(left_col, "Toán rời rạc & Thuật toán", "Tiến độ: 45%", "#F59E0B", 0.45)
        self.add_course_item(left_col, "Kỹ năng Giao tiếp Tiếng Anh", "Tiến độ: 15%", "#10B981", 0.15)

        # Cột Phải
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
        ctk.CTkLabel(frame, text=title, text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(frame, text=status, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(anchor="w", pady=(0, 5))
        ctk.CTkProgressBar(frame, progress_color=color, fg_color=COLOR_BG_APP, height=6, corner_radius=3).pack(fill="x")
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

# TRANG 2: ROADMAP
class RoadmapPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(35, 15))
        ctk.CTkLabel(header, text="Lộ Trình & AI Mentor", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=0)
        container.grid_columnconfigure(0, weight=5)
        container.grid_columnconfigure(1, weight=5)

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

        right_card = SaaSCard(container)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5)
        
        chat_header = ctk.CTkFrame(right_card, fg_color="transparent", border_width=1, border_color=COLOR_BORDER)
        chat_header.pack(fill="x")
        ctk.CTkLabel(chat_header, text="✨  AI Mentor (Gemini)", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left", padx=20, pady=20)
        
        chat_area = ctk.CTkScrollableFrame(right_card, fg_color="transparent")
        chat_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_bubble(chat_area, "Đề xuất cho mình lộ trình AI Engineer.", True)
        self.add_bubble(chat_area, "Mình đã cập nhật lộ trình. Bạn nên học 'Deep Learning' vào kỳ này. Mình có đính kèm tài liệu tham khảo trong hệ thống.", False)

        entry_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        entry_frame.pack(fill="x", padx=20, pady=20)
        entry = ctk.CTkEntry(entry_frame, placeholder_text="Hỏi Mentor...", height=40, corner_radius=6, fg_color=COLOR_BG_APP, border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(entry_frame, text="Gửi", width=60, height=40, fg_color=COLOR_PRIMARY, text_color="white", corner_radius=6, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")).pack(side="right")

    def add_bubble(self, parent, text, is_user):
        bg = COLOR_PRIMARY_LIGHT if is_user else COLOR_BG_APP
        border = COLOR_PRIMARY_LIGHT if is_user else COLOR_BORDER
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", pady=8)
        bubble = ctk.CTkFrame(container, fg_color=bg, corner_radius=8, border_width=1, border_color=border)
        bubble.pack(side="right" if is_user else "left", padx=10)
        ctk.CTkLabel(bubble, text=text, text_color=COLOR_TEXT_MAIN, justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=13), wraplength=250).pack(padx=15, pady=10)

# CÁC TRANG CÒN LẠI 
class CommunityPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Cộng đồng & Thảo luận", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 15))
        for i in range(3):
            card = SaaSCard(self)
            card.pack(fill="x", padx=35, pady=8)
            ctk.CTkLabel(card, text="[Hỏi đáp] Tài liệu ôn thi Cấu trúc Dữ liệu", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=25, pady=(20, 5))
            ctk.CTkLabel(card, text="Đăng bởi: Học viên A • 2 giờ trước • 15 bình luận", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=25, pady=(0, 20))

class RecruitmentPage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Thị Trường Tuyển Dụng", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 15))
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=30)
        grid.grid_columnconfigure((0, 1), weight=1)
        for i in range(4):
            card = SaaSCard(grid)
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            ctk.CTkLabel(card, text="🏢 Công ty Cổ phần VNG", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=25, pady=(25, 2))
            ctk.CTkLabel(card, text="Thực tập sinh AI Engineer", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=25)
            ctk.CTkButton(card, text="Ứng tuyển ngay", fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, height=35, corner_radius=6, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=25, pady=25)

#HỒ SƠ & TÀI KHOẢN
class ProfilePage(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(
            self, text="Hồ sơ & Trình tạo CV", 
            font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w", padx=35, pady=(35, 15))

        main_box = ctk.CTkFrame(self, fg_color="transparent")
        main_box.pack(fill="both", expand=True, padx=30)
        main_box.grid_columnconfigure((0,1), weight=1)

        # CỘT TRÁI: THIẾT LẬP TÀI KHOẢN
        form = SaaSCard(main_box)
        form.grid(row=0, column=0, sticky="nsew", padx=5)
        
        header_form = ctk.CTkFrame(form, fg_color="transparent")
        header_form.pack(fill="x", padx=30, pady=(25, 15))
        ctk.CTkLabel(
            header_form, text="Thiết lập Tài khoản", 
            font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(side="left")
        
        # Avatar Upload Section
        avatar_frame = ctk.CTkFrame(form, fg_color="transparent")
        avatar_frame.pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(
            avatar_frame, text="👤", font=ctk.CTkFont(size=40), text_color=COLOR_PRIMARY
        ).pack(side="left", padx=(0, 15))
        ctk.CTkButton(
            avatar_frame, text="Tải ảnh lên", 
            fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, 
            font=ctk.CTkFont(family=FONT_MAIN, weight="bold"), height=30
        ).pack(side="left")
        #trường thông tin
        fields = [
            ("Họ và tên", "Ly"),
            ("Email liên hệ", "ly.student@university.edu.vn"),
            ("Chuyên ngành", "Công nghệ Thông tin"),
            ("Kỹ năng chính", "Java, C++, Python, SQL Server"),
            ("Liên kết GitHub", "github.com/ly-workspace")
        ]
        
        for label, placeholder in fields:
            ctk.CTkLabel(
                form, text=label, 
                font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), 
                text_color=COLOR_TEXT_SUB
            ).pack(anchor="w", padx=30, pady=(5, 5))
            
            entry = ctk.CTkEntry(
                form, height=40, corner_radius=6, fg_color=COLOR_BG_APP, 
                border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN
            )
            entry.insert(0, placeholder) # Điền sẵn dữ liệu mẫu
            entry.pack(fill="x", padx=30, pady=(0, 10))
        
        ctk.CTkButton(
            form, text="Lưu thay đổi", 
            fg_color=COLOR_PRIMARY, text_color="white", 
            corner_radius=6, height=40, font=ctk.CTkFont(family=FONT_MAIN, weight="bold")
        ).pack(pady=(15, 25), padx=30, fill="x")

        # CỘT PHẢI: XEM TRƯỚC CV
        preview = SaaSCard(main_box)
        preview.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(
            preview, text="Bản xem trước CV", 
            font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(pady=(25, 15))
        
        # Layout A4
        paper = ctk.CTkFrame(
            preview, fg_color=COLOR_BG_CARD, width=340, height=480, 
            corner_radius=0, border_width=1, border_color=COLOR_BORDER
        )
        paper.pack(pady=10)
        paper.pack_propagate(False)
        
        # Header CV
        top_paper = ctk.CTkFrame(paper, fg_color=COLOR_BG_APP, corner_radius=0, height=90)
        top_paper.pack(fill="x")
        ctk.CTkLabel(
            top_paper, text="LY", 
            font=ctk.CTkFont(family=FONT_MAIN, size=20, weight="bold"), 
            text_color=COLOR_PRIMARY
        ).pack(pady=(20, 2))
        ctk.CTkLabel(
            top_paper, text="Sinh viên Công nghệ Thông tin", 
            font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB
        ).pack()
        
        # Body CV
        body_paper = ctk.CTkFrame(paper, fg_color="transparent")
        body_paper.pack(fill="both", expand=True, padx=25, pady=20)

        # Kỹ năng
        ctk.CTkLabel(
            body_paper, text="KỸ NĂNG CHUYÊN MÔN", 
            font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w")
        ctk.CTkLabel(
            body_paper, 
            text="• Ngôn ngữ: Java, C++, Python\n• Cơ sở dữ liệu: SQL Server\n• Công cụ quản lý: Git / GitHub", 
            justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=12), 
            text_color=COLOR_TEXT_SUB
        ).pack(anchor="w", pady=(5, 15))

        # Dự án
        ctk.CTkLabel(
            body_paper, text="DỰ ÁN NỔI BẬT", 
            font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w")
        
        # Dự án 1
        p1_frame = ctk.CTkFrame(body_paper, fg_color="transparent")
        p1_frame.pack(fill="x", pady=(5, 8))
        ctk.CTkLabel(
            p1_frame, text="Phần mềm Quản lý Truy cập Internet", 
            font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w")
        ctk.CTkLabel(
            p1_frame, 
            text="- Thiết kế GUI thân thiện bằng Java Swing\n- Xây dựng và tích hợp logic Database SQL Server", 
            justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=11), 
            text_color=COLOR_TEXT_SUB
        ).pack(anchor="w")

        # Dự án 2
        p2_frame = ctk.CTkFrame(body_paper, fg_color="transparent")
        p2_frame.pack(fill="x", pady=(5, 0))
        ctk.CTkLabel(
            p2_frame, text="Dự án web_Edupro", 
            font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), 
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w")
        ctk.CTkLabel(
            p2_frame, 
            text="- Quản lý mã nguồn dự án qua Repository GitHub", 
            justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=11), 
            text_color=COLOR_TEXT_SUB
        ).pack(anchor="w")

        # Xuất PDF
        ctk.CTkButton(
            preview, text="Xuất File PDF", 
            font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), 
            fg_color=COLOR_PRIMARY, text_color="white", 
            corner_radius=6, height=42
        ).pack(pady=20, padx=40, fill="x")

if __name__ == "__main__":
    app = AICareerBridgeEnterprise()
    app.mainloop()