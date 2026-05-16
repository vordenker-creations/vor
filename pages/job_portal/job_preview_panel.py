from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect,
                             QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor

class JobPreviewPanel(QFrame):
    apply_clicked = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(0)
        self.setMaximumWidth(0) # Initially hidden
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        self.data = None
        self.is_open = False
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # --- Detail Widget ---
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        self.detail_layout.setContentsMargins(0, 0, 0, 0)
        self.detail_layout.setSpacing(0)
        
        # Fade animation for content change
        self.opacity_effect = QGraphicsOpacityEffect(self.detail_widget)
        self.detail_widget.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._setup_detail_ui()
        self.main_layout.addWidget(self.detail_widget)
        
        # Width Animation for Expand/Collapse
        self.width_anim = QPropertyAnimation(self, b"maximumWidth")
        self.width_anim.setDuration(400)
        self.width_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _setup_detail_ui(self):
        # 1. Header (Sticky)
        self.header = QFrame()
        self.header.setFixedHeight(240)
        self.header.setStyleSheet("background-color: #F8FAFC; border-bottom: 1px solid #E2E8F0;")
        hv = QVBoxLayout(self.header)
        hv.setContentsMargins(32, 40, 32, 32)
        hv.setSpacing(20)
        
        # Close Button
        self.close_btn = QPushButton("×", self.header)
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #94A3B8; font-size: 24px; font-weight: 300; border: none;
            }
            QPushButton:hover { color: #0F172A; }
        """)
        self.close_btn.clicked.connect(self.hide_panel)
        self.close_btn.move(10, 10)
        
        # Logo & Meta
        top_h = QHBoxLayout()
        self.logo_box = QFrame()
        self.logo_box.setFixedSize(56, 56)
        self.logo_box.setStyleSheet("background: #0F172A; border-radius: 14px; border: none;")
        self.logo_lbl = QLabel("O", self.logo_box)
        self.logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_lbl.setStyleSheet("color: white; font-weight: 800; font-size: 20px; background: transparent; border: none;")
        self.logo_lbl.setFixedSize(56, 56)
        top_h.addWidget(self.logo_box)
        
        meta_v = QVBoxLayout()
        meta_v.setSpacing(4)
        self.company_name = QLabel("Company Name")
        self.company_name.setStyleSheet("font-size: 14px; font-weight: 600; color: #64748B; border: none; background: transparent;")
        self.posted_date = QLabel("Posted 2 days ago")
        self.posted_date.setStyleSheet("font-size: 12px; color: #94A3B8; border: none; background: transparent;")
        meta_v.addWidget(self.company_name)
        meta_v.addWidget(self.posted_date)
        top_h.addLayout(meta_v)
        top_h.addStretch()
        hv.addLayout(top_h)
        
        # Title
        self.title_lbl = QLabel("Job Title")
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        hv.addWidget(self.title_lbl)
        
        # Action Buttons
        ah = QHBoxLayout()
        ah.setSpacing(12)
        
        self.apply_btn = QPushButton("Apply Now")
        self.apply_btn.setFixedHeight(46)
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.clicked.connect(lambda: self.apply_clicked.emit(self.data))
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 12px;
                font-size: 14px; font-weight: 700; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        
        self.save_btn = QPushButton("Save Opportunity")
        self.save_btn.setFixedHeight(46)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: white; border: 1.5px solid #E2E8F0; border-radius: 12px;
                color: #0F172A; font-size: 14px; font-weight: 600; padding: 0 20px;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #CBD5E1; }
        """)
        
        ah.addWidget(self.apply_btn, 1)
        ah.addWidget(self.save_btn)
        hv.addLayout(ah)
        
        self.detail_layout.addWidget(self.header)
        
        # 2. Scrollable Body
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("""
            QScrollArea { background: white; border: none; }
            QScrollBar:vertical { border: none; background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: #E2E8F0; border-radius: 3px; }
        """)
        
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background-color: white;")
        cv = QVBoxLayout(self.content_container)
        cv.setContentsMargins(32, 32, 32, 40)
        cv.setSpacing(32)
        
        # Quick Stats
        self.stats_h = QHBoxLayout()
        self.stats_h.setSpacing(20)
        
        def create_stat(icon, title):
            w = QWidget()
            l = QVBoxLayout(w)
            l.setSpacing(4)
            l.setContentsMargins(0, 0, 0, 0)
            t = QLabel(f"{icon} {title}")
            t.setStyleSheet("font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; border: none;")
            v = QLabel("N/A")
            v.setStyleSheet("font-size: 13px; font-weight: 600; color: #1E293B; border: none;")
            l.addWidget(t)
            l.addWidget(v)
            return w, v
            
        self.sal_stat, self.sal_lbl = create_stat("💰", "Salary")
        self.loc_stat, self.loc_lbl = create_stat("📍", "Location")
        self.typ_stat, self.typ_lbl = create_stat("🕒", "Job Type")
        
        self.stats_h.addWidget(self.sal_stat)
        self.stats_h.addWidget(self.loc_stat)
        self.stats_h.addWidget(self.typ_stat)
        cv.addLayout(self.stats_h)
        
        # Sections
        self.desc_sec = self._add_section(cv, "Role Overview", "Loading...")
        self.req_sec = self._add_section(cv, "Key Requirements", "Loading...")
        self.skill_sec = self._add_section(cv, "Target Skills", "Loading...")
        
        cv.addStretch()
        self.scroll.setWidget(self.content_container)
        self.detail_layout.addWidget(self.scroll)

    def _add_section(self, layout, title, text):
        sv = QVBoxLayout()
        sv.setSpacing(12)
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        
        d = QLabel(text)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 14px; color: #475569; line-height: 1.6; border: none; background: transparent;")
        
        sv.addWidget(t)
        sv.addWidget(d)
        layout.addLayout(sv)
        return d

    def set_job(self, data):
        if not data: return
        self.data = data
        
        # Start fade out if already open
        if self.is_open:
            self.fade_anim.setStartValue(1.0)
            self.fade_anim.setEndValue(0.2)
            self.fade_anim.finished.connect(self._update_data_and_fade_in)
            self.fade_anim.start()
        else:
            self._update_data_and_fade_in()
            self.show_panel()

    def _update_data_and_fade_in(self):
        try:
            self.fade_anim.finished.disconnect(self._update_data_and_fade_in)
        except: pass
        
        # Update Data
        self.title_lbl.setText(self.data.get("title", ""))
        self.company_name.setText(self.data.get("company", ""))
        self.posted_date.setText(f"Posted {self.data.get('posted_time', 'Recently')}")
        
        self.sal_lbl.setText(self.data.get("salary", "N/A"))
        self.loc_lbl.setText(self.data.get("location", "N/A"))
        self.typ_lbl.setText(self.data.get("type", "N/A"))
        
        self.logo_box.setStyleSheet(f"background: {self.data.get('logo_bg', '#0F172A')}; border-radius: 14px; border: none;")
        self.logo_lbl.setText(self.data.get("company_initials", "O"))
        
        desc = self.data.get("description", "Join our growing team and help shape the future.")
        self.desc_sec.setText(desc)
        
        self.req_sec.setText("• Strong proficiency in relevant technologies\n• Problem-solving mindset\n• Excellent communication skills")
        self.skill_sec.setText("Python • AI/ML • UI Design • Cloud Infrastructure")
        
        self.scroll.verticalScrollBar().setValue(0)
        
        # Fade in
        self.fade_anim.setStartValue(0.2 if self.is_open else 0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def show_panel(self):
        if self.is_open: return
        self.is_open = True
        self.setMinimumWidth(450)
        self.width_anim.setStartValue(0)
        self.width_anim.setEndValue(450)
        self.width_anim.start()

    def hide_panel(self):
        if not self.is_open: return
        self.is_open = False
        self.width_anim.setStartValue(self.width())
        self.width_anim.setEndValue(0)
        self.width_anim.finished.connect(lambda: self.setMinimumWidth(0))
        self.width_anim.start()
        # Notify parent to deselect cards
        if hasattr(self.parent(), "clear_selection"):
            self.parent().clear_selection()

