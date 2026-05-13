import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from style_utils import (GLOBAL_BG, apply_neumorphic_outer_shadow, 
                         create_neumorphic_input, create_glowing_button)

class LoginPage(QWidget):
    def __init__(self, on_login=None, on_register_click=None):
        super().__init__()
        self.on_login_callback = on_login
        self.on_register_click_callback = on_register_click
        
        self.setWindowTitle("AI Career Bridge - Login")
        self.setStyleSheet(f"background-color: {GLOBAL_BG}; font-family: 'Segoe UI', sans-serif;")
        self.resize(1100, 800)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(60, 60, 60, 60)
        main_layout.setSpacing(60)
        
        # ==========================================
        # LEFT WIDGET: Feature Overview
        # ==========================================
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Title with Badge
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        badge_lbl = QLabel("AI")
        badge_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_lbl.setFixedSize(50, 50)
        badge_lbl.setStyleSheet("color: #6366f1; font-size: 20px; font-weight: 900; background: transparent;")
        badge_container = apply_neumorphic_outer_shadow(badge_lbl, radius=15, offset=5, blur=15)
        title_layout.addWidget(badge_container)
        
        title_text = QLabel("AI INSIGHT")
        title_text.setStyleSheet("color: darkslategray; font-size: 38px; font-weight: 900;")
        title_layout.addWidget(title_text)
        
        left_layout.addLayout(title_layout)
        left_layout.addSpacing(15)
        
        # Subtitle
        subtitle = QLabel("Elevate your career with AI-driven analytics and personal roadmaps")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #64748b; font-size: 18px; font-weight: 500;")
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(40)
        
        # Feature Pills
        features = [
            ("🐍", "Python"),
            ("🧠", "Neural Networks"),
            ("🗣️", "NLP"),
            ("👁️", "Computer Vision"),
            ("📊", "Data Science"),
            ("☁️", "Cloud AI")
        ]
        
        for icon, text in features:
            pill_btn = QPushButton(f"{icon}   {text}")
            pill_btn.setFixedHeight(55)
            pill_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            pill_btn.setStyleSheet("color: #334155; font-weight: 700; font-size: 15px; text-align: left; padding-left: 20px;")
            shadowed_pill = apply_neumorphic_outer_shadow(pill_btn, radius=27, offset=6, blur=15)
            left_layout.addWidget(shadowed_pill)
        
        main_layout.addWidget(left_widget, 1)

        # ==========================================
        # RIGHT WIDGET: Login Form Card
        # ==========================================
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        form_content = QWidget()
        form_inner = QVBoxLayout(form_content)
        form_inner.setContentsMargins(40, 50, 40, 50)
        form_inner.setSpacing(25)
        
        welcome_title = QLabel("Welcome Back")
        welcome_title.setStyleSheet("font-size: 32px; font-weight: 800; color: #1e293b;")
        welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_inner.addWidget(welcome_title)
        
        # Inputs
        self.email_input = create_neumorphic_input("Email Address", "📧")
        self.password_input = create_neumorphic_input("Password", "🔒", is_password=True)
        
        self.email_entry = self.email_input
        self.password_entry = self.password_input
        
        form_inner.addWidget(self.email_input)
        form_inner.addWidget(self.password_input)
        
        # Forgot Password
        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forgot_btn.setStyleSheet("""
            QPushButton { color: #1E5F74; font-weight: 600; font-size: 13px; border: none; background: transparent; }
            QPushButton:hover { color: #25758f; text-decoration: underline; }
        """)
        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        forgot_layout.addWidget(forgot_btn)
        form_inner.addLayout(forgot_layout)
        
        # Sign In CTA
        self.login_btn = create_glowing_button("SIGN IN", height=50)
        self.login_btn.btn.clicked.connect(self._handle_login)
        form_inner.addWidget(self.login_btn)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_text = QLabel("Don't have an account?")
        footer_text.setStyleSheet("color: #64748b; font-size: 14px; font-weight: 500;")
        
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.setStyleSheet("""
            QPushButton { color: #1E5F74; font-weight: 800; font-size: 14px; border: none; background: transparent; }
            QPushButton:hover { color: #25758f; text-decoration: underline; }
        """)
        self.register_btn.clicked.connect(self._handle_register_click)
        
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(self.register_btn)
        form_inner.addLayout(footer_layout)
        
        # Apply Main Card Shadow
        shadowed_card = apply_neumorphic_outer_shadow(form_content, radius=35, offset=12, blur=30)
        right_layout.addWidget(shadowed_card)
        
        main_layout.addWidget(right_widget, 1)

    def _handle_login(self):
        email = self.email_entry.text()
        password = self.password_entry.text()
        if self.on_login_callback:
            self.on_login_callback(email, password)

    def _handle_register_click(self):
        if self.on_register_click_callback:
            self.on_register_click_callback()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())
