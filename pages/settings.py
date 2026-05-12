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
