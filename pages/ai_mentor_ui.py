import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextBrowser, QLineEdit, QFrame,
                             QScrollArea, QGridLayout, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QFont, QColor

def create_shadow():
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 10))
    return shadow

class AIMentorPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("AIMentorPage")
        
        # Main background
        self.setStyleSheet("background-color: #F8FAFC;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F8FAFC; }")
        
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Content Layout
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)

        # ====================
        # TOP TOOLBAR
        # ====================
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        # Breadcrumbs
        lbl_breadcrumbs = QLabel("AI Mentor / Career Guidance")
        lbl_breadcrumbs.setStyleSheet("color: #64748B; font-size: 14px; font-weight: 500;")
        header_layout.addWidget(lbl_breadcrumbs)
        
        header_layout.addStretch()

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search mentors or topics... (Ctrl+K)")
        self.search_bar.setFixedWidth(280)
        self.search_bar.setFixedHeight(36)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 18px;
                padding: 0 16px;
                color: #0F172A;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
            }
        """)
        header_layout.addWidget(self.search_bar)

        # Book Session Button
        btn_book = QPushButton("Book Session")
        btn_book.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_book.setFixedHeight(36)
        btn_book.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: white;
                border-radius: 18px;
                padding: 0 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #1E293B;
            }
        """)
        header_layout.addWidget(btn_book)

        # Avatar
        lbl_avatar = QLabel()
        lbl_avatar.setFixedSize(36, 36)
        lbl_avatar.setStyleSheet("""
            background: #2DD4BF;
            border-radius: 18px;
        """)
        header_layout.addWidget(lbl_avatar)

        content_layout.addLayout(header_layout)

        # ====================
        # BODY LAYOUT
        # ====================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(24)

        # --------------------
        # LEFT AREA
        # --------------------
        left_area = QWidget()
        left_layout = QVBoxLayout(left_area)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(24)

        # Section 1: Mentor Overview Card
        overview_card = QFrame()
        overview_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38BDF8, stop:1 #2DD4BF);
                border-radius: 20px;
            }
        """)
        overview_card.setMinimumHeight(180)
        overview_layout = QVBoxLayout(overview_card)
        overview_layout.setContentsMargins(32, 32, 32, 32)
        
        lbl_greeting = QLabel("Your Career Journey Starts Here.")
        lbl_greeting.setStyleSheet("color: white; font-size: 28px; font-weight: 700; background: transparent;")
        overview_layout.addWidget(lbl_greeting)
        
        lbl_greeting_sub = QLabel("Get personalized guidance from industry experts and AI.")
        lbl_greeting_sub.setStyleSheet("color: #F8FAFC; font-size: 16px; background: transparent; margin-top: 4px;")
        overview_layout.addWidget(lbl_greeting_sub)
        
        overview_layout.addStretch()
        
        btn_actions_layout = QHBoxLayout()
        btn_find_mentor = QPushButton("Find Mentor")
        btn_find_mentor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_find_mentor.setStyleSheet("""
            QPushButton {
                background: white;
                color: #0F172A;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #F1F5F9;
            }
        """)
        
        btn_schedule = QPushButton("Schedule Session")
        btn_schedule.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_schedule.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: 1px solid white;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)
        btn_actions_layout.addWidget(btn_find_mentor)
        btn_actions_layout.addWidget(btn_schedule)
        btn_actions_layout.addStretch()
        overview_layout.addLayout(btn_actions_layout)

        left_layout.addWidget(overview_card)

        # Section 2: Recommended Mentors
        lbl_recommended = QLabel("Recommended Mentors")
        lbl_recommended.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700;")
        left_layout.addWidget(lbl_recommended)

        mentors_layout = QGridLayout()
        mentors_layout.setSpacing(16)
        
        mentors = [
            {"name": "Sarah Chen", "role": "Senior Data Scientist", "match": "95%"},
            {"name": "Alex Kumar", "role": "Lead Product Manager", "match": "92%"},
            {"name": "Elena Rodriguez", "role": "UX Researcher", "match": "88%"}
        ]

        for i, mentor in enumerate(mentors):
            m_card = QFrame()
            m_card.setGraphicsEffect(create_shadow())
            m_card.setStyleSheet("""
                QFrame {
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 20px;
                }
            """)
            m_layout = QVBoxLayout(m_card)
            m_layout.setContentsMargins(20, 20, 20, 20)
            
            # Avatar & Match
            m_top = QHBoxLayout()
            m_avatar = QLabel()
            m_avatar.setFixedSize(48, 48)
            m_avatar.setStyleSheet("background: #E2E8F0; border-radius: 24px; border: none;")
            m_top.addWidget(m_avatar)
            
            m_top.addStretch()
            
            m_match = QLabel(mentor["match"] + " Match")
            m_match.setStyleSheet("""
                color: #2DD4BF;
                background: #F0FDFA;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
                border: none;
            """)
            m_top.addWidget(m_match)
            m_layout.addLayout(m_top)
            
            # Name & Role
            m_name = QLabel(mentor["name"])
            m_name.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; margin-top: 8px; border: none;")
            m_layout.addWidget(m_name)
            
            m_role = QLabel(mentor["role"])
            m_role.setStyleSheet("color: #64748B; font-size: 13px; border: none;")
            m_layout.addWidget(m_role)
            
            m_layout.addStretch()
            
            # Connect Button
            m_btn = QPushButton("Connect")
            m_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            m_btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    color: #0F172A;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    padding: 8px 0;
                    font-weight: 600;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: #F8FAFC;
                    border-color: #CBD5E1;
                }
            """)
            m_layout.addWidget(m_btn)
            
            mentors_layout.addWidget(m_card, 0, i)

        left_layout.addLayout(mentors_layout)

        # Section 3: Career Guidance Panel (Split View)
        guidance_layout = QHBoxLayout()
        guidance_layout.setSpacing(24)

        # Timeline (Left Side of Split)
        timeline_card = QFrame()
        timeline_card.setGraphicsEffect(create_shadow())
        timeline_card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }
        """)
        timeline_layout = QVBoxLayout(timeline_card)
        timeline_layout.setContentsMargins(24, 24, 24, 24)
        
        lbl_timeline = QLabel("Career Roadmap")
        lbl_timeline.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700; border: none;")
        timeline_layout.addWidget(lbl_timeline)
        
        steps = ["Learn Python Basics", "Complete AI Project", "Build Portfolio", "Apply for Internships"]
        for i, step in enumerate(steps):
            s_layout = QHBoxLayout()
            s_dot = QLabel("•")
            s_dot.setStyleSheet("color: #38BDF8; font-size: 24px; font-weight: bold; border: none;")
            s_layout.addWidget(s_dot)
            s_text = QLabel(step)
            color = "#0F172A" if i < 2 else "#64748B"
            s_text.setStyleSheet(f"color: {color}; font-size: 14px; border: none; font-weight: {'600' if i < 2 else '400'};")
            s_layout.addWidget(s_text)
            s_layout.addStretch()
            timeline_layout.addLayout(s_layout)
        
        timeline_layout.addStretch()
        guidance_layout.addWidget(timeline_card, 1)

        # AI Assistant Chat (Right Side of Split)
        chat_card = QFrame()
        chat_card.setGraphicsEffect(create_shadow())
        chat_card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }
        """)
        chat_layout = QVBoxLayout(chat_card)
        chat_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_chat = QLabel("AI Mentor Assistant")
        lbl_chat.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        chat_layout.addWidget(lbl_chat)
        
        self.chat_box = QTextBrowser()
        self.chat_box.setStyleSheet("""
            QTextBrowser {
                background: transparent;
                border: none;
                color: #334155;
                font-size: 14px;
            }
        """)
        self.chat_box.setOpenExternalLinks(True)
        chat_layout.addWidget(self.chat_box)
        
        # Input Area
        input_frame = QWidget()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)
        
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Ask AI Mentor...")
        self.entry.setFixedHeight(40)
        self.entry.setStyleSheet("""
            QLineEdit {
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                color: #0F172A;
                padding: 0 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
                background: #FFFFFF;
            }
        """)
        self.entry.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.entry)
        
        btn_send = QPushButton("Send")
        btn_send.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_send.setFixedHeight(40)
        btn_send.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: white;
                border-radius: 8px;
                font-weight: 600;
                border: none;
                padding: 0 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1E293B;
            }
        """)
        btn_send.clicked.connect(self.send_message)
        input_layout.addWidget(btn_send)
        
        chat_layout.addWidget(input_frame)
        
        guidance_layout.addWidget(chat_card, 2) # Chat takes more space

        left_layout.addLayout(guidance_layout)
        body_layout.addWidget(left_area, 1)

        # --------------------
        # RIGHT AREA
        # --------------------
        right_area = QWidget()
        right_area.setFixedWidth(320)
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(24)

        # AI Insights Panel
        insights_card = QFrame()
        insights_card.setGraphicsEffect(create_shadow())
        insights_card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }
        """)
        insights_layout = QVBoxLayout(insights_card)
        insights_layout.setContentsMargins(20, 20, 20, 20)
        insights_layout.setSpacing(16)
        
        lbl_insights = QLabel("AI Insights")
        lbl_insights.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        insights_layout.addWidget(lbl_insights)
        
        # Career Probability
        cp_layout = QVBoxLayout()
        cp_layout.setSpacing(4)
        lbl_cp = QLabel("Data Scientist Role Match")
        lbl_cp.setStyleSheet("color: #64748B; font-size: 13px; border: none;")
        cp_layout.addWidget(lbl_cp)
        
        cp_bar_layout = QHBoxLayout()
        cp_val = QLabel("85%")
        cp_val.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 700; border: none;")
        cp_bar_layout.addWidget(cp_val)
        
        bar_bg = QFrame()
        bar_bg.setFixedHeight(8)
        bar_bg.setStyleSheet("background: #E2E8F0; border-radius: 4px; border: none;")
        
        bar_fg = QFrame(bar_bg)
        bar_fg.setStyleSheet("background: #38BDF8; border-radius: 4px; border: none;")
        bar_fg.resize(180, 8) # Visual progress indicator
        
        cp_bar_layout.addWidget(bar_bg, 1)
        cp_layout.addLayout(cp_bar_layout)
        insights_layout.addLayout(cp_layout)

        # Recommended Skills
        lbl_skills = QLabel("Recommended Skills to Learn:")
        lbl_skills.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600; border: none; margin-top: 8px;")
        insights_layout.addWidget(lbl_skills)
        
        skills = ["Machine Learning", "Deep Learning", "SQL", "Cloud Computing"]
        skills_layout = QVBoxLayout()
        skills_layout.setSpacing(8)
        for skill in skills:
            sk_lbl = QLabel(f"• {skill}")
            sk_lbl.setStyleSheet("color: #64748B; font-size: 13px; border: none;")
            skills_layout.addWidget(sk_lbl)
        insights_layout.addLayout(skills_layout)
        
        right_layout.addWidget(insights_card)

        # Upcoming Sessions
        sessions_card = QFrame()
        sessions_card.setGraphicsEffect(create_shadow())
        sessions_card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }
        """)
        sessions_layout = QVBoxLayout(sessions_card)
        sessions_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_sessions = QLabel("Upcoming Sessions")
        lbl_sessions.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        sessions_layout.addWidget(lbl_sessions)
        
        sess_box = QFrame()
        sess_box.setStyleSheet("background: #F8FAFC; border-radius: 12px; border: none; margin-top: 12px;")
        sess_box_layout = QVBoxLayout(sess_box)
        sess_box_layout.setContentsMargins(16, 16, 16, 16)
        
        sess_title = QLabel("Portfolio Review")
        sess_title.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 600; border: none;")
        sess_box_layout.addWidget(sess_title)
        
        sess_with = QLabel("with Sarah Chen")
        sess_with.setStyleSheet("color: #64748B; font-size: 13px; border: none;")
        sess_box_layout.addWidget(sess_with)
        
        sess_time = QLabel("Today, 3:00 PM (in 2 hours)")
        sess_time.setStyleSheet("color: #38BDF8; font-size: 13px; font-weight: 600; border: none; margin-top: 4px;")
        sess_box_layout.addWidget(sess_time)
        
        sessions_layout.addWidget(sess_box)
        right_layout.addWidget(sessions_card)

        # Recent Mentor Activity
        activity_card = QFrame()
        activity_card.setGraphicsEffect(create_shadow())
        activity_card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 20px;
            }
        """)
        activity_layout = QVBoxLayout(activity_card)
        activity_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_activity = QLabel("Recent Activity")
        lbl_activity.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700; border: none;")
        activity_layout.addWidget(lbl_activity)
        
        activities = [
            ("Alex Kumar left feedback", "2 days ago"),
            ("Completed 'Python Basics'", "4 days ago"),
            ("Elena viewed your profile", "1 week ago")
        ]
        
        for act, time in activities:
            act_layout = QVBoxLayout()
            act_layout.setSpacing(2)
            act_layout.setContentsMargins(0, 8, 0, 8)
            
            act_title = QLabel(act)
            act_title.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 500; border: none;")
            act_layout.addWidget(act_title)
            
            act_time = QLabel(time)
            act_time.setStyleSheet("color: #64748B; font-size: 12px; border: none;")
            act_layout.addWidget(act_time)
            
            activity_layout.addLayout(act_layout)
        
        right_layout.addWidget(activity_card)
        right_layout.addStretch()

        body_layout.addWidget(right_area)
        content_layout.addLayout(body_layout)
        
        # Initial AI Message
        self.append_message("AI Mentor", "Hello! I am your AI Career Mentor. I can help you build your roadmap, prepare for interviews, or analyze your skills. What would you like to focus on today?")

    def append_message(self, sender, text):
        color = "#0F172A" if sender == "AI Mentor" else "#64748B"
        html = f"<div style='margin-bottom: 12px;'><b style='color: {color};'>{sender}:</b><br><span style='color: #334155;'>{text}</span></div>"
        html = html.replace("**", "<b>").replace("`", "<code>")
        self.chat_box.append(html)
        self.chat_box.verticalScrollBar().setValue(self.chat_box.verticalScrollBar().maximum())

    def send_message(self, text=None):
        msg = text if isinstance(text, str) else self.entry.text()
        if not msg.strip(): return
        
        if not isinstance(text, str):
            self.entry.clear()
            
        self.append_message("You", msg)
        
        # Mock AI Response
        QTimer.singleShot(600, lambda: self.append_message("AI Mentor", f"I am analyzing your request: <b>{msg}</b>. Please wait a moment while I generate personalized insights."))
