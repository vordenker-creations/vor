import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QGraphicsDropShadowEffect, QSizePolicy, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

class FileCategoryItem(QPushButton):
    def __init__(self, text, icon, is_active=False, parent=None):
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
        self.setText(f"{icon}  {text}")

class FileCard(QFrame):
    def __init__(self, name, size, date, icon, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 200)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            QFrame:hover { border: 1px solid #38BDF8; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 15)
        layout.setSpacing(10)
        
        # Icon
        ic = QLabel(icon)
        ic.setStyleSheet("font-size: 48px; background: transparent; border: none;")
        ic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ic)
        
        # Text
        n_lbl = QLabel(name)
        n_lbl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 13px; border: none;")
        n_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        n_lbl.setWordWrap(True)
        layout.addWidget(n_lbl)
        
        layout.addStretch()
        
        d_layout = QVBoxLayout()
        d_layout.setSpacing(2)
        s_lbl = QLabel(size); s_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; border: none;")
        s_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dt_lbl = QLabel(date); dt_lbl.setStyleSheet("color: #94A3B8; font-size: 10px; border: none;")
        dt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d_layout.addWidget(s_lbl); d_layout.addWidget(dt_lbl)
        layout.addLayout(d_layout)

class FileManagerPage(QWidget):
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
        layout.setSpacing(20)
        
        h_lbl = QLabel("Cloud Storage")
        h_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        layout.addWidget(h_lbl)
        
        upload_btn = QPushButton("Upload Files")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #38BDF8; color: white; border-radius: 10px;
                padding: 12px; font-weight: 700; font-size: 14px; border: none;
            }
            QPushButton:hover { background-color: #0284C7; }
        """)
        layout.addWidget(upload_btn)
        
        layout.addWidget(FileCategoryItem("All Files", "📂", True))
        layout.addWidget(FileCategoryItem("Documents", "📄"))
        layout.addWidget(FileCategoryItem("Assignments", "📝"))
        layout.addWidget(FileCategoryItem("Media", "🖼️"))
        layout.addWidget(FileCategoryItem("Shared with me", "👥"))
        layout.addWidget(FileCategoryItem("Starred", "⭐"))
        layout.addWidget(FileCategoryItem("Trash", "🗑️"))
        
        layout.addStretch()
        
        # Storage usage
        st_card = QFrame()
        st_card.setStyleSheet("background: #F8FAFC; border-radius: 12px; padding: 10px;")
        sl = QVBoxLayout(st_card)
        st_l = QLabel("Storage")
        st_l.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 12px;")
        sl.addWidget(st_l)
        pb = QProgressBar(); pb.setValue(65); pb.setFixedHeight(6); pb.setTextVisible(False)
        pb.setStyleSheet("QProgressBar { background: #E2E8F0; border: none; border-radius: 3px; } QProgressBar::chunk { background: #38BDF8; border-radius: 3px; }")
        sl.addWidget(pb)
        ss_l = QLabel("1.2 GB of 2.0 GB used")
        ss_l.setStyleSheet("color: #64748B; font-size: 11px;")
        sl.addWidget(ss_l)
        layout.addWidget(st_card)
        
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
        
        bc = QLabel("My Files / <font color='#38BDF8'>Documents</font>")
        bc.setStyleSheet("color: #64748B; font-size: 14px; font-weight: 500;")
        t_layout.addWidget(bc)
        
        t_layout.addStretch()
        
        search = QLineEdit(); search.setPlaceholderText("Search files..."); search.setFixedWidth(240)
        search.setStyleSheet("background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;")
        t_layout.addWidget(search)
        
        layout.addWidget(toolbar)
        
        # Content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        sc = QWidget()
        form_l = QVBoxLayout(sc)
        form_l.setContentsMargins(32, 32, 32, 32)
        form_l.setSpacing(32)
        
        # Grid
        grid = QGridLayout()
        grid.setSpacing(24)
        files = [
            ("Thesis_Final.pdf", "2.4 MB", "Oct 12, 2024", "📄"),
            ("Study_Plan.xlsx", "450 KB", "Oct 10, 2024", "📊"),
            ("Presentation.pptx", "12.0 MB", "Oct 08, 2024", "📽️"),
            ("Profile_Pic.png", "1.2 MB", "Oct 05, 2024", "🖼️"),
            ("Draft_Notes.txt", "12 KB", "Oct 01, 2024", "📝"),
        ]
        for i, (n, s, d, icon) in enumerate(files):
            row, col = divmod(i, 4)
            grid.addWidget(FileCard(n, s, d, icon), row, col)
        form_l.addLayout(grid)
        form_l.addStretch()
        
        scroll.setWidget(sc)
        layout.addWidget(scroll)
        self.main_layout.addWidget(workspace, stretch=1)

    def _setup_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(340)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        fd_l = QLabel("File Details")
        fd_l.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 16px;")
        layout.addWidget(fd_l)
        
        # Preview Placeholder
        prev = QFrame()
        prev.setFixedHeight(200)
        prev.setStyleSheet("background: #F1F5F9; border-radius: 12px; border: 2px dashed #CBD5E1;")
        pl = QVBoxLayout(prev); pl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pp_l = QLabel("Preview Placeholder")
        pp_l.setStyleSheet("color: #94A3B8; font-weight: 600;")
        pl.addWidget(pp_l)
        layout.addWidget(prev)
        
        # Metadata
        for k, v in [("Type", "PDF Document"), ("Size", "2.4 MB"), ("Modified", "Oct 12, 2024"), ("Owner", "Me")]:
            row = QHBoxLayout()
            kl = QLabel(k); kl.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 500;")
            row.addWidget(kl)
            row.addStretch()
            vl = QLabel(v); vl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 600;")
            row.addWidget(vl)
            layout.addLayout(row)
            
        layout.addStretch()
        
        for act in [("Share File", True), ("Download", False)]:
            btn = QPushButton(act[0])
            if act[1]:
                btn.setStyleSheet("background: #38BDF8; color: white; border-radius: 8px; padding: 12px; font-weight: 700;")
            else:
                btn.setStyleSheet("background: white; border: 1px solid #E2E8F0; color: #0F172A; border-radius: 8px; padding: 12px; font-weight: 700;")
            layout.addWidget(btn)
            
        self.main_layout.addWidget(panel)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = FileManagerPage()
    window.resize(1400, 900)
    window.show()
    sys.exit(app.exec())
