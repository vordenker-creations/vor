import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QLineEdit, 
                             QTextEdit, QGraphicsDropShadowEffect, QSizePolicy,
                             QSplitter, QProgressBar, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QCursor

class SectionCard(QFrame):
    def __init__(self, title, icon, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 1px solid #38BDF8;
                background-color: #F0F9FF;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(12)
        
        ic_lbl = QLabel(icon)
        ic_lbl.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #0F172A; font-weight: 600; font-size: 13px; border: none; background: transparent;")
        
        layout.addWidget(ic_lbl)
        layout.addWidget(t_lbl)
        layout.addStretch()
        
        drag_handle = QLabel("⋮⋮")
        drag_handle.setStyleSheet("color: #CBD5E1; font-size: 16px; border: none; background: transparent;")
        layout.addWidget(drag_handle)

class ResumeEditorSection(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        
        header = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700; border: none; background: transparent;")
        header.addWidget(t_lbl)
        header.addStretch()
        
        opt_btn = QPushButton("✨ AI Optimize")
        opt_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD;
                border-radius: 6px; padding: 4px 12px; font-size: 11px; font-weight: 700;
            }
            QPushButton:hover { background-color: #E0F2FE; }
        """)
        header.addWidget(opt_btn)
        self.layout.addLayout(header)

class ResumeBuilderPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_left_sidebar()
        self._setup_main_editor()
        self._setup_right_preview()

    def _setup_left_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(20)
        
        header = QLabel("Resume Sections")
        header.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        layout.addWidget(header)
        
        # Template Selector Mock
        tpl_card = QFrame()
        tpl_card.setFixedHeight(100)
        tpl_card.setStyleSheet("background-color: #F1F5F9; border-radius: 12px; border: 1px dashed #CBD5E1;")
        tpl_layout = QVBoxLayout(tpl_card)
        tpl_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tpl_lbl = QLabel("Template: <b>Modern Professional</b>")
        tpl_lbl.setStyleSheet("color: #475569; font-size: 12px;")
        change_btn = QPushButton("Change Template")
        change_btn.setStyleSheet("color: #38BDF8; font-weight: 700; font-size: 11px; border: none; background: transparent;")
        tpl_layout.addWidget(tpl_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        tpl_layout.addWidget(change_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tpl_card)
        
        # Section List
        sections = [
            ("Header & Contact", "👤"),
            ("Professional Summary", "📝"),
            ("Work Experience", "💼"),
            ("Education", "🎓"),
            ("Skills & Tech Stack", "🛠️"),
            ("Certifications", "📜"),
            ("Projects", "🚀")
        ]
        
        for title, icon in sections:
            layout.addWidget(SectionCard(title, icon))
            
        layout.addStretch()
        
        # Tips Card
        tips = QFrame()
        tips.setStyleSheet("background-color: #F8FAFC; border-radius: 12px; border: 1px solid #E2E8F0;")
        tl = QVBoxLayout(tips)
        tl.addWidget(QLabel("💡 Pro Tip", styleSheet="color: #0F172A; font-weight: 700; font-size: 12px;"))
        tl.addWidget(QLabel("Use action verbs like 'Architected' or 'Spearheaded' to stand out.", wordWrap=True, styleSheet="color: #64748B; font-size: 11px; line-height: 1.4;"))
        layout.addWidget(tips)
        
        self.main_layout.addWidget(sidebar)

    def _setup_main_editor(self):
        editor_container = QWidget()
        layout = QVBoxLayout(editor_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(72)
        toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        t_layout = QHBoxLayout(toolbar)
        t_layout.setContentsMargins(24, 0, 24, 0)
        
        title = QLabel("Resume Builder")
        title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 700;")
        t_layout.addWidget(title)
        
        t_layout.addStretch()
        
        for btn_text, is_primary in [("Preview", False), ("Export PDF", False), ("AI Optimize Full", True)]:
            btn = QPushButton(btn_text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            if is_primary:
                btn.setStyleSheet("background-color: #38BDF8; color: white; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 13px; border: none;")
            else:
                btn.setStyleSheet("background-color: white; color: #0F172A; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 16px; font-weight: 700; font-size: 13px;")
            t_layout.addWidget(btn)
            
        layout.addWidget(toolbar)
        
        # Scrollable Form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(40, 32, 40, 40)
        form_layout.setSpacing(32)
        
        # Section 1: Header
        header_sec = ResumeEditorSection("Resume Header")
        gl = QGridLayout()
        gl.setSpacing(16)
        for i, (lbl, placeholder) in enumerate([("Full Name", "John Doe"), ("Email", "john@example.com"), ("Phone", "+1 234 567 890"), ("Location", "San Francisco, CA")]):
            row, col = divmod(i, 2)
            v = QVBoxLayout()
            v.setSpacing(6)
            l = QLabel(lbl); l.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600;")
            e = QLineEdit(); e.setPlaceholderText(placeholder)
            e.setStyleSheet("""
                QLineEdit {
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    color: #0F172A;
                }
                QLineEdit:focus {
                    background-color: #FFFFFF;
                    border: 1px solid #38BDF8;
                }
            """)
            v.addWidget(l); v.addWidget(e)
            gl.addLayout(v, row, col)
        header_sec.layout.addLayout(gl)
        form_layout.addWidget(header_sec)
        
        # Section 2: Summary
        summary_sec = ResumeEditorSection("Professional Summary")
        summary_edit = QTextEdit()
        summary_edit.setPlaceholderText("Write a compelling summary of your career goals and achievements...")
        summary_edit.setMinimumHeight(120)
        summary_edit.setStyleSheet("""
            QTextEdit {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 12px;
                color: #0F172A;
            }
            QTextEdit:focus {
                background-color: #FFFFFF;
                border: 1px solid #38BDF8;
            }
        """)
        summary_sec.layout.addWidget(summary_edit)
        form_layout.addWidget(summary_sec)
        
        # Section 3: Experience
        exp_sec = ResumeEditorSection("Work Experience")
        for _ in range(1): # Mock one entry
            item = QFrame()
            item.setStyleSheet("background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;")
            il = QVBoxLayout(item)
            il.addWidget(QLabel("Senior Software Engineer", styleSheet="color: #0F172A; font-weight: 700;"))
            il.addWidget(QLabel("Google • 2021 - Present", styleSheet="color: #64748B; font-size: 12px;"))
            il.addWidget(QLabel("• Spearheaded the development of a new AI-driven search ranking algorithm...", wordWrap=True, styleSheet="color: #475569; font-size: 13px; margin-top: 8px;"))
            exp_sec.layout.addWidget(item)
        add_exp = QPushButton("+ Add Experience")
        add_exp.setStyleSheet("color: #38BDF8; font-weight: 700; font-size: 13px; border: none; background: transparent; text-align: left;")
        exp_sec.layout.addWidget(add_exp)
        form_layout.addWidget(exp_sec)
        
        form_layout.addStretch()
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        self.main_layout.addWidget(editor_container, stretch=1)

    def _setup_right_preview(self):
        preview_panel = QFrame()
        preview_panel.setFixedWidth(420)
        preview_panel.setStyleSheet("background-color: #F1F5F9; border-left: 1px solid #E2E8F0; border-radius: 0;")
        
        layout = QVBoxLayout(preview_panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        header = QLabel("Live Preview")
        header.setStyleSheet("color: #0F172A; font-size: 16px; font-weight: 700;")
        layout.addWidget(header)
        
        # Paper Simulation
        paper = QFrame()
        paper.setFixedSize(370, 520) # Scaled A4
        paper.setStyleSheet("background-color: #FFFFFF; border-radius: 2px;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 8)
        paper.setGraphicsEffect(shadow)
        
        pl = QVBoxLayout(paper)
        pl.setContentsMargins(20, 20, 20, 20)
        pl.setSpacing(10)
        
        # Mock Preview Content
        name = QLabel("JOHN DOE")
        name.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 900; letter-spacing: 1px; border-bottom: 2px solid #0F172A; padding-bottom: 5px;")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pl.addWidget(name)
        
        sub = QLabel("Software Engineer • john@example.com")
        sub.setStyleSheet("color: #475569; font-size: 9px; font-weight: 600;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pl.addWidget(sub)
        
        pl.addSpacing(10)
        summary_title = QLabel("PROFESSIONAL SUMMARY")
        summary_title.setStyleSheet("color: #0F172A; font-size: 10px; font-weight: 800; background: #F1F5F9; padding: 3px;")
        pl.addWidget(summary_title)
        
        pl.addStretch()
        layout.addWidget(paper, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # AI Suggestions
        ai_card = QFrame()
        ai_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px;")
        al = QVBoxLayout(ai_card)
        al.setSpacing(12)
        
        ai_title = QHBoxLayout()
        ai_title.addWidget(QLabel("✨ AI Analysis", styleSheet="color: #0F172A; font-weight: 700; font-size: 14px;"))
        ai_title.addStretch()
        al.addLayout(ai_title)
        
        score_layout = QHBoxLayout()
        score_lbl = QLabel("ATS Score:")
        score_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 600;")
        score_val = QLabel("78/100")
        score_val.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 800;")
        score_layout.addWidget(score_lbl); score_layout.addStretch(); score_layout.addWidget(score_val)
        al.addLayout(score_layout)
        
        bar = QProgressBar()
        bar.setFixedHeight(6)
        bar.setValue(78)
        bar.setTextVisible(False)
        bar.setStyleSheet("QProgressBar { background: #E2E8F0; border-radius: 3px; border: none; } QProgressBar::chunk { background: #10B981; border-radius: 3px; }")
        al.addWidget(bar)
        
        suggestion = QLabel("Add more keywords related to 'Cloud Infrastructure' to improve your score for DevOps roles.")
        suggestion.setWordWrap(True)
        suggestion.setStyleSheet("color: #475569; font-size: 11px; line-height: 1.4;")
        al.addWidget(suggestion)
        
        layout.addWidget(ai_card)
        layout.addStretch()
        
        self.main_layout.addWidget(preview_panel)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ResumeBuilderPage()
    window.resize(1400, 900)
    window.show()
    sys.exit(app.exec())
