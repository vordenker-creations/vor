import customtkinter as ctk
import tkinter as tk
from config import *
from components import SaaSCard

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
        
        self.nodes_data = {}
        self.edges_data = []

        self._setup_graph()
        self._draw_graph()

        # Progress bar
        prog_frame = ctk.CTkFrame(canvas_container, fg_color="transparent")
        prog_frame.place(relx=0.05, rely=0.9, anchor="sw")
        ctk.CTkLabel(prog_frame, text="ROADMAP PROGRESS: 65%", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_PRIMARY).pack(side="left", padx=10)
        bar = ctk.CTkProgressBar(prog_frame, width=150, height=8, progress_color=COLOR_PRIMARY)
        bar.pack(side="left")
        bar.set(0.65)

    def _setup_graph(self):
        # Define Graph Theory based Nodes and Edges
        self.nodes_data = {
            "N1": {"x": 100, "y": 150, "name": "PYTHON", "status": "core"},
            "N2": {"x": 250, "y": 100, "name": "CS101", "status": "done"},
            "N3": {"x": 250, "y": 200, "name": "CS102", "status": "done"},
            "N4": {"x": 400, "y": 80,  "name": "DB201", "status": "todo"},
            "N5": {"x": 400, "y": 150, "name": "IT202", "status": "todo"},
            "N6": {"x": 550, "y": 120, "name": "SE301", "status": "done"},
            "N7": {"x": 700, "y": 100, "name": "AI401", "status": "todo"},
            "N8": {"x": 700, "y": 200, "name": "SE303", "status": "todo"},
            "N9": {"x": 850, "y": 150, "name": "FINAL", "status": "core"},
        }
        self.edges_data = [
            ("N1", "N2"), ("N1", "N3"),
            ("N2", "N4"), ("N2", "N5"),
            ("N3", "N5"),
            ("N5", "N6"), ("N4", "N6"),
            ("N6", "N7"), ("N6", "N8"),
            ("N7", "N9"), ("N8", "N9")
        ]

    def _draw_graph(self):
        self.canvas.delete("all")
        
        # Draw edges first (Z-index background)
        for src, dst in self.edges_data:
            n1 = self.nodes_data[src]
            n2 = self.nodes_data[dst]
            color = get_color(COLOR_SUCCESS) if n1["status"] in ["done", "core"] and n2["status"] in ["done", "core"] else get_color(COLOR_TEXT_SUB)
            self.canvas.create_line(n1["x"], n1["y"], n2["x"], n2["y"], fill=color, width=2, tags="edge")

        # Draw nodes (Z-index foreground)
        for node_id, data in self.nodes_data.items():
            self._draw_node(node_id, data)

    def _draw_node(self, node_id, data):
        x, y = data["x"], data["y"]
        r = 30
        status = data["status"]

        bg_color = get_color(COLOR_BG_CARD)
        border_color = get_color(COLOR_SUCCESS) if status == "done" else get_color(COLOR_BORDER)
        text_color = get_color(COLOR_TEXT_MAIN)
        
        if status == "core":
            border_color = get_color(COLOR_WARNING)
            bg_color = get_color(COLOR_BG_CARD)
        elif status == "done":
            bg_color = get_color(COLOR_SUCCESS)
            text_color = "white"

        # Create glow layer (hidden initially)
        glow = self.canvas.create_oval(x-r-10, y-r-10, x+r+10, y+r+10, fill="", outline=get_color(COLOR_PRIMARY), width=4, state="hidden", tags=(f"glow_{node_id}", "glow"))

        # Create node circle
        node = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=bg_color, outline=border_color, width=3, tags=(node_id, "node"))
        
        # Create text
        txt = self.canvas.create_text(x, y, text=data["name"], fill=text_color, font=(FONT_MAIN, 10, "bold"), tags=(node_id, "text"))

        # Bind events
        for item in (node, txt):
            self.canvas.tag_bind(item, "<Enter>", lambda e, nid=node_id: self._on_hover_enter(nid))
            self.canvas.tag_bind(item, "<Leave>", lambda e, nid=node_id: self._on_hover_leave(nid))

    def _on_hover_enter(self, node_id):
        self.canvas.itemconfig(f"glow_{node_id}", state="normal")
        # Z-index management: bring node and text to front
        self.canvas.tag_raise(f"glow_{node_id}")
        self.canvas.tag_raise(node_id)

    def _on_hover_leave(self, node_id):
        self.canvas.itemconfig(f"glow_{node_id}", state="hidden")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x500")
    app.configure(fg_color=COLOR_BG_APP)
    tab = SkillTreeTab(app)
    tab.pack(fill="both", expand=True)
    app.mainloop()