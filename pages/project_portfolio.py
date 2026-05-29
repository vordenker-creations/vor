from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernCard")
        self.setStyleSheet("""
            #ModernCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(15, 23, 42, 10))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)

class ProjectPortfolioPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(16)
        
        title_lbl = QLabel("💼 Project Portfolio")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        
        btn_add = QPushButton("+ Add New Project")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; font-weight: 700; font-size: 13px;
                border-radius: 18px; padding: 0 20px; height: 36px; border: none;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        header_layout.addWidget(btn_add)
        
        main_layout.addWidget(header)
        
        # Content Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        projects = [
            ("AI Career Planner", "Python, PyQt6, Ollama AI", "A desktop application helping students build study roadmaps via generative AI.", "85%"),
            ("E-Commerce Web API", "Go, PostgreSQL, Redis", "High-performance backend API with JWT auth and caching layer.", "100%"),
            ("Stock Tracker App", "React Native, Node.js", "Mobile application tracking real-time crypto and stock assets.", "40%")
        ]
        
        row, col = 0, 0
        for title, tech, desc, prog in projects:
            card = ModernCard()
            card.internal_layout.setSpacing(12)
            
            c_header = QHBoxLayout()
            c_t = QLabel(title)
            c_t.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 800;")
            c_header.addWidget(c_t)
            c_header.addStretch()
            
            opts = QPushButton("⋮")
            opts.setFixedSize(24, 24)
            opts.setStyleSheet("color: #64748B; font-weight: 800; border: none; background: transparent; font-size: 16px;")
            opts.setCursor(Qt.CursorShape.PointingHandCursor)
            c_header.addWidget(opts)
            
            card.internal_layout.addLayout(c_header)
            
            c_tech = QLabel(f"🛠 {tech}")
            c_tech.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: 600;")
            card.internal_layout.addWidget(c_tech)
            
            c_desc = QLabel(desc)
            c_desc.setStyleSheet("color: #475569; font-size: 13px; line-height: 1.4;")
            c_desc.setWordWrap(True)
            card.internal_layout.addWidget(c_desc)
            card.internal_layout.addStretch()
            
            c_foot = QHBoxLayout()
            c_foot.addWidget(QLabel("Completion:", styleSheet="color: #94A3B8; font-size: 11px;"))
            
            from PyQt6.QtWidgets import QProgressBar
            bar = QProgressBar()
            bar.setFixedHeight(6)
            bar.setRange(0, 100)
            bar.setValue(int(prog.strip('%')))
            bar.setTextVisible(False)
            color = "#10B981" if prog == "100%" else "#38BDF8"
            bar.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border-radius: 3px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}")
            
            c_foot.addWidget(bar)
            c_foot.addWidget(QLabel(prog, styleSheet="color: #0F172A; font-size: 11px; font-weight: 600;"))
            
            card.internal_layout.addLayout(c_foot)
            
            grid.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        content_layout.addLayout(grid)
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
