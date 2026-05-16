import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem,
                             QHeaderView, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

class AdminCategoryItem(QPushButton):
    def __init__(self, text, count=0, is_active=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        bg = "#E0F2FE" if is_active else "transparent"
        color = "#0284C7" if is_active else "#64748B"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border-radius: 12px;
                padding-left: 20px;
                text-align: left;
                font-weight: {'700' if is_active else '500'};
                border: none;
            }}
            QPushButton:hover {{ background-color: #F1F5F9; }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 20, 0)
        self.setText(text)
        
        if count > 0:
            badge = QLabel(str(count))
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setFixedSize(24, 20)
            badge_bg = "#38BDF8" if is_active else "#E2E8F0"
            badge_fg = "white" if is_active else "#64748B"
            badge.setStyleSheet(f"background-color: {badge_bg}; color: {badge_fg}; border-radius: 10px; font-size: 10px; font-weight: 700; border: none;")
            layout.addStretch()
            layout.addWidget(badge)

class AdminPanelPage(QWidget):
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
        sidebar.setFixedWidth(320)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(24, 32, 24, 24)
        layout.setSpacing(20)
        
        h_lbl = QLabel("Admin Console")
        h_lbl.setStyleSheet("color: #0F172A; font-size: 22px; font-weight: 800;")
        layout.addWidget(h_lbl)
        
        create_btn = QPushButton("+ Create New User")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #38BDF8; color: white; border-radius: 12px;
                padding: 12px; font-weight: 700; font-size: 14px; border: none;
            }
            QPushButton:hover { background-color: #0284C7; }
        """)
        layout.addWidget(create_btn)
        
        # Categories
        layout.addWidget(AdminCategoryItem("Students", 1240, True))
        layout.addWidget(AdminCategoryItem("Mentors", 85))
        layout.addWidget(AdminCategoryItem("Reports", 12))
        layout.addWidget(AdminCategoryItem("System Health", 0))
        layout.addWidget(AdminCategoryItem("AI Moderation", 3))
        
        layout.addStretch()
        
        # Version info
        v_lbl = QLabel("System v4.2.1-Stable")
        v_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 500;")
        layout.addWidget(v_lbl)
        
        self.main_layout.addWidget(sidebar)

    def _setup_main_workspace(self):
        workspace = QWidget()
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(80)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(32, 0, 32, 0)
        
        search = QLineEdit()
        search.setPlaceholderText("Search users, logs, transactions...")
        search.setFixedWidth(320)
        search.setStyleSheet("background-color: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px 14px;")
        t_layout.addWidget(search)
        
        t_layout.addStretch()
        
        for btn_text in ["AI Moderation", "Broadcast"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("background-color: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px 20px; font-weight: 700; font-size: 13px;")
            t_layout.addWidget(btn)
        
        layout.addWidget(toolbar)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        content = QWidget()
        main_v = QVBoxLayout(content)
        main_v.setContentsMargins(40, 40, 40, 40)
        main_v.setSpacing(32)
        
        # 6 KPI Cards
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)
        kpis = [
            ("Total Users", "15.2k", "↑ 12%"), ("Active Sessions", "432", "Live"),
            ("Revenue", "$12.4k", "Monthly"), ("System Load", "24%", "Optimal"),
            ("Pending Reports", "12", "Urgent"), ("AI Accuracy", "98.2%", "Model v4")
        ]
        for i, (t, v, s) in enumerate(kpis):
            card = QFrame()
            card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px;")
            cl = QVBoxLayout(card)
            t_lbl = QLabel(t); t_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase;")
            v_lbl = QLabel(v); v_lbl.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 800;")
            s_lbl = QLabel(s); s_lbl.setStyleSheet("color: #10B981; font-size: 11px; font-weight: 600;")
            cl.addWidget(t_lbl); cl.addWidget(v_lbl); cl.addWidget(s_lbl)
            kpi_grid.addWidget(card, i // 3, i % 3)
        main_v.addLayout(kpi_grid)
        
        # User Management Table
        u_lbl = QLabel("User Management")
        u_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        main_v.addWidget(u_lbl)
        
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Role", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px;
                gridline-color: transparent; outline: none;
            }
            QHeaderView::section {
                background-color: #F8FAFC; padding: 12px; border: none;
                color: #64748B; font-weight: 700; font-size: 12px;
            }
        """)
        
        users = [
            ("Alice Smith", "Student", "Active"),
            ("Bob Johnson", "Mentor", "Active"),
            ("Charlie Brown", "Student", "Suspended"),
            ("Diana Prince", "Mentor", "Pending"),
            ("Ethan Hunt", "Student", "Active")
        ]
        
        for i, (n, r, s) in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(n))
            self.table.setItem(i, 1, QTableWidgetItem(r))
            self.table.setItem(i, 2, QTableWidgetItem(s))
            btn_act = QPushButton("Manage")
            btn_act.setStyleSheet("color: #38BDF8; font-weight: 700;")
            self.table.setCellWidget(i, 3, btn_act)
            
        main_v.addWidget(self.table)
        
        main_v.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.main_layout.addWidget(workspace, stretch=1)

    def _setup_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(340)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(28, 32, 28, 24)
        layout.setSpacing(28)
        
        # Live Online
        lo_lbl = QLabel("Live Online Users")
        lo_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 16px;")
        layout.addWidget(lo_lbl)
        
        for _ in range(3):
            row = QHBoxLayout()
            row.setSpacing(12)
            av = QLabel("👤"); av.setFixedSize(32, 32); av.setStyleSheet("background: #F1F5F9; border-radius: 16px;")
            av.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tl = QVBoxLayout(); tl.setSpacing(2)
            n_l = QLabel("User Name"); n_l.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 600;")
            r_l = QLabel("Viewing Dashboard"); r_l.setStyleSheet("color: #94A3B8; font-size: 11px;")
            tl.addWidget(n_l); tl.addWidget(r_l)
            row.addWidget(av); row.addLayout(tl); row.addStretch()
            layout.addLayout(row)
            
        # AI Moderation Assistant
        mod_card = QFrame()
        mod_card.setStyleSheet("background-color: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 16px;")
        ml = QVBoxLayout(mod_card)
        
        m_t = QLabel("🤖 AI Moderation Assistant")
        m_t.setStyleSheet("color: #0284C7; font-weight: 800; font-size: 14px;")
        ml.addWidget(m_t)
        
        m_d = QLabel("3 messages were auto-flagged for review in 'Community'.")
        m_d.setWordWrap(True)
        m_d.setStyleSheet("color: #0369A1; font-size: 12px; line-height: 1.4;")
        ml.addWidget(m_d)
        
        btn_rev = QPushButton("Review Now")
        btn_rev.setStyleSheet("background: #0284C7; color: white; border-radius: 8px; padding: 8px; font-weight: 700;")
        ml.addWidget(btn_rev)
        layout.addWidget(mod_card)
        
        # Critical Alerts
        ca_lbl = QLabel("Critical Alerts")
        ca_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 16px;")
        layout.addWidget(ca_lbl)
        
        for a in ["Database latency spike", "High login failures"]:
            al = QLabel(f"⚠️ {a}")
            al.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 500;")
            layout.addWidget(al)
            
        layout.addStretch()
        self.main_layout.addWidget(panel)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = AdminPanelPage()
    window.resize(1400, 900)
    window.show()
    sys.exit(app.exec())
