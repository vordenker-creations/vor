import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                             QPushButton, QFrame, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QPixmap
from neumorphic_components import NeumorphicFrame, NeumorphicInput, GlowingButton, NeumorphicButton
from database import crud

class RegisterNeumorphicPage(QWidget):
    def __init__(self, parent=None, on_back_click=None, on_register=None):
        super().__init__(parent)
        self.on_back_click = on_back_click
        self.on_register = on_register
        
        self.setWindowTitle("AI INSIGHT - Đăng ký Neumorphic")
        self.setStyleSheet("background-color: #F0F2F5; font-family: 'Segoe UI', sans-serif;")
        
        # Main Layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Left Panel (Decorative/Branding)
        self._setup_left_panel()
        
        # Right Panel (Form)
        self._setup_right_panel()

    def _setup_left_panel(self):
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #F0F2F5;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(60, 60, 60, 60)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Branding
        brand_container = NeumorphicFrame(radius=20, offset=6, blur=15)
        brand_container.setFixedSize(80, 80)
        brand_label = QLabel("AI")
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_label.setStyleSheet("color: #1E5F74; font-size: 28px; font-weight: 900;")
        brand_container.add_widget(brand_label)
        left_layout.addWidget(brand_container)
        
        left_layout.addSpacing(20)
        
        title = QLabel("AI INSIGHT")
        title.setStyleSheet("color: #1e293b; font-size: 48px; font-weight: 900; letter-spacing: -2px;")
        left_layout.addWidget(title)
        
        subtitle = QLabel("Hệ thống đào tạo nhân lực AI toàn diện.")
        subtitle.setStyleSheet("color: #64748b; font-size: 20px; font-weight: 500;")
        left_layout.addWidget(subtitle)
        
        left_layout.addSpacing(40)
        
        # Decorative Elements (Feature Pills)
        features = [
            ("🚀", "Lộ trình cá nhân hóa"),
            ("🤖", "AI Mentor 24/7"),
            ("📈", "Phân tích kỹ năng"),
            ("💼", "Kết nối việc làm")
        ]
        
        for icon, text in features:
            pill = NeumorphicButton(f"{icon}  {text}")
            pill.setFixedHeight(50)
            pill.setFixedWidth(280)
            left_layout.addWidget(pill)
            
        left_layout.addStretch()
        
        self.main_layout.addWidget(left_panel, 4)

    def _setup_right_panel(self):
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Registration Card
        self.card = NeumorphicFrame(radius=40, offset=15, blur=35)
        self.card.setFixedWidth(550)
        
        # Card Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(25)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        welcome_label = QLabel("Tạo tài khoản")
        welcome_label.setStyleSheet("color: #1e293b; font-size: 32px; font-weight: 900;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        desc_label = QLabel("Bắt đầu hành trình chinh phục AI ngay hôm nay")
        desc_label.setStyleSheet("color: #64748b; font-size: 14px; font-weight: 500;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(welcome_label)
        header_layout.addWidget(desc_label)
        content_layout.addLayout(header_layout)
        
        # Form Fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)
        
        self.fullname_input = NeumorphicInput("Họ và Tên", "👤")
        self.email_input = NeumorphicInput("Email / Tên đăng nhập", "📧")
        self.major_input = NeumorphicInput("Ngành học / Nghề nghiệp", "💼")
        self.password_input = NeumorphicInput("Mật khẩu", "🔒", is_password=True)
        self.confirm_input = NeumorphicInput("Xác nhận mật khẩu", "🔒", is_password=True)
        
        form_layout.addWidget(self.fullname_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.major_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_input)
        
        content_layout.addLayout(form_layout)
        
        # Register Button
        self.register_btn = GlowingButton("ĐĂNG KÝ NGAY")
        self.register_btn.setFixedHeight(55)
        self.register_btn.clicked.connect(self._handle_register)
        content_layout.addWidget(self.register_btn)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        login_text = QLabel("Đã có tài khoản?")
        login_text.setStyleSheet("color: #64748b; font-size: 14px;")
        
        self.login_link = QPushButton("Đăng nhập")
        self.login_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_link.setStyleSheet("""
            QPushButton {
                color: #1E5F74;
                font-weight: 800;
                font-size: 14px;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #25758f;
            }
        """)
        self.login_link.clicked.connect(self.on_back_click if self.on_back_click else lambda: None)
        
        footer_layout.addWidget(login_text)
        footer_layout.addWidget(self.login_link)
        content_layout.addLayout(footer_layout)
        
        self.card.add_layout(content_layout)
        right_layout.addWidget(self.card)
        
        self.main_layout.addWidget(right_panel, 6)

    def _handle_register(self):
        fullname = self.fullname_input.text()
        email = self.email_input.text()
        major = self.major_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not all([fullname, email, major, password, confirm]):
            print("Vui lòng điền đầy đủ thông tin.")
            return
            
        if password != confirm:
            print("Mật khẩu không khớp.")
            return
            
        print(f"Đang đăng ký: {fullname} ({email})")
        
        try:
            crud.save_student_profile(email, fullname, major)
            if self.on_register:
                self.on_register(email, password)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = RegisterNeumorphicPage()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
