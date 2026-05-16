from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar, QGridLayout, QComboBox, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class BuilderHeroMetric(QFrame):
    def __init__(self, title, value, color="#38BDF8", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 20px;")
        l = QVBoxLayout(self)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(6)
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 10px; font-weight: 800; color: #94A3B8; text-transform: uppercase; border: none;")
        l.addWidget(t)
        
        v = QLabel(value)
        v.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {color}; border: none;")
        l.addWidget(v)

class RoadmapBuilderView(QWidget):
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
        hero_card = QFrame()
        hero_card.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        hl = QHBoxLayout(hero_card); hl.setContentsMargins(32, 32, 32, 32); hl.setSpacing(40)
        
        info = QVBoxLayout(); info.setSpacing(10)
        tag = QLabel("✨ AI ROADMAP ENGINE")
        tag.setStyleSheet("font-size: 12px; font-weight: 800; color: #38BDF8;")
        title = QLabel("Custom Curriculum Builder")
        title.setStyleSheet("font-size: 26px; font-weight: 800; color: #0F172A; border: none;")
        desc = QLabel("Define your career goals and let our AI architect a personalized learning path with optimized milestones and resource recommendations.")
        desc.setWordWrap(True); desc.setStyleSheet("font-size: 14px; color: #64748B; border: none; line-height: 1.5;")
        
        info.addWidget(tag); info.addWidget(title); info.addWidget(desc); info.addStretch()
        hl.addLayout(info, 1)
        
        metrics = QGridLayout(); metrics.setSpacing(12)
        metrics.addWidget(BuilderHeroMetric("Complexity", "Advanced", "#EF4444"), 0, 0)
        metrics.addWidget(BuilderHeroMetric("Duration", "6 Months", "#38BDF8"), 0, 1)
        metrics.addWidget(BuilderHeroMetric("Confidence", "94%", "#10B981"), 1, 0)
        metrics.addWidget(BuilderHeroMetric("Readiness", "High", "#8B5CF6"), 1, 1)
        hl.addLayout(metrics)
        
        cl.addWidget(hero_card)

        # 2. Builder Wizard
        wizard = QFrame()
        wizard.setStyleSheet("background: white; border: 1px solid #E2E8F0; border-radius: 24px;")
        wl = QVBoxLayout(wizard); wl.setContentsMargins(32, 32, 32, 32); wl.setSpacing(24)
        
        wl.addWidget(QLabel("Configure Your Path", styleSheet="font-size: 18px; font-weight: 800; color: #0F172A; border: none;"))
        
        form_grid = QGridLayout(); form_grid.setSpacing(24)
        
        def add_field(label, widget, r, c):
            v = QVBoxLayout(); v.setSpacing(8)
            lbl = QLabel(label); lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #475569; border: none;")
            widget.setFixedHeight(44)
            widget.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0 12px; font-size: 13px;")
            v.addWidget(lbl); v.addWidget(widget)
            form_grid.addLayout(v, r, c)
            
        # Select Career
        cb_career = QComboBox(); cb_career.addItems(["Senior AI Engineer", "Cloud Architect", "Full-Stack Developer", "Cybersecurity Lead"])
        add_field("Target Career Role", cb_career, 0, 0)
        
        # Skill Level
        cb_level = QComboBox(); cb_level.addItems(["Beginner", "Intermediate", "Advanced", "Professional"])
        add_field("Current Proficiency", cb_level, 0, 1)
        
        # Tech Preferences
        le_tech = QLineEdit(); le_tech.setPlaceholderText("e.g. Python, AWS, React, PyTorch")
        add_field("Preferred Technologies", le_tech, 1, 0)
        
        # Intensity
        cb_intensity = QComboBox(); cb_intensity.addItems(["Standard (10h/week)", "Intensive (25h/week)", "Accelerated (40h/week)"])
        add_field("Learning Intensity", cb_intensity, 1, 1)
        
        wl.addLayout(form_grid)
        
        # Action Button
        btn_generate = QPushButton("Generate Personalized Roadmap ✨")
        btn_generate.setFixedHeight(50)
        btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_generate.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 14px;
                font-weight: 800; font-size: 14px; border: none;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        wl.addWidget(btn_generate)
        
        cl.addWidget(wizard)

        # 3. Preview Section
        preview_sec = QFrame()
        preview_sec.setStyleSheet("background: #F1F5F9; border-radius: 24px; border: 1px dashed #CBD5E1;")
        preview_sec.setMinimumHeight(400)
        pl = QVBoxLayout(preview_sec); pl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        msg = QLabel("Generation Preview")
        msg.setStyleSheet("color: #94A3B8; font-size: 16px; font-weight: 600;")
        pl.addWidget(msg)
        
        cl.addWidget(preview_sec)

        cl.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)
