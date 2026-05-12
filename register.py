import sys
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *
from components import SaaSCard, AnimationEngine
from database import crud

class RegisterPage(QWidget):
    def __init__(self, parent=None, on_back_click=None, on_register=None):
        super().__init__(parent)
        self.on_back_click = on_back_click
        self.on_register = on_register
        self.setObjectName("RegisterPage")
        self.setStyleSheet(f"background-color: {COLOR_BG_APP};")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.circles = []
        self._generate_circles()
        self._setup_content()

    def _generate_circles(self):
        colors = [QColor("#00D1FF"), QColor("#10B981"), QColor("#6366F1")]
        for _ in range(12):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            r = random.randint(30, 100)
            color = random.choice(colors)
            self.circles.append((x, y, r, color))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for x, y, r, color in self.circles:
            for i in range(4):
                alpha_r = r + (i * 15)
                painter.setPen(QColor(color.red(), color.green(), color.blue(), 25))
                painter.drawEllipse(QPoint(x, y), alpha_r, alpha_r)

    def _setup_content(self):
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card = SaaSCard()
        self.card.setFixedSize(800, 700)
        card_layout = self.card.internal_layout
        card_layout.setContentsMargins(40, 30, 40, 30)
        title_lbl = QLabel("CREATE ACCOUNT")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 28px; font-weight: bold;")
        card_layout.addWidget(title_lbl)
        sub_lbl = QLabel("Start your AI career journey today.")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_lbl.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 13px;")
        card_layout.addWidget(sub_lbl)
        card_layout.addSpacing(20)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        form_widget = QWidget()
        form_widget.setStyleSheet("background: transparent;")
        grid = QGridLayout(form_widget)
        grid.setSpacing(20)
        self.name_lbl, self.name_entry = self._create_field("Full Name", "👤 Full Name")
        grid.addWidget(self.name_lbl, 0, 0)
        grid.addWidget(self.name_entry, 1, 0)
        major_lbl = QLabel("Major")
        major_lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 11px; font-weight: bold;")
        self.major_combo = QComboBox()
        self.major_combo.addItems(["Computer Science", "Information Technology", "AI & Data Science", "Digital Business"])
        self.major_combo.setFixedHeight(40)
        self.major_combo.setStyleSheet(self._get_combo_style())
        grid.addWidget(major_lbl, 0, 1)
        grid.addWidget(self.major_combo, 1, 1)
        self.email_lbl, self.email_entry = self._create_field("Student Email", "📧 email@vku.udn.vn")
        grid.addWidget(self.email_lbl, 2, 0)
        grid.addWidget(self.email_entry, 3, 0)
        self.sem_lbl, self.sem_entry = self._create_field("Current Semester", "📖 e.g. 4")
        grid.addWidget(self.sem_lbl, 2, 1)
        grid.addWidget(self.sem_entry, 3, 1)
        self.univ_lbl, self.univ_entry = self._create_field("University", "🏫 University Name")
        grid.addWidget(self.univ_lbl, 4, 0)
        grid.addWidget(self.univ_entry, 5, 0)
        self.total_sem_lbl, self.total_sem_entry = self._create_field("Total Semesters", "📅 e.g. 8")
        grid.addWidget(self.total_sem_lbl, 4, 1)
        grid.addWidget(self.total_sem_entry, 5, 1)
        self.pass_lbl, self.pass_entry = self._create_field("Password", "🔒 Password", is_password=True)
        grid.addWidget(self.pass_lbl, 6, 0)
        grid.addWidget(self.pass_entry, 7, 0)
        self.confirm_lbl, self.confirm_entry = self._create_field("Confirm Password", "🔒 Confirm Password", is_password=True)
        grid.addWidget(self.confirm_lbl, 6, 1)
        grid.addWidget(self.confirm_entry, 7, 1)
        scroll.setWidget(form_widget)
        card_layout.addWidget(scroll)
        self.terms_check = QCheckBox("I agree to the Terms & Conditions.")
        self.terms_check.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 11px;")
        card_layout.addWidget(self.terms_check, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("CANCEL")
        btn_cancel.setFixedHeight(45)
        btn_cancel.setStyleSheet(f"QPushButton {{ background: transparent; border: 1px solid {COLOR_BORDER}; color: {COLOR_TEXT_MAIN}; border-radius: 10px; font-weight: bold; }} QPushButton:hover {{ background: {COLOR_BG_APP}; }}")
        btn_cancel.clicked.connect(self.on_back_click)
        btn_layout.addWidget(btn_cancel)
        btn_reg = QPushButton("REGISTER NOW")
        btn_reg.setFixedHeight(45)
        btn_reg.setStyleSheet(f"QPushButton {{ background: {COLOR_PRIMARY}; color: white; border-radius: 10px; font-weight: bold; }} QPushButton:hover {{ background: #00B4D8; }}")
        btn_reg.clicked.connect(self._handle_register)
        btn_layout.addWidget(btn_reg)
        card_layout.addLayout(btn_layout)
        content_layout.addWidget(self.card)
        self.main_layout.addWidget(content_area)

    def _create_field(self, label_text, placeholder, is_password=False):
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 11px; font-weight: bold;")
        entry = QLineEdit()
        entry.setPlaceholderText(placeholder)
        if is_password: entry.setEchoMode(QLineEdit.EchoMode.Password)
        entry.setFixedHeight(40)
        entry.setStyleSheet(f"QLineEdit {{ background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 10px; padding: 0 12px; color: {COLOR_TEXT_MAIN}; }} QLineEdit:focus {{ border: 2px solid {COLOR_PRIMARY}; }}")
        return lbl, entry

    def _get_combo_style(self):
        return f"QComboBox {{ background-color: {COLOR_BG_APP}; border: 1px solid {COLOR_BORDER}; border-radius: 10px; padding: 0 12px; color: {COLOR_TEXT_MAIN}; }} QComboBox::drop-down {{ border: none; }} QComboBox QAbstractItemView {{ background-color: {COLOR_BG_CARD}; color: {COLOR_TEXT_MAIN}; selection-background-color: {COLOR_PRIMARY}; border: 1px solid {COLOR_BORDER}; }}"

    def _handle_register(self):
        if not self.terms_check.isChecked():
            print("Please agree to terms.")
            return
        
        email = self.email_entry.text()
        full_name = self.name_entry.text()
        major = self.major_combo.currentText()
        password = self.pass_entry.text()
        confirm = self.confirm_entry.text()
        
        if not email or not full_name or not password:
            print("Please fill in all required fields.")
            return
            
        if password != confirm:
            print("Passwords do not match.")
            return
            
        print(f"Registering student: {full_name} ({email})")
        try:
            crud.save_student_profile(email, full_name, major)
            if self.on_register:
                self.on_register(email, password)
        except Exception as e:
            print(f"Registration error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    reg = RegisterPage(on_back_click=lambda: print("Back"))
    window.setCentralWidget(reg)
    window.resize(1100, 800)
    window.show()
    sys.exit(app.exec())
