from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class SectionItem(QFrame):
    clicked = pyqtSignal(str)
    
    def __init__(self, title, icon, status="incomplete", is_active=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.title = title
        
        self.update_style(is_active)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(12)
        
        # Icon
        self.icon_lbl = QLabel(icon)
        self.icon_lbl.setStyleSheet("font-size: 16px; border: none; background: transparent;")
        layout.addWidget(self.icon_lbl)
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(f"font-size: 13px; font-weight: {'600' if is_active else '500'}; color: {'#0284C7' if is_active else '#1E293B'}; border: none; background: transparent;")
        layout.addWidget(self.title_lbl)
        
        layout.addStretch()
        
        # Status
        status_color = "#10B981" if status == "complete" else "#CBD5E1"
        self.status_dot = QWidget()
        self.status_dot.setFixedSize(8, 8)
        self.status_dot.setStyleSheet(f"background-color: {status_color}; border-radius: 4px; border: none;")
        layout.addWidget(self.status_dot)
        
    def update_style(self, is_active):
        if is_active:
            self.setStyleSheet("""
                SectionItem {
                    background-color: #F0F9FF;
                    border-radius: 12px;
                    border-left: 4px solid #38BDF8;
                }
            """)
        else:
            self.setStyleSheet("""
                SectionItem {
                    background-color: transparent;
                    border-radius: 12px;
                    border: none;
                }
                SectionItem:hover {
                    background-color: #F1F5F9;
                }
            """)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title)
        super().mousePressEvent(event)

class ResumeSidebar(QFrame):
    section_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(20)
        
        # Top Header
        header = QVBoxLayout()
        header.setSpacing(12)
        title = QLabel("Resume Builder")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
        header.addWidget(title)
        
        btn_new = QPushButton("+ Create Resume")
        btn_new.setFixedHeight(44)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 12px;
                font-size: 13px; font-weight: 700; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        header.addWidget(btn_new)
        layout.addLayout(header)
        
        # Search
        search = QFrame()
        search.setFixedHeight(40)
        search.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;")
        sl = QHBoxLayout(search)
        sl.setContentsMargins(12, 0, 12, 0)
        ico = QLabel("🔍")
        ico.setStyleSheet("font-size: 12px; border: none;")
        sl.addWidget(ico)
        lbl = QLabel("Search sections...")
        lbl.setStyleSheet("color: #94A3B8; font-size: 12px; border: none;")
        sl.addWidget(lbl)
        sl.addStretch()
        layout.addWidget(search)
        
        # Section List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(4)
        
        self.sections = [
            ("Personal Info", "👤", "complete"),
            ("Summary", "📝", "complete"),
            ("Education", "🎓", "complete"),
            ("Experience", "💼", "complete"),
            ("Skills", "⚡", "complete"),
            ("Projects", "🚀", "incomplete"),
            ("Certifications", "📜", "incomplete"),
            ("Languages", "🌐", "incomplete"),
            ("References", "👥", "incomplete")
        ]
        
        self.items = []
        for i, (name, icon, status) in enumerate(self.sections):
            item = SectionItem(name, icon, status, is_active=(i==0))
            item.clicked.connect(self._handle_click)
            self.list_layout.addWidget(item)
            self.items.append(item)
            
        self.list_layout.addStretch()
        scroll.setWidget(self.list_widget)
        layout.addWidget(scroll)
        
        # Bottom Stats
        bottom = QFrame()
        bottom.setStyleSheet("border-top: 1px solid #E2E8F0; padding-top: 16px;")
        bl = QVBoxLayout(bottom)
        bl.setContentsMargins(0, 16, 0, 0)
        bl.setSpacing(12)
        
        # Completion Card
        comp_card = QFrame()
        comp_card.setStyleSheet("background-color: #F8FAFC; border-radius: 16px; padding: 12px; border: 1px solid #E2E8F0;")
        cl = QVBoxLayout(comp_card)
        cl.setSpacing(8)
        
        clt = QHBoxLayout()
        clt_lbl = QLabel("Completion")
        clt_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #64748B; border: none;")
        clt_val = QLabel("65%")
        clt_val.setStyleSheet("font-size: 11px; font-weight: 800; color: #10B981; border: none;")
        clt.addWidget(clt_lbl); clt.addStretch(); clt.addWidget(clt_val)
        cl.addLayout(clt)
        
        bar = QFrame()
        bar.setFixedHeight(6)
        bar.setStyleSheet("background-color: #E2E8F0; border-radius: 3px; border: none;")
        bar_fg = QFrame(bar)
        bar_fg.setFixedHeight(6)
        bar_fg.setFixedWidth(140) # 65% of ~216px
        bar_fg.setStyleSheet("background-color: #10B981; border-radius: 3px; border: none;")
        cl.addWidget(bar)
        bl.addWidget(comp_card)
        
        # ATS Mini Card
        ats_card = QFrame()
        ats_card.setStyleSheet("background-color: #0F172A; border-radius: 16px; padding: 12px;")
        al = QHBoxLayout(ats_card)
        al.setSpacing(12)
        
        ats_score = QLabel("82")
        ats_score.setFixedSize(36, 36)
        ats_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ats_score.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: 800; border: 2px solid #38BDF8; border-radius: 18px;")
        
        ats_info = QVBoxLayout()
        ats_info.setSpacing(0)
        ats_lbl = QLabel("ATS Score")
        ats_lbl.setStyleSheet("color: white; font-size: 12px; font-weight: 700;")
        ats_status = QLabel("Good match")
        ats_status.setStyleSheet("color: #94A3B8; font-size: 10px;")
        ats_info.addWidget(ats_lbl)
        ats_info.addWidget(ats_status)
        
        al.addWidget(ats_score)
        al.addLayout(ats_info)
        al.addStretch()
        bl.addWidget(ats_card)
        
        layout.addWidget(bottom)

    def _handle_click(self, title):
        for item in self.items:
            item.update_style(item.title == title)
        self.section_selected.emit(title)
