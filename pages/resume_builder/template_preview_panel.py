from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect,
                             QSizePolicy, QSlider, QProgressBar, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor

class CustomizationSlider(QWidget):
    def __init__(self, label, min_v, max_v, current_v, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        head = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #475569; border: none;")
        self.val_lbl = QLabel(str(current_v))
        self.val_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #38BDF8; border: none;")
        head.addWidget(lbl)
        head.addStretch()
        head.addWidget(self.val_lbl)
        layout.addLayout(head)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(min_v, max_v)
        self.slider.setValue(current_v)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px; background: #F1F5F9; border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #38BDF8; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px;
            }
        """)
        self.slider.valueChanged.connect(lambda v: self.val_lbl.setText(str(v)))
        layout.addWidget(self.slider)

class TemplatePreviewPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(340)
        self.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(24)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        self.content_layout = QVBoxLayout(container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(28)

        # 1. Selection Info (Sticky at top of scroll)
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("background: #F8FAFC; border-radius: 16px; border: 1px solid #E2E8F0;")
        il = QVBoxLayout(self.info_frame)
        self.selected_tpl_lbl = QLabel("No Template Selected")
        self.selected_tpl_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0F172A; border: none;")
        self.selected_cat_lbl = QLabel("Select a template to start designing")
        self.selected_cat_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none;")
        il.addWidget(self.selected_tpl_lbl)
        il.addWidget(self.selected_cat_lbl)
        self.content_layout.addWidget(self.info_frame)

        # 2. AI Optimization
        self._setup_ai_section()

        # 3. Typography & Styling
        self._setup_studio_section()

        # 4. ATS & Analytics
        self._setup_ats_section()

        self.content_layout.addStretch()
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

        # 5. Global Actions
        self._setup_actions()

    def _setup_ai_section(self):
        ai_card = QFrame()
        ai_card.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0F172A, stop:1 #1E293B); border-radius: 20px;")
        al = QVBoxLayout(ai_card)
        al.setContentsMargins(20, 20, 20, 20)
        al.setSpacing(12)

        title = QLabel("✨ AI RECOMMENDATION")
        title.setStyleSheet("font-size: 11px; font-weight: 800; color: #38BDF8; letter-spacing: 1px;")
        al.addWidget(title)

        score_h = QHBoxLayout()
        score_lbl = QLabel("98%")
        score_lbl.setStyleSheet("font-size: 32px; font-weight: 800; color: white;")
        match_desc = QLabel("Matches your\n<b>Senior Developer</b> role")
        match_desc.setStyleSheet("font-size: 12px; color: #94A3B8;")
        score_h.addWidget(score_lbl); score_h.addSpacing(12); score_h.addWidget(match_desc); score_h.addStretch()
        al.addLayout(score_h)

        btn_optimize = QPushButton("AI Auto-Optimize")
        btn_optimize.setFixedHeight(36)
        btn_optimize.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_optimize.setStyleSheet("""
            QPushButton {
                background: #38BDF8; color: #0F172A; border-radius: 10px;
                font-weight: 800; font-size: 11px; border: none;
            }
            QPushButton:hover { background: #7DD3FC; }
        """)
        al.addWidget(btn_optimize)

        self.content_layout.addWidget(ai_card)

    def _setup_studio_section(self):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("DESIGN STUDIO"); lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 800; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)

        # Font Selector
        font_combo = QComboBox()
        font_combo.addItems(["Inter (Default)", "SF Pro Display", "Helvetica Neue", "Roboto", "Lora"])
        font_combo.setFixedHeight(36)
        font_combo.setStyleSheet("""
            QComboBox {
                background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;
                padding: 0 12px; font-size: 12px; font-weight: 600; color: #475569;
            }
            QComboBox::drop-down { border: none; }
        """)
        sec.addWidget(font_combo)

        # Color Theme
        colors = QHBoxLayout(); colors.setSpacing(8)
        for c in ["#38BDF8", "#0F172A", "#10B981", "#8B5CF6", "#EF4444"]:
            btn = QPushButton(); btn.setFixedSize(24, 24)
            btn.setStyleSheet(f"background: {c}; border-radius: 12px; border: 2px solid white;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            colors.addWidget(btn)
        colors.addStretch(); sec.addLayout(colors)

        sec.addWidget(CustomizationSlider("Base Font Size", 8, 16, 11))
        sec.addWidget(CustomizationSlider("Line Height", 1, 5, 2))
        sec.addWidget(CustomizationSlider("Section Spacing", 10, 60, 32))

        self.content_layout.addLayout(sec)

    def _setup_ats_section(self):
        sec = QVBoxLayout(); sec.setSpacing(16)
        lbl = QLabel("ATS ANALYTICS"); lbl.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 800; letter-spacing: 1px; border: none;")
        sec.addWidget(lbl)

        for item, score in [("Scanability", 95), ("Keywords", 82), ("Layout Parsing", 100)]:
            row = QVBoxLayout(); row.setSpacing(4)
            rl = QHBoxLayout()
            rl.addWidget(QLabel(item, styleSheet="font-size: 12px; color: #475569; font-weight: 600; border: none;"))
            rl.addStretch()
            rl.addWidget(QLabel(f"{score}%", styleSheet="font-size: 11px; color: #10B981; font-weight: 800; border: none;"))
            row.addLayout(rl)
            pb = QProgressBar(); pb.setFixedHeight(4); pb.setValue(score); pb.setTextVisible(False)
            pb.setStyleSheet("QProgressBar { background: #F1F5F9; border-radius: 2px; border: none; } QProgressBar::chunk { background: #10B981; border-radius: 2px; }")
            row.addWidget(pb); sec.addLayout(row)

        self.content_layout.addLayout(sec)

    def _setup_actions(self):
        self.actions_layout = QVBoxLayout(); self.actions_layout.setSpacing(10)
        
        btn_preview = QPushButton("Full Preview")
        btn_preview.setFixedHeight(46); btn_preview.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_preview.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #E2E8F0; border-radius: 14px;
                color: #0F172A; font-weight: 800; font-size: 13px;
            }
            QPushButton:hover { background: #F8FAFC; }
        """)
        
        btn_export = QPushButton("Export PDF")
        btn_export.setFixedHeight(46); btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export.setStyleSheet("""
            QPushButton {
                background: #0F172A; color: white; border-radius: 14px;
                font-weight: 800; font-size: 13px; border: none;
            }
            QPushButton:hover { background: #1E293B; }
        """)

        self.actions_layout.addWidget(btn_preview)
        self.actions_layout.addWidget(btn_export)
        self.main_layout.addLayout(self.actions_layout)

    def update_selected_tpl(self, data):
        self.selected_tpl_lbl.setText(data['name'])
        self.selected_cat_lbl.setText(f"{data['category']} Template • ATS Score: {data['ats_score']}%")
        self.info_frame.setStyleSheet(f"background: {data.get('color', '#F8FAFC')}; border-radius: 16px; border: 1px solid #E2E8F0;")
