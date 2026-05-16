import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QGraphicsDropShadowEffect, QSizePolicy, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor, QPainter, QPen, QBrush

class VideoContainer(QFrame):
    def __init__(self, name, is_speaker=False, parent=None):
        super().__init__(parent)
        radius = 24 if is_speaker else 16
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: {radius}px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.addStretch()
        
        # Overlay
        overlay = QFrame()
        overlay.setFixedHeight(40)
        overlay.setStyleSheet("background: rgba(0, 0, 0, 0.4); border-radius: 10px; border: none;")
        ol = QHBoxLayout(overlay)
        
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: white; font-weight: 600; font-size: 12px; background: transparent;")
        ol.addWidget(name_lbl)
        ol.addStretch()
        
        mic_lbl = QLabel("🎙️")
        mic_lbl.setStyleSheet("font-size: 14px; background: transparent;")
        ol.addWidget(mic_lbl)
        
        layout.addWidget(overlay)

class VideoMeetingPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_left_sidebar()
        self._setup_main_workspace()
        self._setup_right_panel()

    def _setup_left_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(20)
        
        h_lbl = QLabel("Live Classroom")
        h_lbl.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        layout.addWidget(h_lbl)
        
        create_btn = QPushButton("Create New Meeting")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9; color: #0F172A; border: 1px solid #E2E8F0;
                border-radius: 12px; padding: 10px; font-weight: 700; font-size: 13px;
            }
            QPushButton:hover { background-color: #E2E8F0; }
        """)
        layout.addWidget(create_btn)
        
        us_lbl = QLabel("Upcoming Sessions")
        us_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 700; text-transform: uppercase;")
        layout.addWidget(us_lbl)
        
        for t, time in [("Advanced AI Workshop", "10:00 AM"), ("Math 201 Office Hours", "02:30 PM"), ("Career Prep Seminar", "Tomorrow")]:
            card = QFrame()
            card.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;")
            cl = QVBoxLayout(card)
            tl = QLabel(t); tl.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 13px;")
            dt = QLabel(time); dt.setStyleSheet("color: #64748B; font-size: 11px;")
            cl.addWidget(tl); cl.addWidget(dt)
            layout.addWidget(card)
            
        layout.addStretch()
        self.main_layout.addWidget(sidebar)

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
        t_layout.setContentsMargins(24, 0, 24, 0)
        
        title_v = QVBoxLayout()
        title_v.setSpacing(2)
        st = QLabel("Session: AI Ethics & Safety")
        st.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        dt = QLabel("🔴 01:24:05")
        dt.setStyleSheet("color: #EF4444; font-size: 12px; font-weight: 600;")
        title_v.addWidget(st); title_v.addWidget(dt)
        t_layout.addLayout(title_v)
        
        t_layout.addStretch()
        
        # Controls
        controls = QHBoxLayout()
        controls.setSpacing(12)
        for icon in ["🎙️", "📷", "🖥️", "✋"]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("background: #F1F5F9; border-radius: 22px; font-size: 16px; border: none;")
            controls.addWidget(btn)
        t_layout.addLayout(controls)
        
        t_layout.addSpacing(20)
        
        end_btn = QPushButton("End Meeting")
        end_btn.setStyleSheet("background: #EF4444; color: white; border-radius: 8px; padding: 8px 16px; font-weight: 700;")
        t_layout.addWidget(end_btn)
        
        layout.addWidget(toolbar)
        
        # Main Video Area
        video_area = QWidget()
        v_layout = QVBoxLayout(video_area)
        v_layout.setContentsMargins(24, 24, 24, 24)
        v_layout.setSpacing(16)
        
        # Speaker
        speaker = VideoContainer("Prof. Sarah Jenkins (Speaker)", True)
        v_layout.addWidget(speaker, stretch=3)
        
        # Participant Grid
        grid = QHBoxLayout()
        grid.setSpacing(12)
        for name in ["Alex Rivera", "John Doe (You)", "Maria Garcia", "Kevin Lee"]:
            grid.addWidget(VideoContainer(name))
        v_layout.addLayout(grid, stretch=1)
        
        layout.addWidget(video_area)
        self.main_layout.addWidget(workspace, stretch=1)

    def _setup_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(340)
        panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        # AI Meeting Assistant
        ai_card = QFrame()
        ai_card.setStyleSheet("background-color: #0F172A; border-radius: 16px;")
        al = QVBoxLayout(ai_card)
        at = QLabel("✨ AI Meeting Assistant")
        at.setStyleSheet("color: #38BDF8; font-weight: 800; font-size: 14px;")
        al.addWidget(at)
        ad = QLabel("Summary: The professor is currently explaining the trolley problem in the context of autonomous vehicles.")
        ad.setWordWrap(True)
        ad.setStyleSheet("color: #E2E8F0; font-size: 12px; line-height: 1.4;")
        al.addWidget(ad)
        layout.addWidget(ai_card)
        
        # Attendees
        att_l = QLabel("Attendees (24)")
        att_l.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 14px;")
        layout.addWidget(att_l)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        sc = QWidget()
        sl = QVBoxLayout(sc)
        for n in ["Prof. Sarah Jenkins", "Alex Rivera", "Maria Garcia", "Kevin Lee", "Liam Smith", "Olivia Brown"]:
            row = QHBoxLayout()
            i_l = QLabel("👤")
            i_l.setStyleSheet("font-size: 14px;")
            row.addWidget(i_l)
            n_l = QLabel(n)
            n_l.setStyleSheet("color: #475569; font-size: 13px; font-weight: 500;")
            row.addWidget(n_l)
            row.addStretch()
            sl.addLayout(row)
        sl.addStretch()
        scroll.setWidget(sc)
        layout.addWidget(scroll)
        
        # Live Chat Mock
        chat_box = QFrame()
        chat_box.setStyleSheet("background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;")
        cl = QVBoxLayout(chat_box)
        ct_l = QLabel("Live Chat")
        ct_l.setStyleSheet("color: #0F172A; font-weight: 700; font-size: 12px;")
        cl.addWidget(ct_l)
        msg = QLabel("Alex: Will the recording be available later?")
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #64748B; font-size: 11px;")
        cl.addWidget(msg)
        inp = QLineEdit(); inp.setPlaceholderText("Send a message..."); inp.setStyleSheet("background: white; border-radius: 6px; padding: 4px;")
        cl.addWidget(inp)
        layout.addWidget(chat_box)
        
        self.main_layout.addWidget(panel)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = VideoMeetingPage()
    window.resize(1400, 900)
    window.show()
    sys.exit(app.exec())
