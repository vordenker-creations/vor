import sys
from PyQt6.QtWidgets import QWidget, QFrame, QGraphicsDropShadowEffect, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from neumorphic_components import NeumorphicFrame, NeumorphicInput, NeumorphicButton, GlowingButton

GLOBAL_BG = "#F0F2F5"

def apply_neumorphic_outer_shadow(widget, radius=25, offset=8, blur=20):
    """
    Wraps a widget in the new optimized NeumorphicFrame.
    """
    container = NeumorphicFrame(radius=radius, offset=offset, blur=blur)
    container.content_layout.setContentsMargins(10, 10, 10, 10)
    
    # Strip background from wrapped widget
    widget.setStyleSheet(widget.styleSheet() + "; background: transparent; border: none;")
    container.add_widget(widget)
    return container

def apply_neumorphic_inset_shadow(widget, radius=25):
    """
    Applies the new inset shadow style.
    """
    widget.setStyleSheet(f"background-color: {GLOBAL_BG}; border-radius: {radius}px; border-top: 2px solid #d1d5db; border-left: 2px solid #d1d5db; border-bottom: 2px solid #ffffff; border-right: 2px solid #ffffff;")
    return widget

def create_neumorphic_input(placeholder, icon_text="", is_password=False):
    """
    Returns the new NeumorphicInput component.
    """
    return NeumorphicInput(placeholder, icon_text, is_password)

def create_glowing_button(text, width=None, height=50):
    """
    Returns the new GlowingButton component.
    """
    container = GlowingButton(text, width, height)
    wrapper = QWidget()
    l = QVBoxLayout(wrapper)
    l.setContentsMargins(0,0,0,0)
    l.addWidget(container)
    wrapper.btn = container
    return wrapper
