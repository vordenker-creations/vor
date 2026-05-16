from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QFrame, QScrollArea, QGraphicsDropShadowEffect,
                             QGraphicsOpacityEffect, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QRect
from PyQt6.QtGui import QColor, QFont, QKeyEvent

class SearchResultItem(QFrame):
    clicked = pyqtSignal(object)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_selected = False
        
        self.setStyleSheet("""
            SearchResultItem {
                background-color: transparent;
                border-radius: 16px;
                border: 2px solid transparent;
            }
            SearchResultItem:hover {
                background-color: #F8FAFC;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(16)
        
        # Icon
        self.icon_lbl = QLabel(data.get("icon", "🔍"))
        self.icon_lbl.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        layout.addWidget(self.icon_lbl)
        
        # Text Info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.title_lbl = QLabel(data.get("title", "Untitled"))
        self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        
        self.sub_lbl = QLabel(data.get("subtitle", "No description available"))
        self.sub_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none; background: transparent;")
        
        text_layout.addWidget(self.title_lbl)
        text_layout.addWidget(self.sub_lbl)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Category Badge
        self.badge = QLabel(data.get("category", "General").upper())
        self.badge.setStyleSheet("""
            font-size: 10px; font-weight: 800; color: #38BDF8; 
            background-color: #F0F9FF; border-radius: 6px; padding: 4px 8px; border: none;
        """)
        layout.addWidget(self.badge)
        
        # Shortcut hint
        if data.get("shortcut"):
            self.hint = QLabel(data["shortcut"])
            self.hint.setStyleSheet("font-size: 11px; font-weight: 600; color: #94A3B8; border: none;")
            layout.addWidget(self.hint)

    def set_selected(self, selected):
        self.is_selected = selected
        if selected:
            self.setStyleSheet("""
                SearchResultItem {
                    background-color: #F0F9FF;
                    border: 2px solid #38BDF8;
                    border-radius: 16px;
                }
            """)
            self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #0284C7; border: none; background: transparent;")
        else:
            self.setStyleSheet("""
                SearchResultItem {
                    background-color: transparent;
                    border-radius: 16px;
                    border: 2px solid transparent;
                }
                SearchResultItem:hover {
                    background-color: #F8FAFC;
                }
            """)
            self.title_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none; background: transparent;")

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)
        super().mousePressEvent(event)

class CommandPaletteWidget(QFrame):
    command_executed = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(780)
        self.setStyleSheet("""
            CommandPaletteWidget {
                background-color: #FFFFFF;
                border-radius: 28px;
                border: 1px solid #E2E8F0;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(60)
        shadow.setXOffset(0)
        shadow.setYOffset(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 1. Search Area
        self.search_container = QWidget()
        self.search_container.setFixedHeight(84)
        sc_layout = QHBoxLayout(self.search_container)
        sc_layout.setContentsMargins(24, 0, 24, 0)
        sc_layout.setSpacing(16)
        
        ico = QLabel("🔍")
        ico.setStyleSheet("font-size: 24px; border: none;")
        sc_layout.addWidget(ico)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Search pages, commands, AI tools...")
        self.input.setStyleSheet("""
            QLineEdit {
                border: none; background: transparent;
                font-size: 19px; font-weight: 500; color: #0F172A;
                padding: 10px 0;
            }
        """)
        sc_layout.addWidget(self.input)
        
        hint = QLabel("ESC to close")
        hint.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 600; border: none;")
        sc_layout.addWidget(hint)
        
        layout.addWidget(self.search_container)
        
        # Separator
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #E2E8F0; border: none;")
        layout.addWidget(line)
        
        # 1.5 Filter Tabs
        self.tabs_container = QWidget()
        self.tabs_container.setFixedHeight(48)
        tl = QHBoxLayout(self.tabs_container)
        tl.setContentsMargins(24, 0, 24, 0)
        tl.setSpacing(8)
        
        self.filter_btns = []
        for cat in ["All", "Navigation", "AI Tools", "Files", "Social"]:
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; color: #64748B; border-radius: 12px;
                    padding: 6px 14px; font-size: 12px; font-weight: 600; border: 1px solid transparent;
                }
                QPushButton:hover { background-color: #F1F5F9; }
                QPushButton:checked { 
                    background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD;
                }
            """)
            if cat == "All": btn.setChecked(True)
            btn.clicked.connect(lambda ch, c=cat: self._on_filter_changed(c))
            tl.addWidget(btn)
            self.filter_btns.append(btn)
        tl.addStretch()
        layout.addWidget(self.tabs_container)
        
        # Separator 2
        line2 = QFrame()
        line2.setFixedHeight(1)
        line2.setStyleSheet("background-color: #F1F5F9; border: none;")
        layout.addWidget(line2)

        # 2. Results Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        self.scroll.setMaximumHeight(480)
        
        self.result_container = QWidget()
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setContentsMargins(12, 12, 12, 12)
        self.result_layout.setSpacing(4)
        
        self.scroll.setWidget(self.result_container)
        layout.addWidget(self.scroll)
        
        # Footer
        footer = QFrame()
        footer.setFixedHeight(48)
        footer.setStyleSheet("background-color: #F8FAFC; border-bottom-left-radius: 28px; border-bottom-right-radius: 28px; border-top: 1px solid #E2E8F0;")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(24, 0, 24, 0)
        
        f_hint = QLabel("↑↓ Navigate • ENTER Select • TAB Filter")
        f_hint.setStyleSheet("font-size: 11px; font-weight: 700; color: #64748B; border: none;")
        fl.addWidget(f_hint)
        fl.addStretch()
        
        layout.addWidget(footer)
        
        self.all_data = self._get_mock_data()
        self.current_filter = "All"
        self.recent_data = []
        self.result_widgets = []
        self.selected_index = -1
        
        self.input.textChanged.connect(self._on_search)
        self._refresh_results(self.all_data)

    def _on_filter_changed(self, category):
        self.current_filter = category
        for btn in self.filter_btns:
            btn.setChecked(btn.text() == category)
        self._on_search(self.input.text())

    def _get_mock_data(self):
        return [
            {"title": "Dashboard", "subtitle": "Overview of your progress", "category": "Navigation", "icon": "⌂", "index": 0},
            {"title": "Resume Builder", "subtitle": "Create and optimize your CV", "category": "Navigation", "icon": "📝", "index": 1},
            {"title": "Interview Prep", "subtitle": "AI-powered mock interviews", "category": "Navigation", "icon": "🎙️", "index": 5},
            {"title": "AI Mentor", "subtitle": "Talk with your career assistant", "category": "AI Tools", "icon": "✦", "index": 6},
            {"title": "Academic Roadmap", "subtitle": "Visualize your learning path", "category": "Navigation", "icon": "🗺", "index": 4},
            {"title": "Settings", "subtitle": "App and profile configuration", "category": "General", "icon": "⚙", "index": 8},
            {"title": "Python AI Roadmap", "subtitle": "Curated path for AI engineering", "category": "Navigation", "icon": "🐍", "index": 4},
            {"title": "Frontend Development", "subtitle": "React, Vue, and modern CSS", "category": "Navigation", "icon": "💻", "index": 4},
            {"title": "Generate AI Resume", "subtitle": "Let AI build your base resume", "category": "AI Tools", "icon": "✨", "action": "ai_gen_resume"},
            {"title": "Mock Behavioral Interview", "subtitle": "Practice soft skills with AI", "category": "AI Tools", "icon": "🗣", "action": "ai_mock_behavioral"},
            {"title": "Analyze Python Assignment", "subtitle": "Get feedback on your code", "category": "Files", "icon": "📁", "action": "file_analyze"},
            {"title": "Resume_Final_2026.pdf", "subtitle": "Uploaded yesterday", "category": "Files", "icon": "📄", "action": "open_file"},
            {"title": "Project_Proposal.docx", "subtitle": "In Drafts", "category": "Files", "icon": "📜", "action": "open_file"},
            {"title": "Global Tech Community", "subtitle": "5.2k members online", "category": "Social", "icon": "🌐", "index": 3},
            {"title": "AI-Bridge Discord", "subtitle": "Join the official community", "category": "Social", "icon": "💬", "index": 3}
        ]

    def _on_search(self, text):
        if not text and self.recent_data:
            self._refresh_results(self.recent_data)
            return
        elif not text:
            self._refresh_results(self.all_data)
            return

        filtered = []
        for d in self.all_data:
            match_text = text.lower() in d["title"].lower() or text.lower() in d["subtitle"].lower()
            match_cat = self.current_filter == "All" or d["category"] == self.current_filter
            if match_text and match_cat:
                filtered.append(d)
        self._refresh_results(filtered)

    def _refresh_results(self, data):
        # Clear current
        for w in self.result_widgets:
            self.result_layout.removeWidget(w)
            w.deleteLater()
        self.result_widgets = []
        
        for d in data:
            item = SearchResultItem(d)
            item.clicked.connect(self._handle_item_clicked)
            self.result_layout.addWidget(item)
            self.result_widgets.append(item)
            
        if self.result_widgets:
            self.selected_index = 0
            self.result_widgets[0].set_selected(True)
        else:
            self.selected_index = -1
            
        self.result_layout.addStretch()

    def _handle_item_clicked(self, data):
        if data not in self.recent_data:
            self.recent_data.insert(0, data)
            if len(self.recent_data) > 3: self.recent_data.pop()
        self.command_executed.emit(data)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Down:
            if self.selected_index < len(self.result_widgets) - 1:
                self.result_widgets[self.selected_index].set_selected(False)
                self.selected_index += 1
                self.result_widgets[self.selected_index].set_selected(True)
                self._ensure_visible(self.result_widgets[self.selected_index])
        elif event.key() == Qt.Key.Key_Up:
            if self.selected_index > 0:
                self.result_widgets[self.selected_index].set_selected(False)
                self.selected_index -= 1
                self.result_widgets[self.selected_index].set_selected(True)
                self._ensure_visible(self.result_widgets[self.selected_index])
        elif event.key() == Qt.Key.Key_Return:
            if self.selected_index != -1:
                self._handle_item_clicked(self.result_widgets[self.selected_index].data)
        elif event.key() == Qt.Key.Key_Escape:
            self.command_executed.emit({"action": "close"})
        else:
            super().keyPressEvent(event)

    def _ensure_visible(self, widget):
        self.scroll.ensureWidgetVisible(widget)

class CommandPaletteOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.bg_frame = QFrame(self)
        self.bg_frame.setStyleSheet("background-color: rgba(15, 23, 42, 0.4);") # Dark blur effect
        
        self.palette_widget = CommandPaletteWidget(self)
        self.layout.addWidget(self.palette_widget)
        
        # Opacity animation for overlay
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
    def show_animated(self, window_rect):
        self.setGeometry(window_rect)
        self.show()
        self.palette_widget.input.setFocus()
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(200)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def hide_animated(self):
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(160)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.anim.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg_frame.setGeometry(self.rect())

    def mousePressEvent(self, event):
        # Close if clicked outside the palette widget
        if not self.palette_widget.geometry().contains(event.pos()):
            self.hide_animated()
        super().mousePressEvent(event)
