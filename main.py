import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
import random
from datetime import datetime

# Import cấu hình và giao diện cơ sở
from config import *
from i18n import _, set_language
from components import AnimationEngine, GlassCard

# Import các trang
from pages.dashboard import DashboardPage
from pages.roadmap import RoadmapPage
from pages.community import CommunityPage
from pages.recruitment import RecruitmentPage
from pages.profile import ProfilePage
from pages.course_detail import CourseDetailPage  
from pages.learning import LearningPage

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
        try:
            x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
            y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2) - 15
            
            self.tooltip_window = tk.Toplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True) 
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            
            bg_color = resolve_color(COLOR_BG_CARD)
            fg_color = resolve_color(COLOR_TEXT_MAIN)
            border_color = resolve_color(COLOR_BORDER)
            
            label = tk.Label(self.tooltip_window, text=self.text, bg=bg_color, fg=fg_color, 
                             font=(FONT_MAIN, 10, "bold"), padx=12, pady=6, borderwidth=1, relief="flat", 
                             highlightthickness=1, highlightbackground=border_color)
            label.pack()
        except Exception: pass

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            try:
                self.tooltip_window.destroy()
            except Exception: pass
            self.tooltip_window = None

class PopupMenu:
    current_menu = None
    def __init__(self, parent_window, button_widget, items, title=None, is_submenu=False, anchor_pos="top"):
        self.parent_window = parent_window
        self.button_widget = button_widget
        self.items = items
        self.title = title
        self.is_submenu = is_submenu
        self.anchor_pos = anchor_pos
        self.submenu = None
        
        if not is_submenu and PopupMenu.current_menu:
            try: PopupMenu.current_menu.close()
            except: pass
        
        if not is_submenu: PopupMenu.current_menu = self
        
        self.menu_window = tk.Toplevel(parent_window)
        self.menu_window.withdraw()
        self.menu_window.wm_overrideredirect(True)
        
        self.frame = ctk.CTkFrame(self.menu_window, fg_color=COLOR_BG_CARD, border_width=1, border_color=COLOR_BORDER, corner_radius=8)
        self.frame.pack(padx=0, pady=0)
        
        if title:
            ctk.CTkLabel(self.frame, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), 
                         text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 10))
            ctk.CTkFrame(self.frame, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=15, pady=(0, 5))
        
        for item in items:
            if item[0] == "-":
                ctk.CTkFrame(self.frame, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=15, pady=4)
            else:
                text, color, action = item
                btn = ctk.CTkButton(self.frame, text=text, fg_color="transparent", text_color=color, anchor="w",
                                    hover_color=("#F1F5F9", "#2D3748"), height=35, font=ctk.CTkFont(family=FONT_MAIN, size=13))
                if isinstance(action, list):
                    btn.configure(text=f"{text}  ▶")
                    btn.bind("<Enter>", lambda e, b=btn, a=action: self.show_submenu(b, a))
                else:
                    btn.bind("<Enter>", lambda e: self.close_submenu())
                    btn.configure(command=lambda a=action: self.handle_action(a))
                btn.pack(fill="x", padx=8, pady=2)
        
        self.menu_window.update_idletasks()
        self.position_menu()
        self.menu_window.deiconify()
        self.menu_window.bind("<FocusOut>", lambda e: self.close())

    def position_menu(self):
        try:
            bx, by = self.button_widget.winfo_rootx(), self.button_widget.winfo_rooty()
            bw, bh = self.button_widget.winfo_width(), self.button_widget.winfo_height()
            mh = self.menu_window.winfo_reqheight()
            mx = bx + bw + 5
            my = by - mh + bh if (self.anchor_pos == "bottom" and not self.is_submenu) else by
            self.menu_window.geometry(f"+{mx}+{my}")
        except Exception: pass

    def show_submenu(self, button, actions):
        self.close_submenu()
        self.submenu = PopupMenu(self.parent_window, button, actions, is_submenu=True)

    def close_submenu(self):
        if self.submenu:
            try: self.submenu.close()
            except: pass
            self.submenu = None

    def handle_action(self, action):
        if action: action()
        self.close()

    def close(self):
        self.close_submenu()
        try: self.menu_window.destroy()
        except: pass
        if PopupMenu.current_menu == self: PopupMenu.current_menu = None

class AICareerBridgeEnterprise(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.sidebar_width = 75
        self.current_page_name = "DashboardPage"
        self.nav_buttons = {}
        self.frames = {}
        self.build_ui()

    def setup_window(self):
        ww, wh = 1250, 780
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        cx, cy = int(sw/2 - ww/2), int(sh/2 - wh/2)
        self.geometry(f"{ww}x{wh}+{cx}+{cy}")
        self.configure(fg_color=COLOR_BG_APP)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def fade_out_window(self, callback, step=0.08):
        try:
            alpha = self.attributes("-alpha")
            if alpha > 0.0:
                self.attributes("-alpha", max(alpha - step, 0.0))
                self.after(25, lambda: self.fade_out_window(callback, step))
            else:
                callback()
        except: callback()

    def fade_in_window(self, step=0.08):
        try:
            alpha = self.attributes("-alpha")
            if alpha < 1.0:
                self.attributes("-alpha", min(alpha + step, 1.0))
                self.after(25, lambda: self.fade_in_window(step))
        except: pass

    def build_ui(self):
        self.title(_("app_title"))
        self.setup_sidebar()
        self.setup_topbar()
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_BG_APP)
        self.main_container.grid(row=1, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        pages = [DashboardPage, RoadmapPage, CommunityPage, RecruitmentPage, ProfilePage, CourseDetailPage, LearningPage]
        for P in pages:
            f = P(self.main_container, self)
            self.frames[P.__name__] = f

        self.add_button = ctk.CTkButton(self, text="+", width=56, height=56, corner_radius=28, font=(FONT_MAIN, 24, "bold"),
                                        fg_color=COLOR_PRIMARY, command=self.handle_add_action)
        self.show_page(self.current_page_name)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=self.sidebar_width, corner_radius=0, fg_color=COLOR_BG_APP, 
                                     border_width=1, border_color=COLOR_BORDER)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.pack_propagate(False)

        self.avatar_btn = ctk.CTkButton(self.sidebar, text="👤", width=45, height=45, corner_radius=22, 
                                        fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, font=(FONT_MAIN, 20))
        self.avatar_btn.pack(pady=(25, 20))
        self.avatar_btn.configure(command=self.show_avatar_menu)
        ToolTip(self.avatar_btn, _("profile_tooltip"))

        self.menu_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_box.pack(fill="both", expand=True, padx=5)

        navs = [("DashboardPage", "📊", _("nav_dashboard")), ("RoadmapPage", "🧭", _("nav_roadmap")),
                ("CommunityPage", "👥", _("nav_community")), ("RecruitmentPage", "💼", _("nav_recruitment")),
                ("ProfilePage", "👤", _("nav_profile"))]
        for p, i, t in navs: self.create_nav_btn(p, i, t)

        self.bottom_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.bottom_box.pack(side="bottom", fill="x", pady=20)
        self.settings_btn = ctk.CTkButton(self.bottom_box, text="⚙️", width=45, height=45, fg_color="transparent", 
                                          text_color=COLOR_TEXT_SUB, font=(FONT_MAIN, 20), command=self.show_settings_menu)
        self.settings_btn.pack()

    def create_nav_btn(self, page, icon, text):
        c = ctk.CTkFrame(self.menu_box, fg_color="transparent", height=45)
        c.pack(fill="x", pady=4, padx=10)
        c.pack_propagate(False)

        ind = ctk.CTkFrame(c, width=3, fg_color="transparent", corner_radius=2)
        ind.pack(side="left", fill="y", pady=8)
        btn = ctk.CTkButton(c, text=icon, font=(FONT_MAIN, 18), fg_color="transparent", text_color=COLOR_TEXT_SUB,
                            hover_color=COLOR_BG_APP, corner_radius=6, width=40, command=lambda: self.show_page(page))
        btn.pack(side="left", fill="y", padx=(5, 0))

        lbl = ctk.CTkLabel(c, text=text, font=(FONT_MAIN, 13, "bold"), text_color=COLOR_TEXT_SUB)
        ToolTip(btn, text)
        self.nav_buttons[page] = {"btn": btn, "indicator": ind, "label": lbl}

    def setup_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=COLOR_BG_APP, border_width=1, border_color=COLOR_BORDER)
        self.topbar.grid(row=0, column=1, sticky="nsew")
        s_box = ctk.CTkFrame(self.topbar, fg_color=COLOR_BG_APP, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        s_box.pack(side="right", padx=30, pady=15)
        ctk.CTkLabel(s_box, text="🔍", text_color=COLOR_TEXT_SUB).pack(side="left", padx=10)
        ctk.CTkEntry(s_box, placeholder_text=_("search_placeholder"), width=250, height=35, fg_color="transparent", border_width=0).pack(side="left", padx=(0, 10))

    def show_page(self, name):
        if getattr(self, "current_page_name", None) == name and name in self.frames and self.frames[name].winfo_ismapped():
            return

        self.current_page_name = name

        for k, v in self.nav_buttons.items():
            v["btn"].configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)
            v["label"].configure(text_color=COLOR_TEXT_SUB)
            v["indicator"].configure(fg_color="transparent")

        highlight = "DashboardPage" if name in ("LearningPage", "CourseDetailPage") else name
        if highlight in self.nav_buttons:
            v = self.nav_buttons[highlight]
            v["btn"].configure(fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY)
            v["label"].configure(text_color=COLOR_PRIMARY)
            v["indicator"].configure(fg_color=COLOR_PRIMARY)

        for f in self.frames.values(): 
            f.grid_forget()
            f.place_forget()

        if name in self.frames: 
            target_frame = self.frames[name]

            # Slide Up Animation
            def animate_slide(current_rely):
                if current_rely <= 0:
                    target_frame.place_forget()
                    target_frame.grid(row=0, column=0, sticky="nsew")
                    if name == "DashboardPage":
                        self.add_button.place(relx=1.0, rely=1.0, x=-30, y=-30, anchor="se")
                        self.add_button.lift()
                    else:
                        self.add_button.place_forget()
                else:
                    target_frame.place(relx=0, rely=current_rely, relwidth=1, relheight=1)
                    self.after(15, lambda: animate_slide(current_rely - 0.01))

            animate_slide(0.06)

    def handle_add_action(self):
        from tkinter import filedialog, messagebox
        f = filedialog.askopenfilename()
        if f: messagebox.showinfo("Info", f"File selected: {f}")

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
            (_("menu_theme"), COLOR_TEXT_MAIN, self.toggle_theme),
            (_("menu_data"), COLOR_TEXT_MAIN, [
                (_("menu_data_manage"), COLOR_TEXT_MAIN, None)
            ]),
            (_("menu_lang"), COLOR_TEXT_MAIN, [
                (_("menu_lang_en"), COLOR_TEXT_MAIN, lambda: self.change_lang("en")),
                (_("menu_lang_vi"), COLOR_TEXT_MAIN, lambda: self.change_lang("vi"))
            ]),
            (_("menu_support"), COLOR_TEXT_MAIN, [
                (_("menu_support_ver"), COLOR_TEXT_MAIN, None),
                (_("menu_support_contact"), COLOR_TEXT_MAIN, None),
                (_("menu_support_shortcuts"), COLOR_TEXT_MAIN, None)
            ]),
            ("-",),
            (_("menu_logout"), "#DC2626", None), 
            (_("menu_exit"), COLOR_TEXT_MAIN, self.destroy) 
        ]
        PopupMenu(self, self.settings_btn, items, anchor_pos="bottom")

    def toggle_theme(self):
        def apply():
            ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")
            self.sidebar.configure(fg_color=COLOR_BG_APP)
            self.fade_in_window(0.1)
        self.fade_out_window(apply, 0.1)

    def change_lang(self, code):
        def apply():
            set_language(code)
            for widget in self.winfo_children(): widget.destroy()
            self.build_ui()
            self.fade_in_window(0.1)
        self.fade_out_window(apply, 0.1)

if __name__ == "__main__":
    app = AICareerBridgeEnterprise()
    app.mainloop()

