from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QGraphicsDropShadowEffect, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor, QPainter, QPen

class EventCard(QFrame):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedHeight(100)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 18px;
            }
            QFrame:hover {
                border-color: #38BDF8;
                background-color: #F8FAFC;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(15, 23, 42, 8))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(16)
        
        # 1. Icon & Connector Node
        icon_container = QVBoxLayout()
        icon_container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.icon_lbl = QLabel(data.get("icon", "⚡"))
        self.icon_lbl.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        icon_container.addWidget(self.icon_lbl)
        layout.addLayout(icon_container)
        
        # 2. Content
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        
        title_h = QHBoxLayout()
        title_h.setSpacing(8)
        self.title_lbl = QLabel(data.get("title", "Event Title"))
        self.title_lbl.setStyleSheet("font-weight: 700; font-size: 13px; color: #0F172A; border: none;")
        
        self.priority_lbl = QLabel(data.get("priority", "Standard"))
        p_color = "#64748B"
        if data.get("priority") == "Critical": p_color = "#EF4444"
        elif data.get("priority") == "Important": p_color = "#F59E0B"
        elif data.get("priority") == "AI Generated": p_color = "#8B5CF6"
        
        self.priority_lbl.setStyleSheet(f"""
            font-size: 9px; font-weight: 800; color: {p_color}; 
            background: {p_color}15; padding: 2px 6px; border-radius: 4px;
        """)
        
        title_h.addWidget(self.title_lbl)
        title_h.addWidget(self.priority_lbl)
        title_h.addStretch()
        info_v.addLayout(title_h)
        
        self.desc_lbl = QLabel(data.get("desc", "Description of the operation."))
        self.desc_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none;")
        self.desc_lbl.setWordWrap(True)
        info_v.addWidget(self.desc_lbl)
        
        source_h = QHBoxLayout()
        self.source_lbl = QLabel(f"Source: {data.get('source', 'System')}")
        self.source_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 600;")
        self.time_lbl = QLabel(data.get("time", "Just now"))
        self.time_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        source_h.addWidget(self.source_lbl); source_h.addStretch(); source_h.addWidget(self.time_lbl)
        info_v.addLayout(source_h)
        
        layout.addLayout(info_v, 1)

class RealtimeActivityTimeline(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.setup_mock_events()

    def setup_mock_events(self):
        events = [
            {"title": "AI Roadmap Optimized", "desc": "Career path intelligence updated for Cloud Architecture goal.", "icon": "✨", "priority": "AI Generated", "source": "Neural-X Engine", "time": "2m ago"},
            {"title": "Milestone Achieved", "desc": "Python Advanced Patterns module completed with 98% score.", "icon": "🏆", "priority": "Important", "source": "Learning Track", "time": "15m ago"},
            {"title": "Sync Completed", "desc": "GitHub integration synchronized 12 repositories successfully.", "icon": "💻", "priority": "Standard", "source": "Integration Hub", "time": "1h ago"},
            {"title": "Security Alert", "desc": "New login detected from unusual location. Identity verified.", "icon": "🛡️", "priority": "Critical", "source": "L-Shield", "time": "3h ago"},
            {"title": "Community Update", "desc": "3 new responses to your 'Distributed Systems' post.", "icon": "👥", "priority": "Standard", "source": "Community", "time": "5h ago"}
        ]
        
        for e in events:
            self.add_event(e)

    def add_event(self, data):
        card = EventCard(data)
        self.layout.addWidget(card)
