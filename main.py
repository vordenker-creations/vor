
import customtkinter as ctk
from datetime import datetime
from PIL import Image
import os

# Import cấu hình
from config import *

# Import các trang từ thư mục pages
from pages.dashboard import DashboardPage
from pages.roadmap import RoadmapPage
from pages.community import CommunityPage
from pages.recruitment import RecruitmentPage
from pages.profile import ProfilePage

ctk.set_appearance_mode("light")

class AICareerBridgeEnterprise(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI-Career Bridge - Enterprise Edition")
        self.geometry("1200x700") 
        self.configure(fg_color=COLOR_BG_APP)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frames = {}
        self.nav_buttons = {}

        self.setup_sidebar()
        self.setup_topbar()
        
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_APP)
        self.main_container.grid(row=1, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Khởi tạo tất cả các trang và lưu vào dictionary frames
        for PageClass in (DashboardPage, RoadmapPage, CommunityPage, RecruitmentPage, ProfilePage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame

        self.show_page("DashboardPage")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.pack_propagate(False)
        
        # --- BẮT ĐẦU PHẦN CẬP NHẬT LOGO ---
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        # Thêm padx=20 để cả cụm logo cách mép trái của sidebar một khoảng cho đẹp
        logo_frame.pack(pady=(25, 15), fill="x", padx=20) 
        
        try:
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_dir, "logoAI.png")
            logo_img_data = Image.open(logo_path)
            
            # 1. Thu nhỏ logo xuống cỡ 45x45 (hoặc 50x50 tùy bạn)
            my_logo = ctk.CTkImage(light_image=logo_img_data, dark_image=logo_img_data, size=(45, 45))
            
            # 2. Đặt logo ép sang bên trái (side="left")
            logo_label = ctk.CTkLabel(logo_frame, text="", image=my_logo)
            logo_label.pack(side="left", padx=(0, 10)) # padx=(0,10) đẩy chữ cách logo 10px
            
            # 3. Thêm chữ nằm ngang hàng, ngay bên phải logo
            text_label = ctk.CTkLabel(logo_frame, text="AI BRIDGE", font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), text_color=COLOR_TEXT_MAIN)
            text_label.pack(side="left")
            
        except Exception as e:
            print(f"Lỗi tải logo: {e}")
            ctk.CTkLabel(logo_frame, text="🎓 BRIDGE", font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        # --- KẾT THÚC PHẦN LOGO ---

        ctk.CTkLabel(self.sidebar, text="MAIN MENU", font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=20, pady=(10, 5))
        
        # Khung chứa menu: Dùng Frame thường, chiếm không gian trống ở giữa
        self.menu_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_container.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        # Khởi tạo các nút
        self.create_nav_btn("DashboardPage", "📊", "Tổng quan")
        self.create_nav_btn("RoadmapPage", "🧭", "Lộ trình & AI")
        self.create_nav_btn("CommunityPage", "👥", "Cộng đồng")
        self.create_nav_btn("RecruitmentPage", "💼", "Tuyển dụng")
        self.create_nav_btn("ProfilePage", "👤", "Tài khoản & CV") 

        # Box nâng cấp
        upgrade_box = ctk.CTkFrame(self.sidebar, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        upgrade_box.pack(side="bottom", fill="x", padx=15, pady=(10, 20))
        ctk.CTkLabel(upgrade_box, text="Gói Pro - 30 Ngày", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(pady=(10, 5))
        ctk.CTkProgressBar(upgrade_box, progress_color=COLOR_PRIMARY, fg_color=COLOR_BORDER, height=6).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(upgrade_box, text="Nâng cấp", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), fg_color=COLOR_PRIMARY, text_color="white", height=28, corner_radius=6).pack(pady=(5, 10), padx=15, fill="x")

    def create_nav_btn(self, page_name, icon, text):
        # 1. ÉP CỨNG chiều cao của khung chứa nút ở mức 45 pixel
        btn_container = ctk.CTkFrame(self.menu_container, fg_color="transparent", height=45)
        
        # 2. KHÓA TÍNH NĂNG tự động phình to của Frame (rất quan trọng)
        btn_container.pack_propagate(False) 
        
        # 3. Cố định nó lên trên cùng
        btn_container.pack(side="top", fill="x", padx=10, pady=2)
        
        indicator = ctk.CTkFrame(btn_container, width=4, fg_color="transparent", corner_radius=2)
        # pady=6 để vạch xanh ngắn lại một chút cho đẹp, không bị chạm mép
        indicator.pack(side="left", fill="y", pady=6) 
        
        btn = ctk.CTkButton(btn_container, text=f"{icon}   {text}", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"),
                            anchor="w", fg_color="transparent", text_color=COLOR_TEXT_SUB,
                            hover_color=COLOR_BG_APP, height=38, corner_radius=6)
        btn.configure(command=lambda p=page_name: self.show_page(p))
        
        # Dùng fill="both" để nút bám sát vào khung 45px đã ép cứng ở trên
        btn.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        self.nav_buttons[page_name] = {"btn": btn, "indicator": indicator}
    def setup_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER)
        self.topbar.grid(row=0, column=1, sticky="nsew")
        
        # 1. CỤM THÔNG TIN (Nằm bên trái)
        left_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        left_frame.pack(side="left", padx=30, pady=15)
        
        # --- Sắp xếp theo thứ tự: 3 gạch -> Avatar & Tên -> Thông báo -> Ngày tháng ---
        
        # 1. Nút 3 gạch
        self.toggle_btn = ctk.CTkButton(left_frame, text="☰", width=40, height=40, fg_color="transparent", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(size=20), hover_color=COLOR_BORDER, corner_radius=8, command=self.toggle_sidebar)
        self.toggle_btn.pack(side="left", padx=(0, 15))
        
        # 2. Avatar (Icon hình người)
        ctk.CTkLabel(left_frame, text="👤", font=ctk.CTkFont(size=24), text_color=COLOR_PRIMARY).pack(side="left", padx=(0, 8))
        
        # 3. Tên + Chức vụ
        user_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        user_frame.pack(side="left", padx=(0, 20))
        # Chuyển anchor="w" để chữ căn lề trái bám theo icon avatar
        ctk.CTkLabel(user_frame, text="Bùi Hậu", font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(user_frame, text="Sinh viên IT", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_TEXT_SUB).pack(anchor="w")
        
        # 4. Chuông thông báo
        ctk.CTkButton(left_frame, text="🔔", width=40, height=40, fg_color="transparent", border_width=1, border_color=COLOR_BORDER, text_color=COLOR_TEXT_MAIN, corner_radius=8).pack(side="left", padx=(0, 20))
        
        # 5. Ngày tháng
        current_date = datetime.now().strftime("%d %b, %Y")
        ctk.CTkLabel(left_frame, text=f"📅 {current_date}", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(side="left", padx=(0, 0))


        # 2. Ô TÌM KIẾM (Nằm bên phải)
        search_frame = ctk.CTkFrame(self.topbar, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        search_frame.pack(side="right", padx=30, pady=15)
        
        ctk.CTkLabel(search_frame, text="🔍", text_color=COLOR_TEXT_SUB).pack(side="left", padx=(10, 5))
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tìm kiếm khóa học, kỹ năng...", width=300, height=35, fg_color="transparent", border_width=0, text_color=COLOR_TEXT_MAIN)
        search_entry.pack(side="left", padx=(0, 10))
    def toggle_sidebar(self):
        # Kiểm tra xem sidebar đang hiện hay ẩn
        if self.sidebar.winfo_ismapped():
            # Nếu đang hiện -> dùng grid_remove để ẩn đi, phần màn hình chính sẽ tự động tràn ra
            self.sidebar.grid_remove()
        else:
            # Nếu đang ẩn -> dùng grid để hiện lại đúng vị trí ban đầu
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def show_page(self, page_name):
        for name, elements in self.nav_buttons.items():
            elements["btn"].configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)
            elements["indicator"].configure(fg_color="transparent")
        
        active_elements = self.nav_buttons[page_name]
        active_elements["btn"].configure(fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY)
        active_elements["indicator"].configure(fg_color=COLOR_PRIMARY)
        
        for frame in self.frames.values():
            frame.grid_forget()
        if page_name in self.frames:
            self.frames[page_name].grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = AICareerBridgeEnterprise()
    app.mainloop()