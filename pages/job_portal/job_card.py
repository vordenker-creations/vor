from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen

class AIMatchIndicator(QWidget):
    def __init__(self, score, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self.score = score
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background circle
        painter.setPen(QPen(QColor(241, 245, 249), 4))
        painter.drawEllipse(4, 4, 42, 42)
        
        # Draw progress arc
        color = QColor("#38BDF8") 
        if self.score > 90: color = QColor("#10B981") 
        elif self.score > 75: color = QColor("#38BDF8") 
        elif self.score < 50: color = QColor("#EF4444") 
            
        painter.setPen(QPen(color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        span_angle = int(-self.score / 100.0 * 360 * 16)
        painter.drawArc(4, 4, 42, 42, 90 * 16, span_angle)
        
        # Draw text
        painter.setPen(QColor("#0F172A"))
        font = QFont("Inter", 10, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.score}%")

class JobCard(QFrame):
    clicked = pyqtSignal(dict)
    apply_clicked = pyqtSignal(dict)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.selected = False
        self.setFixedHeight(220)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setup_ui()
        self.setup_shadow()

    def setup_ui(self):
        self.setProperty("class", "JobCard")
        self.setStyleSheet("""
            QFrame[class="JobCard"] {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #E2E8F0;
            }
            QFrame[class="JobCard"]:hover {
                border: 1px solid #38BDF8;
                background-color: #FFFFFF;
            }
            QFrame[class="JobCard"][selected="true"] {
                border: 2px solid #38BDF8;
                background-color: #F0F9FF;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(12)
        
        # --- Top Header ---
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Logo
        logo_container = QFrame()
        logo_container.setFixedSize(48, 48)
        logo_container.setStyleSheet(f"""
            background-color: {self.data.get('logo_bg', '#F1F5F9')};
            border-radius: 12px;
            border: none;
        """)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_text = QLabel(self.data.get("company_initials", "CO"))
        logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_text.setStyleSheet("color: white; font-weight: 800; font-size: 16px; border: none; background: transparent;")
        logo_layout.addWidget(logo_text)
        header_layout.addWidget(logo_container)
        
        # Title & Company
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        
        title_lbl = QLabel(self.data.get("title", "Job Title"))
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        title_lbl.setWordWrap(True)
        
        company_h = QHBoxLayout()
        company_h.setSpacing(6)
        company_lbl = QLabel(self.data.get("company", "Company"))
        company_lbl.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none; background: transparent;")
        
        verified_badge = QLabel("✓")
        verified_badge.setFixedSize(14, 14)
        verified_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        verified_badge.setStyleSheet("background-color: #38BDF8; color: white; border-radius: 7px; font-size: 8px; font-weight: bold;")
        
        company_h.addWidget(company_lbl)
        company_h.addWidget(verified_badge)
        company_h.addStretch()
        
        info_v.addWidget(title_lbl)
        info_v.addLayout(company_h)
        header_layout.addLayout(info_v, 1)
        
        # AI Match
        self.match_indicator = AIMatchIndicator(self.data.get("match_score", 85))
        header_layout.addWidget(self.match_indicator)
        
        self.main_layout.addLayout(header_layout)
        
        # --- Middle Tags ---
        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(6)
        
        tags = [
            (self.data.get("location", "Remote"), "#F1F5F9", "#475569"),
            (self.data.get("type", "Full-time"), "#ECFDF5", "#059669"),
            (self.data.get("salary", "$100k+"), "#FEF3C7", "#D97706")
        ]
        
        for text, bg, color in tags:
            lbl = QLabel(text)
            lbl.setStyleSheet(f"""
                background-color: {bg};
                color: {color};
                padding: 4px 10px;
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
                border: none;
            """)
            tags_layout.addWidget(lbl)
            
        tags_layout.addStretch()
        self.main_layout.addLayout(tags_layout)
        
        # Spacing
        self.main_layout.addStretch()
        
        # --- Bottom Footer ---
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(10)
        
        time_lbl = QLabel(self.data.get('posted_time', 'Recently'))
        time_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; font-weight: 500; border: none; background: transparent;")
        footer_layout.addWidget(time_lbl)
        
        footer_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(64, 32)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; border: 1px solid #E2E8F0;
                border-radius: 10px; color: #64748B; font-size: 12px; font-weight: 600;
            }
            QPushButton:hover { background-color: #F8FAFC; border-color: #CBD5E1; color: #0F172A; }
        """)
        footer_layout.addWidget(save_btn)
        
        apply_btn = QPushButton("Apply")
        apply_btn.setFixedSize(80, 32)
        apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_btn.clicked.connect(lambda: self.apply_clicked.emit(self.data))
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0F172A; color: white; border-radius: 10px;
                font-size: 12px; font-weight: 700; border: none;
            }
            QPushButton:hover { background-color: #1E293B; }
        """)
        footer_layout.addWidget(apply_btn)
        
        self.main_layout.addLayout(footer_layout)

    def setup_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(15, 23, 42, 15))
        self.setGraphicsEffect(self.shadow)

    def set_selected(self, selected):
        self.selected = selected
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        
        if selected:
            self.shadow.setColor(QColor(56, 189, 248, 30))
        else:
            self.shadow.setColor(QColor(15, 23, 42, 15))

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)
