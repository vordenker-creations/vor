<<<<<<< HEAD
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, ChipButton

class SettingsPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; } QWidget#qt_scrollarea_viewport { background-color: transparent; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Main Settings Card
        card = SaaSCard(border_color="#00A2FF")
        card.setStyleSheet(f"SaaSCard {{ background-color: {COLOR_BG_APP}; border: 2px solid #00A2FF; border-radius: 16px; }}")
        
        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(20)
        card.internal_layout.addLayout(card_layout)
        
        # --- Left Column (Labels) ---
        left_col = QVBoxLayout()
        left_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # System & Preferences
        lbl_sys = QLabel("⚙️ System & Preferences")
        lbl_sys.setStyleSheet(f"color: #00E5FF; font-size: 18px; font-weight: bold;")
        left_col.addWidget(lbl_sys)
        left_col.addSpacing(5)
        
        left_col.addWidget(QLabel("System Brightness", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        left_col.addSpacing(5)
        left_col.addWidget(QLabel("Application Language", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        
        left_col.addSpacing(20)
        
        # Security & Login
        lbl_sec = QLabel("🔒 Security & Login")
        lbl_sec.setStyleSheet(f"color: #00E5FF; font-size: 18px; font-weight: bold;")
        left_col.addWidget(lbl_sec)
        left_col.addSpacing(5)
        
        lbl_cp = QLabel("Change Password")
        lbl_cp.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold; margin-left: 20px;")
        left_col.addWidget(lbl_cp)
        left_col.addSpacing(5)
        
        left_col.addWidget(QLabel("Default Language", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        left_col.addSpacing(5)
        left_col.addWidget(QLabel("Skill Assessment Frequency", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        left_col.addSpacing(5)
        left_col.addWidget(QLabel("Career Goal Settings", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        
        left_col.addSpacing(20)
        
        # Account & Support
        lbl_acc = QLabel("👤 Account & Support")
        lbl_acc.setStyleSheet(f"color: #00E5FF; font-size: 18px; font-weight: bold;")
        left_col.addWidget(lbl_acc)
        left_col.addSpacing(5)
        
        lbl_ai = QLabel("Application Information")
        lbl_ai.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 14px; font-weight: bold; margin-left: 20px;")
        left_col.addWidget(lbl_ai)
        left_col.addSpacing(5)
        
        left_col.addWidget(QLabel("ⓘ Version: 1.2.0", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        left_col.addSpacing(2)
        left_col.addWidget(QLabel("🖥️ Platform: Desktop (Windows/macOS)", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        left_col.addSpacing(2)
        left_col.addWidget(QLabel("📄 License: Educational", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px; margin-left: 20px;"))
        
        card_layout.addLayout(left_col, 1)
        
        # --- Right Column (Controls) ---
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        right_col.addSpacing(25) # Align with System Brightness
        
        # Brightness Slider
        bright_layout = QHBoxLayout()
        bright_layout.addWidget(QLabel("🔅", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 16px;"))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(40)
        slider.setStyleSheet("""
            QSlider::groove:horizontal { border: 1px solid #999999; height: 8px; background: #333333; border-radius: 4px; }
            QSlider::sub-page:horizontal { background: #00E5FF; border-radius: 4px; }
            QSlider::handle:horizontal { background: #E0F7FA; border: 1px solid #5c5c5c; width: 18px; margin-top: -5px; margin-bottom: -5px; border-radius: 9px; }
        """)
        bright_layout.addWidget(slider)
        bright_layout.addWidget(QLabel("🔆", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 16px;"))
        right_col.addLayout(bright_layout)
        right_col.addSpacing(10)
        
        # Language Dropdown
        lang_cb = QComboBox()
        lang_cb.addItems(["English", "Vietnamese"])
        lang_cb.setStyleSheet(f"background-color: transparent; border: 1px solid #00A2FF; color: {COLOR_TEXT_MAIN}; border-radius: 4px; padding: 5px;")
        right_col.addWidget(lang_cb)
        
        right_col.addSpacing(35) # Align with Change Password
        
        # Change Password Section
        btn_cp = QPushButton("CHANGE PASSWORD")
        btn_cp.setStyleSheet(f"background-color: transparent; color: {COLOR_TEXT_MAIN}; border: 2px solid #00E5FF; border-radius: 8px; padding: 6px; font-weight: bold;")
        right_col.addWidget(btn_cp)
        right_col.addSpacing(5)
        
        def create_input(placeholder):
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setEchoMode(QLineEdit.EchoMode.Password)
            inp.setStyleSheet(f"background-color: transparent; border: 1px solid #00A2FF; border-radius: 4px; padding: 6px; color: {COLOR_TEXT_MAIN};")
            return inp
            
        right_col.addWidget(create_input("Current Password"))
        right_col.addSpacing(2)
        right_col.addWidget(create_input("New Password"))
        right_col.addSpacing(2)
        right_col.addWidget(create_input("Confirm New Password"))
        
        right_col.addSpacing(25) # Align with Account Upgrade Support
        
        # Upgrade Support
        btn_upg = QPushButton("UPGRADE ACCOUNT")
        btn_upg.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #8A2BE2); color: white; border: none; border-radius: 8px; padding: 8px; font-weight: bold; font-size: 14px;")
        right_col.addWidget(btn_upg)
        right_col.addSpacing(5)
        
        right_col.addWidget(QLabel("Current Tier: Free", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px;"))
        right_col.addSpacing(2)
        right_col.addWidget(QLabel("Contact Support for Upgrades", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px;"))
        right_col.addSpacing(2)
        right_col.addWidget(QLabel("Contact Support Email: support@aibridge.edu", styleSheet=f"color: {COLOR_TEXT_MAIN}; font-size: 14px;"))
        
        card_layout.addLayout(right_col, 1)
        
        content_layout.addWidget(card)
        
        # Bottom Buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 10, 0, 0)
        
        btn_logout = QPushButton("⏻ Logout\n╰→ Logout of Account")
        btn_logout.setStyleSheet(f"background-color: transparent; color: {COLOR_TEXT_MAIN}; border: none; text-align: left; font-size: 14px;")
        if self.controller:
            btn_logout.clicked.connect(lambda: self.controller.central_widget.setCurrentIndex(0))
        bottom_layout.addWidget(btn_logout)
        
        bottom_layout.addStretch()
        
        btn_save = QPushButton("SAVE CHANGES")
        btn_save.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #0088FF); color: white; border: none; border-radius: 8px; padding: 10px 30px; font-weight: bold; font-size: 14px;")
        bottom_layout.addWidget(btn_save)
        
        btn_cancel = QPushButton("CANCEL")
        btn_cancel.setStyleSheet(f"background-color: transparent; color: {COLOR_TEXT_MAIN}; border: 1px solid {COLOR_TEXT_SUB}; border-radius: 8px; padding: 10px 30px; font-weight: bold; font-size: 14px;")
        bottom_layout.addWidget(btn_cancel)
        
        content_layout.addLayout(bottom_layout)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
=======
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt
from config import *
from i18n import _, set_language
from components import SaaSCard, ModernSwitch

class SettingsPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("SettingsPage")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setContentsMargins(35, 35, 35, 35)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Header
        lbl_title = QLabel(_("settings_tooltip"))
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 28px; font-weight: bold;")
        self.layout.addWidget(lbl_title)

        # --- Appearance Section ---
        self._add_section_header(_("menu_theme"))
        appearance_card = SaaSCard()
        
        # Theme Toggle
        theme_row = self._create_setting_row(
            "🌓 " + _("menu_theme"), 
            "Chuyển đổi giữa chế độ sáng và tối",
            ModernSwitch()
        )
        appearance_card.internal_layout.addLayout(theme_row)
        
        # Language Selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([_("menu_lang_vi"), _("menu_lang_en")])
        self.lang_combo.setFixedWidth(150)
        self.lang_combo.setStyleSheet(self._combo_style())
        from i18n import CURRENT_LANG
        self.lang_combo.setCurrentIndex(0 if CURRENT_LANG == "vi" else 1)
        self.lang_combo.currentIndexChanged.connect(self._change_language)
        
        lang_row = self._create_setting_row(
            "🌐 " + _("menu_lang"), 
            "Chọn ngôn ngữ hiển thị của ứng dụng",
            self.lang_combo
        )
        appearance_card.internal_layout.addLayout(lang_row)
        
        self.layout.addWidget(appearance_card)

        # --- App Preferences Section ---
        self._add_section_header("TÙY CHỌN ỨNG DỤNG")
        pref_card = SaaSCard()
        
        # Notifications Toggle
        notif_switch = ModernSwitch()
        notif_switch.set_checked(True)
        notif_row = self._create_setting_row(
            "🔔 Thông báo", 
            "Nhận thông báo về các sự kiện và cập nhật mới",
            notif_switch
        )
        pref_card.internal_layout.addLayout(notif_row)
        
        # Auto-Updates Toggle
        update_switch = ModernSwitch()
        update_switch.set_checked(True)
        update_row = self._create_setting_row(
            "🔄 Cập nhật tự động", 
            "Tự động tải xuống và cài đặt các bản cập nhật mới nhất",
            update_switch
        )
        pref_card.internal_layout.addLayout(update_row)
        
        # Analytics Toggle
        analytics_switch = ModernSwitch()
        analytics_row = self._create_setting_row(
            "📊 Thu thập dữ liệu", 
            "Chia sẻ dữ liệu ẩn danh để giúp chúng tôi cải thiện ứng dụng",
            analytics_switch
        )
        pref_card.internal_layout.addLayout(analytics_row)
        
        self.layout.addWidget(pref_card)

        # --- Support & Info Section ---
        self._add_section_header(_("menu_support"))
        support_card = SaaSCard()
        sup_layout = support_card.internal_layout
        
        for item in ["menu_support_ver", "menu_support_contact", "menu_support_shortcuts"]:
            btn = QPushButton(_(item))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"QPushButton {{ text-align: left; background: transparent; color: {COLOR_TEXT_SUB}; padding: 8px 5px; border: none; font-size: 14px; }} QPushButton:hover {{ color: {COLOR_PRIMARY}; }}")
            sup_layout.addWidget(btn)
        self.layout.addWidget(support_card)

        # Version Info at bottom
        lbl_ver = QLabel("AI-Career Bridge v1.0.0-enterprise")
        lbl_ver.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 11px; margin-top: 20px;")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(lbl_ver)

    def _add_section_header(self, text):
        lbl = QLabel(text.upper())
        lbl.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 12px; font-weight: bold; margin-top: 15px; margin-left: 5px;")
        self.layout.addWidget(lbl)

    def _create_setting_row(self, title, description, widget):
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(5, 10, 5, 10)
        
        text_container = QVBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 15px; font-weight: bold;")
        text_container.addWidget(lbl_title)
        
        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px;")
        lbl_desc.setWordWrap(True)
        text_container.addWidget(lbl_desc)
        
        row_layout.addLayout(text_container)
        row_layout.addStretch()
        row_layout.addWidget(widget)
        
        return row_layout

    def _combo_style(self):
        return f"""
            QComboBox {{ 
                background: {COLOR_BG_APP}; 
                border: 1px solid {COLOR_BORDER}; 
                border-radius: 6px; 
                padding: 5px 10px; 
                color: {COLOR_TEXT_MAIN}; 
                font-size: 13px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLOR_BG_CARD};
                color: {COLOR_TEXT_MAIN};
                selection-background-color: {COLOR_PRIMARY};
                border: 1px solid {COLOR_BORDER};
                outline: none;
            }}
        """

    def _change_language(self, index):
        lang_code = "vi" if index == 0 else "en"
        set_language(lang_code)
        # In a real app, we would emit a signal to refresh all UI components
        print(f"Language changed to: {lang_code}")
>>>>>>> 9b699e38554945b1a68fc554b4f59c385a4b5718
