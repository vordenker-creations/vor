import sys
from PyQt6.QtWidgets import QApplication

# --- DESIGN SYSTEM ---
FONT_MAIN = "Segoe UI Variable Display" if sys.platform == "win32" else "SF Pro Display"
if sys.platform == "linux":
    FONT_MAIN = "Ubuntu"

# Ultra-Modern Neumorphic Theme
COLOR_BG_APP = "#F8FAFC"        # New Base App Background
COLOR_BG_CARD = "#FFFFFF"       # Cards/Panels
COLOR_PRIMARY = "#38BDF8"       # Brand Cyan
COLOR_PRIMARY_LIGHT = "#7DD3FC" # Hover cyan
COLOR_TEXT_MAIN = "#0F172A"     # Slate 900
COLOR_TEXT_SUB = "#64748B"      # Slate 500
COLOR_BORDER = "#E2E8F0"        # Light gray border

COLOR_SUCCESS = "#10B981"       # Emerald 500
COLOR_WARNING = "#F59E0B"      
COLOR_DANGER = "#EF4444"

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
    QLabel.Header {{ font-size: 26px; font-weight: 800; color: {COLOR_TEXT_MAIN}; letter-spacing: -0.5px; }}
    
    QPushButton {{ 
        background-color: {COLOR_PRIMARY}; 
        color: #ffffff; 
        border-radius: 10px; 
        font-weight: 600; 
        padding: 10px 18px; 
        font-family: "{FONT_MAIN}", "Segoe UI", sans-serif; 
        border: none;
    }}
    QPushButton:hover {{ 
        background-color: {COLOR_PRIMARY_LIGHT}; 
    }}
    QPushButton:pressed {{ 
        background-color: #0284C7; 
    }}
    
    QPushButton.Secondary {{
        background-color: #ffffff;
        color: {COLOR_TEXT_MAIN};
        border: 1px solid {COLOR_BORDER};
    }}
    QPushButton.Secondary:hover {{
        background-color: #F1F5F9;
    }}
    
    QLineEdit, QTextEdit, QComboBox {{ 
        background-color: #ffffff; 
        border: 1px solid {COLOR_BORDER}; 
        border-radius: 10px; 
        padding: 10px 16px; 
        color: {COLOR_TEXT_MAIN}; 
        font-family: "{FONT_MAIN}", "Segoe UI", sans-serif; 
        font-size: 14px;
    }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ 
        border: 1px solid {COLOR_PRIMARY}; 
        outline: none; 
        background-color: #FFFFFF;
    }}
    
    QProgressBar {{ 
        border: none; 
        background-color: #F1F5F9; 
        border-radius: 4px; 
        height: 6px; 
        text-align: center; 
        color: transparent; 
    }}
    QProgressBar::chunk {{ 
        background-color: {COLOR_PRIMARY}; 
        border-radius: 4px; 
    }}
    
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: #CBD5E1;
        min-height: 30px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #94A3B8;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    
    QScrollBar:horizontal {{
        background: transparent;
        height: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background: #CBD5E1;
        min-width: 30px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: #94A3B8;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
    """
