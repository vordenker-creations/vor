from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

from .certification_card import CertificationCard, AchievementBadge

class CertificationTrackerView(QWidget):
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
        cl.setContentsMargins(32, 32, 32, 40)
        cl.setSpacing(32)

        # 1. Hero Section
        self._setup_hero(cl)

        # 2. Achievement Badges
        self._setup_badges(cl)

        # 3. Certification Grid
        self._setup_certs(cl)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

    def _setup_hero(self, layout):
        hero = QFrame()
        hero.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(32, 32, 32, 32)
        hl.setSpacing(40)
        
        info = QVBoxLayout()
        info.setSpacing(8)
        
        tag = QLabel("✨ ACHIEVEMENT INTELLIGENCE")
        tag.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        
        title = QLabel("Career Validation Profile")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none;")
        
        desc = QLabel("You have 12 verified credentials. Your profile is <b>highly attractive</b> for Senior AI Architect roles.\nNext recommended milestone: <b>AWS Solutions Architect</b>.")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc)
        hl.addLayout(info, 1)
        
        # Mini Stats
        stats = QGridLayout()
        stats.setSpacing(12)
        
        def add_mini(label, val, r, c):
            v = QVBoxLayout()
            v.setSpacing(2)
            l1 = QLabel(val); l1.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")
            l2 = QLabel(label); l2.setStyleSheet("font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase;")
            v.addWidget(l1); v.addWidget(l2)
            stats.addLayout(v, r, c)
            
        add_mini("Certs", "12", 0, 0)
        add_mini("Badges", "45", 0, 1)
        add_mini("Skills", "128", 1, 0)
        add_mini("Rank", "Top 5%", 1, 1)
        
        hl.addLayout(stats)
        layout.addWidget(hero)

    def _setup_badges(self, layout):
        sec = QVBoxLayout()
        sec.setSpacing(16)
        
        lbl = QLabel("Unlocked Achievements")
        lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        sec.addWidget(lbl)
        
        bh = QHBoxLayout()
        bh.setSpacing(20)
        
        bh.addWidget(AchievementBadge("🚀", "Fast Learner", "Epic"))
        bh.addWidget(AchievementBadge("🧠", "AI Master", "Legendary"))
        bh.addWidget(AchievementBadge("🔥", "Streak Pro", "Rare"))
        bh.addWidget(AchievementBadge("⚡", "Quick Fixer", "Common"))
        bh.addWidget(AchievementBadge("🎨", "UI Design", "Rare"))
        bh.addStretch()
        
        sec.addLayout(bh)
        layout.addLayout(sec)

    def _setup_certs(self, layout):
        sec = QVBoxLayout()
        sec.setSpacing(16)
        
        lbl = QLabel("Verified Credentials")
        lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        sec.addWidget(lbl)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        certs = [
            {"title": "AWS Solutions Architect", "provider": "Amazon Web Services", "logo": "☁️", "state": "in_progress", "date": "Exp. Dec 2024", "is_ai_priority": True},
            {"title": "Professional ML Engineer", "provider": "Google Cloud", "logo": "🤖", "state": "completed", "date": "Issued Oct 2023"},
            {"title": "Meta Front-End Developer", "provider": "Coursera / Meta", "logo": "💻", "state": "completed", "date": "Issued Jan 2023"},
            {"title": "Azure AI Fundamentals", "provider": "Microsoft", "logo": "🧠", "state": "expiring", "date": "Expires in 12 days"},
        ]
        
        for i, c in enumerate(certs):
            card = CertificationCard(c)
            grid.addWidget(card, i // 2, i % 2)
            
        sec.addLayout(grid)
        layout.addLayout(sec)
