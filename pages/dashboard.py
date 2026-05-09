import customtkinter as ctk
import tkinter as tk
import json
import random
from config import *
from components import BasePage, GlassCard, AnimatedProgressBar, StatusPulse, AnimationEngine, CountUpLabel, SkeletonLoader

class DashboardPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.content_pad = 35
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable.pack(fill="both", expand=True)
        self._build_bento_grid()
        self._load_mock_data_async()

    def _build_bento_grid(self):
        self.hero_banner = GlassCard(self.scrollable, fg_color=COLOR_PRIMARY_LIGHT, hover_effect=False)
        self.hero_banner.pack(fill="x", padx=self.content_pad, pady=(self.content_pad, 15))
        
        self.hero_canvas = tk.Canvas(self.hero_banner, bg=get_color(COLOR_PRIMARY_LIGHT), highlightthickness=0, bd=0)
        self.hero_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.hero_banner.bind("<Configure>", lambda e: self._draw_hero_decor())

        hero_text = ctk.CTkFrame(self.hero_banner, fg_color="transparent")
        hero_text.pack(side="left", padx=40, pady=35)
        
        status_frame = ctk.CTkFrame(hero_text, fg_color="transparent")
        status_frame.pack(anchor="w", pady=(0, 10))
        self.ai_pulse = StatusPulse(status_frame, size=8)
        self.ai_pulse.pack(side="left", padx=(0, 5))
        ctk.CTkLabel(status_frame, text="HỆ THỐNG AI MENTOR ĐÃ KÍCH HOẠT", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), 
                     text_color=COLOR_PRIMARY).pack(side="left")
        
        ctk.CTkLabel(hero_text, text="Tối ưu hóa Lộ trình Học tập\nKiến tạo Tương lai Kỹ sư.", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=28, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN, justify="left").pack(anchor="w")
        
        ctk.CTkButton(hero_text, text="Tiếp tục Học tập  ➔", 
                      font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), 
                      fg_color=COLOR_PRIMARY, text_color="white", height=40, corner_radius=6,
                      command=lambda: self.controller.show_page("LearningPage")).pack(anchor="w", pady=(20, 0))

        self.grid_frame = ctk.CTkFrame(self.scrollable, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=self.content_pad-5, pady=10)
        self.grid_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.stats = {}
        self.stats['progress'] = self._create_stat_card(self.grid_frame, 0, 0, "Tiến độ Lộ trình", suffix="%")
        self.stats['credits'] = self._create_stat_card(self.grid_frame, 0, 1, "Tín chỉ Tích lũy", format_str="{}/120")
        self.stats['gpa'] = self._create_stat_card(self.grid_frame, 0, 2, "Điểm GPA", format_str="{}")

        self.left_col = GlassCard(self.grid_frame)
        self.left_col.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        header_l = ctk.CTkFrame(self.left_col, fg_color="transparent")
        header_l.pack(fill="x", padx=25, pady=(25, 15))
        ctk.CTkLabel(header_l, text="Học phần đang diễn ra", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        self.courses_container = ctk.CTkFrame(self.left_col, fg_color="transparent")
        self.courses_container.pack(fill="both", expand=True)
        # Skeleton loaders for initial state
        for _ in range(3): SkeletonLoader(self.courses_container, width=300, height=60).pack(fill="x", padx=25, pady=10)

        self.right_col = GlassCard(self.grid_frame)
        self.right_col.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(self.right_col, text="Sự kiện & Deadline", font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=25, pady=(25, 15))
        self.events_container = ctk.CTkFrame(self.right_col, fg_color="transparent")
        self.events_container.pack(fill="both", expand=True)
        # Skeleton loaders
        for _ in range(2): SkeletonLoader(self.events_container, width=200, height=50).pack(fill="x", padx=25, pady=10)

    def _create_stat_card(self, parent, row, col, title, suffix="", format_str="{}"):
        card = GlassCard(parent)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        top_box = ctk.CTkFrame(card, fg_color="transparent")
        top_box.pack(fill="x", padx=20, pady=(20, 5))
        ctk.CTkLabel(top_box, text=title, font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), text_color=COLOR_TEXT_SUB).pack(side="left")
        val_lbl = CountUpLabel(card, format_str=format_str, suffix=suffix, font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN)
        val_lbl.pack(anchor="w", padx=20, pady=(0, 20))
        return val_lbl

    def _load_mock_data_async(self):
        def fetch_data():
            mock_payload = {
                "stats": {"progress": "65", "credits": "84", "gpa": "3.8"},
                "courses": [
                    {"title": "Lập trình Python Nâng cao", "status": "Tiến độ: 80%", "color": COLOR_PRIMARY, "progress": 0.8},
                    {"title": "Toán rời rạc & Thuật toán", "status": "Tiến độ: 45%", "color": "#F59E0B", "progress": 0.45},
                    {"title": "Kỹ năng Giao tiếp Tiếng Anh", "status": "Tiến độ: 15%", "color": "#10B981", "progress": 0.15}
                ],
                "events": [
                    {"date": "12 Th4", "title": "Workshop Trí tuệ Nhân tạo", "time": "08:00 Sáng - Online"},
                    {"date": "15 Th4", "title": "Nộp Đồ án Cơ sở 2", "time": "14:00 Chiều - Hệ thống"}
                ]
            }
            self.update_data(mock_payload)
        self.after(800, fetch_data) # Reduced delay for snappier feel

    def _draw_hero_decor(self):
        self.hero_canvas.delete("all")
        w = self.hero_banner.winfo_width()
        h = self.hero_banner.winfo_height()
        if w < 10: return
        for _ in range(8):
            x, y = random.randint(0, w), random.randint(0, h)
            r = random.randint(20, 60)
            self.hero_canvas.create_oval(x-r, y-r, x+r, y+r, outline=get_color(COLOR_PRIMARY), width=1)

    def _add_course_item(self, parent, title, status, color, progress, delay=0):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        AnimationEngine.fade_in_widget(frame, delay_ms=delay)
        
        title_btn = ctk.CTkButton(
            frame, text=title, text_color=COLOR_TEXT_MAIN, 
            font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"),
            fg_color="transparent", hover_color=COLOR_BG_APP, anchor="w",
            command=lambda: getattr(self, "controller", None) and self.controller.show_page("CourseDetailPage")
        )
        title_btn.pack(anchor="w", fill="x")
        ctk.CTkLabel(frame, text=status, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(anchor="w", pady=(0, 5), padx=10)
        
        bar = AnimatedProgressBar(frame, color=color, height=6)
        bar.pack(fill="x", padx=10)
        bar.set_target(progress)
        ctk.CTkFrame(parent, height=1, fg_color=COLOR_BORDER).pack(fill="x", pady=(15, 0))

    def update_data(self, json_payload):
        try:
            data = json.loads(json_payload) if isinstance(json_payload, str) else json_payload
            
            if "stats" in data:
                self.stats['progress'].set_target(data["stats"].get("progress", "0"))
                self.stats['credits'].set_target(data["stats"].get("credits", "0"))
                self.stats['gpa'].set_target(float(data["stats"].get("gpa", "0.0")))

            if "courses" in data:
                for widget in self.courses_container.winfo_children(): widget.destroy()
                for i, course in enumerate(data["courses"]):
                    self._add_course_item(self.courses_container, course["title"], course["status"], 
                                          course.get("color", COLOR_PRIMARY), course["progress"], delay=i*100)

            if "events" in data:
                for widget in self.events_container.winfo_children(): widget.destroy()
                for i, event in enumerate(data["events"]):
                    self._add_event_item(self.events_container, event["date"], event["title"], event["time"], delay=i*100)

        except Exception as e: print(f"Lỗi update_data: {e}")

    def _add_event_item(self, parent, date, title, time_str, delay=0):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        AnimationEngine.fade_in_widget(frame, delay_ms=delay)
        
        date_box = ctk.CTkFrame(frame, fg_color=COLOR_PRIMARY_LIGHT, corner_radius=6, width=50, height=50)
        date_box.pack(side="left", padx=(0, 15))
        date_box.pack_propagate(False)
        parts = date.split()
        ctk.CTkLabel(date_box, text=parts[0], font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold"), text_color=COLOR_PRIMARY).pack(pady=(5,0))
        ctk.CTkLabel(date_box, text=parts[1] if len(parts)>1 else "", font=ctk.CTkFont(family=FONT_MAIN, size=11), text_color=COLOR_PRIMARY).pack()
        
        txt_box = ctk.CTkFrame(frame, fg_color="transparent")
        txt_box.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(txt_box, text=title, text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(txt_box, text=time_str, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(anchor="w")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x800")
    app.configure(fg_color=COLOR_BG_APP)
    page = DashboardPage(app, None)
    page.pack(fill="both", expand=True)
    app.mainloop()