import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextBrowser, QLineEdit, QFrame,
                             QScrollArea, QGridLayout, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QFont, QColor

def apply_shadow(widget, blur=30, offset=(0, 8), opacity=0.08):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(offset[0])
    shadow.setYOffset(offset[1])
    shadow.setColor(QColor(15, 23, 42, int(255 * opacity)))
    widget.setGraphicsEffect(shadow)
    return shadow

class ModernCard(QFrame):
    def __init__(self, parent=None, radius=24, bg_color="#FFFFFF", border_color="#E2E8F0"):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: {radius}px;
            }}
        """)
        apply_shadow(self)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

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
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Content Layout
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(32)

        # ====================
        # TOP TOOLBAR
        # ====================
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        # Breadcrumbs
        lbl_breadcrumbs = QLabel("AI Mentor  /  <b>Career Guidance</b>")
        lbl_breadcrumbs.setStyleSheet("color: #64748B; font-size: 14px; font-weight: 600;")
        header_layout.addWidget(lbl_breadcrumbs)
        
        header_layout.addStretch()

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search mentors or topics...")
        self.search_bar.setFixedWidth(300)
        self.search_bar.setFixedHeight(40)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
                padding: 0 16px; color: #0F172A; font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #38BDF8; }
        """)
        header_layout.addWidget(self.search_bar)

        btn_book = QPushButton("Book Session")
        btn_book.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_book.setFixedHeight(40)
        btn_book.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 12px;
                padding: 0 24px; font-weight: 700; font-size: 14px;
            }
            QPushButton:hover { background: #1E293B; }
        """)
        header_layout.addWidget(btn_book)

        lbl_avatar = QLabel()
        lbl_avatar.setFixedSize(40, 40)
        lbl_avatar.setStyleSheet("background: #38BDF8; border-radius: 20px;")
        header_layout.addWidget(lbl_avatar)

        content_layout.addLayout(header_layout)

        # ====================
        # BODY LAYOUT
        # ====================
        body_layout = QHBoxLayout()
        body_layout.setSpacing(32)

        # --------------------
        # LEFT AREA
        # --------------------
        left_area = QWidget()
        left_layout = QVBoxLayout(left_area)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(32)

        # Section 1: Hero Card
        overview_card = QFrame()
        overview_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38BDF8, stop:1 #8B5CF6);
                border-radius: 28px;
            }
        """)
        apply_shadow(overview_card)
        overview_card.setMinimumHeight(200)
        overview_layout = QVBoxLayout(overview_card)
        overview_layout.setContentsMargins(40, 40, 40, 40)
        
        lbl_greeting = QLabel("Your AI Career Journey.")
        lbl_greeting.setStyleSheet("color: white; font-size: 32px; font-weight: 800; background: transparent; letter-spacing: -1px;")
        overview_layout.addWidget(lbl_greeting)
        
        lbl_greeting_sub = QLabel("Personalized guidance from global industry leaders.")
        lbl_greeting_sub.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px; background: transparent; font-weight: 500;")
        overview_layout.addWidget(lbl_greeting_sub)
        
        overview_layout.addStretch()
        
        btn_actions_layout = QHBoxLayout()
        btn_find_mentor = QPushButton("Find Mentor")
        btn_find_mentor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_find_mentor.setStyleSheet("""
            QPushButton {
                background: white; color: #0F172A; border-radius: 10px;
                padding: 12px 28px; font-weight: 700; font-size: 14px; border: none;
            }
            QPushButton:hover { background: #F1F5F9; }
        """)
        
        btn_schedule = QPushButton("Schedule")
        btn_schedule.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_schedule.setStyleSheet("""
            QPushButton {
                background: transparent; color: white; border: 2px solid white; border-radius: 10px;
                padding: 10px 28px; font-weight: 700; font-size: 14px;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.1); }
        """)
        btn_actions_layout.addWidget(btn_find_mentor)
        btn_actions_layout.addWidget(btn_schedule)
        btn_actions_layout.addStretch()
        overview_layout.addLayout(btn_actions_layout)

        left_layout.addWidget(overview_card)

        # Section 2: Recommended Mentors
        lbl_recommended = QLabel("Featured Mentors")
        lbl_recommended.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 800;")
        left_layout.addWidget(lbl_recommended)

        mentors_layout = QGridLayout()
        mentors_layout.setSpacing(20)
        
        mentors = [
            {"name": "Sarah Chen", "role": "Senior Data Scientist", "match": "95%", "color": "#8B5CF6"},
            {"name": "Alex Kumar", "role": "Lead Product Manager", "match": "92%", "color": "#F59E0B"},
            {"name": "Elena Rodriguez", "role": "UX Researcher", "match": "88%", "color": "#10B981"}
        ]

        for i, mentor in enumerate(mentors):
            m_card = ModernCard(radius=24)
            m_layout = m_card.layout
            
            # Avatar & Match
            m_top = QHBoxLayout()
            m_avatar = QLabel()
            m_avatar.setFixedSize(56, 56)
            m_avatar.setStyleSheet(f"background: {mentor['color']}; border-radius: 28px; border: none;")
            m_top.addWidget(m_avatar)
            
            m_top.addStretch()
            
            m_match = QLabel(mentor["match"])
            m_match.setStyleSheet(f"""
                color: {mentor['color']}; background: {mentor['color']}15;
                padding: 6px 12px; border-radius: 12px; font-size: 12px; font-weight: 800; border: none;
            """)
            m_top.addWidget(m_match)
            m_layout.addLayout(m_top)
            
            m_name = QLabel(mentor["name"])
            m_name.setStyleSheet("color: #0F172A; font-size: 17px; font-weight: 800; margin-top: 12px; border: none;")
            m_layout.addWidget(m_name)
            
            m_role = QLabel(mentor["role"])
            m_role.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 500; border: none;")
            m_layout.addWidget(m_role)
            
            m_layout.addStretch()
            
            m_btn = QPushButton("Connect")
            m_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            m_btn.setStyleSheet("""
                QPushButton {
                    background: #F8FAFC; color: #0F172A; border: 1px solid #E2E8F0;
                    border-radius: 10px; padding: 10px 0; font-weight: 700; font-size: 13px;
                }
                QPushButton:hover { background: #F1F5F9; border-color: #CBD5E1; }
            """)
            m_layout.addWidget(m_btn)
            
            mentors_layout.addWidget(m_card, 0, i)

        left_layout.addLayout(mentors_layout)

        # Section 3: Guidance & Chat
        guidance_layout = QHBoxLayout()
        guidance_layout.setSpacing(32)

        # Roadmap Card
        roadmap_card = ModernCard(radius=24)
        rl = roadmap_card.layout
        
        lbl_rl = QLabel("Career Path")
        lbl_rl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800; border: none;")
        rl.addWidget(lbl_rl)
        
        steps = [("Learn Python", True), ("AI Project", True), ("Portfolio", False), ("Internship", False)]
        for text, completed in steps:
            s_layout = QHBoxLayout()
            s_icon = QLabel("✓" if completed else "○")
            s_icon.setStyleSheet(f"color: {'#38BDF8' if completed else '#CBD5E1'}; font-size: 18px; font-weight: 800; border: none;")
            s_layout.addWidget(s_icon)
            s_text = QLabel(text)
            s_text.setStyleSheet(f"color: {'#0F172A' if completed else '#64748B'}; font-size: 14px; font-weight: 600; border: none;")
            s_layout.addWidget(s_text)
            s_layout.addStretch()
            rl.addLayout(s_layout)
        
        rl.addStretch()
        guidance_layout.addWidget(roadmap_card, 2)

        # Chat Card
        chat_card = ModernCard(radius=24)
        chat_layout = chat_card.layout
        
        lbl_chat = QLabel("AI Mentor Assistant")
        lbl_chat.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800; border: none;")
        chat_layout.addWidget(lbl_chat)
        
        self.chat_box = QTextBrowser()
        self.chat_box.setStyleSheet("background: transparent; border: none; color: #475569; font-size: 14px; line-height: 1.5;")
        self.chat_box.setOpenExternalLinks(True)
        chat_layout.addWidget(self.chat_box)
        
        input_frame = QFrame()
        input_frame.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;")
        i_layout = QHBoxLayout(input_frame)
        i_layout.setContentsMargins(8, 4, 8, 4)
        
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Ask me anything...")
        self.entry.setStyleSheet("background: transparent; border: none; color: #0F172A; padding: 8px; font-size: 14px;")
        self.entry.returnPressed.connect(self.send_message)
        i_layout.addWidget(self.entry)
        
        btn_send = QPushButton("➤")
        btn_send.setFixedSize(36, 36)
        btn_send.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_send.setStyleSheet("background: #38BDF8; color: white; border-radius: 10px; font-size: 16px; border: none;")
        btn_send.clicked.connect(self.send_message)
        i_layout.addWidget(btn_send)
        
        chat_layout.addWidget(input_frame)
        guidance_layout.addWidget(chat_card, 3)

        left_layout.addLayout(guidance_layout)
        body_layout.addWidget(left_area, 1)

        # --------------------
        # RIGHT AREA
        # --------------------
        right_area = QWidget()
        right_area.setFixedWidth(340)
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(32)

        # Insights Card
        insights_card = ModernCard(radius=24)
        il = insights_card.layout
        il.setSpacing(20)
        
        lbl_ins = QLabel("AI Insights")
        lbl_ins.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800; border: none;")
        il.addWidget(lbl_ins)
        
        # Skill Progress
        def add_skill_progress(name, val):
            v_l = QVBoxLayout()
            v_l.setSpacing(8)
            t_l = QHBoxLayout()
            n_l = QLabel(name); n_l.setStyleSheet("color: #475569; font-size: 13px; font-weight: 600; border: none;")
            p_l = QLabel(f"{val}%"); p_l.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: 800; border: none;")
            t_l.addWidget(n_l); t_l.addStretch(); t_l.addWidget(p_l)
            v_l.addLayout(t_l)
            bar_bg = QFrame(); bar_bg.setFixedHeight(6); bar_bg.setStyleSheet("background: #F1F5F9; border-radius: 3px; border: none;")
            bar_fg = QFrame(bar_bg); bar_fg.setFixedHeight(6); bar_fg.setFixedWidth(int(2.4 * val)); bar_fg.setStyleSheet("background: #38BDF8; border-radius: 3px; border: none;")
            v_l.addWidget(bar_bg)
            il.addLayout(v_l)
            
        add_skill_progress("Python Engineering", 85)
        add_skill_progress("Data Science", 65)
        add_skill_progress("UI/UX Design", 40)
        
        right_layout.addWidget(insights_card)

        # Sessions Card
        sess_card = ModernCard(radius=24)
        sl = sess_card.layout
        lbl_sl = QLabel("Upcoming")
        lbl_sl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800; border: none;")
        sl.addWidget(lbl_sl)
        
        item = QFrame()
        item.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0;")
        il_layout = QVBoxLayout(item)
        il_layout.setContentsMargins(16, 16, 16, 16)
        it = QLabel("Portfolio Review"); it.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700; border: none;")
        iw = QLabel("with Sarah Chen"); iw.setStyleSheet("color: #64748B; font-size: 13px; border: none;")
        it_m = QLabel("Today, 3:00 PM"); it_m.setStyleSheet("color: #38BDF8; font-size: 12px; font-weight: 800; border: none; margin-top: 4px;")
        il_layout.addWidget(it); il_layout.addWidget(iw); il_layout.addWidget(it_m)
        sl.addWidget(item)
        
        right_layout.addWidget(sess_card)
        right_layout.addStretch()

        body_layout.addWidget(right_area)
        content_layout.addLayout(body_layout)
        
        self.append_message("AI Mentor", "Hello! I am your AI Career Mentor. How can I help you today?")

    def append_message(self, sender, text):
        color = "#0F172A" if sender == "AI Mentor" else "#38BDF8"
        html = f"<div style='margin-bottom: 16px;'><b style='color: {color};'>{sender}</b><br><span style='color: #475569;'>{text}</span></div>"
        self.chat_box.append(html)
        self.chat_box.verticalScrollBar().setValue(self.chat_box.verticalScrollBar().maximum())

    def send_message(self, text=None):
        msg = text if isinstance(text, str) else self.entry.text()
        if not msg.strip(): return
        if not isinstance(text, str): self.entry.clear()
        self.append_message("You", msg)
        QTimer.singleShot(600, lambda: self.append_message("AI Mentor", f"Analyzing your request about <b>{msg}</b>..."))
