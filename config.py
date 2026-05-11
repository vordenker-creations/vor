import sys
from PyQt6.QtWidgets import QApplication

# --- DESIGN SYSTEM ---
FONT_MAIN = "Segoe UI"

# Theme Colors (Using Dark Theme as default for the new UI)
COLOR_BG_APP = "#0B192C"
COLOR_BG_CARD = "#1E2A38"
COLOR_PRIMARY = "#00D1FF"
COLOR_PRIMARY_LIGHT = "#003333"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#94A3B8"
COLOR_BORDER = "#1E2D3D"

COLOR_SUCCESS = "#10B981"      
COLOR_WARNING = "#F59E0B"      
COLOR_DANGER = "#DC2626"

def get_global_stylesheet():
    """Returns the master CSS for the PyQt6 application."""
    return f"""
    QMainWindow, QWidget#MainContainer {{
        background-color: {COLOR_BG_APP};
        color: {COLOR_TEXT_MAIN};
        font-family: "{FONT_MAIN}";
    }}
    
    /* Typography */
    QLabel {{
        color: {COLOR_TEXT_MAIN};
        font-family: "{FONT_MAIN}";
    }}
    QLabel.SubText {{
        color: {COLOR_TEXT_SUB};
    }}
    QLabel.Header {{
        font-size: 24px;
        font-weight: bold;
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {COLOR_PRIMARY};
        color: #000000;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: #00B4D8;
    }}
    QPushButton.NavButton {{
        background-color: transparent;
        color: {COLOR_TEXT_SUB};
        font-size: 20px;
        border-radius: 12px;
    }}
    QPushButton.NavButton:hover {{
        background-color: {COLOR_BG_CARD};
    }}
    QPushButton.NavButton:checked {{
        background-color: {COLOR_PRIMARY_LIGHT};
        color: {COLOR_PRIMARY};
        border-left: 3px solid {COLOR_PRIMARY};
        border-radius: 0px;
    }}
    
    /* Inputs */
    QLineEdit {{
        background-color: {COLOR_BG_APP};
        border: 1px solid {COLOR_BORDER};
        border-radius: 8px;
        padding: 8px 12px;
        color: {COLOR_TEXT_MAIN};
    }}
    QLineEdit:focus {{
        border: 1px solid {COLOR_PRIMARY};
    }}
    
    /* Progress Bars */
    QProgressBar {{
        border: none;
        background-color: {COLOR_BORDER};
        border-radius: 4px;
        height: 8px;
        text-align: center;
        color: transparent;
    }}
    QProgressBar::chunk {{
        background-color: {COLOR_PRIMARY};
        border-radius: 4px;
    }}
    """
