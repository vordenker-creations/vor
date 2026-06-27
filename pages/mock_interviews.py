from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from database import crud

class ClickableCard(QFrame):
    def __init__(self, title, desc, icon, color, on_click, parent=None):
        super().__init__(parent)
        self.setObjectName("ClickableCard")
        self.title = title
        self.on_click = on_click
        
        self.setStyleSheet("""
            #ClickableCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
            #ClickableCard:hover {
                border: 1px solid #CBD5E1;
                background-color: #F8FAFC;
            }
        """)
        
        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(15, 23, 42, 12))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)
        self.internal_layout.setSpacing(12)
        
        # Icon Label
        i_lbl = QLabel(icon)
        i_lbl.setStyleSheet(f"font-size: 32px; background: {color}15; padding: 12px; border-radius: 12px; border: none;")
        i_lbl.setFixedSize(56, 56)
        i_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title Label
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700; border: none; background: transparent;")
        
        # Description Label
        d_lbl = QLabel(desc)
        d_lbl.setStyleSheet("color: #64748B; font-size: 12px; border: none; background: transparent;")
        d_lbl.setWordWrap(True)
        
        self.internal_layout.addWidget(i_lbl)
        self.internal_layout.addWidget(t_lbl)
        self.internal_layout.addWidget(d_lbl)
        self.internal_layout.addStretch()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click(self.title)
        super().mousePressEvent(event)

class MockInterviewsPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header Bar
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        header_layout.setSpacing(16)
        
        title_lbl = QLabel("🎙 Mock Interviews")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        
        btn_practice = QPushButton("Start AI Voice Interview")
        btn_practice.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_practice.setStyleSheet("""
            QPushButton {
                background: #2563EB; color: white; font-weight: 700; font-size: 13px;
                border-radius: 18px; padding: 0 20px; height: 36px; border: none;
            }
            QPushButton:hover { background: #1D4ED8; }
        """)
        btn_practice.clicked.connect(lambda: self._start_interview_flow("Technical: System Design"))
        header_layout.addWidget(btn_practice)
        
        main_layout.addWidget(header)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        # Select category header
        cat_title = QLabel("Select Interview Type")
        cat_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        content_layout.addWidget(cat_title)
        
        # Grid of Cards
        grid = QGridLayout()
        grid.setSpacing(16)
        
        types = [
            ("Technical: System Design", "Architect scalable systems. Real-world constraints.", "🏗", "#3B82F6"),
            ("Behavioral & Soft Skills", "STAR method, cultural fit, leadership.", "🤝", "#10B981"),
            ("Frontend Engineering", "React, DOM, Web Performance, CSS.", "🎨", "#F59E0B"),
            ("Backend Engineering", "Databases, API design, concurrency.", "⚙", "#6366F1")
        ]
        
        row, col = 0, 0
        for title, desc, icon, color in types:
            card = ClickableCard(title, desc, icon, color, on_click=self._start_interview_flow, parent=self)
            grid.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        content_layout.addLayout(grid)
        
        # Past Performance
        past_title = QLabel("Recent Interview Feedback")
        past_title.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; margin-top: 10px;")
        content_layout.addWidget(past_title)
        
        # Feedback Container
        self.feedback_widget = QWidget()
        self.feedback_lay = QVBoxLayout(self.feedback_widget)
        self.feedback_lay.setContentsMargins(0, 0, 0, 0)
        self.feedback_lay.setSpacing(12)
        content_layout.addWidget(self.feedback_widget)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Initial Refresh
        self.refresh()

    def _start_interview_flow(self, category):
        student = crud.get_current_student()
        if not student:
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập hệ thống để thực hiện phỏng vấn.")
            return
            
        from pages.mock_interview_dialog import MockInterviewDialog
        dialog = MockInterviewDialog(category, student["id"], self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def refresh(self):
        # Clear feedback layout
        while self.feedback_lay.count():
            item = self.feedback_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        student = crud.get_current_student()
        if not student:
            lbl_empty = QLabel("Vui lòng đăng nhập để xem lịch sử phỏng vấn.")
            lbl_empty.setStyleSheet("color: #64748B; font-size: 13px; font-style: italic;")
            self.feedback_lay.addWidget(lbl_empty)
            return
            
        interviews = crud.get_mock_interviews(student["id"])
        if not interviews:
            lbl_empty = QLabel("Chưa thực hiện cuộc phỏng vấn nào. Hãy chọn một chủ đề phía trên để bắt đầu thử sức!")
            lbl_empty.setStyleSheet("color: #64748B; font-size: 13px; font-style: italic; border: none; background: transparent;")
            self.feedback_lay.addWidget(lbl_empty)
            return
            
        for item in interviews:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 16px;
                }
            """)
            shadow = QGraphicsDropShadowEffect(card)
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(15, 23, 42, 8))
            shadow.setOffset(0, 3)
            card.setGraphicsEffect(shadow)
            
            lay = QVBoxLayout(card)
            lay.setContentsMargins(18, 18, 18, 18)
            lay.setSpacing(10)
            
            row1 = QHBoxLayout()
            title_lbl = QLabel(f"🎙️ {item['category']}")
            title_lbl.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: bold; border: none; background: transparent;")
            
            score_lbl = QLabel(f"Điểm: {item['score']:.1f} / 10")
            score_lbl.setStyleSheet("color: #10B981; font-weight: 800; font-size: 12px; background: #D1FAE5; padding: 4px 10px; border-radius: 8px; border: none;")
            
            row1.addWidget(title_lbl)
            row1.addStretch()
            row1.addWidget(score_lbl)
            lay.addLayout(row1)
            
            date_lbl = QLabel(f"Ngày thực hiện: {item['date_str']}")
            date_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 600; border: none; background: transparent;")
            lay.addWidget(date_lbl)
            
            # Line separator
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet("background-color: #F1F5F9; max-height: 1px; border: none;")
            lay.addWidget(line)
            
            feedback_lbl = QLabel(item['feedback'])
            feedback_lbl.setWordWrap(True)
            feedback_lbl.setStyleSheet("color: #475569; font-size: 12px; line-height: 1.5; border: none; background: transparent;")
            lay.addWidget(feedback_lbl)
            
            self.feedback_lay.addWidget(card)
