from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout, 
                             QLineEdit, QComboBox, QCheckBox, QSlider)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush

class ToggleSwitch(QWidget):
    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self._checked = checked
        self._thumb_pos = 22 if checked else 2
        
        self.animation = QPropertyAnimation(self, b"thumb_pos")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    @pyqtProperty(int)
    def thumb_pos(self):
        return self._thumb_pos
        
    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            self.animation.setStartValue(self._thumb_pos)
            self.animation.setEndValue(22 if self._checked else 2)
            self.animation.start()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        bg_color = QColor("#38BDF8") if self._checked else QColor("#E2E8F0")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        
        # Thumb
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(self._thumb_pos, 2, 20, 20)

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(16)

class SettingsPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_category_sidebar()
        self._setup_main_workspace()
        self._setup_right_panel()

    def _setup_category_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(8)
        
        header = QLabel("Settings")
        header.setStyleSheet("color: #0F172A; font-size: 24px; font-weight: 700; border: none; padding-bottom: 16px;")
        layout.addWidget(header)
        
        search = QLineEdit()
        search.setPlaceholderText("Search settings...")
        search.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 10px 16px; color: #0F172A; font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #38BDF8; }
        """)
        layout.addWidget(search)
        layout.addSpacing(16)
        
        categories = [
            "Account", "Profile Preferences", "Notifications", "Appearance", 
            "Accessibility", "Privacy & Security", "AI Assistant", 
            "Integrations", "Storage & Sync", "Keyboard Shortcuts", "About Application"
        ]
        
        self.cat_buttons = []
        for i, cat in enumerate(categories):
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            if i == 0: btn.setChecked(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; border: none; text-align: left;
                    padding: 12px 16px; border-radius: 8px; color: #64748B;
                    font-size: 14px; font-weight: 500;
                }
                QPushButton:hover { background-color: #F8FAFC; color: #0F172A; }
                QPushButton:checked { background-color: #E0F2FE; color: #0284C7; font-weight: 600; }
            """)
            layout.addWidget(btn)
            self.cat_buttons.append(btn)
            btn.clicked.connect(lambda checked, b=btn: self._on_category_clicked(b))
            
        layout.addStretch()
        self.main_layout.addWidget(sidebar)

    def _on_category_clicked(self, clicked_btn):
        for btn in self.cat_buttons:
            if btn != clicked_btn:
                btn.setChecked(False)
            else:
                btn.setChecked(True)

    def _setup_main_workspace(self):
        workspace = QWidget()
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(32, 0, 32, 0)
        
        # Breadcrumbs
        bc_layout = QVBoxLayout()
        bc_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bc_layout.setSpacing(2)
        bc_lbl = QLabel("Settings / Account")
        bc_lbl.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
        title = QLabel("Account Settings")
        title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700; border: none;")
        bc_layout.addWidget(bc_lbl)
        bc_layout.addWidget(title)
        t_layout.addLayout(bc_layout)
        
        t_layout.addStretch()
        
        btn_reset = QPushButton("Reset")
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.setStyleSheet("""
            QPushButton {
                background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 8px 16px; color: #64748B; font-weight: 600; font-size: 14px;
            }
            QPushButton:hover { background: #F8FAFC; color: #0F172A; }
        """)
        btn_save = QPushButton("Save Changes")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background: #38BDF8; border: none; border-radius: 8px;
                padding: 8px 16px; color: #FFFFFF; font-weight: 600; font-size: 14px;
            }
            QPushButton:hover { background: #0284C7; }
        """)
        t_layout.addWidget(btn_reset)
        t_layout.addWidget(btn_save)
        
        layout.addWidget(toolbar)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(32, 32, 32, 32)
        c_layout.setSpacing(24)
        c_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Section 1: Personal Info
        card1 = ModernCard()
        lbl1 = QLabel("Personal Information")
        lbl1.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 600; border: none;")
        card1.layout.addWidget(lbl1)
        
        grid1 = QGridLayout()
        grid1.setSpacing(16)
        
        def create_field(label_text, placeholder):
            w = QWidget()
            l = QVBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(6)
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color: #475569; font-size: 13px; font-weight: 500; border: none;")
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setStyleSheet("""
                QLineEdit {
                    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
                    padding: 10px 12px; color: #0F172A; font-size: 14px;
                }
                QLineEdit:focus { border: 1px solid #38BDF8; }
            """)
            l.addWidget(lbl)
            l.addWidget(inp)
            return w
            
        grid1.addWidget(create_field("Full Name", "John Doe"), 0, 0)
        grid1.addWidget(create_field("Email Address", "john.doe@example.com"), 0, 1)
        grid1.addWidget(create_field("Phone Number", "+1 (555) 000-0000"), 1, 0)
        
        card1.layout.addLayout(grid1)
        c_layout.addWidget(card1)
        
        # Section 2: Security & Password
        card2 = ModernCard()
        lbl2 = QLabel("Security")
        lbl2.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 600; border: none;")
        card2.layout.addWidget(lbl2)
        
        def create_toggle_row(title, subtitle, checked=False):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            
            texts = QVBoxLayout()
            texts.setSpacing(2)
            t1 = QLabel(title)
            t1.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 500; border: none;")
            t2 = QLabel(subtitle)
            t2.setStyleSheet("color: #64748B; font-size: 13px; border: none;")
            texts.addWidget(t1)
            texts.addWidget(t2)
            
            l.addLayout(texts)
            l.addStretch()
            l.addWidget(ToggleSwitch(checked=checked))
            return w
            
        card2.layout.addWidget(create_toggle_row("Two-Factor Authentication", "Add an extra layer of security to your account.", True))
        card2.layout.addWidget(create_toggle_row("Login Alerts", "Get notified when someone logs into your account.", True))
        
        btn_pwd = QPushButton("Change Password")
        btn_pwd.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_pwd.setStyleSheet("""
            QPushButton {
                background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 10px 16px; color: #0F172A; font-weight: 600; font-size: 14px;
            }
            QPushButton:hover { background: #F8FAFC; }
        """)
        btn_pwd.setFixedWidth(160)
        card2.layout.addWidget(btn_pwd)
        
        c_layout.addWidget(card2)
        
        # Section 3: Profile Preferences & Appearance
        card3 = ModernCard()
        lbl3 = QLabel("Profile Preferences")
        lbl3.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 600; border: none;")
        card3.layout.addWidget(lbl3)
        
        vis_layout = QVBoxLayout()
        vis_layout.setSpacing(6)
        vis_lbl = QLabel("Profile Visibility")
        vis_lbl.setStyleSheet("color: #475569; font-size: 13px; font-weight: 500; border: none;")
        vis_cb = QComboBox()
        vis_cb.addItems(["Public", "Network Only", "Private"])
        vis_cb.setCursor(Qt.CursorShape.PointingHandCursor)
        vis_cb.setStyleSheet("""
            QComboBox {
                background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 10px 12px; color: #0F172A; font-size: 14px;
            }
            QComboBox::drop-down { border: none; }
        """)
        vis_layout.addWidget(vis_lbl)
        vis_layout.addWidget(vis_cb)
        card3.layout.addLayout(vis_layout)
        
        card3.layout.addWidget(create_toggle_row("Show Academic Information", "Allow others to see your university and courses.", True))
        card3.layout.addWidget(create_toggle_row("Show Career Status", "Let recruiters know you are actively looking.", True))
        
        c_layout.addWidget(card3)
        
        # Section 4: Storage & Sync
        card4 = ModernCard()
        lbl4 = QLabel("Storage & Sync")
        lbl4.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 600; border: none;")
        card4.layout.addWidget(lbl4)
        card4.layout.addWidget(create_toggle_row("Cloud Sync", "Automatically sync your settings across devices.", True))
        
        storage_layout = QVBoxLayout()
        storage_layout.setSpacing(8)
        s_lbl = QLabel("Local Storage Usage (2.4 GB / 5.0 GB)")
        s_lbl.setStyleSheet("color: #475569; font-size: 13px; font-weight: 500; border: none;")
        storage_layout.addWidget(s_lbl)
        
        progress = QFrame()
        progress.setFixedHeight(8)
        progress.setStyleSheet("background: #E2E8F0; border-radius: 4px; border: none;")
        p_inner = QFrame(progress)
        p_inner.setFixedHeight(8)
        p_inner.setFixedWidth(200) # mock progress
        p_inner.setStyleSheet("background: #38BDF8; border-radius: 4px; border: none;")
        storage_layout.addWidget(progress)
        
        card4.layout.addLayout(storage_layout)
        c_layout.addWidget(card4)
        
        c_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.main_layout.addWidget(workspace)

    def _setup_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(320)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Quick Help
        h_lbl = QLabel("Quick Help")
        h_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        layout.addWidget(h_lbl)
        
        def create_link(text):
            lbl = QLabel(f"•  {text}")
            lbl.setStyleSheet("color: #38BDF8; font-size: 14px; font-weight: 500; border: none;")
            lbl.setCursor(Qt.CursorShape.PointingHandCursor)
            return lbl
            
        layout.addWidget(create_link("Settings Documentation"))
        layout.addWidget(create_link("Keyboard Shortcuts"))
        layout.addWidget(create_link("Common Fixes"))
        
        layout.addSpacing(16)
        
        # Live Preview
        p_lbl = QLabel("Live Preview")
        p_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        layout.addWidget(p_lbl)
        
        preview_box = QFrame()
        preview_box.setFixedHeight(120)
        preview_box.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;")
        pb_layout = QVBoxLayout(preview_box)
        pb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pb_layout.addWidget(QLabel("UI Preview Area", styleSheet="color: #64748B; font-weight: 500; font-size: 14px; border: none;"))
        layout.addWidget(preview_box)
        
        layout.addSpacing(16)
        
        # Recent Changes
        rc_lbl = QLabel("Recent Changes")
        rc_lbl.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        layout.addWidget(rc_lbl)
        
        def create_history(text, time_str):
            w = QWidget()
            l = QVBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(2)
            t1 = QLabel(text)
            t1.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 500; border: none;")
            t2 = QLabel(time_str)
            t2.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
            l.addWidget(t1)
            l.addWidget(t2)
            return w
            
        layout.addWidget(create_history("Changed Password", "2 hours ago"))
        layout.addWidget(create_history("Enabled Two-Factor Auth", "Yesterday at 4:30 PM"))
        layout.addWidget(create_history("Updated Profile Visibility", "Oct 12, 2024"))
        
        layout.addStretch()
        self.main_layout.addWidget(panel)
