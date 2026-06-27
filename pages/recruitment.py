import sys
import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QStackedWidget,
                             QLineEdit, QGraphicsDropShadowEffect, QProgressBar, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

from core.config import (COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB, 
                         COLOR_BORDER, COLOR_BG_APP, COLOR_BG_CARD)
from ui_core.neumorphic_components import NeumorphicFrame, GlowingButton
from ui_core.components import AnimationEngine

# ==================================================
# MOCK DATA
# ==================================================
MOCK_JOBS = [
    {
        "id": 1,
        "title": "Junior AI Engineer",
        "company": "DeepMind Vietnam",
        "salary": "$1,200 - $2,000",
        "location": "Ho Chi Minh City (Hybrid)",
        "posted_date": "1 day ago",
        "description": "We are seeking a Junior AI Engineer to help build state-of-the-art machine learning models. You will work alongside senior researchers to deploy and optimize neural networks on cloud edge devices.\n\nKey Responsibilities:\n- Preprocess large-scale textual and visual datasets.\n- Train and evaluate PyTorch/TensorFlow models.\n- Integrate model endpoints into our client dashboard application.\n- Document experimental results and participate in code reviews.\n\nRequired Qualifications:\n- Strong Python programming skills.\n- Familiarity with deep learning frameworks (PyTorch preferred).\n- Knowledge of Docker and CI/CD pipelines.",
        "skills": ["Python", "PyTorch", "Git", "FastAPI", "Docker"],
        "created_date": "May 26, 2026"
    },
    {
        "id": 2,
        "title": "UI/UX Designer",
        "company": "Aether Studio",
        "salary": "$800 - $1,500",
        "location": "Hanoi (Remote)",
        "posted_date": "2 days ago",
        "description": "Aether Studio is looking for a creative UI/UX Designer to design interfaces for modern desktop and mobile applications. You will create wireframes, high-fidelity mockups, and interactive prototypes that prioritize accessibility and gorgeous visuals.\n\nKey Responsibilities:\n- Collaborate with product managers to define user flows.\n- Design clean visual layouts following modern Figma guidelines.\n- Create graphic assets, illustrations, and customized icons.\n- Conduct usability testing and iterate based on user feedback.",
        "skills": ["Figma", "UI Design", "Prototyping", "Design Systems", "Adobe CC"],
        "created_date": "May 25, 2026"
    },
    {
        "id": 3,
        "title": "Frontend Developer (React)",
        "company": "SaaSify Tech",
        "salary": "$1,000 - $1,800",
        "location": "Da Nang (On-site)",
        "posted_date": "3 days ago",
        "description": "Join our frontend engineering team to build scalable, responsive web dashboards. We specialize in real-time telemetry systems and require a developer with strong state-management experience.\n\nKey Responsibilities:\n- Implement clean component architectures using React and TypeScript.\n- Optimize web application loading speed and rendering performance.\n- Work closely with backend engineers to integrate RESTful APIs.\n- Cover frontend components with unit tests using Jest.",
        "skills": ["JavaScript", "React", "TypeScript", "HTML5/CSS3", "TailwindCSS"],
        "created_date": "May 24, 2026"
    },
    {
        "id": 4,
        "title": "Python Backend Developer",
        "company": "Nexus Solutions",
        "salary": "$1,100 - $1,900",
        "location": "Ho Chi Minh City (Hybrid)",
        "posted_date": "4 days ago",
        "description": "Nexus Solutions is looking for a backend developer skilled in Python and asynchronous database systems. You will build and optimize core microservices that power millions of active user requests.\n\nKey Responsibilities:\n- Design, implement, and maintain FastAPI/SQLAlchemy endpoints.\n- Optimize PostgreSQL query performances and database indexing.\n- Set up secure authentication systems (OAuth2, JWT).\n- Containerize backend environments using Docker compose.",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "REST API"],
        "created_date": "May 23, 2026"
    },
    {
        "id": 5,
        "title": "Data Scientist",
        "company": "Fintech Lab",
        "salary": "$1,500 - $2,500",
        "location": "Hanoi (Hybrid)",
        "posted_date": "5 days ago",
        "description": "We are seeking a Data Scientist to join our risk assessment team. You will analyze historical financial transactions, identify fraud patterns, and build predictive classifiers.\n\nKey Responsibilities:\n- Perform exploratory data analysis (EDA) using Pandas and Seaborn.\n- Build and train XGBoost/RandomForest classifiers.\n- Deploy real-time inference models into production environments.\n- Write SQL queries to aggregate transactional data from warehouses.",
        "skills": ["Python", "Pandas", "Scikit-Learn", "SQL", "Data Analytics"],
        "created_date": "May 22, 2026"
    },
    {
        "id": 6,
        "title": "DevOps Engineer",
        "company": "Skyward Cloud Services",
        "salary": "$1,800 - $3,000",
        "location": "Ho Chi Minh City (Remote)",
        "posted_date": "1 week ago",
        "description": "Skyward Cloud Services is hiring a DevOps engineer to manage our multi-region Kubernetes deployments. You will automate CI/CD pipelines and configure monitoring and alerting services.\n\nKey Responsibilities:\n- Configure GitLab CI/GitHub Actions workflows for automated builds.\n- Provision cloud infrastructure using Terraform.\n- Manage Kubernetes clusters (EKS/GKE) and Helm charts.\n- Implement monitoring stacks using Prometheus and Grafana.",
        "skills": ["Kubernetes", "Docker", "Terraform", "CI/CD", "AWS", "Prometheus"],
        "created_date": "May 20, 2026"
    },
    {
        "id": 7,
        "title": "Mobile App Intern (Flutter)",
        "company": "SwiftApp Inc.",
        "salary": "$400 - $600",
        "location": "Da Nang (Hybrid)",
        "posted_date": "1 week ago",
        "description": "SwiftApp Inc. is looking for a Flutter Developer Intern to support the development of cross-platform apps for iOS and Android. You will learn modern application architectures and state management systems under direct mentorship.\n\nKey Responsibilities:\n- Write clean, maintainable Dart code using Provider/Bloc state management.\n- Implement complex custom UI elements and micro-animations.\n- Integrate local caching, native APIs, and third-party push notifications.\n- Publish apps to Apple App Store and Google Play Console.",
        "skills": ["Flutter", "Dart", "Mobile Design", "REST APIs", "Git"],
        "created_date": "May 20, 2026"
    },
    {
        "id": 8,
        "title": "AI Product Manager",
        "company": "GenAI Tech",
        "salary": "$2,000 - $3,500",
        "location": "Hanoi (On-site)",
        "posted_date": "2 weeks ago",
        "description": "We are seeking a Product Manager to lead our newly formed Generative AI user applications division. You will work at the intersection of business strategy, AI engineering, and user-centric design.\n\nKey Responsibilities:\n- Define product vision, roadmap, and core features.\n- Conduct market research and compile user persona reports.\n- Align cross-functional engineering, design, and marketing teams.\n- Analyze metrics to evaluate feature performance and optimize conversion.",
        "skills": ["Agile", "Product Management", "AI/ML Concepts", "Wireframing", "Analytics"],
        "created_date": "May 13, 2026"
    }
]

# ==================================================
# COMPACT JOB CARD
# ==================================================
class JobCard(QFrame):
    clicked = pyqtSignal(dict)
    
    def __init__(self, job_data, is_selected=False, parent=None):
        super().__init__(parent)
        self.job_data = job_data
        self.is_selected = is_selected
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(115)
        
        self.setup_ui()
        self.update_style()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        # Header (Job Title + Posted Date)
        header_h = QHBoxLayout()
        header_h.setSpacing(10)
        
        self.title_lbl = QLabel(self.job_data.get("title", ""))
        self.title_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #0F172A; background: transparent; border: none;")
        self.title_lbl.setWordWrap(False)
        
        self.date_lbl = QLabel(self.job_data.get("posted_date", ""))
        self.date_lbl.setStyleSheet("font-size: 10px; font-weight: 500; color: #64748B; background: transparent; border: none;")
        self.date_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        header_h.addWidget(self.title_lbl, stretch=1)
        header_h.addWidget(self.date_lbl)
        layout.addLayout(header_h)
        
        # Company
        self.company_lbl = QLabel(self.job_data.get("company", ""))
        self.company_lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #2563EB; background: transparent; border: none;")
        layout.addWidget(self.company_lbl)
        
        # Metadata (Salary & Location)
        meta_h = QHBoxLayout()
        meta_h.setSpacing(12)
        
        self.salary_lbl = QLabel(f"💵 {self.job_data.get('salary', '')}")
        self.salary_lbl.setStyleSheet("font-size: 11px; font-weight: 500; color: #475569; background: transparent; border: none;")
        
        self.loc_lbl = QLabel(f"📍 {self.job_data.get('location', '')}")
        self.loc_lbl.setStyleSheet("font-size: 11px; font-weight: 500; color: #475569; background: transparent; border: none;")
        self.loc_lbl.setWordWrap(False)
        
        meta_h.addWidget(self.salary_lbl)
        meta_h.addWidget(self.loc_lbl, stretch=1)
        layout.addLayout(meta_h)
        
        layout.addStretch()
        
    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("""
                JobCard {
                    background-color: #F0F9FF;
                    border: 2px solid #2563EB;
                    border-radius: 12px;
                }
            """)
        else:
            self.setStyleSheet("""
                JobCard {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
                JobCard:hover {
                    background-color: #F8FAFC;
                    border: 1px solid #CBD5E1;
                }
            """)
            
    def set_selected(self, selected):
        self.is_selected = selected
        self.update_style()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.job_data)
        super().mousePressEvent(event)

# ==================================================
# SEARCH BAR
# ==================================================
class JobSearchBar(QFrame):
    text_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(38)
        self.setStyleSheet("background: #F1F5F9; border-radius: 10px; border: none;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)
        
        icon = QLabel("🔍")
        icon.setStyleSheet("color: #64748B; font-size: 13px; background: transparent; border: none;")
        layout.addWidget(icon)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Search jobs, companies, skills...")
        self.input.setStyleSheet("background: transparent; color: #0F172A; font-size: 13px; font-weight: 500; border: none;")
        self.input.textChanged.connect(self.text_changed.emit)
        layout.addWidget(self.input)

# ==================================================
# SKELETON LOADER
# ==================================================
class JobDetailSkeleton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(24)
        
        # Top Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0) # Indeterminate
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #2563EB;
                border-radius: 1px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Header skeleton (Title & Company placeholder)
        header_v = QVBoxLayout()
        header_v.setSpacing(10)
        
        # Title bar placeholder
        title_placeholder = QFrame()
        title_placeholder.setFixedHeight(26)
        title_placeholder.setFixedWidth(280)
        title_placeholder.setStyleSheet("background-color: #F1F5F9; border-radius: 6px;")
        header_v.addWidget(title_placeholder)
        
        # Company bar placeholder
        company_placeholder = QFrame()
        company_placeholder.setFixedHeight(16)
        company_placeholder.setFixedWidth(130)
        company_placeholder.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 4px;")
        header_v.addWidget(company_placeholder)
        
        layout.addLayout(header_v)
        
        # Metadata row skeleton (three horizontal card placeholders)
        meta_h = QHBoxLayout()
        meta_h.setSpacing(16)
        for _ in range(3):
            meta_box = QFrame()
            meta_box.setFixedHeight(64)
            meta_box.setStyleSheet("background-color: #FFFFFF; border: 1px dashed #E2E8F0; border-radius: 10px;")
            meta_h.addWidget(meta_box)
        layout.addLayout(meta_h)
        
        # Description section skeleton (multiple lines of text)
        desc_v = QVBoxLayout()
        desc_v.setSpacing(12)
        
        section_placeholder = QFrame()
        section_placeholder.setFixedHeight(16)
        section_placeholder.setFixedWidth(120)
        section_placeholder.setStyleSheet("background-color: #F1F5F9; border-radius: 4px;")
        desc_v.addWidget(section_placeholder)
        
        for _ in range(4):
            line = QFrame()
            line.setFixedHeight(10)
            line.setStyleSheet("background-color: #F8FAFC; border-radius: 3px;")
            line.setMinimumWidth(200)
            desc_v.addWidget(line)
        layout.addLayout(desc_v)
        
        # Skills section skeleton
        skills_v = QVBoxLayout()
        skills_v.setSpacing(12)
        skills_title_placeholder = QFrame()
        skills_title_placeholder.setFixedHeight(16)
        skills_title_placeholder.setFixedWidth(100)
        skills_title_placeholder.setStyleSheet("background-color: #F1F5F9; border-radius: 4px;")
        skills_v.addWidget(skills_title_placeholder)
        
        skills_h = QHBoxLayout()
        skills_h.setSpacing(8)
        skills_h.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for w in [70, 85, 60, 90]:
            chip = QFrame()
            chip.setFixedHeight(26)
            chip.setFixedWidth(w)
            chip.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 13px;")
            skills_h.addWidget(chip)
        skills_v.addLayout(skills_h)
        layout.addLayout(skills_v)
        
        layout.addStretch()
        
        # Button skeleton
        btn_placeholder = QFrame()
        btn_placeholder.setFixedHeight(44)
        btn_placeholder.setFixedWidth(160)
        btn_placeholder.setStyleSheet("background-color: #F1F5F9; border-radius: 22px;")
        layout.addWidget(btn_placeholder)

# ==================================================
# JOB DETAIL PANEL
# ==================================================
class JobDetailPanel(QWidget):
    apply_clicked = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Scroll Area for details
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_widget.setObjectName("JobDetailContent")
        self.content_widget.setStyleSheet("#JobDetailContent { background-color: #FFFFFF; }")
        self.scroll_layout = QVBoxLayout(self.content_widget)
        self.scroll_layout.setContentsMargins(16, 16, 16, 16)
        self.scroll_layout.setSpacing(24)
        self.scroll.setWidget(self.content_widget)
        
        self.main_layout.addWidget(self.scroll, stretch=1)
        
        # Sticky Bottom Bar (Disabled / Read-only for Desktop application)
        self.bottom_bar = QFrame()
        self.bottom_bar.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-top: 1px solid #E2E8F0;
            }
        """)
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(16, 12, 16, 12)
        
        self.btn_apply = GlowingButton("Apply Now", width=180, height=44)
        self.btn_apply.setEnabled(True)
        self.btn_apply.clicked.connect(self._on_apply_clicked)
        self.btn_apply.setStyleSheet(self.btn_apply.styleSheet() + """
            QPushButton:disabled {
                background: #E2E8F0;
                color: #94A3B8;
                border: 1px solid #CBD5E1;
            }
        """)
        self.bottom_layout.addWidget(self.btn_apply)
        self.bottom_layout.addStretch()
        
        self.main_layout.addWidget(self.bottom_bar)
        
        self.job_data = None
        self.setup_ui()
        
    def setup_ui(self):
        # Header (Title + Company)
        self.header_v = QVBoxLayout()
        self.header_v.setSpacing(6)
        
        self.title_lbl = QLabel("Select a Job")
        self.title_lbl.setStyleSheet("font-size: 22px; font-weight: 800; color: #0F172A; background: transparent; border: none; letter-spacing: -0.5px;")
        self.title_lbl.setWordWrap(True)
        self.header_v.addWidget(self.title_lbl)
        
        self.company_lbl = QLabel("")
        self.company_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #2563EB; background: transparent; border: none;")
        self.header_v.addWidget(self.company_lbl)
        
        self.scroll_layout.addLayout(self.header_v)
        
        # Metadata grid / row (Salary, Location, Posted Date)
        self.meta_h = QHBoxLayout()
        self.meta_h.setSpacing(16)
        
        self.salary_card = self.create_meta_card("💵 Salary Range", "")
        self.loc_card = self.create_meta_card("📍 Location", "")
        self.date_card = self.create_meta_card("🗓 Posted Date", "")
        
        self.meta_h.addWidget(self.salary_card)
        self.meta_h.addWidget(self.loc_card)
        self.meta_h.addWidget(self.date_card)
        self.scroll_layout.addLayout(self.meta_h)
        
        # Description
        self.desc_v = QVBoxLayout()
        self.desc_v.setSpacing(10)
        
        self.desc_title = QLabel("Job Description")
        self.desc_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; background: transparent; border: none;")
        self.desc_v.addWidget(self.desc_title)
        
        self.desc_lbl = QLabel("")
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setStyleSheet("font-size: 13px; color: #475569; background: transparent; border: none;")
        self.desc_v.addWidget(self.desc_lbl)
        self.scroll_layout.addLayout(self.desc_v)
        
        # Skills/Tags
        self.skills_v = QVBoxLayout()
        self.skills_v.setSpacing(10)
        
        self.skills_title = QLabel("Key Requirements & Skills")
        self.skills_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; background: transparent; border: none;")
        self.skills_v.addWidget(self.skills_title)
        
        # Container for skills chips
        self.skills_widget = QWidget()
        self.skills_widget.setStyleSheet("background: transparent;")
        self.skills_layout = QHBoxLayout(self.skills_widget)
        self.skills_layout.setContentsMargins(0, 0, 0, 0)
        self.skills_layout.setSpacing(8)
        self.skills_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.skills_v.addWidget(self.skills_widget)
        self.scroll_layout.addLayout(self.skills_v)
        
        self.scroll_layout.addStretch()
        
    def create_meta_card(self, label_text, value_text):
        card = QFrame()
        card.setFixedHeight(64)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
            }
        """)
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(12, 10, 12, 10)
        c_layout.setSpacing(2)
        
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-size: 10px; font-weight: 600; color: #64748B; background: transparent; border: none;")
        
        val = QLabel(value_text)
        val.setStyleSheet("font-size: 12px; font-weight: 700; color: #0F172A; background: transparent; border: none;")
        val.setObjectName("val_label")
        
        c_layout.addWidget(lbl)
        c_layout.addWidget(val)
        return card
        
    def update_job(self, job_data):
        self.job_data = job_data
        if not job_data:
            return
            
        self.btn_apply.setEnabled(True)
        self.btn_apply.setText("Apply Now")
        self.title_lbl.setText(job_data.get("title", ""))
        self.company_lbl.setText(job_data.get("company", ""))
        
        # Update meta cards
        self.salary_card.findChild(QLabel, "val_label").setText(job_data.get("salary", ""))
        self.loc_card.findChild(QLabel, "val_label").setText(job_data.get("location", ""))
        self.date_card.findChild(QLabel, "val_label").setText(job_data.get("created_date", ""))
        
        # Update description with clean spacing
        desc_text = job_data.get("description", "")
        html_desc = desc_text.replace("\n", "<br>")
        self.desc_lbl.setText(f"<div style='line-height: 1.5;'>{html_desc}</div>")
        
        # Clear old skill chips
        while self.skills_layout.count():
            item = self.skills_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add new skill chips
        for skill in job_data.get("skills", []):
            chip = QLabel(skill)
            chip.setStyleSheet("""
                QLabel {
                    background-color: #F0FDF4;
                    color: #15803D;
                    border: 1px solid #BBF7D0;
                    border-radius: 12px;
                    padding: 4px 10px;
                    font-size: 11px;
                    font-weight: 700;
                }
            """)
            self.skills_layout.addWidget(chip)
            
    def _on_apply_clicked(self, checked=False):
        if self.job_data:
            self.apply_clicked.emit(self.job_data)

# ==================================================
# EMPTY STATE
# ==================================================
class JobEmptyState(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)
        
        icon = QLabel("💼")
        icon.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)
        
        title = QLabel("Select a job opportunity")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; background: transparent; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel("Choose a position from the list on the left to see full specifications, requirements, and submit your application details.")
        desc.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; background: transparent; border: none;")
        desc.setWordWrap(True)
        desc.setFixedWidth(320)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)


# ==================================================
# ERROR STATE
# ==================================================
class JobErrorState(QWidget):
    retry_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)
        
        icon = QLabel("⚠️")
        icon.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)
        
        self.title = QLabel("Failed to load details")
        self.title.setStyleSheet("font-size: 18px; font-weight: 800; color: #EF4444; background: transparent; border: none;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        
        self.desc = QLabel("Unable to fetch this job listing. The server might be offline or a connection timeout occurred.")
        self.desc.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; background: transparent; border: none;")
        self.desc.setWordWrap(True)
        self.desc.setFixedWidth(320)
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.desc)
        
        self.btn_retry = QPushButton("Retry Request")
        self.btn_retry.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_retry.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                font-weight: 700;
                font-size: 12px;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        self.btn_retry.clicked.connect(self.retry_clicked.emit)
        layout.addWidget(self.btn_retry, alignment=Qt.AlignmentFlag.AlignCenter)

    def set_error_message(self, message):
        self.desc.setText(message)


# ==================================================
# LIST ERROR CARD
# ==================================================
class ListErrorCard(QFrame):
    retry_clicked = pyqtSignal()
    
    def __init__(self, error_msg, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FEF2F2;
                border: 1px solid #FCA5A5;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        title = QLabel("⚠️ Failed to Sync Jobs")
        title.setStyleSheet("font-size: 13px; font-weight: 700; color: #991B1B; background: transparent; border: none;")
        layout.addWidget(title)
        
        desc = QLabel(error_msg)
        desc.setStyleSheet("font-size: 11px; font-weight: 500; color: #7F1D1D; background: transparent; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        self.btn_retry = QPushButton("Retry Sync")
        self.btn_retry.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_retry.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                font-weight: 700;
                font-size: 11px;
                border-radius: 6px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        self.btn_retry.clicked.connect(self.retry_clicked.emit)
        layout.addWidget(self.btn_retry, alignment=Qt.AlignmentFlag.AlignLeft)


def extract_skills(title, description):
    """
    Extracts key skills from the job title and description
    to populate UI chips when the database does not supply them.
    """
    known_skills = ["Python", "PyTorch", "Git", "FastAPI", "Docker", "Figma", 
                    "UI Design", "Prototyping", "Design Systems", "React", 
                    "TypeScript", "JavaScript", "HTML5", "CSS3", "TailwindCSS", 
                    "PostgreSQL", "Redis", "SQL", "Pandas", "Scikit-Learn", 
                    "Kubernetes", "Terraform", "CI/CD", "AWS", "Prometheus", 
                    "Flutter", "Dart", "Rust", "WebAssembly", "Go"]
    
    text = f"{title} {description}".lower()
    skills = []
    for skill in known_skills:
        if skill.lower() in text:
            skills.append(skill)
            
    if not skills:
        skills = ["Software Engineering", "Tech Development"]
        
    return skills

# ==================================================
# RECRUITMENT TOOLBAR
# ==================================================
class RecruitmentToolbar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(74)
        self.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(24)
        
        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        info_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title_h = QHBoxLayout()
        title_h.setSpacing(12)
        title = QLabel("Job Openings & Recruitment")
        title.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        
        badge = QLabel("Direct Matching")
        badge.setStyleSheet("font-size: 10px; font-weight: 800; color: #2563EB; background: #EFF6FF; padding: 2px 8px; border-radius: 6px; border: 1px solid #BFDBFE;")
        
        title_h.addWidget(title)
        title_h.addWidget(badge)
        title_h.addStretch()
        
        summary = QLabel("Explore job opportunities matching your major and skills, and apply directly")
        summary.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600; border: none;")
        
        info_v.addLayout(title_h)
        info_v.addWidget(summary)
        
        layout.addLayout(info_v)
        layout.addStretch()

# ==================================================
# MAIN PAGE WIDGET
# ==================================================
class RecruitmentPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("RecruitmentPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.selected_job_data = None
        self.current_filter_type = "All"
        self.search_query = ""
        self.applied_job_ids = []
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Toolbar
        self.toolbar = RecruitmentToolbar()
        self.main_layout.addWidget(self.toolbar)
        
        # Content Splitter Layout
        self.content_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.content_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #E2E8F0;
                width: 4px;
                margin: 0 4px;
            }
            QSplitter::handle:hover {
                background-color: #2563EB;
            }
        """)
        
        # --- LEFT PANEL (Job List) ---
        self.left_panel = QFrame()
        self.left_panel.setMinimumWidth(280)
        self.left_panel.setStyleSheet("background: transparent; border: none;")
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(12)
        
        # Search Bar
        self.search_bar = JobSearchBar()
        self.search_bar.text_changed.connect(self._on_search_changed)
        self.left_layout.addWidget(self.search_bar)
        
        # Filter Chips Row
        self.chips_widget = QWidget()
        self.chips_layout = QHBoxLayout(self.chips_widget)
        self.chips_layout.setContentsMargins(0, 0, 0, 0)
        self.chips_layout.setSpacing(6)
        
        self.chip_buttons = {}
        for chip_name in ["All", "Full-time", "Remote", "Hybrid", "Intern"]:
            btn = QPushButton(chip_name)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda checked, name=chip_name: self._on_chip_clicked(name))
            self.chips_layout.addWidget(btn)
            self.chip_buttons[chip_name] = btn
            
        self._update_chip_styles()
        self.left_layout.addWidget(self.chips_widget)
        
        # Job cards scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(8)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll.setWidget(self.list_container)
        self.left_layout.addWidget(self.scroll, stretch=1)
        
        # --- RIGHT PANEL (Job Detail Stack) ---
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """)
        
        # Shadow effect for right panel
        shadow = QGraphicsDropShadowEffect(self.right_panel)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 8)
        self.right_panel.setGraphicsEffect(shadow)
        
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)
        
        self.detail_stack = QStackedWidget()
        
        self.empty_state = JobEmptyState()
        self.skeleton = JobDetailSkeleton()
        self.detail_panel = JobDetailPanel()
        self.detail_panel.apply_clicked.connect(self._on_apply_clicked)
        self.error_state = JobErrorState()
        self.error_state.retry_clicked.connect(self._on_retry_detail)
        
        self.detail_stack.addWidget(self.empty_state)  # Index 0
        self.detail_stack.addWidget(self.skeleton)     # Index 1
        self.detail_stack.addWidget(self.detail_panel)  # Index 2
        self.detail_stack.addWidget(self.error_state)   # Index 3
        
        self.right_layout.addWidget(self.detail_stack)
        
        # Add to content splitter
        self.content_splitter.addWidget(self.left_panel)
        self.content_splitter.addWidget(self.right_panel)
        self.content_splitter.setSizes([380, 700])
        
        # Wrap splitter in layout with margin for breathing room
        wrapper_lay = QHBoxLayout()
        wrapper_lay.setContentsMargins(16, 16, 16, 16)
        wrapper_lay.addWidget(self.content_splitter)
        self.main_layout.addLayout(wrapper_lay)
        
        # Populate initial list by querying the API
        self.job_cards = []
        self.loaded_jobs = []
        self.fetch_jobs()
        
    def _on_chip_clicked(self, name):
        self.current_filter_type = name
        self._update_chip_styles()
        self.refresh_list()
        
    def _update_chip_styles(self):
        for name, btn in self.chip_buttons.items():
            if name == self.current_filter_type:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLOR_PRIMARY};
                        color: white;
                        font-weight: 700;
                        font-size: 11px;
                        border-radius: 14px;
                        padding: 4px 12px;
                        border: none;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #FFFFFF;
                        color: {COLOR_TEXT_SUB};
                        font-weight: 600;
                        font-size: 11px;
                        border-radius: 14px;
                        padding: 4px 12px;
                        border: 1px solid {COLOR_BORDER};
                    }}
                    QPushButton:hover {{
                        background-color: #F8FAFC;
                        border-color: #CBD5E1;
                    }}
                """)
                
    def _on_search_changed(self, text):
        self.search_query = text.lower().strip()
        self.refresh_list()
        
    def refresh(self):
        self.fetch_jobs()

    def fetch_jobs(self):
        # Fetch applied jobs in the background if logged in
        from database import crud
        student = crud.get_current_student()
        if student and student.get("email"):
            self.fetch_applied_jobs(student.get("email"))

        # Cancel previous list worker if it is running
        if hasattr(self, "jobs_worker") and self.jobs_worker.isRunning():
            try:
                self.jobs_worker.success.disconnect()
                self.jobs_worker.error.disconnect()
            except TypeError:
                pass
            self.jobs_worker.terminate()
            self.jobs_worker.wait()

        self.clear_job_list()
        
        # Show a subtle loading indicator in the job list
        loading_lbl = QLabel("Fetching latest jobs...")
        loading_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #64748B; padding: 20px; background: transparent;")
        self.list_layout.addWidget(loading_lbl)
        
        from modules.recruitment_worker import JobsFetchWorker
        self.jobs_worker = JobsFetchWorker()
        self.jobs_worker.success.connect(self._on_jobs_loaded)
        self.jobs_worker.error.connect(self._on_jobs_load_failed)
        self.jobs_worker.start()

    def _on_jobs_loaded(self, jobs):
        self.clear_job_list()
        
        # Enrich jobs with skills and posted date if they don't have them
        for job in jobs:
            if not job.get("skills"):
                job["skills"] = extract_skills(job.get("title", ""), job.get("description", ""))
                
            if not job.get("posted_date") or not job.get("created_date"):
                created_at = job.get("created_at")
                date_str = "Recent"
                if created_at:
                    try:
                        date_str = created_at.split()[0] if " " in created_at else created_at.split("T")[0]
                    except:
                        pass
                job["posted_date"] = date_str
                job["created_date"] = date_str
                
        self.loaded_jobs = jobs
        self.refresh_list()

    def _on_jobs_load_failed(self, error_msg):
        self.clear_job_list()
        
        # Show ListErrorCard in the list layout
        error_card = ListErrorCard(error_msg, self)
        error_card.retry_clicked.connect(self.fetch_jobs)
        self.list_layout.addWidget(error_card)

    def fetch_applied_jobs(self, email):
        if hasattr(self, "applications_worker") and self.applications_worker.isRunning():
            try:
                self.applications_worker.success.disconnect()
                self.applications_worker.error.disconnect()
            except TypeError:
                pass
            self.applications_worker.terminate()
            self.applications_worker.wait()

        from modules.recruitment_worker import ApplicationsFetchWorker
        self.applications_worker = ApplicationsFetchWorker(email)
        self.applications_worker.success.connect(self._on_applications_loaded)
        self.applications_worker.start()

    def _on_applications_loaded(self, applied_ids):
        self.applied_job_ids = applied_ids
        if self.selected_job_data:
            job_id = self.selected_job_data.get("id")
            if job_id in self.applied_job_ids:
                self.detail_panel.btn_apply.setEnabled(False)
                self.detail_panel.btn_apply.setText("Applied")

    def clear_job_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.job_cards.clear()
        
    def refresh_list(self):
        # Clear existing card widgets
        for card in self.job_cards:
            card.deleteLater()
        self.job_cards.clear()
        
        # Filter jobs based on search query and chip filter
        filtered_jobs = []
        jobs_to_filter = getattr(self, "loaded_jobs", [])
        
        for job in jobs_to_filter:
            # Chip filter
            matches_chip = False
            location = job.get("location", "").lower()
            title = job.get("title", "").lower()
            
            if self.current_filter_type == "All":
                matches_chip = True
            elif self.current_filter_type == "Remote" and "remote" in location:
                matches_chip = True
            elif self.current_filter_type == "Hybrid" and "hybrid" in location:
                matches_chip = True
            elif self.current_filter_type == "Intern" and "intern" in title:
                matches_chip = True
            elif self.current_filter_type == "Full-time" and "remote" not in location and "hybrid" not in location and "intern" not in title:
                matches_chip = True
                
            if not matches_chip:
                continue
                
            # Search filter
            if self.search_query:
                company = job.get("company", "").lower()
                description = job.get("description", "").lower()
                skills = [s.lower() for s in job.get("skills", [])]
                
                matches_search = (
                    self.search_query in title or
                    self.search_query in company or
                    self.search_query in description or
                    any(self.search_query in s for s in skills)
                )
                if not matches_search:
                    continue
                    
            filtered_jobs.append(job)
            
        # Draw cards
        for job in filtered_jobs:
            is_selected = self.selected_job_data and self.selected_job_data.get("id") == job.get("id")
            card = JobCard(job, is_selected=is_selected)
            card.clicked.connect(self._on_job_selected)
            self.list_layout.addWidget(card)
            self.job_cards.append(card)
            
        # If no jobs match
        if not jobs_to_filter and self.list_layout.count() == 0:
            empty_lbl = QLabel("No jobs loaded. Please verify connection or retry.")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("font-size: 12px; font-weight: 500; color: #64748B; padding: 20px;")
            empty_lbl.setWordWrap(True)
            self.list_layout.addWidget(empty_lbl)
            
        # If the currently selected job is no longer in the filtered list, clear selection
        if self.selected_job_data and not any(j.get("id") == self.selected_job_data.get("id") for j in filtered_jobs):
            self.selected_job_data = None
            self.detail_stack.setCurrentIndex(0)
            
    def _on_job_selected(self, job_data):
        self.selected_job_data = job_data
        
        # Update selection state visually on all cards
        for card in self.job_cards:
            card.set_selected(card.job_data.get("id") == job_data.get("id"))
            
        # Switch to skeleton loader page
        self.detail_stack.setCurrentIndex(1)
        
        # Cancel previous detail worker if running
        if hasattr(self, "detail_worker") and self.detail_worker.isRunning():
            try:
                self.detail_worker.success.disconnect()
                self.detail_worker.error.disconnect()
            except TypeError:
                pass
            self.detail_worker.terminate()
            self.detail_worker.wait()
            
        # Spawn new worker
        from modules.recruitment_worker import JobDetailFetchWorker
        self.detail_worker = JobDetailFetchWorker(job_data["id"])
        self.detail_worker.success.connect(self._on_detail_loaded)
        self.detail_worker.error.connect(self._on_detail_load_failed)
        self.detail_worker.start()
        
    def _on_detail_loaded(self, full_job_data):
        # Enrich the full_job_data just in case
        if not full_job_data.get("skills"):
            full_job_data["skills"] = extract_skills(full_job_data.get("title", ""), full_job_data.get("description", ""))
            
        if not full_job_data.get("posted_date") or not full_job_data.get("created_date"):
            created_at = full_job_data.get("created_at")
            date_str = "Recent"
            if created_at:
                try:
                    date_str = created_at.split()[0] if " " in created_at else created_at.split("T")[0]
                except:
                    pass
            full_job_data["posted_date"] = date_str
            full_job_data["created_date"] = date_str
            
        if self.selected_job_data and self.selected_job_data.get("id") == full_job_data.get("id"):
            self.detail_panel.update_job(full_job_data)
            if full_job_data.get("id") in getattr(self, "applied_job_ids", []):
                self.detail_panel.btn_apply.setEnabled(False)
                self.detail_panel.btn_apply.setText("Applied")
            self.detail_stack.setCurrentIndex(2)
            AnimationEngine.fade_in_widget(self.detail_panel.content_widget, delay_ms=0, duration=400)
            
    def _on_detail_load_failed(self, error_msg):
        self.error_state.set_error_message(error_msg)
        self.detail_stack.setCurrentIndex(3)
        
    def _on_retry_detail(self):
        if self.selected_job_data:
            self._on_job_selected(self.selected_job_data)

    def _on_apply_clicked(self, job_data):
        from database import crud
        student = crud.get_current_student()
        if not student:
            QMessageBox.warning(self, "Warning", "You must be logged in to apply for jobs.")
            return

        email = student.get("email")
        display_name = student.get("display_name") or student.get("username") or email
        if not email:
            QMessageBox.warning(self, "Warning", "Student profile has no email address. Cannot apply.")
            return

        # Cancel active apply worker if running
        if hasattr(self, "apply_worker") and self.apply_worker.isRunning():
            try:
                self.apply_worker.success.disconnect()
                self.apply_worker.error.disconnect()
            except TypeError:
                pass
            self.apply_worker.terminate()
            self.apply_worker.wait()

        # Disable button and update text
        self.detail_panel.btn_apply.setEnabled(False)
        self.detail_panel.btn_apply.setText("Applying...")

        # Start background worker
        from modules.recruitment_worker import JobApplyWorker
        self.apply_worker = JobApplyWorker(
            job_data.get("id"), 
            email, 
            display_name,
            major=student.get("major"),
            student_year=student.get("student_year", 1)
        )
        self.apply_worker.success.connect(self._on_apply_success)
        self.apply_worker.error.connect(self._on_apply_failed)
        self.apply_worker.start()

    def _on_apply_success(self):
        QMessageBox.information(self, "Success", "Job application submitted successfully!")
        self.detail_panel.btn_apply.setEnabled(False)
        self.detail_panel.btn_apply.setText("Applied")
        if self.selected_job_data:
            job_id = self.selected_job_data.get("id")
            if job_id not in self.applied_job_ids:
                self.applied_job_ids.append(job_id)

    def _on_apply_failed(self, error_msg):
        QMessageBox.critical(self, "Error", f"Failed to submit job application:\n{error_msg}")
        self.detail_panel.btn_apply.setEnabled(True)
        self.detail_panel.btn_apply.setText("Apply Now")

    def cleanup(self):
        """
        Safely stops and terminates all active worker threads.
        """
        if hasattr(self, "jobs_worker") and self.jobs_worker.isRunning():
            try:
                self.jobs_worker.success.disconnect()
                self.jobs_worker.error.disconnect()
            except TypeError:
                pass
            self.jobs_worker.terminate()
            self.jobs_worker.wait()
            
        if hasattr(self, "detail_worker") and self.detail_worker.isRunning():
            try:
                self.detail_worker.success.disconnect()
                self.detail_worker.error.disconnect()
            except TypeError:
                pass
            self.detail_worker.terminate()
            self.detail_worker.wait()

        if hasattr(self, "apply_worker") and self.apply_worker.isRunning():
            try:
                self.apply_worker.success.disconnect()
                self.apply_worker.error.disconnect()
            except TypeError:
                pass
            self.apply_worker.terminate()
            self.apply_worker.wait()

        if hasattr(self, "applications_worker") and self.applications_worker.isRunning():
            try:
                self.applications_worker.success.disconnect()
                self.applications_worker.error.disconnect()
            except TypeError:
                pass
            self.applications_worker.terminate()
            self.applications_worker.wait()
