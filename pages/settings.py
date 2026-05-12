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
