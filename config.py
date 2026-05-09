import customtkinter as ctk

def get_color(color_tuple):
    """Hỗ trợ lấy màu từ Tuple dựa trên theme hiện tại."""
    if isinstance(color_tuple, tuple):
        return color_tuple[1] if ctk.get_appearance_mode() == "Dark" else color_tuple[0]
    return color_tuple

# --- DESIGN SYSTEM ---
FONT_MAIN = "Segoe UI" 

# Appearance Settings
APPEARANCE_MODE = "dark"

# Theme Colors (Light, Dark)
COLOR_BG_APP = ("#F0F2F5", "#0B192C")       # Nền ứng dụng cao cấp
COLOR_BG_CARD = ("#FFFFFF", "#1E2A38")      # Glass Card background
COLOR_PRIMARY = ("#00D1FF", "#00D1FF")      # Electric Cyan
COLOR_PRIMARY_LIGHT = ("#E0F2FE", "#003333") 
COLOR_TEXT_MAIN = ("#1E293B", "#FFFFFF")    
COLOR_TEXT_SUB = ("#64748B", "#94A3B8")     
COLOR_BORDER = ("#E2E8F0", "#1E2D3D")       

# Accent & Interaction
COLOR_GLOW = "#00D1FF"
COLOR_SUCCESS = "#10B981"      
COLOR_WARNING = "#F59E0B"      
COLOR_DANGER = "#DC2626"
