import customtkinter as ctk
import tkinter as tk
import random
from config import *
from components import GlassCard

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login=None, on_register_click=None):
        super().__init__(master, fg_color=COLOR_BG_APP)
        self.on_login = on_login
        self.on_register_click = on_register_click
        
        # Main Grid System (3:7 ratio)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_background()
        self._setup_sidebar()
        self._setup_content()
        self._setup_footer()

    def _setup_background(self):
        # Canvas for floating deep space circles
        self.canvas = tk.Canvas(
            self, bg=get_color(COLOR_BG_APP), highlightthickness=0, 
            bd=0, relief="flat"
        )
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", lambda e: self._draw_decorations())

    def _draw_decorations(self):
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10: return

        colors = ["#00D1FF", "#10B981", "#6366F1"] # Cyan, Green, Indigo
        for _ in range(15):
            x = random.randint(0, w)
            y = random.randint(0, h)
            r = random.randint(20, 80)
            color = random.choice(colors)
            # Simulating blur with multiple concentric circles
            for i in range(5):
                alpha_r = r + (i * 10)
                self.canvas.create_oval(
                    x - alpha_r, y - alpha_r, x + alpha_r, y + alpha_r,
                    outline=color, width=1, tags="decor"
                )

    def _setup_sidebar(self):
        # Column 0: AI Insight Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color="transparent")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=40, pady=60)
        
        ctk.CTkLabel(
            self.sidebar, text="AI INSIGHT", 
            font=ctk.CTkFont(family=FONT_MAIN, size=34, weight="bold"),
            text_color=COLOR_PRIMARY, anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            self.sidebar, text="Elevate your career with AI-driven analytics and personal roadmaps.",
            font=ctk.CTkFont(family=FONT_MAIN, size=14),
            text_color=COLOR_TEXT_SUB, wraplength=250, justify="left", anchor="w"
        ).pack(fill="x", pady=(0, 40))

        # Skill Tags Container
        tag_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        tag_frame.pack(fill="x")
        
        tags = ["Python", "Neural Networks", "NLP", "Computer Vision", "Data Science", "Cloud AI"]
        for tag in tags:
            btn = ctk.CTkButton(
                tag_frame, text=f"• {tag}", width=100, height=32, corner_radius=16,
                fg_color=COLOR_BG_CARD, text_color=COLOR_TEXT_MAIN,
                border_width=1, border_color=COLOR_BORDER,
                font=ctk.CTkFont(family=FONT_MAIN, size=11), hover=False
            )
            btn.pack(side="top", anchor="w", pady=5)

    def _setup_content(self):
        # Column 1: Main Login Card
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        # Header Controls (Top Right)
        self.header = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.header.place(relx=1.0, rely=0, x=-30, y=30, anchor="ne")
        
        self.theme_switch = ctk.CTkSwitch(
            self.header, text="🌙", command=self.toggle_theme,
            progress_color=COLOR_PRIMARY, font=ctk.CTkFont(size=16)
        )
        self.theme_switch.pack(side="right")
        if ctk.get_appearance_mode() == "Light":
            self.theme_switch.select()
            self.theme_switch.configure(text="☀️")

        # Login Card
        self.card = GlassCard(self.main_area, enable_glow=True)
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.75)
        
        # Branding
        ctk.CTkLabel(
            self.card, text="LOGIN",
            font=ctk.CTkFont(family=FONT_MAIN, size=28, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        ).pack(pady=(50, 5))
        
        ctk.CTkLabel(
            self.card, text="Access your professional bridge.",
            font=ctk.CTkFont(family=FONT_MAIN, size=14),
            text_color=COLOR_TEXT_SUB
        ).pack(pady=(0, 40))

        # Input Container
        form = ctk.CTkFrame(self.card, fg_color="transparent")
        form.pack(fill="x", padx=60)

        self.email_entry = self._create_input(form, "Email Address", "👤 email@vku.udn.vn")
        self.pass_entry = self._create_input(form, "Password", "🔒 ••••••••", show="*")

        # Action Buttons
        self.login_btn = ctk.CTkButton(
            self.card, text="LOGIN", height=45, corner_radius=10,
            fg_color=COLOR_PRIMARY, text_color="white",
            font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"),
            hover_color="#00B4D8", command=self._handle_login
        )
        self.login_btn.pack(fill="x", padx=60, pady=(40, 15))

        # Register Redirect
        reg_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        reg_frame.pack(pady=(0, 40))
        ctk.CTkLabel(reg_frame, text="New here?", font=(FONT_MAIN, 12), text_color=COLOR_TEXT_SUB).pack(side="left")
        ctk.CTkButton(reg_frame, text="Create Account", fg_color="transparent", text_color=COLOR_PRIMARY, 
                      font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), width=100, hover=False, 
                      command=self.on_register_click).pack(side="left")

    def _setup_footer(self):
        # Random AI Quotes
        quotes = [
            "\"AI is the new electricity.\" - Andrew Ng",
            "\"Machine learning is the last invention humanity will ever need.\" - Nick Bostrom",
            "\"The goal is to turn data into information, and information into insight.\" - Carly Fiorina",
            "\"AI will either be the best or worst thing for humanity.\" - Stephen Hawking"
        ]
        
        self.quote_lbl = ctk.CTkLabel(
            self, text=random.choice(quotes),
            font=ctk.CTkFont(family=FONT_MAIN, size=11, slant="italic"),
            text_color=COLOR_TEXT_SUB
        )
        self.quote_lbl.place(relx=0.5, rely=0.96, anchor="center")

    def _create_input(self, parent, label, placeholder, show=None):
        ctk.CTkLabel(parent, text=label, font=(FONT_MAIN, 11, "bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=(15, 5))
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder, show=show,
            height=40, corner_radius=10, border_color=COLOR_BORDER,
            fg_color=COLOR_BG_APP
        )
        entry.pack(fill="x")
        entry.bind("<FocusIn>", lambda e: entry.configure(border_color=COLOR_PRIMARY, border_width=2))
        entry.bind("<FocusOut>", lambda e: entry.configure(border_color=COLOR_BORDER, border_width=1))
        return entry

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="☀️")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="🌙")
        self.configure(fg_color=COLOR_BG_APP)
        self.canvas.configure(bg=get_color(COLOR_BG_APP))
        self._draw_decorations()

    def _handle_login(self):
        if self.on_login:
            self.on_login(self.email_entry.get(), self.pass_entry.get())

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x700")
    app.title("AI-Career Bridge | Login")
    login = LoginPage(app, on_register_click=lambda: print("Switch to Register"))
    login.pack(fill="both", expand=True)
    app.mainloop()