import customtkinter as ctk
from config import *
from components import SaaSCard

class YearDetailsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        ctk.CTkLabel(header_frame, text="EXPANDED Y1 DETAILS (Y1 YEAR 1)", 
                     font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")
        
        # Y1-Y4 Highlight Bar
        timeline_bar = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, height=40, corner_radius=20)
        timeline_bar.pack(fill="x", padx=10, pady=(0, 25))
        timeline_bar.pack_propagate(False)
        
        years = [("Y1", COLOR_PRIMARY), ("Y2", COLOR_SUCCESS), ("Y3", COLOR_BORDER), ("Y4", COLOR_BORDER)]
        for i, (yr, color) in enumerate(years):
            btn = ctk.CTkFrame(timeline_bar, fg_color=color, corner_radius=15 if i==0 or i==3 else 0)
            btn.pack(side="left", fill="both", expand=True, padx=1)
            ctk.CTkLabel(btn, text=yr, font=ctk.CTkFont(size=12, weight="bold"), text_color="white").pack(expand=True)

        # Main Columns
        cols_frame = ctk.CTkFrame(self, fg_color="transparent")
        cols_frame.pack(fill="both", expand=True)
        cols_frame.grid_columnconfigure((0, 1), weight=1)

        # Semester 1
        sem1_card = SaaSCard(cols_frame)
        sem1_card.grid(row=0, column=0, padx=10, sticky="nsew")
        
        ctk.CTkLabel(sem1_card, text="Y1 SEMESTER 1: FOUNDATIONS", 
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=20)
        
        self.add_course_item(sem1_card, "CS101: INTRO TO PYTHON", "done")
        self.add_course_item(sem1_card, "MATH101: DISCRETE MATH", "done")
        
        self.add_documents_section(sem1_card, [("LECTURE_NOTES.PDF", "pdf"), ("WORKSHOP_INTRO.MP4", "video")])

        # Semester 2
        sem2_card = SaaSCard(cols_frame)
        sem2_card.grid(row=0, column=1, padx=10, sticky="nsew")
        
        ctk.CTkLabel(sem2_card, text="Y1 SEMESTER 2: CORE CONCEPTS", 
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=20)
        
        self.add_course_item(sem2_card, "CS101: INTRO TO PYTHON", "star")
        self.add_course_item(sem2_card, "MATH101: DISCRETE MATH", "star")
        
        self.add_documents_section(sem2_card, [("AI WORKSHOP", "pdf"), ("VIDEO", "video")])

    def add_course_item(self, parent, title, status):
        item = ctk.CTkFrame(parent, fg_color=COLOR_BG_APP, height=60, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        item.pack(fill="x", padx=20, pady=5)
        item.pack_propagate(False)
        
        # Icon course
        ctk.CTkLabel(item, text="🌐", font=ctk.CTkFont(size=18)).pack(side="left", padx=15)
        
        ctk.CTkLabel(item, text=title, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        
        status_icon = "✔" if status == "done" else "⭐"
        status_color = COLOR_SUCCESS if status == "done" else COLOR_WARNING
        
        ctk.CTkButton(item, text=status_icon, width=28, height=28, corner_radius=14, 
                      fg_color=status_color, text_color="white", font=ctk.CTkFont(size=12)).pack(side="right", padx=15)

    def add_documents_section(self, parent, docs):
        doc_frame = ctk.CTkFrame(parent, fg_color="transparent")
        doc_frame.pack(fill="x", padx=20, pady=(15, 20))
        
        header = ctk.CTkFrame(doc_frame, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="📄 DOCUMENTS", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text="⌵", font=ctk.CTkFont(size=14)).pack(side="right")
        
        for name, type in docs:
            d = ctk.CTkFrame(doc_frame, fg_color="transparent")
            d.pack(fill="x", pady=5)
            icon = "📕" if type == "pdf" else "🎬"
            ctk.CTkLabel(d, text=f"  {icon}  {name}", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_SUB).pack(side="left")