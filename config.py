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
        width: 6px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: #BAE6FD;
        min-height: 30px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #38BDF8;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """
