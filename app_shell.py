import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QStackedWidget, QFrame, QScrollArea,
    QFormLayout, QLineEdit, QCalendarWidget, QGridLayout, QTextBrowser,
    QListWidget, QListWidgetItem, QCheckBox, QProgressBar, QButtonGroup,
    QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from pages.job_portal.job_portal_page import JobPortalPage as ModernJobPortalPage

# ==========================================
# PAGE 0: Dashboard
# ==========================================
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Welcome Banner
        banner = QLabel("Welcome to AI-Career Bridge Dashboard!")
        banner.setStyleSheet("background-color: #38BDF8; color: white; font-size: 24px; font-weight: bold; padding: 20px; border-radius: 10px;")
        layout.addWidget(banner)

        # KPI Cards (Row of 4)
        kpi_layout = QHBoxLayout()
        for title, val in [("Courses", "12"), ("Tasks", "5 Pending"), ("Jobs Applied", "3"), ("AI Sessions", "8")]:
            card = QFrame()
            card.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #E2E8F0;")
            card_layout = QVBoxLayout(card)
            lbl_t = QLabel(title)
            lbl_t.setStyleSheet("color: #64748B; font-weight: bold; border: none;")
            lbl_v = QLabel(val)
            lbl_v.setStyleSheet("font-size: 20px; color: #0F172A; font-weight: bold; border: none;")
            card_layout.addWidget(lbl_t)
            card_layout.addWidget(lbl_v)
            kpi_layout.addWidget(card)
        layout.addLayout(kpi_layout)

        # Tasks Horizontal Layout
        tasks_frame = QFrame()
        tasks_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #E2E8F0; padding: 10px;")
        tasks_layout = QHBoxLayout(tasks_frame)
        lbl_recent = QLabel("Recent Tasks: ")
        lbl_recent.setStyleSheet("border: none; font-weight: bold;")
        tasks_layout.addWidget(lbl_recent)
        for task in ["Finish AI Essay", "Review Math Notes", "Apply to Google"]:
            btn = QPushButton(task)
            btn.setStyleSheet("background-color: #F1F5F9; border: none; border-radius: 5px; padding: 8px 12px;")
            tasks_layout.addWidget(btn)
        tasks_layout.addStretch()
        
        layout.addWidget(tasks_frame)
        layout.addStretch()

# ==========================================
# PAGE 1: Profile & CV Builder
# ==========================================
class ProfileBuilderPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Left: Forms
        left_panel = QWidget()
        form_layout = QFormLayout(left_panel)
        form_layout.addRow(QLabel("<b>Profile & CV Details</b>"))
        form_layout.addRow("Full Name:", QLineEdit())
        form_layout.addRow("Email:", QLineEdit())
        form_layout.addRow("Education:", QLineEdit())
        form_layout.addRow("Experience:", QLineEdit())
        form_layout.addRow("Skills:", QLineEdit())
        
        # Right: A4 Preview
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white; border: 1px solid #E2E8F0; border-radius: 5px; min-width: 400px;")
        right_layout = QVBoxLayout(right_panel)
        preview_lbl = QLabel("CV Preview (A4 format)")
        preview_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_lbl.setStyleSheet("color: #94A3B8; font-size: 18px; border: none;")
        right_layout.addWidget(preview_lbl)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 500])

        layout.addWidget(splitter)

# ==========================================
# PAGE 2: Academic Roadmap
# ==========================================
class AcademicRoadmapPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        title = QLabel("Your Academic Roadmap")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        content_layout.addWidget(title)

        courses = ["Introduction to AI", "Data Structures", "Machine Learning", "Deep Learning", "Capstone Project"]
        for i, course in enumerate(courses):
            item = QFrame()
            item.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px; border: 1px solid #E2E8F0; margin-bottom: 10px;")
            item_layout = QVBoxLayout(item)
            
            chk = QCheckBox(course)
            chk.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")
            if i < 2:
                chk.setChecked(True)
            
            prog = QProgressBar()
            prog.setValue(100 if i < 2 else (50 if i == 2 else 0))
            prog.setStyleSheet("border: none; background-color: #E2E8F0; border-radius: 3px; height: 8px;")
            
            item_layout.addWidget(chk)
            item_layout.addWidget(prog)
            content_layout.addWidget(item)
            
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

# ==========================================
# PAGE 3: Study Tasks & Calendar
# ==========================================
class StudyTasksPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Calendar
        cal = QCalendarWidget()
        cal.setStyleSheet("background-color: white; border: 1px solid #E2E8F0; border-radius: 8px; color: black;")
        layout.addWidget(cal)

        # Kanban Board
        kanban_layout = QHBoxLayout()
        for status in ["To Do", "In Progress", "Done"]:
            col = QFrame()
            col.setStyleSheet("background-color: #F8FAFC; border-radius: 8px; border: 1px solid #E2E8F0;")
            col_layout = QVBoxLayout(col)
            lbl = QLabel(status)
            lbl.setStyleSheet("font-weight: bold; font-size: 16px; border: none;")
            col_layout.addWidget(lbl)
            
            # Dummy tasks
            task = QLabel(f"Task for {status}")
            task.setStyleSheet("background-color: white; padding: 10px; border-radius: 5px; border: 1px solid #CBD5E1;")
            col_layout.addWidget(task)
            col_layout.addStretch()
            
            kanban_layout.addWidget(col)
            
        layout.addLayout(kanban_layout)

# ==========================================
# PAGE 5: AI Mentor & Chat
# ==========================================
class AIMentorPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Chat History
        self.chat_browser = QTextBrowser()
        self.chat_browser.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #E2E8F0; padding: 10px; font-size: 14px; color: #0F172A;")
        self.chat_browser.append("<b>AI Mentor:</b> Hello! How can I help you with your career or studies today?")
        layout.addWidget(self.chat_browser)

        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setStyleSheet("background-color: white; border-radius: 20px; border: 1px solid #E2E8F0; padding: 10px 15px; font-size: 14px; color: #0F172A;")
        self.input_field.returnPressed.connect(self.send_message)
        
        btn_send = QPushButton("Send")
        btn_send.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_send.setStyleSheet("background-color: #38BDF8; color: white; border: none; border-radius: 20px; padding: 10px 20px; font-weight: bold;")
        btn_send.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(btn_send)
        layout.addLayout(input_layout)

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.chat_browser.append(f"<b>You:</b> {text}")
            self.input_field.clear()
            self.chat_browser.append("<b>AI Mentor:</b> I am analyzing your request...")

# ==========================================
# PAGE 6: Certifications
# ==========================================
class CertificationsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Your Certifications")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        certs = ["AWS Cloud Practitioner", "Coursera ML Specialization", "Google IT Support"]
        
        row, col = 0, 0
        for cert in certs:
            card = QFrame()
            card.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #E2E8F0; padding: 20px;")
            c_layout = QVBoxLayout(card)
            
            icon = QLabel("📜")
            icon.setStyleSheet("font-size: 40px; border: none;")
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            lbl_c = QLabel(cert)
            lbl_c.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_c.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px; border: none;")
            
            badge = QLabel("✅ Verified")
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setStyleSheet("color: #10B981; font-weight: bold; border: none;")
            
            c_layout.addWidget(icon)
            c_layout.addWidget(lbl_c)
            c_layout.addWidget(badge)
            
            grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
                
        layout.addLayout(grid)
        layout.addStretch()

# ==========================================
# PAGE 7: Notifications
# ==========================================
class NotificationsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Notifications")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget { background-color: transparent; border: none; } 
            QListWidget::item { background-color: white; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 8px; padding: 15px; color: #0F172A; }
            QListWidget::item:hover { background-color: #F8FAFC; }
        """)
        
        notifs = [
            "🧑‍🏫 Mentor Sarah accepted your request.",
            "📅 New assignment due in 'Machine Learning'.",
            "🚀 Google viewed your application.",
            "🎉 You earned the 'Fast Learner' badge!"
        ]
        
        for n in notifs:
            item = QListWidgetItem(n)
            list_widget.addItem(item)
            
        layout.addWidget(list_widget)

# ==========================================
# PAGE 8: Settings
# ==========================================
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        panel = QFrame()
        panel.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #E2E8F0; padding: 30px;")
        form = QFormLayout(panel)
        form.setSpacing(20)

        lbl_title = QLabel("<b>Account Settings</b>")
        lbl_title.setStyleSheet("font-size: 18px; border: none; margin-bottom: 10px;")
        form.addRow(lbl_title)
        
        inp_name = QLineEdit("John Doe")
        inp_name.setStyleSheet("padding: 8px; border: 1px solid #E2E8F0; border-radius: 5px;")
        form.addRow("Full Name:", inp_name)
        
        inp_email = QLineEdit("john.doe@example.com")
        inp_email.setStyleSheet("padding: 8px; border: 1px solid #E2E8F0; border-radius: 5px;")
        form.addRow("Email:", inp_email)
        
        btn_pwd = QPushButton("Change Password")
        btn_pwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_pwd.setStyleSheet("background-color: #F1F5F9; color: #0F172A; border: none; border-radius: 5px; padding: 8px;")
        form.addRow("Password:", btn_pwd)
        
        theme_toggle = QCheckBox("Enable Dark Theme")
        form.addRow("Appearance:", theme_toggle)
        
        layout.addWidget(panel)
        layout.addStretch()

# ==========================================
# SIDEBAR BUTTON
# ==========================================
class SidebarButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)
        self.setFixedHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #64748B;
                border: none;
                border-left: 4px solid transparent;
                text-align: left;
                padding-left: 15px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #F8FAFC;
            }
            QPushButton:checked {
                background-color: #E0F2FE;
                color: #0284C7;
                border-left: 4px solid #38BDF8;
                font-weight: bold;
            }
        """)

# ==========================================
# MAIN APPLICATION SHELL
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Career Bridge")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #F8FAFC;") # App Background

        # 1. MAIN LAYOUT (QHBoxLayout)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 2. LEFT SIDEBAR
        self._setup_sidebar()

        # 3. RIGHT STACKED WIDGET
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget, 1) # Expanding

        # Initialize and add pages
        self._setup_pages()

    def _setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)

        # Logo
        logo = QLabel("✦ AI-Career Bridge")
        logo.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: bold; padding-left: 15px; margin-bottom: 20px; border: none;")
        sidebar_layout.addWidget(logo)

        # 9 Categories
        items = [
            "Dashboard (Tổng quan)",
            "Profile & CV Builder (Hồ sơ & CV)",
            "Academic Roadmap (Lộ trình học tập)",
            "Study Tasks & Calendar (Nhiệm vụ & Lịch)",
            "Job Portal (Tuyển dụng với AI)",
            "AI Mentor & Chat (Trợ lý AI)",
            "Certifications (Chứng chỉ)",
            "Notifications (Thông báo)",
            "Settings (Cài đặt)"
        ]
        
        icons = ["🏠", "📝", "🗺️", "📅", "💼", "🤖", "📜", "🔔", "⚙️"]

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        for i, text in enumerate(items):
            btn = SidebarButton(f"{icons[i]}   {i}. {text}")
            self.btn_group.addButton(btn, i)
            sidebar_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, idx=i: self.stacked_widget.setCurrentIndex(idx))

        sidebar_layout.addStretch()
        self.main_layout.addWidget(sidebar)

        # Select first item
        self.btn_group.button(0).setChecked(True)

    def _setup_pages(self):
        self.stacked_widget.addWidget(DashboardPage())       # 0
        self.stacked_widget.addWidget(ProfileBuilderPage())  # 1
        self.stacked_widget.addWidget(AcademicRoadmapPage()) # 2
        self.stacked_widget.addWidget(StudyTasksPage())      # 3
        self.stacked_widget.addWidget(ModernJobPortalPage()) # 4
        self.stacked_widget.addWidget(AIMentorPage())        # 5
        self.stacked_widget.addWidget(CertificationsPage())  # 6
        self.stacked_widget.addWidget(NotificationsPage())   # 7
        self.stacked_widget.addWidget(SettingsPage())        # 8

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
