import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
from datetime import datetime

# Import cấu hình
from config import *
from i18n import _, set_language

# Import các trang từ thư mục pages
try:
    from pages.dashboard import DashboardPage
    from pages.roadmap import RoadmapPage
    from pages.community import CommunityPage
    from pages.recruitment import RecruitmentPage
    from pages.profile import ProfilePage
    from pages.course_detail import CourseDetailPage  
    from pages.learning import LearningPage
except ImportError:
    pass

ctk.set_appearance_mode("dark")

def resolve_color(color):
    if isinstance(color, tuple):
        return color[1] if ctk.get_appearance_mode() == "Dark" else color[0]
    return color

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2) - 15
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True) 
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        bg_color = resolve_color(COLOR_BG_CARD)
        fg_color = resolve_color(COLOR_TEXT_MAIN)
        border_color = resolve_color(COLOR_BORDER)
        
        label = tk.Label(self.tooltip_window, text=self.text, bg=bg_color, fg=fg_color, 
                         font=(FONT_MAIN, 10, "bold"), padx=12, pady=6, borderwidth=1, relief="flat", highlightthickness=1, highlightbackground=border_color)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class PopupMenu:
    """Menu popup - Đơn giản, không sập"""
    current_menu = None

    def __init__(self, parent_window, button_widget, items, title=None, is_submenu=False, anchor_pos="top"):
        self.parent_window = parent_window
        self.button_widget = button_widget
        self.items = items
        self.title = title
        self.is_submenu = is_submenu
        self.anchor_pos = anchor_pos
        self.submenu = None
        
        # Đóng menu cũ nếu có
        if not is_submenu and PopupMenu.current_menu:
            try:
                PopupMenu.current_menu.close()
            except:
                pass
        
        if not is_submenu:
            PopupMenu.current_menu = self
        
        # Tạo Toplevel window
        self.menu_window = tk.Toplevel(parent_window)
        self.menu_window.withdraw()
        self.menu_window.wm_overrideredirect(True)
        
        # Tạo frame menu
        self.frame = ctk.CTkFrame(
            self.menu_window,
            fg_color=COLOR_BG_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=8
        )
        self.frame.pack(padx=0, pady=0)
        
        # Thêm title
        if title:
            ctk.CTkLabel(
                self.frame,
                text=title,
                font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"),
                text_color=COLOR_TEXT_MAIN
            ).pack(anchor="w", padx=20, pady=(15, 10))
            
            ctk.CTkFrame(self.frame, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=15, pady=(0, 5))
        
        # Thêm items
        for item in items:
            if item[0] == "-":
                ctk.CTkFrame(self.frame, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=15, pady=4)
            else:
                text, color, action = item
                
                btn = ctk.CTkButton(
                    self.frame,
                    text=text,
                    fg_color="transparent",
                    text_color=color,
                    anchor="w",
                    hover_color=("#F1F5F9", "#2D3748"),
                    height=35,
                    font=ctk.CTkFont(family=FONT_MAIN, size=13),
                    border_width=0
                )
                
                if isinstance(action, list):
                    btn.configure(text=f"{text}  ▶")
                    btn.bind("<Enter>", lambda e, b=btn, a=action: self.show_submenu(b, a))
                else:
                    btn.bind("<Enter>", lambda e: self.close_submenu())
                    btn.configure(command=lambda a=action: self.handle_action(a))
                
                btn.pack(fill="x", padx=8, pady=2)
        
        # Hiển thị
        self.menu_window.update_idletasks()
        self.position_menu()
        self.menu_window.deiconify()
        self.menu_window.lift()
        
        # Xử lý click ngoài
        self.menu_window.bind("<FocusOut>", lambda e: self.close())

    def position_menu(self):
        """Tính vị trí menu"""
        button_x = self.button_widget.winfo_rootx()
        button_y = self.button_widget.winfo_rooty()
        button_width = self.button_widget.winfo_width()
        button_height = self.button_widget.winfo_height()
        
        menu_height = self.menu_window.winfo_reqheight()
        
        menu_x = button_x + button_width + 5
        
        if self.anchor_pos == "bottom" and not self.is_submenu:
            menu_y = button_y - menu_height + button_height
        else:
            menu_y = button_y
            
        self.menu_window.geometry(f"+{menu_x}+{menu_y}")

    def show_submenu(self, button, actions):
        """Mở menu con"""
        self.close_submenu()
        self.submenu = PopupMenu(
            self.parent_window,
            button,
            actions,
            is_submenu=True
        )

    def close_submenu(self):
        """Đóng menu con"""
        if self.submenu:
            try:
                self.submenu.close()
            except:
                pass
            self.submenu = None

    def handle_action(self, action):
        """Xử lý action"""
        if action:
            action()
        self.close()

    def close(self):
        """Đóng menu"""
        self.close_submenu()
        try:
            self.menu_window.destroy()
        except:
            pass
        
        if PopupMenu.current_menu == self:
            PopupMenu.current_menu = None


class AICareerBridgeEnterprise(ctk.CTk):
    def __init__(self):
        super().__init__()

        window_width = 1200
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        self.configure(fg_color=COLOR_BG_APP)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_page_name = "DashboardPage"
        self.build_ui()

    def clear_ui(self):
        for widget in self.winfo_children():
            if isinstance(widget, (ctk.CTkFrame, ctk.CTkButton, ctk.CTkLabel, ctk.CTkScrollableFrame)):
                widget.destroy()

    def build_ui(self):
        self.title(_("app_title"))
        self.frames = {}
        self.nav_buttons = {}

        self.setup_sidebar()
        self.setup_topbar()
        
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_APP)
        self.main_container.grid(row=1, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        page_list = (
            DashboardPage, 
            RoadmapPage, 
            CommunityPage, 
            RecruitmentPage, 
            ProfilePage,
            CourseDetailPage,
            LearningPage
        )

        for PageClass in page_list:
            page_name = PageClass.__name__
            frame = PageClass(parent=self.main_container, controller=self)
            self.frames[page_name] = frame

        self.add_button = ctk.CTkButton(
            self, 
            text="+", 
            width=56, 
            height=56, 
            corner_radius=28,
            font=ctk.CTkFont(size=28, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color="#1E40AF",
            command=self.handle_add_action
        )
        self.show_page(self.current_page_name)

    def change_language(self, lang_code):
        set_language(lang_code)
        self.clear_ui()
        self.build_ui()
        
    def handle_add_action(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(
            title="Chọn tài liệu tải lên",
            filetypes=[("Tài liệu", "*.pdf *.docx *.txt"), ("Tất cả", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Thông báo", f"Đã nhận file: {file_path.split('/')[-1]}")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=75, corner_radius=0, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.pack_propagate(False)
        
        self.avatar_btn = ctk.CTkButton(self.sidebar, text="👤", width=45, height=45, corner_radius=22, 
                                        fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, font=ctk.CTkFont(size=24))
        self.avatar_btn.pack(pady=(20, 15))
        self.avatar_btn.configure(command=self.show_avatar_menu)
        ToolTip(self.avatar_btn, _("profile_tooltip"))

        self.menu_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_container.pack(fill="both", expand=True, padx=5, pady=(10, 0))

        self.create_nav_btn("DashboardPage", "📊", _("nav_dashboard"))
        self.create_nav_btn("RoadmapPage", "🧭", _("nav_roadmap"))
        self.create_nav_btn("CommunityPage", "👥", _("nav_community"))
        self.create_nav_btn("RecruitmentPage", "💼", _("nav_recruitment"))
        self.create_nav_btn("ProfilePage", "👤", _("nav_profile")) 
        
        self.bottom_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.bottom_box.pack(side="bottom", fill="x", pady=(10, 20))

        self.notif_btn = ctk.CTkButton(self.bottom_box, text="🔔", width=45, height=45, corner_radius=8,
                                          fg_color="transparent", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=22), hover_color=COLOR_BG_APP)
        self.notif_btn.pack(pady=5)
        ToolTip(self.notif_btn, _("notif_tooltip"))

        self.settings_btn = ctk.CTkButton(self.bottom_box, text="⚙️", width=45, height=45, corner_radius=8,
                                          fg_color="transparent", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=24), hover_color=COLOR_BG_APP)
        self.settings_btn.pack(pady=5)
        self.settings_btn.configure(command=self.show_settings_menu)
        ToolTip(self.settings_btn, _("settings_tooltip"))

    def create_nav_btn(self, page_name, icon, text):
        btn_container = ctk.CTkFrame(self.menu_container, fg_color="transparent", height=45)
        btn_container.pack_propagate(False) 
        btn_container.pack(side="top", fill="x", padx=10, pady=4)
        
        indicator = ctk.CTkFrame(btn_container, width=3, fg_color="transparent", corner_radius=2)
        indicator.pack(side="left", fill="y", pady=6) 

        btn = ctk.CTkButton(btn_container, text=icon, font=ctk.CTkFont(family=FONT_MAIN, size=20, weight="bold"),
                            anchor="center", fg_color="transparent", text_color=COLOR_TEXT_SUB,
                            hover_color=COLOR_BG_APP, corner_radius=6)
        btn.configure(command=lambda p=page_name: self.show_page(p))
        btn.pack(side="left", fill="both", expand=True, padx=(2, 5))
        
        ToolTip(btn, text)
        self.nav_buttons[page_name] = {"btn": btn, "indicator": indicator}

    def setup_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER)
        self.topbar.grid(row=0, column=1, sticky="nsew")
        
        search_frame = ctk.CTkFrame(self.topbar, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        search_frame.pack(side="right", padx=30, pady=15)
        ctk.CTkLabel(search_frame, text="🔍", text_color=COLOR_TEXT_SUB).pack(side="left", padx=(10, 5))
        search_entry = ctk.CTkEntry(search_frame, placeholder_text=_("search_placeholder"), width=300, height=35, fg_color="transparent", border_width=0, text_color=COLOR_TEXT_MAIN)
        search_entry.pack(side="left", padx=(0, 10))

    def show_avatar_menu(self):
        items = [
            (_("menu_account"), COLOR_TEXT_MAIN, lambda: self.show_page("ProfilePage")),
            (_("menu_upgrade"), COLOR_TEXT_MAIN, None),
            (_("menu_settings"), COLOR_TEXT_MAIN, self.show_settings_menu),
            ("-",), 
            (_("menu_logout"), "#DC2626", None)
        ]
        PopupMenu(self, self.avatar_btn, items, title="Nguyễn Hoàng Đăng Khoa", anchor_pos="top")

    def show_settings_menu(self):
        items = [
            (_("menu_account"), COLOR_TEXT_MAIN, lambda: self.show_page("ProfilePage")),
            (_("menu_settings"), COLOR_TEXT_MAIN, None),
            (_("menu_theme"), COLOR_TEXT_MAIN, self.toggle_appearance_mode),
            (_("menu_data"), COLOR_TEXT_MAIN, [
                (_("menu_data_manage"), COLOR_TEXT_MAIN, None)
            ]),
            (_("menu_lang"), COLOR_TEXT_MAIN, [
                (_("menu_lang_en"), COLOR_TEXT_MAIN, lambda: self.change_language("en")),
                (_("menu_lang_vi"), COLOR_TEXT_MAIN, lambda: self.change_language("vi"))
            ]),
            (_("menu_support"), COLOR_TEXT_MAIN, [
                (_("menu_support_ver"), COLOR_TEXT_MAIN, None),
                (_("menu_support_contact"), COLOR_TEXT_MAIN, None),
                (_("menu_support_shortcuts"), COLOR_TEXT_MAIN, None)
            ]),
            ("-",),
            (_("menu_logout"), "#DC2626", None), 
            (_("menu_exit"), COLOR_TEXT_MAIN, lambda: self.destroy()) 
        ]
        PopupMenu(self, self.settings_btn, items, anchor_pos="bottom")

    def toggle_appearance_mode(self):
        """Chuyển đổi giữa chế độ sáng và tối"""
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def show_page(self, page_name):
        self.current_page_name = page_name
        # 1. Reset màu và indicator của sidebar
        for name, elements in self.nav_buttons.items():
            elements["btn"].configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)
            elements["indicator"].configure(fg_color="transparent")
        
        # 2. Highlight nút đang chọn (nếu trang đó có trên sidebar)
        highlight_page = "DashboardPage" if page_name in ("LearningPage", "CourseDetailPage") else page_name
        if highlight_page in self.nav_buttons:
            active_elements = self.nav_buttons[highlight_page]
            active_elements["btn"].configure(fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY)
            active_elements["indicator"].configure(fg_color=COLOR_PRIMARY)
        
        # 3. Chuyển đổi Frame hiển thị
        for frame in self.frames.values():
            frame.grid_forget()
        
        if page_name in self.frames:
            self.frames[page_name].grid(row=0, column=0, sticky="nsew")

        # 4. Logic ẩn/hiện nút dấu cộng
        # Lưu ý: "DashboardPage" là tên class trang Tổng quát của bạn
        if page_name == "DashboardPage":
            self.add_button.place(relx=1.0, rely=1.0, x=-30, y=-30, anchor="se")
            self.add_button.lift() # Đảm bảo nút luôn nằm trên cùng
        else:
            self.add_button.place_forget()

if __name__ == "__main__":
    app = AICareerBridgeEnterprise()
    app.mainloop()