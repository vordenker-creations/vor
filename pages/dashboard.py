import json
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QProgressBar, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor

from config import *
from components import SaaSCard, CountUpLabel, AnimatedProgressBar, StatusPulse, AnimationEngine
from i18n import _

# --- Hero Banner Component ---

class HeroBanner(SaaSCard):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.circles = []
        self.setStyleSheet(f"""
            HeroBanner {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0f2fe, stop:1 #bae6fd);
                border: 1px solid #bae6fd;
                border-radius: 20px;
            }}
        """)
        # Set fixed vertical size policy for banner
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event): pass
    def leaveEvent(self, event): pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._generate_circles()

    def _generate_circles(self):
        self.circles = []
        w = self.width()
        h = self.height()
        if w < 10: return
        for _ in range(8):
            x, y = random.randint(0, w), random.randint(0, h)
            r = random.randint(20, 60)
            self.circles.append((x, y, r))
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(255, 255, 255, 150))
        painter.setBrush(QColor(255, 255, 255, 60))
        for x, y, r in self.circles:
            painter.drawEllipse(x - r, y - r, r * 2, r * 2)

# --- Main Dashboard Page ---

class DashboardPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.content_pad = 25 # Reduced padding

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(self.content_pad, self.content_pad, self.content_pad, self.content_pad)
        self.main_layout.setSpacing(15) # Optimized spacing

        self._build_bento_grid()
        self._load_mock_data_async()

        AnimationEngine.fade_in_widget(self.hero_banner, delay_ms=200)

    def _build_bento_grid(self):
        # 1. Hero Banner (Fixed Height & Content Restoration)
        self.hero_banner = HeroBanner(self)
        self.hero_banner.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.hero_banner.setFixedHeight(160) # Strictly force compact height
        self.hero_banner.clicked.connect(lambda: getattr(self, "controller", None) and self.controller.show_page("LearningPage"))
        
        # Use existing internal_layout
        self.hero_banner.internal_layout.setContentsMargins(35, 20, 35, 20)
        self.hero_banner.internal_layout.setSpacing(5)

        # Label 1: Status Tag
        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        status_layout.setSpacing(8)
        
        self.ai_pulse = StatusPulse(size=10, color=COLOR_PRIMARY)
        status_layout.addWidget(self.ai_pulse)

        lbl_status = QLabel("● HỆ THỐNG AI MENTOR ĐÃ KÍCH HOẠT")
        lbl_status.setStyleSheet(f"color: {COLOR_PRIMARY}; font-weight: 800; font-size: 11px; letter-spacing: 1.2px;")
        status_layout.addWidget(lbl_status)
        self.hero_banner.internal_layout.addLayout(status_layout)

        # Label 2 & 3: Main Titles
        lbl_title1 = QLabel("Tối ưu hóa Lộ trình Học tập")
        lbl_title1.setStyleSheet("color: #1E293B; font-weight: 900; font-size: 26px; letter-spacing: -0.5px;")
        self.hero_banner.internal_layout.addWidget(lbl_title1)

        lbl_title2 = QLabel("Kiến tạo Tương lai Kỹ sư.")
        lbl_title2.setStyleSheet("color: #1E293B; font-weight: 900; font-size: 26px; letter-spacing: -0.5px;")
        self.hero_banner.internal_layout.addWidget(lbl_title2)

        self.main_layout.addWidget(self.hero_banner)

        # 2. Stat Cards (Fixed Height Row)
        self.stats_row = QWidget()
        self.stats_row.setFixedHeight(120)
        self.stats_row.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        stats_layout = QHBoxLayout(self.stats_row)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(20)

        self.stats = {}
        self.stats['progress'] = self._create_stat_card(stats_layout, "Tiến độ Học kỳ", suffix="%")
        self.stats['credits'] = self._create_stat_card(stats_layout, "Tín chỉ Tích lũy", format_str="{}/120")
        self.stats['gpa'] = self._create_stat_card(stats_layout, "Điểm GPA Hệ 4", format_str="{}")
        
        self.main_layout.addWidget(self.stats_row)

        # 3. Bottom Section (Expanding)
        self.bottom_section = QWidget()
        self.bottom_section.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        bottom_layout = QHBoxLayout(self.bottom_section)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(20)

        # Left Column: Courses
        self.left_col = SaaSCard()
        self.left_col.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        left_content_layout = self.left_col.internal_layout
        
        lbl_left = QLabel("Học phần đang diễn ra")
        lbl_left.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: 800;")
        left_content_layout.addWidget(lbl_left)

        self.courses_container = QWidget()
        self.courses_layout = QVBoxLayout(self.courses_container)
        self.courses_layout.setContentsMargins(0, 10, 0, 0)
        self.courses_layout.setSpacing(15)
        left_content_layout.addWidget(self.courses_container)
        left_content_layout.addStretch() 

        bottom_layout.addWidget(self.left_col, 3) 

        # Right Column: Events
        self.right_col = SaaSCard()
        self.right_col.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_content_layout = self.right_col.internal_layout
        
        lbl_right = QLabel("Sự kiện & Deadline")
        lbl_right.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 18px; font-weight: 800;")
        right_content_layout.addWidget(lbl_right)

        self.events_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_container)
        self.events_layout.setContentsMargins(0, 10, 0, 0)
        self.events_layout.setSpacing(15)
        right_content_layout.addWidget(self.events_container)
        right_content_layout.addStretch() 

        bottom_layout.addWidget(self.right_col, 2)

        self.main_layout.addWidget(self.bottom_section)
        
        # CRITICAL: Set stretch factor so bottom section takes all remaining space
        self.main_layout.setStretchFactor(self.hero_banner, 0)
        self.main_layout.setStretchFactor(self.stats_row, 0)
        self.main_layout.setStretchFactor(self.bottom_section, 1)

    def _create_stat_card(self, parent_layout, title, suffix="", format_str="{}"):
        card = SaaSCard()
        card.setFixedHeight(100)
        layout = card.internal_layout

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 13px; font-weight: bold;")
        layout.addWidget(lbl_title)

        val_lbl = CountUpLabel(format_str=format_str, suffix=suffix)
        val_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold;")
        layout.addWidget(val_lbl)

        parent_layout.addWidget(card)
        return val_lbl

    def _load_mock_data_async(self):
        def fetch_data():
            mock_payload = {
                "stats": {"progress": "65", "credits": "84", "gpa": "3.8"},
                "courses": [
                    {"title": "Lập trình Python Nâng cao", "status": "Tiến độ: 80%", "color": COLOR_PRIMARY, "progress": 0.8},
                    {"title": "Toán rời rạc & Thuật toán", "status": "Tiến độ: 45%", "color": "#F59E0B", "progress": 0.45},
                    {"title": "Kỹ năng Giao tiếp Tiếng Anh", "status": "Tiến độ: 15%", "color": "#10B981", "progress": 0.15}
                ],
                "events": [
                    {"date": "12 Th4", "title": "Workshop Trí tuệ Nhân tạo", "time": "08:00 Sáng - Online"},
                    {"date": "15 Th4", "title": "Nộp Đồ án Cơ sở 2", "time": "14:00 Chiều - Hệ thống"}
                ]
            }
            self.update_data(mock_payload)
        QTimer.singleShot(500, fetch_data)

    def _add_course_item(self, parent_layout, title, status, color, progress, delay=0):
        frame = QWidget()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(2)

        title_btn = QPushButton(title)
        title_btn.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; text-align: left; font-size: 13px; font-weight: bold; background: transparent; border: none;")
        title_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        title_btn.clicked.connect(lambda: getattr(self, "controller", None) and self.controller.show_page("CourseDetailPage"))
        layout.addWidget(title_btn)

        lbl_status = QLabel(status)
        lbl_status.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 11px;")
        layout.addWidget(lbl_status)

        bar = AnimatedProgressBar(color=color)
        bar.setFixedHeight(8)
        bar.set_target(progress)
        layout.addWidget(bar)

        parent_layout.addWidget(frame)

    def _add_event_item(self, parent_layout, date, title, time_str, delay=0):
        frame = QWidget()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 2, 0, 2)

        date_box = QFrame()
        date_box.setFixedSize(45, 45)
        date_box.setStyleSheet(f"background-color: #e0f2fe; border-radius: 10px;")
        date_layout = QVBoxLayout(date_box)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(0)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        parts = date.split()
        lbl_d1 = QLabel(parts[0])
        lbl_d1.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 13px; font-weight: bold;")
        date_layout.addWidget(lbl_d1, alignment=Qt.AlignmentFlag.AlignCenter)

        if len(parts) > 1:
            lbl_d2 = QLabel(parts[1])
            lbl_d2.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 10px;")
            date_layout.addWidget(lbl_d2, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(date_box)

        txt_box = QWidget()
        txt_layout = QVBoxLayout(txt_box)
        txt_layout.setContentsMargins(8, 0, 0, 0)
        txt_layout.setSpacing(2)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 13px; font-weight: bold;")
        txt_layout.addWidget(lbl_title)

        lbl_time = QLabel(time_str)
        lbl_time.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 11px;")
        txt_layout.addWidget(lbl_time)

        layout.addWidget(txt_box)
        parent_layout.addWidget(frame)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_data(self, json_payload):
        try:
            data = json.loads(json_payload) if isinstance(json_payload, str) else json_payload

            if "stats" in data:
                self.stats['progress'].set_target(data["stats"].get("progress", "0"))
                self.stats['credits'].set_target(data["stats"].get("credits", "0"))
                self.stats['gpa'].set_target(float(data["stats"].get("gpa", "0.0")))

            if "courses" in data:
                self.clear_layout(self.courses_layout)
                for i, course in enumerate(data["courses"]):
                    self._add_course_item(self.courses_layout, course["title"], course["status"], 
                                          course.get("color", COLOR_PRIMARY), course["progress"], delay=i*100)

            if "events" in data:
                self.clear_layout(self.events_layout)
                for i, event in enumerate(data["events"]):
                    self._add_event_item(self.events_layout, event["date"], event["title"], event["time"], delay=i*100)

        except Exception as e: 
            print(f"Lỗi update_data: {e}")

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    page = DashboardPage()
    page.resize(1100, 800)
    page.show()
    sys.exit(app.exec())
