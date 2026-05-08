import customtkinter as ctk
from config import *
from components import SaaSCard

class YearDetailsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # --- PHẦN 1: HEADER & AI ANALYSIS (Giống ảnh Student & CV Center) ---
        analysis_grid = ctk.CTkFrame(self, fg_color="transparent")
        analysis_grid.pack(fill="x", pady=(0, 20))
        analysis_grid.grid_columnconfigure(0, weight=6) # Cột trái to cho AI Analysis
        analysis_grid.grid_columnconfigure(1, weight=4) # Cột phải cho danh sách CV/Hồ sơ

        # Khối AI Analysis
        ai_card = SaaSCard(analysis_grid)
        ai_card.grid(row=0, column=0, padx=5, sticky="nsew")
        
        ctk.CTkLabel(ai_card, text="AUTO-GENERATED AI CV & CAREER PATH ANALYSIS", 
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Giả lập khu vực biểu đồ Job Match 92%
        match_frame = ctk.CTkFrame(ai_card, fg_color=COLOR_BG_APP, corner_radius=10)
        match_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(match_frame, text="JOB MATCH STATUS: 92%", font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_PRIMARY).pack(pady=15)
        
        # Phần AI Suggestions
        ctk.CTkLabel(ai_card, text="AI SUGGESTIONS:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(10, 5))
        sug_txt = "• SUGGESTION: Add your Advanced Python course completion to your 'Skills' section.\n• IMPROVEMENT: Rephrase your bio to highlight deep learning projects."
        ctk.CTkLabel(ai_card, text=sug_txt, font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_SUB, justify="left").pack(anchor="w", padx=25, pady=(0, 20))
        
        ctk.CTkButton(ai_card, text="✨ GENERATE NEW AI CV", fg_color=COLOR_PRIMARY, text_color="white", height=35, font=ctk.CTkFont(weight="bold")).pack(fill="x", padx=20, pady=(0, 20))

        # Khối Danh sách hồ sơ (My CVs)
        cv_card = SaaSCard(analysis_grid)
        cv_card.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(cv_card, text="MY CVs / DOCUMENTS", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))
        
        for i, name in enumerate(["Resume 1 (Auto AI)", "Resume 2 (Manual)"]):
            item = ctk.CTkFrame(cv_card, fg_color="transparent")
            item.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(item, text=f"📄 {name}", font=ctk.CTkFont(size=13)).pack(side="left")
            ctk.CTkButton(item, text="VIEW", width=50, height=25, fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, font=ctk.CTkFont(size=10, weight="bold")).pack(side="right", padx=2)

        # --- PHẦN 2: CHI TIẾT HỌC PHẦN Y1 ---
        ctk.CTkLabel(self, text="YEAR 1: ACADEMIC DETAILS", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(20, 10))
        
        course_grid = ctk.CTkFrame(self, fg_color="transparent")
        course_grid.pack(fill="x")
        course_grid.grid_columnconfigure((0, 1), weight=1)

        # Học kỳ 1
        sem1 = SaaSCard(course_grid)
        sem1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(sem1, text="SEMESTER 1", font=ctk.CTkFont(weight="bold"), text_color=COLOR_PRIMARY).pack(pady=10)
        self.add_course_row(sem1, "Discrete Math", "100%")
        self.add_course_row(sem1, "Intro to AI", "100%")
        self.add_course_row(sem1, "C++ Basic", "100%")

        # Học kỳ 2
        sem2 = SaaSCard(course_grid)
        sem2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(sem2, text="SEMESTER 2 (CURRENT)", font=ctk.CTkFont(weight="bold"), text_color="#10B981").pack(pady=10)
        self.add_course_row(sem2, "Advanced Python", "80%")
        self.add_course_row(sem2, "Data Structures", "45%")
        self.add_course_row(sem2, "English Communication", "20%")

    def add_course_row(self, parent, name, progress):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(row, text=progress, font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT_SUB).pack(side="right")
        # Thanh tiến trình mini
        p_val = int(progress.replace('%','')) / 100
        bar = ctk.CTkProgressBar(parent, height=4, progress_color=COLOR_PRIMARY)
        bar.pack(fill="x", padx=15, pady=(0, 10))
        bar.set(p_val)