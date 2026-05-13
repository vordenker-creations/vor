import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                             QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from neumorphic_components import NeumorphicFrame, NeumorphicInput, GlowingButton, NeumorphicButton
from database import crud

class RegisterPage(QWidget):
    def __init__(self, parent=None, on_back_click=None, on_register=None):
        super().__init__(parent)
        self.on_back_click = on_back_click
        self.on_register = on_register
        
        self.setWindowTitle("AI INSIGHT - Đăng ký")
        self.setStyleSheet("background-color: #F0F2F5; font-family: 'Segoe UI', sans-serif;")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(60)
        
        # ==========================================
        # LEFT COLUMN: Branding & Features
        # ==========================================
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Brand Title with Badge (Properly spaced layout)
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(15)
        brand_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        ai_badge = NeumorphicFrame(radius=15, offset=5, blur=12)
        ai_badge.setFixedSize(65, 65) # Icon remains fixed for design consistency
        ai_label = QLabel("AI")
        ai_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ai_label.setStyleSheet("color: #6366f1; font-size: 22px; font-weight: 900;")
        ai_badge.add_widget(ai_label)
        
        brand_title = QLabel("AI INSIGHT")
        brand_title.setStyleSheet("color: #1e293b; font-size: 42px; font-weight: 900; letter-spacing: -1px;")
        
        brand_layout.addWidget(ai_badge)
        brand_layout.addWidget(brand_title)
        left_layout.addLayout(brand_layout)
        
        subtitle = QLabel("Nâng tầm sự nghiệp với trí tuệ nhân tạo và lộ trình cá nhân hóa.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #64748b; font-size: 18px; font-weight: 500; margin-top: 10px;")
        left_layout.addWidget(subtitle)
        
        left_layout.addSpacing(40)
        
        features = [
            ("🐍", "Lập trình Python"), ("🧠", "Mạng nơ-ron"), ("🗣️", "Xử lý ngôn ngữ"),
            ("👁️", "Thị giác máy tính"), ("📊", "Khoa học dữ liệu"), ("☁️", "Điện toán đám mây")
        ]
        for icon, text in features:
            pill = NeumorphicButton(f"{icon}   {text}")
            pill.setFixedHeight(55)
            left_layout.addWidget(pill)
            
        main_layout.addWidget(left_column, 4)
        
        # ==========================================
        # RIGHT COLUMN: The Vietnamese Register Form
        # ==========================================
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.main_card = NeumorphicFrame(radius=35, offset=12, blur=30)
        right_layout.addWidget(self.main_card)
        
        # --- HEADER ---
        header_layout = QVBoxLayout()
        
        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)
        check_lbl = QLabel("✔")
        check_lbl.setStyleSheet("color: #22c55e; font-weight: bold; font-size: 16px;")
        status_text = QLabel("HỆ THỐNG AI MENTOR ĐÃ KÍCH HOẠT")
        status_text.setStyleSheet("color: #94a3b8; font-weight: 800; font-size: 12px; letter-spacing: 1px;")
        status_layout.addWidget(check_lbl)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        header_layout.addLayout(status_layout)
        
        form_title = QLabel("Đăng ký Tài khoản.")
        form_title.setStyleSheet("color: #1e293b; font-size: 34px; font-weight: 900; margin-top: 5px;")
        header_layout.addWidget(form_title)
        
        sub_nav = QLabel("TỔNG QUAN  |  PHÂN TÍCH CV  |  TẠO CV  |  Tiếp tục Học tập")
        sub_nav.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        header_layout.addWidget(sub_nav)
        
        self.main_card.add_layout(header_layout)
        
        # --- SECTION 1: Thông tin tài khoản (2x2 Grid) ---
        sec1_container = NeumorphicFrame(radius=20, offset=6, blur=15)
        sec1_layout = QVBoxLayout()
        sec1_lbl = QLabel("THÔNG TIN TÀI KHOẢN")
        sec1_lbl.setStyleSheet("color: #1e293b; font-size: 11px; font-weight: 800; margin-bottom: 5px;")
        sec1_layout.addWidget(sec1_lbl)
        
        grid1 = QGridLayout()
        grid1.setSpacing(15)
        
        self.fullname_input = NeumorphicInput("Họ và Tên", "👤")
        self.username_input = NeumorphicInput("Tên đăng nhập", "📧")
        self.password_input = NeumorphicInput("Mật khẩu", "🔒", is_password=True)
        self.confirm_input = NeumorphicInput("Xác nhận Mật khẩu", "🔒", is_password=True)
        
        grid1.addWidget(self.fullname_input, 0, 0)
        grid1.addWidget(self.username_input, 0, 1)
        grid1.addWidget(self.password_input, 1, 0)
        grid1.addWidget(self.confirm_input, 1, 1)
        
        sec1_layout.addLayout(grid1)
        sec1_container.content_layout.addLayout(sec1_layout)
        self.main_card.add_widget(sec1_container)
        
        # --- SECTION 2: Hồ sơ cá nhân (3x2 Grid) ---
        sec2_container = NeumorphicFrame(radius=20, offset=6, blur=15)
        sec2_layout = QVBoxLayout()
        sec2_lbl = QLabel("HỒ SƠ CÁ NHÂN")
        sec2_lbl.setStyleSheet("color: #1e293b; font-size: 11px; font-weight: 800; margin-bottom: 5px;")
        sec2_layout.addWidget(sec2_lbl)
        
        grid2 = QGridLayout()
        grid2.setSpacing(15)
        
        self.birth_input = NeumorphicInput("Ngày sinh", "📅")
        self.nation_input = NeumorphicInput("Quốc tịch", "🌍")
        self.edu_input = NeumorphicInput("Học vấn", "🎓")
        self.major_input = NeumorphicInput("Ngành nghề", "💼")
        self.rank_input = NeumorphicInput("Hạng", "🏅")
        self.job_input = NeumorphicInput("Công việc", "⚙")
        
        grid2.addWidget(self.birth_input, 0, 0)
        grid2.addWidget(self.nation_input, 0, 1)
        grid2.addWidget(self.edu_input, 0, 2)
        grid2.addWidget(self.major_input, 1, 0)
        grid2.addWidget(self.rank_input, 1, 1)
        grid2.addWidget(self.job_input, 1, 2)
        
        sec2_layout.addLayout(grid2)
        sec2_container.content_layout.addLayout(sec2_layout)
        self.main_card.add_widget(sec2_container)
        
        # --- SUBMIT BUTTON ---
        submit_layout = QHBoxLayout()
        self.submit_btn = GlowingButton("ĐĂNG KÝ TÀI KHOẢN")
        self.submit_btn.clicked.connect(self._handle_register)
        submit_layout.addStretch()
        submit_layout.addWidget(self.submit_btn)
        submit_layout.addStretch()
        self.main_card.add_layout(submit_layout)
        
        # --- FOOTER ---
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_text = QLabel("Đã có tài khoản?")
        footer_text.setStyleSheet("color: #64748b; font-size: 14px; font-weight: 500;")
        
        self.back_btn = QPushButton("Đăng nhập ngay.")
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton { color: #1E5F74; font-weight: 800; font-size: 14px; border: none; background: transparent; }
            QPushButton:hover { text-decoration: underline; }
        """)
        self.back_btn.clicked.connect(self.on_back_click if self.on_back_click else lambda: None)
        
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(self.back_btn)
        self.main_card.add_layout(footer_layout)
        
        main_layout.addWidget(right_column, 6)

    def _handle_register(self):
        email = self.username_input.text()
        fullname = self.fullname_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not email or not fullname or not password:
            print("Vui lòng điền đầy đủ thông tin.")
            return
        if password != confirm:
            print("Mật khẩu không khớp.")
            return
            
        print(f"Đang đăng ký: {fullname} ({email})")
        try:
            crud.save_student_profile(email, fullname, self.major_input.text())
            if self.on_register:
                self.on_register(email, password)
        except Exception as e:
            print(f"Lỗi đăng ký: {e}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = QWidget()
    win_layout = QVBoxLayout(window)
    reg = RegisterPage()
    win_layout.addWidget(reg)
    window.resize(1300, 900)
    window.show()
    sys.exit(app.exec())
