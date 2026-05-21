import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSpacerItem, QSizePolicy, QLineEdit,
                             QFrame, QGraphicsDropShadowEffect, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QCursor

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


class ProgressStepper(QWidget):
    def __init__(self, steps, current_step=0, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        for i, step_text in enumerate(steps):
            step_container = QVBoxLayout()
            step_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_container.setSpacing(4)

            # The Line/Dot Indicator
            indicator_layout = QHBoxLayout()
            indicator_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            indicator_layout.setSpacing(0)

            # Before line
            if i > 0:
                line_before = QFrame()
                line_before.setFrameShape(QFrame.Shape.HLine)
                line_before.setFixedHeight(2)
                line_before.setFixedWidth(20)
                line_before.setStyleSheet(
                    f"background-color: {COLOR_PRIMARY if i <= current_step else COLOR_BORDER}; border: none;")
                indicator_layout.addWidget(line_before)
            else:
                spacer = QWidget()
                spacer.setFixedWidth(20)
                indicator_layout.addWidget(spacer)

            # Dot
            dot = QLabel()
            dot.setFixedSize(12, 12)
            if i < current_step:
                dot.setStyleSheet(f"background-color: {COLOR_PRIMARY}; border-radius: 6px;")
            elif i == current_step:
                dot.setStyleSheet(f"background-color: #FFFFFF; border: 3px solid {COLOR_PRIMARY}; border-radius: 6px;")
            else:
                dot.setStyleSheet(f"background-color: #FFFFFF; border: 2px solid {COLOR_BORDER}; border-radius: 6px;")
            indicator_layout.addWidget(dot)

            # After line
            if i < len(steps) - 1:
                line_after = QFrame()
                line_after.setFrameShape(QFrame.Shape.HLine)
                line_after.setFixedHeight(2)
                line_after.setFixedWidth(20)
                line_after.setStyleSheet(
                    f"background-color: {COLOR_PRIMARY if i < current_step else COLOR_BORDER}; border: none;")
                indicator_layout.addWidget(line_after)
            else:
                spacer = QWidget()
                spacer.setFixedWidth(20)
                indicator_layout.addWidget(spacer)

            step_container.addLayout(indicator_layout)

            # Label
            lbl = QLabel(step_text)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if i <= current_step:
                lbl.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 11px; font-weight: 700;")
            else:
                lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 11px; font-weight: 500;")
            step_container.addWidget(lbl)

            layout.addLayout(step_container)


class RegisterPage(QWidget):
    def __init__(self, parent=None, on_back_click=None, on_register=None):
        super().__init__(parent)
        self.on_back_click = on_back_click
        self.on_register = on_register

        self.setWindowTitle("AI-Career Bridge - Create Account")
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
        self.content_container.setMinimumSize(1100, 750)

        # --- 4. Main App Layout (Now attached to content_container) ---
        main_layout = QHBoxLayout(self.content_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==========================================
        # LEFT COLUMN (42%): Branding & Features
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

        # Hero Text
        title = QLabel("Start Building Your\nCareer Journey.")
        title.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 42px; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1;")
        left_layout.addWidget(title)

        left_layout.addSpacing(15)

        subtitle = QLabel("Join thousands of professionals accelerating\ntheir growth with AI.")
        subtitle.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 18px; font-weight: 500; line-height: 1.4;")
        left_layout.addWidget(subtitle)

        left_layout.addSpacing(40)

        # Floating Feature Preview Cards
        features_layout = QVBoxLayout()
        features_layout.setSpacing(12)

        features = [
            ("AI Career Roadmaps", "Dynamic paths adapted to your goals", "🗺️"),
            ("AI Mentor Assistance", "Personalized 24/7 academic advice", "🤖"),
            ("Realtime Community", "Connect with peers and professionals", "👥")
        ]

        for t, d, i in features:
            features_layout.addWidget(FeatureCard(t, d, i))

        left_layout.addLayout(features_layout)

        left_layout.addStretch()

        # Bottom Status/Version Footer
        status_layout = QHBoxLayout()
        status_layout.setSpacing(10)
        status_dot = QLabel("●")
        status_dot.setStyleSheet("color: #10B981; font-size: 10px;")
        status_text = QLabel("System Online • v2.4.0")
        status_text.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px; font-weight: 500;")
        status_layout.addWidget(status_dot)
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        left_layout.addLayout(status_layout)

        main_layout.addWidget(left_widget, 42)

        # ==========================================
        # RIGHT COLUMN (58%): Register Form
        # ==========================================
        right_widget = QWidget()
        right_widget.setStyleSheet(f"background-color: {COLOR_BG};")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(40, 40, 60, 40)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Top Right Controls
        top_controls = QHBoxLayout()
        top_controls.addStretch()
        lang_btn = QPushButton("EN ▾")
        lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lang_btn.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; font-weight: 600; border: none; background: transparent;")
        theme_btn = QPushButton("🌙")
        theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        theme_btn.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 16px; border: none; background: transparent;")
        top_controls.addWidget(lang_btn)
        top_controls.addWidget(theme_btn)

        # Floating Help Widget Mock
        help_btn = QPushButton("? Need Help")
        help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        help_btn.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; font-weight: 600; border: none; background: transparent; padding-left: 15px;")
        top_controls.addWidget(help_btn)

        # Register Card
        card = QFrame()
        card.setFixedWidth(520)
        card.setStyleSheet(f"""
            QFrame#RegisterCard {{
                background-color: {COLOR_CARD_BG};
                border-radius: 28px;
                border: 1px solid rgba(0, 0, 0, 0.04);
            }}
        """)
        card.setObjectName("RegisterCard")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(48, 40, 48, 40)
        card_layout.setSpacing(24)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)

        title_lbl = QLabel("Create Account")
        title_lbl.setStyleSheet(
            f"color: {COLOR_TEXT_PRIMARY}; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;")

        subtitle_lbl = QLabel("Start your new journey. No gimmicks. No pretentious.")
        subtitle_lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; font-weight: 500;")

        header_layout.addWidget(title_lbl)
        header_layout.addWidget(subtitle_lbl)
        card_layout.addLayout(header_layout)

        # Progress Stepper Mock
        stepper = ProgressStepper(["Basic Info", "Academic", "Interests", "Confirm"], current_step=0)
        card_layout.addWidget(stepper)

        card_layout.addSpacing(4)

        # Form Fields (Basic Info + Academic Context)
        self.username_input = ModernInput("Username", "jane_doe", "👤")
        card_layout.addWidget(self.username_input)

        self.display_name_input = ModernInput("Display Name", "Jane Doe", "✨")
        card_layout.addWidget(self.display_name_input)

        self.email_input = ModernInput("Email Address", "jane@example.com", "✉️")
        card_layout.addWidget(self.email_input)

        self.password_input = ModernInput("Password", "Create a secure password", "🔑", is_password=True)
        card_layout.addWidget(self.password_input)

        # Academic Fields
        major_year_layout = QHBoxLayout()
        major_year_layout.setSpacing(16)

        self.major_input = ModernInput("Major", "Computer Science", "🎓")
        major_year_layout.addWidget(self.major_input, 2)

        # Student Year dropdown
        year_container = QVBoxLayout()
        year_container.setSpacing(6)
        year_lbl = QLabel("Student Year")
        year_lbl.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY}; font-size: 13px; font-weight: 600;")
        self.year_combo = QComboBox()
        self.year_combo.setFixedHeight(44)
        for i in range(1, 9):
            self.year_combo.addItem(f"Year {i}", i)
        year_container.addWidget(year_lbl)
        year_container.addWidget(self.year_combo)
        major_year_layout.addLayout(year_container, 1)

        card_layout.addLayout(major_year_layout)

        card_layout.addSpacing(4)

        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 600;")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setWordWrap(True)
        self.lbl_error.hide()
        card_layout.addWidget(self.lbl_error)

        # Primary Action Button
        self.create_btn = QPushButton("Create Account")
        self.create_btn.setFixedHeight(48)
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.setStyleSheet(f"""
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
        self.create_btn.clicked.connect(self._handle_register)
        card_layout.addWidget(self.create_btn)

        # Social Divider
        divider_layout = QHBoxLayout()
        line1 = QFrame();
        line1.setFrameShape(QFrame.Shape.HLine);
        line1.setStyleSheet(f"color: {COLOR_BORDER};")
        line2 = QFrame();
        line2.setFrameShape(QFrame.Shape.HLine);
        line2.setStyleSheet(f"color: {COLOR_BORDER};")
        or_lbl = QLabel("or continue with")
        or_lbl.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 12px; font-weight: 500;")
        divider_layout.addWidget(line1)
        divider_layout.addWidget(or_lbl)
        divider_layout.addWidget(line2)
        card_layout.addLayout(divider_layout)

        # Social Buttons
        social_layout = QHBoxLayout()
        social_layout.setSpacing(12)
        social_layout.addWidget(SocialButton("G", "Google"))
        social_layout.addWidget(SocialButton("Hub", "GitHub"))
        social_layout.addWidget(SocialButton("MS", "Microsoft"))
        card_layout.addLayout(social_layout)

        card_layout.addSpacing(4)

        # Bottom Footer Action
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_text = QLabel("Already have an account?")
        footer_text.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 14px; font-weight: 500;")

        self.signin_btn = QPushButton("Sign In")
        self.signin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.signin_btn.setStyleSheet(f"""
            QPushButton {{ color: {COLOR_TEXT_PRIMARY}; font-weight: 700; font-size: 14px; border: none; background: transparent; }}
            QPushButton:hover {{ color: {COLOR_PRIMARY}; }}
        """)
        self.signin_btn.clicked.connect(self.on_back_click if self.on_back_click else lambda: None)

        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(self.signin_btn)
        card_layout.addLayout(footer_layout)

        # Assemble Right Column
        right_container = QVBoxLayout()
        right_container.setContentsMargins(0, 0, 0, 0)
        right_container.addLayout(top_controls)
        right_container.addStretch()
        right_container.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        right_container.addStretch()

        right_layout.addLayout(right_container)
        main_layout.addWidget(right_widget, 58)

        # --- 5. Finalize Scroll Area Assembly ---
        self.scroll_area.setWidget(self.content_container)
        outer_layout.addWidget(self.scroll_area)

    def _handle_register(self):
        username = self.username_input.text().strip()
        display_name = self.display_name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        major = self.major_input.text().strip()
        student_year = self.year_combo.currentData()

        if not email or not username or not password:
            self.lbl_error.setText("Email, username, and password are required.")
            self.lbl_error.show()
            return

        self.lbl_error.hide()
        self.create_btn.setEnabled(False)
        self.create_btn.setText("Creating Account...")

        from modules.auth_worker import RegisterWorker
        self.worker = RegisterWorker(
            email=email,
            password=password,
            username=username,
            display_name=display_name,
            major=major,
            student_year=student_year
        )
        self.worker.success.connect(self._on_register_success)
        self.worker.error.connect(self._on_register_error)
        self.worker.start()

    def _on_register_success(self, res):
        self.create_btn.setEnabled(True)
        self.create_btn.setText("Create Account")
        if self.on_register:
            self.on_register(res)

    def _on_register_error(self, err_msg):
        self.create_btn.setEnabled(True)
        self.create_btn.setText("Create Account")
        self.lbl_error.setText(err_msg)
        self.lbl_error.show()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = RegisterPage()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())