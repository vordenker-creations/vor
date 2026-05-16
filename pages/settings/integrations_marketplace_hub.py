from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class IntegrationMetricCard(QFrame):
    def __init__(self, title, value, status="Healthy", color="#10B981", parent=None):
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
        v.setStyleSheet(f"font-size: 20px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        
        s = QLabel(status)
        s.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {color}15; padding: 2px 8px; border-radius: 6px; border: none;")
        s.setFixedWidth(s.sizeHint().width() + 16)
        
        l.addWidget(t)
        l.addWidget(v)
        l.addWidget(s)

class MarketplaceCard(QFrame):
    def __init__(self, name, icon, category, is_connected=False, parent=None):
        super().__init__(parent)
        self.setFixedHeight(160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 2px solid {'#38BDF8' if is_connected else '#E2E8F0'};
                border-radius: 22px;
            }}
            QFrame:hover {{
                border-color: #38BDF8;
                background-color: #F8FAFC;
            }}
        """)
        
        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(10)
        
        h = QHBoxLayout()
        ico = QLabel(icon); ico.setStyleSheet("font-size: 24px; border: none; background: transparent;")
        h.addWidget(ico); h.addStretch()
        
        if is_connected:
            badge = QLabel("Connected")
            badge.setStyleSheet("font-size: 9px; font-weight: 800; color: #10B981; background: #F0FDF4; padding: 4px 8px; border-radius: 6px; border: 1px solid #BBF7D0;")
            h.addWidget(badge)
        l.addLayout(h)
        
        t = QLabel(name)
        t.setStyleSheet("font-weight: 700; font-size: 14px; color: #0F172A; border: none; background: transparent;")
        l.addWidget(t)
        
        c = QLabel(category)
        c.setStyleSheet("font-size: 11px; color: #64748B; border: none; background: transparent;")
        l.addWidget(c)
        
        l.addStretch()
        
        btn = QPushButton("Manage" if is_connected else "Connect")
        btn.setFixedHeight(32)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {'#F1F5F9' if is_connected else '#0F172A'};
                color: {'#0F172A' if is_connected else 'white'};
                border-radius: 8px;
                font-weight: 700;
                font-size: 11px;
                border: none;
            }}
            QPushButton:hover {{
                background: {'#E2E8F0' if is_connected else '#1E293B'};
            }}
        """)
        l.addWidget(btn)

class IntegrationsMarketplaceHub(QWidget):
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
        tag = QLabel("🔌 CONNECTED ECOSYSTEM")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        title = QLabel("Integrations Hub")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Your productivity ecosystem is <b>92% synchronized</b>. AI is currently managing 4 active workflow automations across 8 connected services.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        grid = QGridLayout(); grid.setSpacing(12)
        grid.addWidget(IntegrationMetricCard("Services", "08", "Active", "#10B981"), 0, 0)
        grid.addWidget(IntegrationMetricCard("Sync Health", "98%", "Excellent", "#10B981"), 0, 1)
        grid.addWidget(IntegrationMetricCard("Automations", "12", "Running", "#38BDF8"), 1, 0)
        grid.addWidget(IntegrationMetricCard("Eco Score", "Elite", "Maximum", "#8B5CF6"), 1, 1)
        hl.addLayout(grid)
        cl.addWidget(hero)

        # 2. Marketplace Section
        market_sec = QWidget()
        ml = QVBoxLayout(market_sec); ml.setContentsMargins(0, 0, 0, 0); ml.setSpacing(16)
        ml.addWidget(QLabel("Available Integrations", styleSheet="font-size: 16px; font-weight: 800; color: #0F172A;"))
        
        market_grid = QGridLayout(); market_grid.setSpacing(16)
        market_grid.addWidget(MarketplaceCard("GitHub", "💻", "Development & Code", True), 0, 0)
        market_grid.addWidget(MarketplaceCard("LinkedIn", "💼", "Professional Network", True), 0, 1)
        market_grid.addWidget(MarketplaceCard("Google Cal", "📅", "Productivity & Scheduling"), 0, 2)
        market_grid.addWidget(MarketplaceCard("Notion", "📝", "Workspace & Knowledge"), 1, 0)
        market_grid.addWidget(MarketplaceCard("Slack", "💬", "Team Communication"), 1, 1)
        market_grid.addWidget(MarketplaceCard("Dropbox", "☁️", "Cloud Storage & Backup"), 1, 2)
        ml.addLayout(market_grid)
        cl.addWidget(market_sec)

        # 3. Workflow Automation Preview
        auto_sec = QFrame()
        auto_sec.setStyleSheet("background: #0F172A; border-radius: 24px;")
        al = QHBoxLayout(auto_sec); al.setContentsMargins(32, 32, 32, 32); al.setSpacing(24)
        
        a_info = QVBoxLayout(); a_info.setSpacing(8)
        a_title = QLabel("Intelligent Automations")
        a_title.setStyleSheet("color: white; font-size: 18px; font-weight: 800;")
        a_desc = QLabel("Connect your roadmap milestones to your Google Calendar and receive AI reminders automatically.")
        a_desc.setStyleSheet("color: #94A3B8; font-size: 13px; line-height: 1.4;")
        a_info.addWidget(a_title); a_info.addWidget(a_desc)
        al.addLayout(a_info, 1)
        
        btn_build = QPushButton("Build Workflow")
        btn_build.setFixedSize(160, 44)
        btn_build.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: #0F172A; border-radius: 12px; font-weight: 800; font-size: 13px;
            }
            QPushButton:hover { background: #7DD3FC; }
        """)
        al.addWidget(btn_build)
        cl.addWidget(auto_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
