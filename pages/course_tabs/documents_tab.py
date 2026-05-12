from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, ChipButton

class DocumentsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        main_card = SaaSCard()
        main_layout = main_card.internal_layout
        
        # Header Controls
        header_layout = QHBoxLayout()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Trình tết cỏ sren document")
        search_input.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 4px; padding: 5px; color: {COLOR_TEXT_MAIN}")
        search_input.setFixedWidth(250)
        header_layout.addWidget(search_input)
        
        cb1 = QComboBox()
        cb1.addItem("Tài liệu")
        cb1.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}")
        header_layout.addWidget(cb1)
        
        cb2 = QComboBox()
        cb2.addItem("Cài liệu 2:")
        cb2.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}")
        header_layout.addWidget(cb2)
        
        cb3 = QComboBox()
        cb3.addItem("Cài Liên 3:")
        cb3.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}")
        header_layout.addWidget(cb3)
        
        header_layout.addStretch()
        
        btn_layout = QVBoxLayout()
        btn1 = QPushButton("📥 Tải xuống tất cả")
        btn1.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}; padding: 4px;")
        btn2 = QPushButton("📥 Tải xuống tất cả")
        btn2.setStyleSheet(f"background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}; padding: 4px;")
        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)
        header_layout.addLayout(btn_layout)
        
        main_layout.addLayout(header_layout)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {COLOR_BORDER};")
        main_layout.addWidget(sep)
        
        # Columns
        cols_layout = QHBoxLayout()
        
        # Column 1
        col1_layout = QVBoxLayout()
        col1_label = QLabel("Cài liên 1:")
        col1_label.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-weight: bold;")
        col1_layout.addWidget(col1_label)
        
        col1_items = [
            "Bài 1: Tổng quan", "Slide 3: Tkinter Overview", "Slide 3: Tkinter Handling ...",
            "Slide 4: Tkinter Handling ...", "Slide 5: Tkinter Widgets", "Slide 6: Tkinter Computer...",
            "Slide 7: Tkinter Overview", "Slide 8: Tkinter Display", "Slide 8: Tkinter Function...",
            "Slide 10: Tkinter Breonm..."
        ]
        for item in col1_items:
            lbl = QLabel(f"📄 {item}")
            lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN};")
            col1_layout.addWidget(lbl)
        col1_layout.addStretch()
        cols_layout.addLayout(col1_layout)
        
        # Column 2
        col2_layout = QVBoxLayout()
        col2_label = QLabel("Cài liên 2:")
        col2_label.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-weight: bold;")
        col2_layout.addWidget(col2_label)
        
        col2_items = [
            "example_custom_widget_final.py", "example_custom_widget_finalao.py",
            "example_custom_widget.py", "example_custom_widget.py", "example_custom_widget.py",
            "example_custom_widget.py", "example_stant_widget.py", "example_custom_widget.py",
            "example_stant_widget.py", "example_custom_widget.py", "example_event_widget.py"
        ]
        for item in col2_items:
            lbl = QLabel(f"📄 {item}")
            lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN};")
            col2_layout.addWidget(lbl)
        col2_layout.addStretch()
        cols_layout.addLayout(col2_layout)
        
        # Column 3
        col3_layout = QVBoxLayout()
        col3_label = QLabel("Cài kiên 3:")
        col3_label.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-weight: bold;")
        col3_layout.addWidget(col3_label)
        
        col3_items = [
            "E-book: https://A-boolc-fue-...",
            "E-book: https://A-boolc-fue-...",
            "E-book: https://A-boolc-fue-..."
        ]
        for item in col3_items:
            lbl = QLabel(f"📘 <a href='#' style='color: {COLOR_PRIMARY};'>{item}</a>")
            lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN};")
            lbl.setOpenExternalLinks(True)
            col3_layout.addWidget(lbl)
        col3_layout.addStretch()
        cols_layout.addLayout(col3_layout)
        
        main_layout.addLayout(cols_layout)
        
        layout.addWidget(main_card)
