import sys
from PyQt6.QtWidgets import QApplication

# --- DESIGN SYSTEM ---
FONT_MAIN = "Segoe UI Variable Display" if sys.platform == "win32" else "SF Pro Display"
if sys.platform == "linux":
    FONT_MAIN = "Ubuntu"

# Ultra-Modern Neumorphic Theme
COLOR_BG_APP = "#F8FAFC"        # New Base App Background
COLOR_BG_CARD = "#FFFFFF"       # Cards/Panels
COLOR_PRIMARY = "#2563EB"       # Modern Premium Royal Blue
COLOR_PRIMARY_LIGHT = "#3B82F6" # Hover Blue
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

# --- BACKEND SERVER URL ---
SERVER_URL = "http://100.80.253.23:8000"


def apply_theme(widget):
    """Applies the current global theme (light/dark) to a specific widget and all its children."""
    from PyQt6.QtWidgets import QWidget, QApplication
    
    # Force Light Mode always (remove dark mode support)
    is_dark = False
    
    # 1. Apply to the parent widget
    _apply_theme_to_single_widget(widget, is_dark)
    
    # 2. Apply to all descendants (findChildren is recursive by default, so we only iterate once)
    for child in widget.findChildren(QWidget):
        try:
            _apply_theme_to_single_widget(child, is_dark)
        except Exception:
            pass


def _apply_theme_to_single_widget(widget, is_dark):
    import re
    # Save original CSS once
    if not hasattr(widget, '_original_css'):
        widget._original_css = widget.styleSheet() or ""
        
    css = widget._original_css
    if css:
        if is_dark:
            # 1. Map Background Colors (only when matching background or background-color properties)
            css = re.sub(r'(background(-color)?:\s*)#F8FAFC', r'\1#0B1120', css, flags=re.I)
            css = re.sub(r'(background(-color)?:\s*)(#FFFFFF|white)', r'\1#1E293B', css, flags=re.I)
            css = re.sub(r'(background(-color)?:\s*)#F1F5F9', r'\1#0F172A', css, flags=re.I)
            
            # 2. Map Text Colors (only when matching color property)
            css = re.sub(r'(color:\s*)#0F172A', r'\1#F8FAFC', css, flags=re.I)
            css = re.sub(r'(color:\s*)#64748B', r'\1#94A3B8', css, flags=re.I)
            css = re.sub(r'(color:\s*)#475569', r'\1#CBD5E1', css, flags=re.I)
            css = re.sub(r'(color:\s*)#334155', r'\1#E2E8F0', css, flags=re.I)
            
            # 3. Map Border Colors (only when matching border or border-color properties)
            css = re.sub(r'(border(-color)?:\s*[^;]*?)#E2E8F0', r'\1#334155', css, flags=re.I)
            css = re.sub(r'(border(-color)?:\s*[^;]*?)#F1F5F9', r'\1#1E293B', css, flags=re.I)
            
            # 4. Brighten primary accent color in dark mode for better readability
            css = re.sub(r'#2563EB', '#3B82F6', css, flags=re.I)
            
        if css != widget.styleSheet():
            widget.setStyleSheet(css)
            if hasattr(widget, 'style'):
                widget.style().unpolish(widget)
                widget.style().polish(widget)
            widget.update()


