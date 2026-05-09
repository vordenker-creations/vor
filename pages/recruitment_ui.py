import customtkinter as ctk
import tkinter as tk
import math
from config import *
from components import SaaSCard

class CircularProgress(ctk.CTkFrame):
    def __init__(self, master, percentage, size=60, color=COLOR_PRIMARY, bg_color=COLOR_BG_CARD, **kwargs):
        super().__init__(master, fg_color="transparent", width=size, height=size, **kwargs)
        self.percentage = percentage
        self.canvas = tk.Canvas(self, width=size, height=size, bg=get_color(bg_color), highlightthickness=0)
        self.canvas.pack()
        
        # Draw background circle
        thickness = 5
        offset = thickness // 2 + 2
        self.canvas.create_oval(offset, offset, size-offset, size-offset, outline=get_color(COLOR_BORDER), width=thickness)
        
        # Draw progress arc
        extent = -(360 * percentage / 100) # Negative for clockwise
        self.canvas.create_arc(offset, offset, size-offset, size-offset, start=90, extent=extent, outline=get_color(color), style=tk.ARC, width=thickness)
        
        # Draw percentage text
        self.canvas.create_text(size//2, size//2, text=f"{percentage}%", font=(FONT_MAIN, 10, "bold"), fill=get_color(COLOR_TEXT_MAIN))

class RecruitmentUI(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        
        ctk.CTkLabel(self, text="AI Recruitment Matching", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=35, pady=(35, 20))

        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=25)
        grid_container.grid_columnconfigure((0, 1), weight=1, uniform="col")

        jobs_data = [
            {"company": "Google Vietnam", "location": "TP. HCM", "title": "AI Research Engineer", "salary": "Thỏa thuận", "match": 92, "skills_has": ["Python", "PyTorch"], "skills_missing": ["C++"]},
            {"company": "Shopee Vietnam", "location": "Hà Nội", "title": "Data Scientist", "salary": "25tr - 40tr VNĐ", "match": 75, "skills_has": ["Python", "SQL"], "skills_missing": ["Spark", "Airflow"]},
            {"company": "VNG Corporation", "location": "TP. HCM", "title": "Machine Learning Engineer", "salary": "30tr - 50tr VNĐ", "match": 85, "skills_has": ["Python", "TensorFlow"], "skills_missing": ["Docker"]},
            {"company": "MoMo", "location": "TP. HCM", "title": "Data Analyst", "salary": "20tr - 35tr VNĐ", "match": 60, "skills_has": ["SQL"], "skills_missing": ["Python", "Tableau"]}
        ]

        for i, job in enumerate(jobs_data):
            row = i // 2
            col = i % 2
            self.create_job_card(grid_container, row, col, job)

    def create_job_card(self, parent, row, col, job):
        card = SaaSCard(parent)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # Left header: Company & Title
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(info_frame, text=job["company"], font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_TEXT_SUB).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=job["title"], font=ctk.CTkFont(family=FONT_MAIN, size=16, weight="bold"), text_color=COLOR_TEXT_MAIN, wraplength=200, justify="left").pack(anchor="w")
        
        # Right header: Circular Progress
        match_color = COLOR_SUCCESS if job["match"] >= 80 else COLOR_WARNING if job["match"] >= 60 else "#DC2626"
        CircularProgress(header, percentage=job["match"], color=match_color).pack(side="right")

        # Details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(details_frame, text=f"📍 {job['location']}   💰 {job['salary']}", font=ctk.CTkFont(family=FONT_MAIN, size=13), text_color=COLOR_TEXT_SUB).pack(anchor="w")

        # Skills Match Analysis
        skills_frame = ctk.CTkFrame(card, fg_color=COLOR_BG_APP, corner_radius=8)
        skills_frame.pack(fill="x", padx=20, pady=10)
        
        has_str = ", ".join(job["skills_has"])
        ctk.CTkLabel(skills_frame, text=f"✓ Đã có: {has_str}", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_SUCCESS).pack(anchor="w", padx=10, pady=(10, 5))
        
        missing_frame = ctk.CTkFrame(skills_frame, fg_color="transparent")
        missing_frame.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(missing_frame, text="⚠ Thiếu:", font=ctk.CTkFont(family=FONT_MAIN, size=12), text_color=COLOR_WARNING).pack(side="left")
        
        for missing in job["skills_missing"]:
            skill_btn = ctk.CTkButton(missing_frame, text=f"{missing} +", height=24, width=60, 
                                      fg_color=COLOR_WARNING, text_color="white", font=ctk.CTkFont(size=11, weight="bold"), corner_radius=12)
            skill_btn.pack(side="left", padx=5)
            # Tooltip can be added here

        # Apply Button
        btn = ctk.CTkButton(card, text="Ứng tuyển ngay", fg_color=COLOR_PRIMARY_LIGHT, text_color=COLOR_PRIMARY, 
                            font=ctk.CTkFont(family=FONT_MAIN, size=13, weight="bold"), corner_radius=6, height=35)
        btn.pack(anchor="w", padx=20, pady=(10, 25))

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x700")
    app.configure(fg_color=COLOR_BG_APP)
    page = RecruitmentUI(app)
    page.pack(fill="both", expand=True)
    app.mainloop()