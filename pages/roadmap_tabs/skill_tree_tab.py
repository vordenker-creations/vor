import customtkinter as ctk
from config import *
from components import SaaSCard
import tkinter as tk

class SkillTreeTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        main_card = SaaSCard(self)
        main_card.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header: Timeline Y1-Y4
        header_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header_frame, text="4-YEAR CAREER ROADMAP: SKILL TREE", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        timeline = ctk.CTkFrame(header_frame, fg_color="transparent")
        timeline.pack(side="right")
        for i, year in enumerate(["Y1", "Y2", "Y3", "Y4"]):
            bg = COLOR_PRIMARY if year == "Y1" else COLOR_BORDER
            btn = ctk.CTkButton(timeline, text=year, width=100, height=30, fg_color=bg, 
                                text_color="white" if year == "Y1" else COLOR_TEXT_SUB, corner_radius=15)
            btn.pack(side="left", padx=5)

        # Canvas Area for Skill Tree
        canvas_container = ctk.CTkFrame(main_card, fg_color=COLOR_BG_APP, corner_radius=15)
        canvas_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.canvas = tk.Canvas(canvas_container, bg=get_color(COLOR_BG_APP), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Thêm các nhóm (Labels)
        self.create_group_label(200, 50, "FOUNDATIONS")
        self.create_group_label(450, 50, "SOFTWARE ENGINEERING")
        self.create_group_label(700, 50, "AI & DATA")

        # Nodes (x, y, text, status: 'done', 'todo', 'core')
        nodes = [
            # Y1
            (100, 150, "PYTHON", "core"),
            (200, 100, "CS101", "done"),
            (200, 200, "CS102", "done"),
            # Y2
            (350, 80, "CS101", "todo"),
            (350, 150, "IT202", "todo"),
            (350, 220, "CS101", "todo"),
            # Y3
            (500, 100, "IT202", "todo"),
            (500, 180, "IT302", "todo"),
            (600, 120, "SE301", "done"),
            # Y4
            (750, 100, "CE205", "todo"),
            (750, 200, "SE303", "todo"),
            (850, 80, "PEGN", "core"),
        ]

        # Vẽ connections (giả lập)
        self.canvas.create_line(150, 150, 200, 100, fill=get_color(COLOR_SUCCESS), width=2)
        self.canvas.create_line(150, 150, 200, 200, fill=get_color(COLOR_SUCCESS), width=2)
        self.canvas.create_line(250, 100, 350, 80, fill=get_color(COLOR_TEXT_SUB), width=1)
        self.canvas.create_line(250, 200, 350, 220, fill=get_color(COLOR_SUCCESS), width=2)

        for x, y, name, status in nodes:
            self.draw_node(x, y, name, status)

        # Progress bar ở góc dưới
        prog_frame = ctk.CTkFrame(canvas_container, fg_color="transparent")
        prog_frame.place(relx=0.05, rely=0.9, anchor="sw")
        ctk.CTkLabel(prog_frame, text="ROADMAP PROGRESS: 65%", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_PRIMARY).pack(side="left", padx=10)
        bar = ctk.CTkProgressBar(prog_frame, width=150, height=8, progress_color=COLOR_PRIMARY)
        bar.pack(side="left")
        bar.set(0.65)

    def create_group_label(self, x, y, text):
        lbl = ctk.CTkLabel(self.canvas, text=text, font=ctk.CTkFont(size=10, weight="bold"), text_color=COLOR_TEXT_SUB)
        lbl.place(x=x, y=y)

    def draw_node(self, x, y, name, status):
        color = COLOR_SUCCESS if status == "done" else COLOR_BORDER
        text_color = "white" if status == "done" else COLOR_TEXT_SUB
        border = COLOR_SUCCESS if status == "done" else COLOR_BORDER
        
        if status == "core":
            color = COLOR_WARNING
            text_color = "white"
            border = COLOR_WARNING

        btn = ctk.CTkButton(self.canvas, text=name, width=60, height=60, corner_radius=30,
                            fg_color=COLOR_BG_CARD, border_width=2, border_color=border,
                            text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(size=10, weight="bold"),
                            hover=False)
        btn.place(x=x-30, y=y-30)
        
        if status == "done":
            ctk.CTkLabel(btn, text="✔", font=ctk.CTkFont(size=10), text_color=COLOR_SUCCESS, fg_color="transparent").place(relx=0.5, rely=0.8, anchor="center")
        elif status == "core":
             ctk.CTkLabel(btn, text="⭐", font=ctk.CTkFont(size=12), text_color="white", fg_color="transparent").place(relx=0.5, rely=0.2, anchor="center")