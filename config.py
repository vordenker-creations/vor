import customtkinter as ctk

def get_color(color_tuple):
    """Helper to resolve color tuples for standard tkinter widgets."""
    if isinstance(color_tuple, tuple):
        return color_tuple[1] if ctk.get_appearance_mode() == "Dark" else color_tuple[0]
    return color_tuple

FONT_MAIN = "Segoe UI" 

# Appearance Settings
APPEARANCE_MODE = "dark"  # "light" or "dark"

# Theme Colors (Light, Dark)
COLOR_BG_APP = ("#F1F5F9", "#09101A")       # Deep teal/slate background
COLOR_BG_CARD = ("#FFFFFF", "#111A24")      # Slightly lighter card background
COLOR_PRIMARY = ("#00B4D8", "#00E5FF")      # Bright cyan active color
COLOR_PRIMARY_LIGHT = ("#E0F2FE", "#003333") # Dark teal background for active items
COLOR_TEXT_MAIN = ("#1E293B", "#FFFFFF")    
COLOR_TEXT_SUB = ("#64748B", "#94A3B8")     
COLOR_BORDER = ("#E2E8F0", "#1E2D3D")       # Slate border
COLOR_SUCCESS = ("#10B981", "#10B981")      
COLOR_WARNING = ("#F59E0B", "#F59E0B")      
COLOR_ACCENT = ("#8B5CF6", "#8B5CF6")
