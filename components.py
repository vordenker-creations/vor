import customtkinter as ctk
import tkinter as tk
import time
import math
from config import *

class AnimationEngine:
    """Utility class to handle smooth frame-by-frame animations."""
    @staticmethod
    def animate_widget_width(widget, target_width, current_width, step=10, delay=20):
        try:
            if not widget.winfo_exists(): return
            if abs(target_width - current_width) <= step:
                widget.configure(width=target_width)
                return
            
            new_width = current_width + step if target_width > current_width else current_width - step
            widget.configure(width=new_width)
            widget.after(delay, lambda: AnimationEngine.animate_widget_width(widget, target_width, new_width, step, delay))
        except Exception: pass

    @staticmethod
    def fade_in_widget(widget, delay_ms=0, initial_alpha=0):
        """Simulates a staggered reveal by delaying the mapping of the widget."""
        def reveal():
            try:
                if widget.winfo_exists(): widget.pack(fill="x", pady=10, padx=20)
            except Exception: pass
        widget.pack_forget()
        widget.after(delay_ms, reveal)

class BaseComponent(ctk.CTkFrame):
    """Base class for all components to ensure consistent scaling and logic."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        try:
            self._scaling_factor = ctk.ScalingTracker.get_widget_scaling(self)
        except AttributeError:
            self._scaling_factor = 1.0

class BasePage(ctk.CTkFrame):
    """Base class for all pages."""
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

class GlassCard(BaseComponent):
    """A card with simulated glassmorphism, glowing border, and hover animations."""
    def __init__(self, master, enable_glow=True, hover_effect=True, **kwargs):
        self.enable_glow = enable_glow
        self.hover_effect = hover_effect
        self.default_border = kwargs.pop("border_color", COLOR_BORDER)
        fg_color = kwargs.pop("fg_color", COLOR_BG_CARD)
        border_width = kwargs.pop("border_width", 1)
        corner_radius = kwargs.pop("corner_radius", 20)
        
        if self.enable_glow:
            self.glow_frame = ctk.CTkFrame(master, fg_color=self.default_border, corner_radius=corner_radius)
            super().__init__(self.glow_frame, fg_color=fg_color, border_width=border_width, 
                             border_color=self.default_border, corner_radius=corner_radius, **kwargs)
            super().pack(fill="both", expand=True, padx=1, pady=1)
        else:
            self.glow_frame = None
            super().__init__(master, fg_color=fg_color, border_width=border_width, 
                             border_color=self.default_border, corner_radius=corner_radius, **kwargs)

        if self.hover_effect:
            self.bind("<Enter>", self._on_enter, add="+")
            self.bind("<Leave>", self._on_leave, add="+")

    def _on_enter(self, event=None):
        if self.glow_frame: self.glow_frame.configure(fg_color=COLOR_PRIMARY)
        else: self.configure(border_color=COLOR_PRIMARY)

    def _on_leave(self, event=None):
        if event:
            x, y = event.x_root, event.y_root
            try:
                x0, y0 = self.winfo_rootx(), self.winfo_rooty()
                x1, y1 = x0 + self.winfo_width(), y0 + self.winfo_height()
                if x0 <= x <= x1 and y0 <= y <= y1: return
            except Exception: pass
        if self.glow_frame: self.glow_frame.configure(fg_color=self.default_border)
        else: self.configure(border_color=self.default_border)

    # Overrides to handle glow_frame
    def pack(self, **kwargs):
        if self.glow_frame: self.glow_frame.pack(**kwargs)
        else: super().pack(**kwargs)
    
    def grid(self, **kwargs):
        if self.glow_frame: self.glow_frame.grid(**kwargs)
        else: super().grid(**kwargs)
    
    def place(self, **kwargs):
        if self.glow_frame: self.glow_frame.place(**kwargs)
        else: super().place(**kwargs)
            
    def pack_forget(self):
        if self.glow_frame: self.glow_frame.pack_forget()
        else: super().pack_forget()

    def grid_forget(self):
        if self.glow_frame: self.glow_frame.grid_forget()
        else: super().grid_forget()

    def configure(self, **kwargs):
        if self.glow_frame:
            if "fg_color" in kwargs: super().configure(fg_color=kwargs.pop("fg_color"))
            if "border_color" in kwargs:
                self.default_border = kwargs["border_color"]
                super().configure(border_color=kwargs.pop("border_color"))
            self.glow_frame.configure(**kwargs)
        else:
            if "border_color" in kwargs: self.default_border = kwargs["border_color"]
            super().configure(**kwargs)

def SaaSCard(master, **kwargs):
    return GlassCard(master, enable_glow=True, hover_effect=True, **kwargs)

class StatusPulse(BaseComponent):
    """A small pulsing dot (Neon) indicating AI thinking or online status."""
    def __init__(self, master, color=COLOR_SUCCESS, size=12, **kwargs):
        super().__init__(master, fg_color="transparent", width=size*2, height=size*2, **kwargs)
        self.color = color
        self.size = size
        self.canvas = tk.Canvas(self, width=size*2, height=size*2, bg=get_color(COLOR_BG_APP), highlightthickness=0)
        self.canvas.pack(expand=True)
        self.dot = self.canvas.create_oval(size//2, size//2, size + size//2, size + size//2, fill=get_color(self.color), outline="")
        self.glow = self.canvas.create_oval(size//2, size//2, size + size//2, size + size//2, fill="", outline=get_color(self.color), width=1)
        self.pulse_phase = 0
        self._pulse()
        
    def _pulse(self):
        self.pulse_phase += 0.1
        scale = (math.sin(self.pulse_phase) + 1) / 2
        glow_size = self.size//2 + scale * self.size
        c_x, c_y = self.size, self.size
        self.canvas.coords(self.glow, c_x - glow_size/2, c_y - glow_size/2, c_x + glow_size/2, c_y + glow_size/2)
        self.after(50, self._pulse)

class AnimatedProgressBar(BaseComponent):
    """A progress bar with smooth interpolation."""
    def __init__(self, master, color=COLOR_PRIMARY, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.progress = ctk.CTkProgressBar(self, progress_color=color)
        self.progress.pack(fill="x", expand=True)
        self.progress.set(0)
        self.target_value = 0
        self.current_value = 0
        
    def set_target(self, value):
        self.target_value = value
        self._animate()
        
    def _animate(self):
        diff = self.target_value - self.current_value
        if abs(diff) > 0.01:
            self.current_value += diff * 0.08
            self.progress.set(self.current_value)
            self.after(30, self._animate)
        else:
            self.current_value = self.target_value
            self.progress.set(self.current_value)

class CountUpLabel(ctk.CTkLabel):
    def __init__(self, master, format_str="{}", suffix="", **kwargs):
        super().__init__(master, text=format_str.format(0) + suffix, **kwargs)
        self.target = 0
        self.current = 0
        self.format_str = format_str
        self.suffix = suffix
        self.is_float = False
        
    def set_target(self, target, duration=1000):
        try:
            if isinstance(target, str):
                target = float(target) if "." in target else int(target)
        except ValueError:
            self.configure(text=str(target) + self.suffix)
            return

        self.target = target
        self.is_float = isinstance(target, float)
        self.current = 0
        steps = 30
        self.step_val = self.target / steps
        self._animate(steps)
        
    def _animate(self, steps_left):
        try:
            if not self.winfo_exists(): return
            if steps_left > 0:
                self.current += self.step_val
                val = round(self.current, 1) if self.is_float else int(self.current)
                self.configure(text=self.format_str.format(val) + self.suffix)
                self.after(40, lambda: self._animate(steps_left - 1))
            else:
                self.configure(text=self.format_str.format(self.target) + self.suffix)
        except Exception: pass

class AnimatedCircularProgress(ctk.CTkFrame):
    def __init__(self, master, size=120, border_color=COLOR_BORDER, progress_color=COLOR_PRIMARY, **kwargs):
        super().__init__(master, fg_color="transparent", width=size, height=size, **kwargs)
        self.size = size
        self.canvas = tk.Canvas(self, width=size, height=size, bg=get_color(COLOR_BG_CARD), highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.border_color = border_color
        self.progress_color = progress_color
        self.arc = None
        self.text_id = None
        self.target_extent = 0
        self.current_extent = 0
        self.canvas.create_oval(10, 10, size-10, size-10, outline=get_color(border_color), width=8)
        
    def set_target(self, percentage):
        self.target_extent = int(-360 * percentage)
        if not self.arc:
            self.arc = self.canvas.create_arc(10, 10, self.size-10, self.size-10, start=90, extent=0, outline=get_color(self.progress_color), width=8, style="arc")
            self.text_id = self.canvas.create_text(self.size/2, self.size/2, text="0%", fill=get_color(COLOR_TEXT_MAIN), font=(FONT_MAIN, 24, "bold"))
        self._animate()

    def _animate(self):
        try:
            if not self.winfo_exists(): return
            if abs(self.target_extent - self.current_extent) > 2:
                self.current_extent += (self.target_extent - self.current_extent) * 0.08
                self.canvas.itemconfig(self.arc, extent=self.current_extent)
                pct = int(abs(self.current_extent) / 360 * 100)
                self.canvas.itemconfig(self.text_id, text=f"{pct}%")
                self.after(30, self._animate)
            else:
                self.canvas.itemconfig(self.arc, extent=self.target_extent)
                pct = int(abs(self.target_extent) / 360 * 100)
                self.canvas.itemconfig(self.text_id, text=f"{pct}%")
        except Exception: pass

class SkeletonLoader(ctk.CTkFrame):
    def __init__(self, master, width=100, height=20, corner_radius=6, **kwargs):
        super().__init__(master, width=width, height=height, corner_radius=corner_radius, **kwargs)
        self.pack_propagate(False)
        self.phase = 0
        self._shimmer()

    def _shimmer(self):
        try:
            if not self.winfo_exists(): return
            self.phase += 0.2
            r = math.sin(self.phase)
            # Alternate between BORDER and BG_APP to simulate shimmer
            self.configure(fg_color=COLOR_BORDER if r > 0 else COLOR_BG_APP)
            self.after(250, self._shimmer)
        except Exception: pass

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("400x300")
    app.configure(fg_color=COLOR_BG_APP)
    card = GlassCard(app, width=300, height=200)
    card.pack(pady=20, padx=20, expand=True, fill="both")
    app.mainloop()
