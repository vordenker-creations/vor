import customtkinter as ctk
from config import *

# Import các Tab từ thư mục con
from pages.roadmap_tabs.overview_tab import OverviewTab
from pages.roadmap_tabs.skill_tree_tab import SkillTreeTab
from pages.roadmap_tabs.year_details_tab import YearDetailsTab
from pages.roadmap_tabs.timetable_tab import TimetableTab

class RoadmapPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(self, text="Lộ Trình Học Tập", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 10))

        # Thanh Tab
        self.tab_nav = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, height=50, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        self.tab_nav.pack(fill="x", padx=35, pady=(0, 15))
        
        self.tab_buttons = {}
        tabs = [
            ("OVERVIEW", self.show_overview),
            ("SKILL TREE", self.show_skill_tree),
            ("Y1 DETAILS", self.show_y1_details),
            ("TIMETABLE", self.show_timetable)
        ]

        for text, command in tabs:
            btn = ctk.CTkButton(self.tab_nav, text=text, fg_color="transparent", text_color=COLOR_TEXT_SUB,
                                font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"),
                                width=120, hover_color=COLOR_BG_APP, command=command)
            btn.pack(side="left", padx=5, pady=8)
            self.tab_buttons[text] = btn

        # Container chứa nội dung
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=30, pady=5)

        self.show_overview()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        for btn in self.tab_buttons.values():
            btn.configure(fg_color="transparent", text_color=COLOR_TEXT_SUB)

    def set_active_tab(self, tab_name):
        self.tab_buttons[tab_name].configure(fg_color=COLOR_PRIMARY, text_color="white")

    def show_overview(self):
        self.clear_container()
        self.set_active_tab("OVERVIEW")
        OverviewTab(self.container).pack(fill="both", expand=True)

    def show_skill_tree(self):
        self.clear_container()
        self.set_active_tab("SKILL TREE")
        SkillTreeTab(self.container).pack(fill="both", expand=True)

    def show_y1_details(self):
        self.clear_container()
        self.set_active_tab("Y1 DETAILS")
        YearDetailsTab(self.container).pack(fill="both", expand=True)

    def show_timetable(self):
        self.clear_container()
        self.set_active_tab("TIMETABLE")
        TimetableTab(self.container).pack(fill="both", expand=True)