import customtkinter as ctk
from config import *

class SaaSCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Lấy giá trị từ kwargs nếu được truyền vào, nếu không thì dùng mặc định
        fg_color = kwargs.pop("fg_color", COLOR_BG_CARD)
        corner_radius = kwargs.pop("corner_radius", 8)
        border_width = kwargs.pop("border_width", 1)
        border_color = kwargs.pop("border_color", COLOR_BORDER)
        
        super().__init__(
            master, 
            fg_color=fg_color, 
            corner_radius=corner_radius, 
            border_width=border_width, 
            border_color=border_color, 
            **kwargs
        )