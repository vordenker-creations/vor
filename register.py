import customtkinter as ctk
import tkinter as tk
import random
from config import *
from components import GlassCard

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master, on_back_click=None):
        super().__init__(master, fg_color=COLOR_BG_APP)
        self.on_back_click = on_back_click
        
        # Grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._setup_background()
        self._setup_header()
        self._setup_content()

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

        colors = ["#00D1FF", "#10B981", "#6366F1"]
        for _ in range(12):
            x = random.randint(0, w)
            y = random.randint(0, h)
            r = random.randint(30, 100)
            color = random.choice(colors)
            for i in range(4):
                alpha_r = r + (i * 15)
                self.canvas.create_oval(
                    x - alpha_r, y - alpha_r, x + alpha_r, y + alpha_r,
                    outline=color, width=1, tags="decor"
                )

    def _setup_header(self):
        # Header Controls (Top Right)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.place(relx=1.0, rely=0, x=-30, y=30, anchor="ne")
        
        # Theme Switcher
        self.theme_switch = ctk.CTkSwitch(
            self.header, text="🌙", command=self.toggle_theme,
            progress_color=COLOR_PRIMARY, font=ctk.CTkFont(size=16)
        )
        self.theme_switch.pack(side="right")
        if ctk.get_appearance_mode() == "Light":
            self.theme_switch.select()
            self.theme_switch.configure(text="☀️")

    def _setup_content(self):
        # Main Register Card - Optimized Dimensions
        self.card = GlassCard(self, enable_glow=True)
        # 75% width, 78% height, shifted down to avoid header
        self.card.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.75, relheight=0.78)

        # Container for content to allow scrolling
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Header Title
        title_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10))
        ctk.CTkLabel(title_frame, text="CREATE ACCOUNT", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=28, weight="bold"), 
                     text_color=COLOR_PRIMARY).pack()
        ctk.CTkLabel(title_frame, text="Start your AI career journey today.", 
                     font=ctk.CTkFont(family=FONT_MAIN, size=13), 
                     text_color=COLOR_TEXT_SUB).pack()

        # Multi-column Grid
        grid_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=30)
        grid_container.grid_columnconfigure((0, 1), weight=1, uniform="col")

        # --- ROW 0: Name & Major ---
        self.name_entry = self._create_field(grid_container, "Full Name", "👤 Full Name", row=0, col=0)
        
        major_frame = ctk.CTkFrame(grid_container, fg_color="transparent")
        major_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=8)
        ctk.CTkLabel(major_frame, text="Major", font=(FONT_MAIN, 11, "bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 2))
        self.major_var = ctk.StringVar(value="Select Major")
        self.major_menu = ctk.CTkOptionMenu(
            major_frame, values=["Computer Science", "Information Technology", "AI & Data Science", "Digital Business"],
            variable=self.major_var, height=40, corner_radius=10, 
            fg_color=COLOR_BG_APP, text_color=COLOR_TEXT_MAIN,
            button_color=COLOR_PRIMARY, button_hover_color="#00B4D8", dynamic_resizing=False
        )
        self.major_menu.pack(fill="x")

        # --- ROW 1: Email & Current Semester ---
        self.email_entry = self._create_field(grid_container, "Student Email", "📧 email@vku.udn.vn", row=1, col=0)
        self.sem_curr_entry = self._create_field(grid_container, "Current Semester", "📖 e.g. 4", row=1, col=1)

        # --- ROW 2: University & Total Semesters ---
        self.univ_entry = self._create_field(grid_container, "University", "🏫 University Name", row=2, col=0)
        self.sem_total_entry = self._create_field(grid_container, "Total Semesters", "📅 e.g. 8", row=2, col=1)

        # --- ROW 3: Password & Confirm Password ---
        pass_col = ctk.CTkFrame(grid_container, fg_color="transparent")
        pass_col.grid(row=3, column=0, sticky="nsew", padx=(0, 15), pady=8)
        ctk.CTkLabel(pass_col, text="Password", font=(FONT_MAIN, 11, "bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 2))
        self.pass_entry = ctk.CTkEntry(pass_col, height=40, corner_radius=10, show="*", fg_color=COLOR_BG_APP, border_color=COLOR_BORDER)
        self.pass_entry.pack(fill="x")
        self.pass_entry.bind("<KeyRelease>", self._update_strength)
        
        # Strength Meter
        self.meter_frame = ctk.CTkFrame(pass_col, fg_color="transparent", height=6)
        self.meter_frame.pack(fill="x", pady=(5, 0))
        self.meter_segments = []
        for i in range(4):
            seg = ctk.CTkFrame(self.meter_frame, fg_color=COLOR_BORDER, height=4, corner_radius=2)
            seg.pack(side="left", fill="x", expand=True, padx=1)
            self.meter_segments.append(seg)

        self.confirm_pass_entry = self._create_field(grid_container, "Confirm Password", "🔒 Confirm Password", row=3, col=1, is_password=True)

        # Terms Checkbox
        self.terms_var = ctk.BooleanVar(value=False)
        self.terms_check = ctk.CTkCheckBox(
            self.scroll_frame, text="I agree to the Terms & Conditions.", 
            variable=self.terms_var, font=(FONT_MAIN, 10), border_width=2, fg_color=COLOR_PRIMARY
        )
        self.terms_check.pack(pady=15)

        # Action Buttons
        btn_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=(0, 15))
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame, text="CANCEL", height=45, corner_radius=10, 
            fg_color="transparent", border_width=1, border_color=COLOR_BORDER,
            text_color=COLOR_TEXT_MAIN, hover_color=COLOR_BG_APP, command=self.on_back_click
        )
        self.cancel_btn.pack(side="left", expand=True, padx=(0, 8))

        self.reg_btn = ctk.CTkButton(
            btn_frame, text="REGISTER NOW", height=45, corner_radius=10,
            fg_color=COLOR_PRIMARY, text_color="white", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"),
            hover_color="#00B4D8", command=self._handle_register
        )
        self.reg_btn.pack(side="left", expand=True, padx=(8, 0))

        # Login Redirect
        login_redir = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        login_redir.pack(pady=(0, 20))
        ctk.CTkLabel(login_redir, text="Already have an account?", font=(FONT_MAIN, 11), text_color=COLOR_TEXT_SUB).pack(side="left")
        ctk.CTkButton(login_redir, text="Login", fg_color="transparent", text_color=COLOR_PRIMARY, 
                      font=ctk.CTkFont(family=FONT_MAIN, size=11, weight="bold"), width=50, hover=False, 
                      command=self.on_back_click).pack(side="left")

    def _create_field(self, parent, label, placeholder, row=None, col=None, is_password=False):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        if row is not None and col is not None:
            padx = (0, 15) if col == 0 else (15, 0)
            field_frame.grid(row=row, column=col, sticky="nsew", pady=8, padx=padx)
        else:
            field_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(field_frame, text=label, font=(FONT_MAIN, 11, "bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=(0, 2))
        
        entry = ctk.CTkEntry(
            field_frame, placeholder_text=placeholder, height=40, corner_radius=10, 
            fg_color=COLOR_BG_APP, border_color=COLOR_BORDER, show="*" if is_password else None
        )
        entry.pack(fill="x")
        entry.bind("<FocusIn>", lambda e: entry.configure(border_color=COLOR_PRIMARY, border_width=2))
        entry.bind("<FocusOut>", lambda e: entry.configure(border_color=COLOR_BORDER, border_width=1))
        return entry

    def _update_strength(self, event=None):
        p = self.pass_entry.get()
        level = 0
        if len(p) > 0: level = 1
        if len(p) > 5: level = 2
        if len(p) > 8: level = 3
        if len(p) > 10 and any(c.isdigit() for c in p): level = 4
        
        colors = [COLOR_DANGER, COLOR_WARNING, "#84CC16", COLOR_SUCCESS]
        for i in range(4):
            if i < level:
                self.meter_segments[i].configure(fg_color=colors[level-1])
            else:
                self.meter_segments[i].configure(fg_color=COLOR_BORDER)

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

    def _handle_register(self):
        if not self.terms_var.get():
            print("Please agree to terms.")
            return
        print("Registering student...")

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1100x800")
    app.title("AI-Career Bridge | Register")
    reg = RegisterPage(app, on_back_click=lambda: print("Back to Login"))
    reg.pack(fill="both", expand=True)
    app.mainloop()