from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QLineEdit, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class FilterSection(QWidget):
    def __init__(self, title, options, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(10)
        
        header = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A;")
        
        toggle = QLabel("▾")
        toggle.setStyleSheet("color: #94A3B8; font-weight: bold;")
        
        header.addWidget(t_lbl)
        header.addStretch()
        header.addWidget(toggle)
        layout.addLayout(header)
        
        for opt in options:
            cb = QCheckBox(opt)
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 13px; color: #64748B; spacing: 10px; font-weight: 500;
                }
                QCheckBox::indicator {
                    width: 20px; height: 20px; border-radius: 6px; border: 2px solid #E2E8F0;
                    background-color: white;
                }
                QCheckBox::indicator:hover { border-color: #38BDF8; }
                QCheckBox::indicator:checked {
                    background-color: #38BDF8; border-color: #38BDF8;
                    image: url(check.png); /* Fallback to color if no image */
                }
            """)
            layout.addWidget(cb)

class JobSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 32, 24, 24)
        layout.setSpacing(32)
        
        # Header
        header_v = QVBoxLayout()
        header_v.setSpacing(8)
        
        title = QLabel("Career Discovery")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A;")
        
        subtitle = QLabel("Find your next AI milestone")
        subtitle.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B;")
        
        header_v.addWidget(title)
        header_v.addWidget(subtitle)
        layout.addLayout(header_v)
        
        # Search Box
        search_container = QFrame()
        search_container.setStyleSheet("""
            background-color: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 14px;
        """)
        sl = QHBoxLayout(search_container)
        sl.setContentsMargins(14, 0, 14, 0)
        
        icon = QLabel("🔍")
        icon.setStyleSheet("border: none; background: transparent; font-size: 14px;")
        
        search = QLineEdit()
        search.setPlaceholderText("Search roles, tech...")
        search.setStyleSheet("""
            QLineEdit {
                border: none; background: transparent; padding: 12px 4px;
                font-size: 13px; font-weight: 500; color: #1E293B;
            }
        """)
        sl.addWidget(icon)
        sl.addWidget(search)
        layout.addWidget(search_container)
        
        # Filters Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(12)
        
        cl.addWidget(FilterSection("Work Arrangement", ["Remote", "Hybrid", "On-site", "Global"]))
        cl.addWidget(FilterSection("Employment Type", ["Full-time", "Internship", "Contract", "Freelance"]))
        cl.addWidget(FilterSection("Experience Level", ["Entry-level", "Junior", "Mid-level", "Senior", "Principal"]))
        cl.addWidget(FilterSection("Salary Range", ["$50k - $100k", "$100k - $150k", "$150k - $200k", "$200k+"]))
        cl.addWidget(FilterSection("Industry", ["Generative AI", "Fintech", "HealthTech", "E-commerce", "SaaS"]))
        
        cl.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Quick Navigation
        self.nav_frame = QFrame()
        self.nav_frame.setStyleSheet("border-top: 1px solid #E2E8F0; padding-top: 16px;")
        nav_v = QVBoxLayout(self.nav_frame)
        nav_v.setContentsMargins(0, 16, 0, 0)
        nav_v.setSpacing(10)
        
        for text, icon in [("Saved Opportunities", "🔖"), ("Application History", "📄"), ("Job Alerts", "🔔")]:
            btn = QPushButton(f" {icon}  {text}")
            btn.setFixedHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left; background-color: transparent; border: none;
                    font-size: 13px; font-weight: 600; color: #475569; padding-left: 8px;
                }
                QPushButton:hover { color: #0284C7; background-color: #F0F9FF; border-radius: 10px; }
            """)
            nav_v.addWidget(btn)
            
        layout.addWidget(self.nav_frame)
