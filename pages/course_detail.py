import customtkinter as ctk
from config import *

# Import các Tab con
from pages.course_tabs.roadmap_tab import RoadmapTab
from pages.course_tabs.documents_tab import DocumentsTab
from pages.course_tabs.exercises_tab import ExercisesTab
from pages.course_tabs.projects_tab import ProjectsTab
from pages.course_tabs.results_tab import ResultsTab
from pages.course_tabs.analytics_tab import AnalyticsTab

class CourseDetailPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        content_pad = 35

        # 1. Header & Nút quay lại
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=content_pad, pady=(content_pad, 10))
        
        btn_back = ctk.CTkButton(header_frame, text="⬅ Quay lại Dashboard", 
                                 fg_color="transparent", text_color=COLOR_TEXT_SUB, 
                                 hover_color=COLOR_BG_APP, width=150, font=ctk.CTkFont(family=FONT_MAIN, weight="bold"),
                                 command=lambda: self.controller.show_page("DashboardPage"))
        btn_back.pack(side="left")

        # Tiêu đề học phần
        ctk.CTkLabel(self, text="CHI TIẾT: LẬP TRÌNH PYTHON NÂNG CAO", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=18, weight="bold"), 
                     text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=content_pad, pady=(10, 10))

        # 2. Thanh Tabs điều hướng ngang
        tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        tabs_frame.pack(fill="x", padx=content_pad, pady=(0, 10))
        
        self.tab_buttons = {}
        tabs = [
            ("Đường lộ trình", self.show_roadmap), 
            ("Tài liệu", self.show_documents), 
            ("Bài tập", self.show_exercises), 
            ("Đồ án", self.show_projects), 
            ("Kết quả", self.show_results),
            ("Phân tích", self.show_analytics)
        ]
        
        for name, command in tabs:
            btn = ctk.CTkButton(tabs_frame, text=name, fg_color="transparent", text_color=COLOR_TEXT_SUB, 
                                font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), 
                                hover_color=COLOR_BG_APP, corner_radius=6, command=command)
            btn.pack(side="left", padx=(0, 5))
            self.tab_buttons[name] = btn

        ctk.CTkFrame(self, height=1, fg_color=COLOR_BORDER).pack(fill="x", padx=content_pad)

        # 3. Main Content Container
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        # Trạng thái ban đầu
        self.show_roadmap()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        for btn in self.tab_buttons.values():
            btn.configure(text_color=COLOR_TEXT_SUB, fg_color="transparent")

    def set_active_tab(self, tab_name):
        self.clear_container()
        if tab_name in self.tab_buttons:
            self.tab_buttons[tab_name].configure(text_color=COLOR_PRIMARY, fg_color=COLOR_PRIMARY_LIGHT)

    def show_roadmap(self):
        self.set_active_tab("Đường lộ trình")
        RoadmapTab(self.container).pack(fill="both", expand=True)

    def show_documents(self):
        self.set_active_tab("Tài liệu")
        DocumentsTab(self.container).pack(fill="both", expand=True)

    def show_exercises(self):
        self.set_active_tab("Bài tập")
        ExercisesTab(self.container).pack(fill="both", expand=True)

    def show_projects(self):
        self.set_active_tab("Đồ án")
        ProjectsTab(self.container).pack(fill="both", expand=True)

    def show_results(self):
        self.set_active_tab("Kết quả")
        ResultsTab(self.container).pack(fill="both", expand=True)

    def show_analytics(self):
        self.set_active_tab("Phân tích")
        AnalyticsTab(self.container).pack(fill="both", expand=True)