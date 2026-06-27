import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSpacerItem, QSizePolicy, QLineEdit,
                             QCheckBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt6.QtGui import QColor, QFont, QCursor, QIcon, QPainter, QBrush, QPen

# Typography and Colors
FONT_FAMILY = "Segoe UI Variable Display" if sys.platform == "win32" else "Inter"
COLOR_BG = "#F8FAFC"
COLOR_CARD_BG = "#FFFFFF"
COLOR_PRIMARY = "#38BDF8"
COLOR_SECONDARY = "#2DD4BF"
COLOR_TEXT_PRIMARY = "#0F172A"
COLOR_TEXT_SECONDARY = "#64748B"
COLOR_BORDER = "#E2E8F0"


class FeatureCard(QFrame):
    def __init__(self, title, desc, icon, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            FeatureCard {{
                background-color: {COLOR_CARD_BG};
                border: 1px solid #E5E7EB;
                border-radius: 20px;
            }}
            FeatureCard:hover {{
                border: 1px solid {COLOR_PRIMARY};
                background-color: #F0F9FF;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # Icon
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 24px; color: {COLOR_PRIMARY}; background: transparent; border: none;")
        layout.addWidget(icon_lbl)

        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 15px; font-weight: 700; background: transparent; border: none;")
        text_layout.addWidget(t_lbl)

        d_lbl = QLabel(desc)
        d_lbl.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px; font-weight: 500; background: transparent; border: none;")
        text_layout.addWidget(d_lbl)

        layout.addLayout(text_layout)
        layout.addStretch()


class ModernInput(QWidget):
    def __init__(self, label, placeholder, icon="", is_password=False, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 13px; font-weight: 600;")
        layout.addWidget(lbl)

        self.input_container = QFrame()
        self.input_container.setFixedHeight(44)
        self.input_container.setStyleSheet(f"""
            QFrame {{
                background-color: #F8FAFC;
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
        """)

        cont_layout = QHBoxLayout(self.input_container)
        cont_layout.setContentsMargins(12, 0, 12, 0)
        cont_layout.setSpacing(10)

        if icon:
            i_lbl = QLabel(icon)
            i_lbl.setStyleSheet(
                f"color: {COLOR_TEXT_SECONDARY}; font-size: 16px; border: none; background: transparent;")
            cont_layout.addWidget(i_lbl)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        if is_password:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.line_edit.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {COLOR_TEXT_PRIMARY};
                font-size: 14px;
            }}
        """)

        # Focus events for container styling
        self.line_edit.focusInEvent = self._on_focus_in
        self.line_edit.focusOutEvent = self._on_focus_out

        cont_layout.addWidget(self.line_edit)

        if is_password:
            self.toggle_btn = QPushButton("👁")
            self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.toggle_btn.setStyleSheet(
                f"color: {COLOR_TEXT_SECONDARY}; font-size: 16px; border: none; background: transparent;")
            self.toggle_btn.clicked.connect(self._toggle_password)
            cont_layout.addWidget(self.toggle_btn)

        layout.addWidget(self.input_container)

    def _on_focus_in(self, event):
        self.input_container.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_PRIMARY};
                border-radius: 8px;
            }}
        """)
        QLineEdit.focusInEvent(self.line_edit, event)

    def _on_focus_out(self, event):
        self.input_container.setStyleSheet(f"""
            QFrame {{
                background-color: #F8FAFC;
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
        """)
        QLineEdit.focusOutEvent(self.line_edit, event)

    def _toggle_password(self):
        if self.line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("🔒")
        else:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("👁")

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)


class SocialButton(QPushButton):
    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        i_lbl = QLabel(icon)
        i_lbl.setStyleSheet("font-size: 16px; background: transparent; border: none;")
        t_lbl = QLabel(text)
        t_lbl.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 14px; font-weight: 600; background: transparent; border: none;")

        layout.addWidget(i_lbl)
        layout.addWidget(t_lbl)

        self.setStyleSheet(f"""
            SocialButton {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
            }}
            SocialButton:hover {{
                background-color: #F1F5F9;
                border-color: #CBD5E1;
            }}
        """)


class LoginPage(QWidget):
    def __init__(self, on_login=None, on_register_click=None):
        super().__init__()
        self.on_login_callback = on_login
        self.on_register_click_callback = on_register_click

        self.setWindowTitle("AI Career Bridge - Sign In")
        self.setStyleSheet(f"background-color: {COLOR_BG}; font-family: '{FONT_FAMILY}', sans-serif;")

        # --- 1. Master Wrapper Layout ---
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # --- 2. Scroll Area Setup ---
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # --- 3. Content Container Setup ---
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background: transparent;")
        # Enforce minimum size to prevent layout crushing before scrollbar triggers
        self.content_container.setMinimumSize(1000, 750)

        # --- 4. Main App Layout (Now attached to content_container) ---
        main_layout = QHBoxLayout(self.content_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==========================================
        # LEFT COLUMN (40%): Branding & Onboarding
        # ==========================================
        left_widget = QWidget()
        left_widget.setStyleSheet(f"background-color: {COLOR_BG};")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(60, 60, 40, 40)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Logo Area
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_icon = QLabel("✧")
        logo_icon.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 28px;")
        logo_text = QLabel("AI-Career Bridge")
        logo_text.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 20px; font-weight: 800; letter-spacing: -0.5px;")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        left_layout.addLayout(logo_layout)

        left_layout.addSpacing(60)

        # Titles
        self.title = QLabel("Build Your\nFuture With AI.")
        self.title.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 42px; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1;")
        left_layout.addWidget(self.title)

        left_layout.addSpacing(15)

        self.subtitle = QLabel("Smart academic roadmap and career\nnetworking platform.")
        self.subtitle.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 18px; font-weight: 500; line-height: 1.4;")
        left_layout.addWidget(self.subtitle)

        left_layout.addSpacing(40)

        # Feature Cards
        features_layout = QVBoxLayout()
        features_layout.setSpacing(12)

        features = [
            ("AI Mentor Guidance", "Personalized academic and career advice", "🤖"),
            ("Smart Career Roadmaps", "Dynamic paths adapted to your goals", "🗺️"),
            ("Skill Gap Analytics", "Real-time insights on your progress", "📊"),
            ("Real-Time Community", "Connect with peers and professionals", "👥")
        ]

        for title, desc, icon in features:
            features_layout.addWidget(FeatureCard(title, desc, icon))

        left_layout.addLayout(features_layout)

        left_layout.addStretch()

        # Bottom Left Info
        status_layout = QHBoxLayout()
        status_layout.setSpacing(10)
        status_dot = QLabel("●")
        status_dot.setStyleSheet("color: #10B981; font-size: 10px;")
        status_text = QLabel("All systems operational • v2.4.0")
        status_text.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px; font-weight: 500;")
        status_layout.addWidget(status_dot)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        left_layout.addLayout(status_layout)

        self.left_widget = left_widget
        main_layout.addWidget(self.left_widget, 4)

        # ==========================================
        # RIGHT COLUMN (60%): Login Form
        # ==========================================
        self.right_widget = QWidget()
        self.right_widget.setStyleSheet(f"background-color: {COLOR_BG};")
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(40, 60, 60, 60)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Top Right Controls
        top_controls = QHBoxLayout()
        top_controls.addStretch()
        self.lang_btn = QPushButton("EN ▾")
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lang_btn.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; font-weight: 600; border: none; background: transparent;")
        self.lang_btn.clicked.connect(self._toggle_language)

        top_controls.addWidget(self.lang_btn)

        # Login Card
        self.card = QFrame()
        self.card.setFixedWidth(460)
        self.card.setStyleSheet(f"""
            QFrame#LoginCard {{
                background-color: {COLOR_CARD_BG};
                border-radius: 28px;
                border: 1px solid rgba(0, 0, 0, 0.04);
            }}
        """)
        self.card.setObjectName("LoginCard")

        # Add drop shadow
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 8)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(48, 48, 48, 48)
        card_layout.setSpacing(24)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.welcome_title = QLabel("Welcome Back")
        self.welcome_title.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;")
        self.welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.welcome_sub = QLabel("Login to continue your journey.")
        self.welcome_sub.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 15px; font-weight: 500;")
        self.welcome_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(self.welcome_title)
        header_layout.addWidget(self.welcome_sub)
        card_layout.addLayout(header_layout)

        card_layout.addSpacing(10)

        # Inputs
        self.email_entry = ModernInput("Email", "Enter your email", "✉️")
        self.password_entry = ModernInput("Password", "Enter your password", "🔑", is_password=True)

        card_layout.addWidget(self.email_entry)
        card_layout.addWidget(self.password_entry)

        # Remember / Forgot
        options_layout = QHBoxLayout()
        self.remember_cb = QCheckBox("Remember me")
        self.remember_cb.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remember_cb.setStyleSheet(f"""
            QCheckBox {{ color: {COLOR_TEXT_SECONDARY}; font-size: 13px; font-weight: 500; spacing: 8px; }}
            QCheckBox::indicator {{ width: 16px; height: 16px; border-radius: 4px; border: 1px solid {COLOR_BORDER}; background: #F8FAFC; }}
            QCheckBox::indicator:checked {{ background: {COLOR_PRIMARY}; border: 1px solid {COLOR_PRIMARY}; }}
        """)

        self.forgot_btn = QPushButton("Forgot password?")
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_btn.setStyleSheet(f"""
            QPushButton {{ color: {COLOR_PRIMARY}; font-size: 13px; font-weight: 600; border: none; background: transparent; }}
            QPushButton:hover {{ color: {COLOR_SECONDARY}; text-decoration: underline; }}
        """)

        options_layout.addWidget(self.remember_cb)
        options_layout.addStretch()
        options_layout.addWidget(self.forgot_btn)
        card_layout.addLayout(options_layout)

        # Error label
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 600;")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setWordWrap(True)
        self.lbl_error.hide()
        card_layout.addWidget(self.lbl_error)

        # Sign In Button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setFixedHeight(48)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLOR_SECONDARY}, stop:1 {COLOR_PRIMARY});
                color: white;
                font-size: 15px;
                font-weight: 700;
                border-radius: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #14B8A6, stop:1 #0EA5E9);
            }}
            QPushButton:pressed {{
                background: #0284C7;
            }}
        """)
        self.login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(self.login_btn)

        card_layout.addSpacing(10)

        # Divider
        divider_layout = QHBoxLayout()
        line1 = QFrame();
        line1.setFrameShape(QFrame.Shape.HLine);
        line1.setStyleSheet(f"color: {COLOR_BORDER};")
        line2 = QFrame();
        line2.setFrameShape(QFrame.Shape.HLine);
        line2.setStyleSheet(f"color: {COLOR_BORDER};")
        self.or_lbl = QLabel("or continue with")
        self.or_lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px; font-weight: 500;")
        divider_layout.addWidget(line1)
        divider_layout.addWidget(self.or_lbl)
        divider_layout.addWidget(line2)
        card_layout.addLayout(divider_layout)

        # Social Buttons
        social_layout = QHBoxLayout()
        social_layout.setSpacing(12)
        social_layout.addWidget(SocialButton("G", "Google"))
        social_layout.addWidget(SocialButton("Hub", "GitHub"))
        social_layout.addWidget(SocialButton("MS", "Microsoft"))
        card_layout.addLayout(social_layout)

        card_layout.addSpacing(10)

        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer_text = QLabel("Don't have an account?")
        self.footer_text.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; font-weight: 500;")

        self.register_btn = QPushButton("Create Account")
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.setStyleSheet(f"""
            QPushButton {{ color: {COLOR_TEXT_PRIMARY}; font-weight: 700; font-size: 14px; border: none; background: transparent; }}
            QPushButton:hover {{ color: {COLOR_PRIMARY}; }}
        """)
        self.register_btn.clicked.connect(self._handle_register_click)

        footer_layout.addWidget(self.footer_text)
        footer_layout.addWidget(self.register_btn)
        card_layout.addLayout(footer_layout)

        # Assemble Right Column
        right_container = QVBoxLayout()
        right_container.setContentsMargins(0, 0, 0, 0)
        right_container.addLayout(top_controls)
        right_container.addStretch()
        right_container.addWidget(self.card, alignment=Qt.AlignmentFlag.AlignCenter)
        right_container.addStretch()

        self.right_layout.addLayout(right_container)
        main_layout.addWidget(self.right_widget, 6)

        # --- 5. Finalize Scroll Area Assembly ---
        self.scroll_area.setWidget(self.content_container)
        outer_layout.addWidget(self.scroll_area)

        # Initialize States
        self.is_en = True
        self.is_dark = False

    def _handle_login(self):
        email = self.email_entry.text().strip()
        password = self.password_entry.text().strip()
        if not email or not password:
            self.lbl_error.setText("Email and password are required.")
            self.lbl_error.show()
            return

        self.lbl_error.hide()
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Signing In..." if self.is_en else "Đang Đăng Nhập...")

        from modules.auth_worker import LoginWorker
        self.worker = LoginWorker(email, password)
        self.worker.success.connect(self._on_login_success)
        self.worker.error.connect(self._on_login_error)
        self.worker.start()

    def _on_login_success(self, student_info):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In" if self.is_en else "Đăng Nhập")
        if self.on_login_callback:
            self.on_login_callback(student_info)

    def _on_login_error(self, err_msg):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In" if self.is_en else "Đăng Nhập")
        self.lbl_error.setText(err_msg)
        self.lbl_error.show()

    def _handle_register_click(self):
        if self.on_register_click_callback:
            self.on_register_click_callback()

    def _toggle_language(self):
        self.is_en = not getattr(self, "is_en", True)
        if self.is_en:
            self.lang_btn.setText("EN ▾")
            self.welcome_title.setText("Welcome Back")
            self.welcome_sub.setText("Login to continue your journey.")
            self.login_btn.setText("Sign In")
            self.register_btn.setText("Create Account")
            self.remember_cb.setText("Remember me")
            self.forgot_btn.setText("Forgot password?")
            self.title.setText("Build Your\nFuture With AI.")
            self.subtitle.setText("Smart academic roadmap and career\nnetworking platform.")
            self.or_lbl.setText("or continue with")
            self.footer_text.setText("Don't have an account?")
        else:
            self.lang_btn.setText("VI ▾")
            self.welcome_title.setText("Chào mừng trở lại")
            self.welcome_sub.setText("Đăng nhập để tiếp tục hành trình của bạn.")
            self.login_btn.setText("Đăng Nhập")
            self.register_btn.setText("Tạo Tài Khoản")
            self.remember_cb.setText("Ghi nhớ đăng nhập")
            self.forgot_btn.setText("Quên mật khẩu?")
            self.title.setText("Xây Dựng\nTương Lai Cùng AI.")
            self.subtitle.setText("Lộ trình học tập thông minh và\nnền tảng kết nối nghề nghiệp.")
            self.or_lbl.setText("hoặc tiếp tục với")
            self.footer_text.setText("Chưa có tài khoản?")

    def _toggle_theme(self):
        pass


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LoginPage()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())