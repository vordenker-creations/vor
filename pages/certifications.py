import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QGraphicsDropShadowEffect, QSizePolicy, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

class CategoryItem(QPushButton):
    def __init__(self, text, count=0, is_active=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        bg = "#E0F2FE" if is_active else "transparent"
        color = "#0284C7" if is_active else "#64748B"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border-radius: 10px;
                padding-left: 15px;
                text-align: left;
                font-weight: {'700' if is_active else '500'};
                border: none;
            }}
            QPushButton:hover {{ background-color: #F1F5F9; }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        self.setText(text)
        
        if count > 0:
            badge = QLabel(str(count))
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedSize(20, 20)
            badge_bg = "#38BDF8" if is_active else "#E2E8F0"
            badge_fg = "white" if is_active else "#64748B"
            badge.setStyleSheet(f"background-color: {badge_bg}; color: {badge_fg}; border-radius: 10px; font-size: 10px; font-weight: 700; border: none;")
            layout.addStretch()
            layout.addWidget(badge)

class CertCard(QFrame):
    def __init__(self, title, provider, date, logo_text, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 280)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 22px;
            }
            QFrame:hover {
                border: 1px solid #38BDF8;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(12)
        
        # Logo Area
        logo = QFrame()
        logo.setFixedSize(60, 60)
        logo.setStyleSheet("background-color: #F1F5F9; border-radius: 12px; border: none;")
        ll = QVBoxLayout(logo)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lt = QLabel(logo_text)
        lt.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        ll.addWidget(lt)
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Text
        t_lbl = QLabel(title)
        t_lbl.setWordWrap(True)
        t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 15px; border: none; background: transparent;")
        layout.addWidget(t_lbl)
        
        p_lbl = QLabel(provider)
        p_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_lbl.setStyleSheet("color: #64748B; font-size: 13px; border: none; background: transparent;")
        layout.addWidget(p_lbl)
        
        layout.addStretch()
        
        d_lbl = QLabel(f"Issued {date}")
        d_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; border: none; background: transparent;")
        layout.addWidget(d_lbl)
        
        verify_btn = QPushButton("✓ Verified")
        verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD;
                border-radius: 8px; padding: 6px; font-size: 11px; font-weight: 700;
            }
        """)
        layout.addWidget(verify_btn)

class CertificationsPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_left_sidebar()
        self._setup_main_workspace()
        self._setup_right_panel()

    def _setup_left_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(16)
        
        h_lbl = QLabel("Certifications")
        h_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        layout.addWidget(h_lbl)
        
        layout.addWidget(CategoryItem("All Tracks", 8, True))
        layout.addWidget(CategoryItem("Programming", 3))
        layout.addWidget(CategoryItem("AI & Data Science", 2))
        layout.addWidget(CategoryItem("Cloud Architecture", 2))
        layout.addWidget(CategoryItem("Cybersecurity", 1))
        
        layout.addStretch()
        
        # New Badge Card
        nb = QFrame()
        nb.setStyleSheet("background-color: #0F172A; border-radius: 16px;")
        nbl = QVBoxLayout(nb)
        nbl.setContentsMargins(16, 16, 16, 16)
        
        t1 = QLabel("Digital Badges")
        t1.setStyleSheet("color: #38BDF8; font-weight: 800; font-size: 12px;")
        nbl.addWidget(t1)
        
        t2 = QLabel("Share your verified achievements on LinkedIn with one click.")
        t2.setWordWrap(True)
        t2.setStyleSheet("color: #E2E8F0; font-size: 11px; line-height: 1.4;")
        nbl.addWidget(t2)
        
        layout.addWidget(nb)
        
        self.main_layout.addWidget(sidebar)

    def _setup_main_workspace(self):
        workspace = QWidget()
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(24, 0, 24, 0)
        
        search = QLineEdit()
        search.setPlaceholderText("Search certificates...")
        search.setFixedWidth(240)
        search.setStyleSheet("background-color: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;")
        t_layout.addWidget(search)
        
        t_layout.addStretch()
        
        for btn_text, is_primary in [("Export", False), ("Upload Certificate", True)]:
            btn = QPushButton(btn_text)
            if is_primary:
                btn.setStyleSheet("background-color: #38BDF8; color: white; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 13px; border: none;")
            else:
                btn.setStyleSheet("background-color: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 13px;")
            t_layout.addWidget(btn)
        
        layout.addWidget(toolbar)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        content = QWidget()
        form_layout = QVBoxLayout(content)
        form_layout.setContentsMargins(32, 32, 32, 32)
        form_layout.setSpacing(32)
        
        # KPI Row
        kpi_row = QHBoxLayout()
        for t, v, c in [("Total Certs", "08", "#38BDF8"), ("Skill Badges", "15", "#2DD4BF"), ("Hours Learned", "320", "#F59E0B"), ("Completion Rate", "94%", "#8B5CF6")]:
            card = QFrame()
            card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
            cl = QVBoxLayout(card)
            t_lbl = QLabel(t)
            t_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase;")
            cl.addWidget(t_lbl)
            v_lbl = QLabel(v)
            v_lbl.setStyleSheet(f"color: {c}; font-size: 20px; font-weight: 800;")
            cl.addWidget(v_lbl)
            kpi_row.addWidget(card)
        form_layout.addLayout(kpi_row)
        
        # Grid
        grid_lbl = QLabel("My Credentials")
        grid_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        form_layout.addWidget(grid_lbl)
        
        grid = QGridLayout()
        grid.setSpacing(24)
        certs = [
            ("AWS Solutions Architect", "Amazon Web Services", "Oct 2024", "☁️"),
            ("Deep Learning Specialty", "DeepLearning.AI", "Sep 2024", "🧠"),
            ("Python Expert Track", "Codecademy", "Aug 2024", "🐍"),
            ("Professional Scrum Master", "Scrum.org", "Jul 2024", "🏃"),
        ]
        for i, (t, p, d, l) in enumerate(certs):
            row, col = divmod(i, 3)
            grid.addWidget(CertCard(t, p, d, l), row, col)
        form_layout.addLayout(grid)
        
        form_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.main_layout.addWidget(workspace, stretch=1)

    def _setup_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(320)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        # AI Recommendations
        ai_card = QFrame()
        ai_card.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px;")
        al = QVBoxLayout(ai_card)
        at = QLabel("✨ AI Recommendations")
        at.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px;")
        al.addWidget(at)
        ad = QLabel("Based on your Cloud track, the 'Google Professional Data Engineer' cert would increase your job match probability by 25%.")
        ad.setWordWrap(True)
        ad.setStyleSheet("color: #64748B; font-size: 12px; line-height: 1.5;")
        al.addWidget(ad)
        layout.addWidget(ai_card)
        
        # Upcoming Deadlines
        ul = QLabel("Upcoming Milestones")
        ul.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px;")
        layout.addWidget(ul)
        
        for m, d in [("Azure Fundamentals", "Oct 28"), ("Certified AI Engineer", "Nov 15")]:
            row = QHBoxLayout()
            ml = QLabel(m)
            ml.setStyleSheet("color: #475569; font-size: 13px; font-weight: 500;")
            row.addWidget(ml)
            row.addStretch()
            dl = QLabel(d)
            dl.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: 700;")
            row.addWidget(dl)
            layout.addLayout(row)
            
        layout.addStretch()
        self.main_layout.addWidget(panel)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CertificationsPage()
    window.resize(1400, 900)
    window.show()
    sys.exit(app.exec())
