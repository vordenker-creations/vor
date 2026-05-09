import customtkinter as ctk
from config import *
from components import SaaSCard, AnimatedProgressBar, AnimationEngine, CountUpLabel

class AnalyticsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=7)
        grid.grid_columnconfigure(1, weight=3)

        # Left: Chart
        left_card = SaaSCard(grid, border_color="#F59E0B") # Yellow
        left_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(left_card, delay_ms=100)
        
        ctk.CTkLabel(left_card, text="Phân tích (Analytics)", font=ctk.CTkFont(family=FONT_MAIN, size=20, weight="bold")).pack(anchor="w", padx=25, pady=(25, 10))
        ctk.CTkLabel(left_card, text="Overall course trọng tâm khảo sát", font=ctk.CTkFont(family=FONT_MAIN, size=14), text_color=COLOR_TEXT_SUB).pack(anchor="w", padx=25)
        
        # Fake Bar Chart
        chart_frame = ctk.CTkFrame(left_card, fg_color="transparent", height=200)
        chart_frame.pack(fill="x", padx=25, pady=20)
        chart_frame.pack_propagate(False)
        
        y_axis = ctk.CTkFrame(chart_frame, fg_color="transparent", width=40)
        y_axis.pack(side="left", fill="y")
        for val in ["120%", "100%", "80%", "60%", "40%", "20%", "0%"]:
            ctk.CTkLabel(y_axis, text=val, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=10)).pack(expand=True)
            
        bars = ctk.CTkFrame(chart_frame, fg_color="transparent")
        bars.pack(side="left", fill="both", expand=True, padx=10)
        
        bar_data = [("Tuần 1", 0.4), ("Tuần 2", 0.6), ("Nguyên", 0.8), ("Thông số", 1.0), ("Môn", 0.9)]
        for label, pct in bar_data:
            col = ctk.CTkFrame(bars, fg_color="transparent")
            col.pack(side="left", fill="both", expand=True)
            # spacer
            ctk.CTkFrame(col, fg_color="transparent").pack(fill="both", expand=True)
            # bar
            bar_fill = ctk.CTkFrame(col, fg_color=COLOR_PRIMARY if pct < 1.0 else COLOR_SUCCESS)
            # Animation for bar
            bar_fill.pack(fill="x", side="bottom", padx=10)
            def anim_bar(w, h_pct):
                w.configure(height=int(180 * h_pct))
            self.after(200, lambda w=bar_fill, p=pct: anim_bar(w, p))
            
        # Labels below bars
        x_axis = ctk.CTkFrame(left_card, fg_color="transparent")
        x_axis.pack(fill="x", padx=(75, 25))
        for label, _ in bar_data:
            ctk.CTkLabel(x_axis, text=label, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=11)).pack(side="left", expand=True)

        # Right: Key metrics & Skills
        right_card = SaaSCard(grid)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        AnimationEngine.fade_in_widget(right_card, delay_ms=300)
        
        ctk.CTkLabel(right_card, text="Key năng giúp:", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        r1 = ctk.CTkFrame(right_card, fg_color="transparent")
        r1.pack(fill="x", padx=20)
        ctk.CTkLabel(r1, text="Bài tập: 9.0\nĐồ án: 9.0", justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(side="left", expand=True, anchor="w")
        ctk.CTkLabel(r1, text="Kết quả: 9.5", justify="left", font=ctk.CTkFont(family=FONT_MAIN, size=12)).pack(side="left", expand=True, anchor="w")
        
        ctk.CTkLabel(right_card, text="Comparison", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        for label, val in [("11zph", 0.95), ("12gn", 0.32), ("12gn", 0.67), ("12gn", 0.65)]:
            r = ctk.CTkFrame(right_card, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(r, text=label, text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=11), width=40, anchor="w").pack(side="left")
            p = AnimatedProgressBar(r, color=COLOR_PRIMARY, height=4)
            p.pack(side="left", padx=10, fill="x", expand=True)
            p.set_target(val)
            c = CountUpLabel(r, format_str="{}", suffix="%", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(size=11))
            c.pack(side="right")
            c.set_target(int(val*100))

        ctk.CTkLabel(right_card, text="Key skills gap", font=ctk.CTkFont(family=FONT_MAIN, size=15, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        tbl = ctk.CTkFrame(right_card, fg_color="transparent")
        tbl.pack(fill="x", padx=20, pady=(0, 20))
        ctk.CTkLabel(tbl, text="Kỹ năng", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=0, sticky="w", pady=5)
        ctk.CTkLabel(tbl, text="Vã cg", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=1, sticky="e", pady=5, padx=10)
        ctk.CTkLabel(tbl, text="Stáng", text_color=COLOR_TEXT_SUB, font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=2, sticky="e", pady=5)
        
        skills = [("Tdan", "9.0", "5.0"), ("Tim-long", "9.0", "5.5"), ("Thống", "9.0", "5.5"), ("Toán", "9.0", "5.5")]
        for i, (s1, s2, s3) in enumerate(skills):
            ctk.CTkLabel(tbl, text=s1, font=ctk.CTkFont(size=11)).grid(row=i+1, column=0, sticky="w", pady=2)
            ctk.CTkLabel(tbl, text=s2, font=ctk.CTkFont(size=11)).grid(row=i+1, column=1, sticky="e", pady=2, padx=10)
            ctk.CTkLabel(tbl, text=s3, font=ctk.CTkFont(size=11)).grid(row=i+1, column=2, sticky="e", pady=2)
        tbl.grid_columnconfigure(0, weight=1)
