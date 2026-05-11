import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout,QStackedWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from config import get_global_stylesheet

# Import our modularized pages
from pages.dashboard import DashboardPage
from pages.profile import ProfilePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Career Bridge | Masterclass")
        self.resize(1200, 800)

        # 1. The Central Canvas
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainContainer")
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet("background-color: #1E2A38;")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        #buttons
        btn_dash = QPushButton("📊")
        btn_dash.setProperty("class", "NavButton")

        btn_prof = QPushButton("👤")
        btn_prof.setProperty("class", "NavButton")

        sidebar_layout.addWidget(btn_dash)
        sidebar_layout.addWidget(btn_prof)
        self.pages_container = QStackedWidget()

        #add pages for the buttons
        self.pages_container.addWidget(DashboardPage()) #0
        self.pages_container.addWidget(ProfilePage()) #1

        btn_dash.clicked.connect(lambda: self.pages_container.setCurrentIndex(0))
        btn_prof.clicked.connect(lambda: self.pages_container.setCurrentIndex(1))
        # Apply our Dark Theme from config.py

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages_container)
        self.setStyleSheet(get_global_stylesheet())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
