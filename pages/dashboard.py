import json
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QProgressBar, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor

from config import *
from components import SaaSCard, CountUpLabel, AnimatedProgressBar, StatusPulse, AnimationEngine
from i18n import _

# --- Hero Banner Component ---

class HeroBanner(SaaSCard):
    # PyQt6 update: Handled canvas drawing directly within QWidget via paintEvent
    def __init__(self, parent=None):
        super().__init__(parent)
        self.circles = []
        self.setStyleSheet(f"""
            HeroBanner {{
                background-color: {COLOR_PRIMARY_LIGHT};
                border: 1px solid {COLOR_BORDER};
                border-radius: 16px;
            }}
        """)

    def enterEvent(self, event): pass # UI Fix: Disable SaaSCard hover effect for HeroBanner

    def leaveEvent(self, event): pass # UI Fix: Disable SaaSCard hover effect for HeroBanner


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
        super().paintEvent(event) # Let QFrame draw the stylesheet background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(COLOR_PRIMARY))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for x, y, r in self.circles:
            painter.drawEllipse(x - r, y - r, r * 2, r * 2)

# --- Main Dashboard Page ---

class DashboardPage(QWidget):
    # PyQt6 update: Inheriting from QWidget
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.content_pad = 35

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # PyQt6 update: Using QScrollArea instead of CTkScrollableFrame
        self.scrollable = QScrollArea(self)
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollable.setStyleSheet("background: transparent;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(self.content_pad, self.content_pad, self.content_pad, self.content_pad)
        self.scroll_layout.setSpacing(15)

        self.scrollable.setWidget(self.scroll_content)
        main_layout.addWidget(self.scrollable)

        self._build_bento_grid()
        self._load_mock_data_async()

        from components import AnimationEngine
        AnimationEngine.fade_in_widget(self.hero_banner, delay_ms=200)

    def _build_bento_grid(self):
        self.hero_banner = HeroBanner(self)
        QWidget().setLayout(self.hero_banner.layout()) # Remove SaaSCard's default layout
        hero_layout = QHBoxLayout(self.hero_banner)
        hero_layout.setContentsMargins(40, 35, 40, 35)

        hero_text = QWidget()
        hero_text_layout = QVBoxLayout(hero_text)
        hero_text_layout.setContentsMargins(0, 0, 0, 0)
        hero_text_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # PyQt6 update: Enum usage

        status_frame = QWidget()
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.ai_pulse = StatusPulse(size=8)
        status_layout.addWidget(self.ai_pulse)

        lbl_ai = QLabel(_("dash_hero_activated"))
        lbl_ai.setStyleSheet(f"color: {COLOR_PRIMARY}; font-weight: bold; font-size: 11px;")
        status_layout.addWidget(lbl_ai)

        hero_text_layout.addWidget(status_frame)

        lbl_title = QLabel(_("dash_hero_title"))
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-weight: bold; font-size: 28px;")
        hero_text_layout.addWidget(lbl_title)

        btn_continue = QPushButton(_("dash_btn_continue"))
        # PyQt6 update: CSS styling for button instead of CTk attributes
        btn_continue.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY}; 
                color: white; 
                font-weight: bold; 
                border-radius: 6px; 
                padding: 10px;
            }}
        """)
        btn_continue.setCursor(Qt.CursorShape.PointingHandCursor)
        # PyQt6 update: Signal/Slot lambda
        btn_continue.clicked.connect(lambda: getattr(self, "controller", None) and self.controller.show_page("LearningPage"))
        hero_text_layout.addWidget(btn_continue)

        hero_layout.addWidget(hero_text)
        self.scroll_layout.addWidget(self.hero_banner)

        # Grid Layout for Bento
        self.grid_frame = QWidget()
        grid_layout = QGridLayout(self.grid_frame)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(10)
        self.scroll_layout.addWidget(self.grid_frame)

        self.stats = {}
        self.stats['progress'] = self._create_stat_card(grid_layout, 0, 0, _("dash_stat_progress"), suffix="%")
        self.stats['credits'] = self._create_stat_card(grid_layout, 0, 1, _("dash_stat_credits"), format_str="{}/120")
        self.stats['gpa'] = self._create_stat_card(grid_layout, 0, 2, _("dash_stat_gpa"), format_str="{}")

        self.left_col = SaaSCard()
        left_layout = self.left_col.internal_layout # UI Fix: Use pre-existing internal_layout
        grid_layout.addWidget(self.left_col, 1, 0, 1, 2)

        lbl_left = QLabel(_("dash_current_courses"))
        lbl_left.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(lbl_left)

        self.courses_container = QWidget()
        self.courses_layout = QVBoxLayout(self.courses_container)
        self.courses_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.courses_container)

        self.right_col = SaaSCard()
        right_layout = self.right_col.internal_layout # UI Fix: Use pre-existing internal_layout
        grid_layout.addWidget(self.right_col, 1, 2)

        lbl_right = QLabel(_("dash_events_deadlines"))
        lbl_right.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 16px; font-weight: bold;")
        right_layout.addWidget(lbl_right)

        self.events_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_container)
        self.events_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.events_container)

    def _create_stat_card(self, parent_layout, row, col, title, suffix="", format_str="{}"):
        card = SaaSCard()
        layout = card.internal_layout # UI Fix: Use pre-existing internal_layout

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 13px; font-weight: bold;")
        layout.addWidget(lbl_title)

        val_lbl = CountUpLabel(format_str=format_str, suffix=suffix)
        val_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 24px; font-weight: bold;")
        layout.addWidget(val_lbl)

        parent_layout.addWidget(card, row, col)
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
        # PyQt6 update: QTimer.singleShot instead of tkinter's after()
        QTimer.singleShot(800, fetch_data)

    def _add_course_item(self, parent_layout, title, status, color, progress, delay=0):
        frame = QWidget()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 5, 0, 5)

        title_btn = QPushButton(title)
        title_btn.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; text-align: left; font-size: 14px; font-weight: bold; background: transparent; border: none;")
        title_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        title_btn.clicked.connect(lambda: getattr(self, "controller", None) and self.controller.show_page("CourseDetailPage"))
        layout.addWidget(title_btn)

        lbl_status = QLabel(status)
        lbl_status.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
        layout.addWidget(lbl_status)

        bar = AnimatedProgressBar(color=color)
        bar.set_target(progress)
        layout.addWidget(bar)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background-color: {COLOR_BORDER};")
        layout.addWidget(line)

        parent_layout.addWidget(frame)

    def _add_event_item(self, parent_layout, date, title, time_str, delay=0):
        frame = QWidget()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 5, 0, 5)

        date_box = QFrame()
        date_box.setFixedSize(50, 50)
        date_box.setStyleSheet(f"background-color: {COLOR_PRIMARY_LIGHT}; border-radius: 6px;")
        date_layout = QVBoxLayout(date_box)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        parts = date.split()
        lbl_d1 = QLabel(parts[0])
        lbl_d1.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 15px; font-weight: bold;")
        date_layout.addWidget(lbl_d1, alignment=Qt.AlignmentFlag.AlignCenter)

        if len(parts) > 1:
            lbl_d2 = QLabel(parts[1])
            lbl_d2.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 11px;")
            date_layout.addWidget(lbl_d2, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(date_box)

        txt_box = QWidget()
        txt_layout = QVBoxLayout(txt_box)
        txt_layout.setContentsMargins(10, 0, 0, 0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold;")
        txt_layout.addWidget(lbl_title)

        lbl_time = QLabel(time_str)
        lbl_time.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
        txt_layout.addWidget(lbl_time)

        layout.addWidget(txt_box)
        parent_layout.addWidget(frame)

    # PyQt6 update: Helper method to clear items from layout dynamically
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

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