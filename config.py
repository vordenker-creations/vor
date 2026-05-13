import sys
from PyQt6.QtWidgets import QApplication

# --- DESIGN SYSTEM ---
FONT_MAIN = "Segoe UI Variable Display" if sys.platform == "win32" else "SF Pro Display"
if sys.platform == "linux":
    FONT_MAIN = "Ubuntu"

# Ultra-Modern Neumorphic Theme
COLOR_BG_APP = "#F0F2F5"        # Standard Neumorphic Background
COLOR_BG_CARD = "#F0F2F5"       # Match background for neumorphism
COLOR_PRIMARY = "#1E5F74"       # Brand Blue-Teal
COLOR_PRIMARY_LIGHT = "#25758f" # Hover teal
COLOR_TEXT_MAIN = "#1e293b"     # Slate 800
COLOR_TEXT_SUB = "#64748b"      # Slate 500
COLOR_BORDER = "#d1d5db"        # Light gray border

COLOR_SUCCESS = "#0070F3"       # Vercel Blue (repurposed for success/accents)
COLOR_WARNING = "#F5A623"      
COLOR_DANGER = "#EE0000"

def get_global_stylesheet():
    """Returns the master CSS for the PyQt6 application."""
    return f"""
    QMainWindow, QWidget#MainContainer {{
        background-color: {COLOR_BG_APP};
        color: {COLOR_TEXT_MAIN};
        font-family: "{FONT_MAIN}", "Segoe UI", sans-serif;
    }}
    QLabel {{ color: {COLOR_TEXT_MAIN}; font-family: "{FONT_MAIN}", "Segoe UI", sans-serif; }}
    QLabel.SubText {{ color: {COLOR_TEXT_SUB}; }}
    QLabel.Header {{ font-size: 24px; font-weight: 800; color: {COLOR_TEXT_MAIN}; letter-spacing: -0.5px; }}
    
    QPushButton {{ 
        background-color: {COLOR_PRIMARY}; 
        color: #ffffff; 
        border-radius: 8px; 
        font-weight: 600; 
        padding: 10px 16px; 
        font-family: "{FONT_MAIN}", "Segoe UI", sans-serif; 
        border: 1px solid {COLOR_PRIMARY};
    }}
    QPushButton:hover {{ background-color: {COLOR_PRIMARY_LIGHT}; border: 1px solid {COLOR_PRIMARY_LIGHT}; }}
    QPushButton:pressed {{ background-color: #000000; }}
    
    QPushButton.Secondary {{
        background-color: #ffffff;
        color: {COLOR_TEXT_MAIN};
        border: 1px solid {COLOR_BORDER};
    }}
    QPushButton.Secondary:hover {{
        background-color: #f5f5f5;
    }}
    
    QLineEdit, QTextEdit, QComboBox {{ 
        background-color: #ffffff; 
        border: 1px solid {COLOR_BORDER}; 
        border-radius: 8px; 
        padding: 10px 14px; 
        color: {COLOR_TEXT_MAIN}; 
        font-family: "{FONT_MAIN}", "Segoe UI", sans-serif; 
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ border: 1px solid #999999; outline: none; }}
    
    QProgressBar {{ 
        border: none; 
        background-color: #F3F3F3; 
        border-radius: 4px; 
        height: 8px; 
        text-align: center; 
        color: transparent; 
    }}
    QProgressBar::chunk {{ background-color: {COLOR_SUCCESS}; border-radius: 4px; }}
    
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: #D4D4D4;
        min-height: 30px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #A3A3A3;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """
