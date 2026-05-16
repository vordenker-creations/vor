from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, QComboBox, 
                             QButtonGroup)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor
from .job_card import JobCard

class JobFeed(QWidget):
    job_selected = pyqtSignal(dict)
    apply_requested = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F8FAFC;")
        self.job_cards = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self._setup_header(layout)
        
        # Feed Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                min-height: 40px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setContentsMargins(32, 32, 32, 40)
        self.grid_layout.setSpacing(24)
        
        self._setup_mock_jobs()
        
        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll)

    def _setup_header(self, layout):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(32, 0, 32, 0)
        hl.setSpacing(24)
        
        # Info
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        info_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title_h = QHBoxLayout()
        title_h.setSpacing(12)
        title = QLabel("Explore Opportunities")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        ai_badge = QLabel("AI Recommended")
        ai_badge.setStyleSheet("""
            background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD;
            border-radius: 8px; padding: 4px 10px; font-size: 10px; font-weight: 700;
        """)
        
        title_h.addWidget(title)
        title_h.addWidget(ai_badge)
        title_h.addStretch()
        
        count = QLabel("1,245 matching roles found")
        count.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none;")
        
        info_v.addLayout(title_h)
        info_v.addWidget(count)
        hl.addLayout(info_v)
        
        hl.addStretch()
        
        # Sort
        sort_h = QHBoxLayout()
        sort_h.setSpacing(12)
        sort_lbl = QLabel("Sort by")
        sort_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; font-weight: 600; border: none;")
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["AI Match Score", "Recent Postings", "Highest Salary"])
        self.sort_combo.setFixedHeight(36)
        self.sort_combo.setFixedWidth(160)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                padding: 0 12px; font-size: 13px; font-weight: 600; color: #1E293B;
            }
            QComboBox::drop-down { border: none; width: 0px; }
        """)
        
        sort_h.addWidget(sort_lbl)
        sort_h.addWidget(self.sort_combo)
        hl.addLayout(sort_h)
        
        layout.addWidget(header)

    def _setup_mock_jobs(self):
        jobs = [
            {"title": "Senior AI Engineer", "company": "OpenAI", "company_initials": "O", "logo_bg": "#000000", "location": "San Francisco / Remote", "type": "Full-time", "salary": "$250k - $400k", "match_score": 98, "posted_time": "2h ago", "description": "We are looking for a Senior AI Engineer to join our core team. You will be responsible for scaling our latest models and developing infrastructure for high-performance computing."},
            {"title": "Machine Learning Intern", "company": "NVIDIA", "company_initials": "N", "logo_bg": "#76B900", "location": "Santa Clara, CA", "type": "Internship", "salary": "$50 - $80/hr", "match_score": 92, "posted_time": "5h ago", "description": "Join our DL research lab as an intern. Work on state-of-the-art vision models and accelerate inference using TensorRT."},
            {"title": "Frontend Architect", "company": "Vercel", "company_initials": "V", "logo_bg": "#000000", "location": "Remote", "type": "Full-time", "salary": "$180k - $240k", "match_score": 88, "posted_time": "1d ago", "description": "Define the future of the web. Build performant, accessible components that power millions of sites."},
            {"title": "Data Scientist", "company": "Tesla", "company_initials": "T", "logo_bg": "#E81919", "location": "Austin, TX / Hybrid", "type": "Full-time", "salary": "$140k - $210k", "match_score": 85, "posted_time": "3h ago", "description": "Apply statistical methods to Autopilot data. Detect anomalies and improve safety through data-driven insights."},
            {"title": "Product Designer", "company": "Airbnb", "company_initials": "A", "logo_bg": "#FF5A5F", "location": "Remote", "type": "Contract", "salary": "$120 - $160/hr", "match_score": 79, "posted_time": "12h ago", "description": "Craft beautiful user journeys for our global community of hosts and guests."},
            {"title": "Backend Developer (Go)", "company": "Cloudflare", "company_initials": "C", "logo_bg": "#F38020", "location": "Lisbon / Hybrid", "type": "Full-time", "salary": "€80k - €120k", "match_score": 82, "posted_time": "2d ago", "description": "Scale the global network. Write efficient, secure Go code to handle trillions of requests per day."},
            {"title": "Security Engineer", "company": "CrowdStrike", "company_initials": "C", "logo_bg": "#FC0000", "location": "Remote", "type": "Full-time", "salary": "$160k - $220k", "match_score": 94, "posted_time": "4h ago", "description": "Hunt threats and build defensive layers. Protect our customers from the most advanced adversaries."},
            {"title": "Mobile Engineer (Flutter)", "company": "ByteDance", "company_initials": "B", "logo_bg": "#000000", "location": "Singapore", "type": "Full-time", "salary": "$120k - $180k", "match_score": 76, "posted_time": "6h ago", "description": "Create engaging mobile experiences for TikTok users globally using Flutter."}
        ]
        
        for i, job in enumerate(jobs):
            card = JobCard(job)
            card.clicked.connect(self._handle_card_clicked)
            card.apply_clicked.connect(self.apply_requested.emit)
            self.job_cards.append(card)
            self.grid_layout.addWidget(card, i // 2, i % 2)
        
        # Add stretch to avoid giant cards if few results
        self.grid_layout.setRowStretch(len(jobs)//2 + 1, 1)

    def _handle_card_clicked(self, data):
        for card in self.job_cards:
            card.set_selected(card.data == data)
        self.job_selected.emit(data)
