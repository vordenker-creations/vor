from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class SystemMetricCard(QFrame):
    def __init__(self, title, value, status="Stable", color="#10B981", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }}
        """)
        l = QVBoxLayout(self)
        l.setContentsMargins(16, 16, 16, 16)
        l.setSpacing(6)
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 10px; font-weight: 800; color: #94A3B8; text-transform: uppercase; border: none; background: transparent;")
        
        v = QLabel(value)
        v.setStyleSheet(f"font-size: 18px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        
        s = QLabel(status)
        s.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {color}15; padding: 2px 8px; border-radius: 6px; border: none;")
        s.setFixedWidth(s.sizeHint().width() + 16)
        
        l.addWidget(t)
        l.addWidget(v)
        l.addWidget(s)

class InfoRow(QWidget):
    def __init__(self, label, value, parent=None):
        super().__init__(parent)
        l = QHBoxLayout(self)
        l.setContentsMargins(0, 8, 0, 8)
        
        lbl = QLabel(label)
        lbl.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500; border: none;")
        
        val = QLabel(value)
        val.setStyleSheet("font-size: 13px; color: #0F172A; font-weight: 700; border: none;")
        
        l.addWidget(lbl)
        l.addStretch()
        l.addWidget(val)

class AboutApplicationWorkspace(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        cl = QVBoxLayout(container)
        cl.setContentsMargins(32, 24, 32, 32)
        cl.setSpacing(32)

        # 1. Hero Summary
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(24)
        
        info = QVBoxLayout(); info.setSpacing(8)
        tag = QLabel("🖥️ PLATFORM INTELLIGENCE")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("AI-Career Bridge")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Enterprise Career Intelligence Platform. Your system is currently running <b>Version 2.4.0-pro</b> with full AI acceleration active.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        grid = QGridLayout(); grid.setSpacing(12)
        grid.addWidget(SystemMetricCard("Build", "2.4.0", "Latest", "#10B981"), 0, 0)
        grid.addWidget(SystemMetricCard("AI Engine", "Neural-X", "Active", "#38BDF8"), 0, 1)
        grid.addWidget(SystemMetricCard("Health", "99.2%", "Optimal", "#10B981"), 1, 0)
        grid.addWidget(SystemMetricCard("Security", "L-Shield", "Secure", "#8B5CF6"), 1, 1)
        hl.addLayout(grid)
        cl.addWidget(hero)

        # 2. Application Information
        info_card = QFrame()
        info_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        il = QVBoxLayout(info_card); il.setContentsMargins(24, 24, 24, 24); il.setSpacing(10)
        il.addWidget(QLabel("Platform Details", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none; margin-bottom: 10px;"))
        
        il.addWidget(InfoRow("Application Version", "2.4.0 (Professional Edition)"))
        il.addWidget(InfoRow("Release Channel", "Stable Production"))
        il.addWidget(InfoRow("Build Number", "AI-CB-2024-X92"))
        il.addWidget(InfoRow("Architecture", "x86_64 Desktop Core"))
        il.addWidget(InfoRow("Inference Engine", "Optimized CUDA/Metal Hybrid"))
        cl.addWidget(info_card)

        # 3. System Diagnostics
        diag_sec = QWidget()
        dl = QVBoxLayout(diag_sec); dl.setContentsMargins(0, 0, 0, 0); dl.setSpacing(16)
        dl.addWidget(QLabel("Realtime Diagnostics", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        diag_grid = QGridLayout(); diag_grid.setSpacing(16)
        
        def add_diag_card(title, value, pct, r, c):
            card = QFrame()
            card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 18px;")
            v_l = QVBoxLayout(card); v_l.setContentsMargins(16, 16, 16, 16); v_l.setSpacing(10)
            h = QHBoxLayout()
            h.addWidget(QLabel(title, styleSheet="font-size: 11px; font-weight: 800; color: #94A3B8;")); h.addStretch()
            h.addWidget(QLabel(value, styleSheet="font-size: 11px; font-weight: 700; color: #0F172A;"))
            v_l.addLayout(h)
            pb = QProgressBar(); pb.setFixedHeight(4); pb.setValue(pct); pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #F1F5F9; border-radius: 2px; border: none; } QProgressBar::chunk { background: #38BDF8; border-radius: 2px; }")
            v_l.addWidget(pb)
            diag_grid.addWidget(card, r, c)

        add_diag_card("CPU Utilization", "12%", 12, 0, 0)
        add_diag_card("Memory Usage", "1.4 GB / 8GB", 18, 0, 1)
        add_diag_card("GPU Acceleration", "Active (40%)", 40, 1, 0)
        add_diag_card("AI Cache Health", "98%", 98, 1, 1)
        dl.addLayout(diag_grid)
        cl.addWidget(diag_sec)

        # 4. Updates Timeline
        update_card = QFrame()
        update_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 22px;")
        ul = QVBoxLayout(update_card); ul.setContentsMargins(24, 24, 24, 24); ul.setSpacing(16)
        ul.addWidget(QLabel("Release History", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A; border: none;"))
        
        updates = [
            ("v2.4.0", "New Career Path Intelligence & Skill Graph visualizations.", "Today"),
            ("v2.3.5", "Performance optimizations for large resume dataset parsing.", "Last Week"),
            ("v2.3.0", "AI Mentor integration with GPT-4 Omni support.", "2 Weeks Ago")
        ]
        for ver, desc, time in updates:
            row = QVBoxLayout(); row.setSpacing(4)
            h = QHBoxLayout()
            h.addWidget(QLabel(ver, styleSheet="font-weight: 800; font-size: 13px; color: #0F172A;"))
            h.addStretch()
            h.addWidget(QLabel(time, styleSheet="font-size: 11px; color: #94A3B8;"))
            row.addLayout(h)
            row.addWidget(QLabel(desc, styleSheet="font-size: 12px; color: #64748B;"))
            ul.addLayout(row)
            
        cl.addWidget(update_card)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
