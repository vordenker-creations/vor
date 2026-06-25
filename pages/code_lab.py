import sys
import io
import json
import re
import traceback
import urllib.request
import urllib.error
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGraphicsDropShadowEffect, QGridLayout,
    QLineEdit, QComboBox, QSplitter, QTextBrowser, QPlainTextEdit, QMessageBox,
    QProgressBar, QDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont, QGuiApplication
from database import code_lab_db
from pages.code_lab_challenge_dialog import AddChallengeDialog

class ClickableCard(QFrame):
    def __init__(self, challenge_data, on_click=None, parent=None):
        super().__init__(parent)
        self.challenge_data = challenge_data
        self.on_click = on_click
        self.setObjectName("ClickableCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            #ClickableCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            #ClickableCard:hover {
                border: 1px solid #38BDF8;
                background-color: #243249;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
        
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(14, 12, 14, 12)
        self.internal_layout.setSpacing(6)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.challenge_data)
        super().mousePressEvent(event)

class CodeLabPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.active_challenge = None
        self.challenges_list = []
        
        from PyQt6.QtCore import QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.time_left = 1800 # 30 mins
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet("background-color: transparent; border-bottom: 1px solid rgba(148, 163, 184, 0.1);")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(16)
        
        title_lbl = QLabel("💻 Code & Algorithm Lab")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: 900; color: #0F172A; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)
        
        sub_lbl = QLabel("Practice algorithms with instant local tests and AI mentor analysis")
        sub_lbl.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 600; border: none; background: transparent;")
        header_layout.addWidget(sub_lbl)
        
        header_layout.addStretch()
        main_layout.addWidget(header)
        
        # Splitter Layout (Left Explorer, Right Workspace)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: rgba(148, 163, 184, 0.1);
                width: 1px;
            }
        """)
        
        # --- LEFT EXPLORER ---
        left_explorer = QWidget()
        left_lay = QVBoxLayout(left_explorer)
        left_lay.setContentsMargins(20, 20, 10, 20)
        left_lay.setSpacing(16)
        
        # Progress Card
        progress_card = QFrame()
        progress_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
        pc_lay = QVBoxLayout(progress_card)
        pc_lay.setContentsMargins(15, 12, 15, 12)
        pc_lay.setSpacing(8)
        
        self.progress_lbl = QLabel("Challenges Solved: 0 / 0")
        self.progress_lbl.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: bold; background: transparent; border: none;")
        pc_lay.addWidget(self.progress_lbl)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #F8FAFC;
                border-radius: 3px;
                border: none;
            }
            QProgressBar::chunk {
                background: #10B981;
                border-radius: 3px;
            }
        """)
        pc_lay.addWidget(self.progress_bar)
        left_lay.addWidget(progress_card)
        
        # Filters Row
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search challenges...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
            }
        """)
        self.search_box.textChanged.connect(self._apply_filters)
        left_lay.addWidget(self.search_box)
        
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["All Difficulties", "Easy", "Medium", "Hard"])
        self.diff_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #0F172A;
                selection-background-color: #38BDF8;
                selection-color: #F8FAFC;
                border: 1px solid #E2E8F0;
            }
        """)
        self.diff_combo.currentTextChanged.connect(self._apply_filters)
        left_lay.addWidget(self.diff_combo)
        
        self.btn_add_challenge = QPushButton("➕ Add Challenge")
        self.btn_add_challenge.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_challenge.setStyleSheet("""
            QPushButton {
                background-color: #0284C7;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0369A1;
            }
        """)
        self.btn_add_challenge.clicked.connect(self._open_add_challenge_dialog)
        left_lay.addWidget(self.btn_add_challenge)
        
        # Challenges Scroll List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.list_content = QWidget()
        self.list_layout = QVBoxLayout(self.list_content)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(12)
        self.list_layout.addStretch()
        
        scroll.setWidget(self.list_content)
        left_lay.addWidget(scroll)
        
        main_splitter.addWidget(left_explorer)
        
        # --- RIGHT WORKSPACE ---
        self.workspace_stack = QWidget()
        work_lay = QVBoxLayout(self.workspace_stack)
        work_lay.setContentsMargins(10, 20, 20, 20)
        work_lay.setSpacing(0)
        
        # State 0: Welcome Pane
        self.welcome_card = QFrame()
        self.welcome_card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px;")
        wc_lay = QVBoxLayout(self.welcome_card)
        wc_lay.setContentsMargins(40, 40, 40, 40)
        wc_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wc_lay.setSpacing(16)
        
        code_icon = QLabel("💻")
        code_icon.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        wc_lay.addWidget(code_icon)
        
        wc_title = QLabel("AI Code & Algorithm Playground")
        wc_title.setStyleSheet("color: #0F172A; font-size: 20px; font-weight: 800; background: transparent; border: none;")
        wc_lay.addWidget(wc_title)
        
        wc_desc = QLabel("Select an algorithmic challenge from the left panel to open the interactive coding workspace, write your solution, run test cases, and obtain instant AI complexity analysis and optimization feedback.")
        wc_desc.setStyleSheet("color: #94A3B8; font-size: 13px; line-height: 1.5; background: transparent; border: none;")
        wc_desc.setWordWrap(True)
        wc_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wc_lay.addWidget(wc_desc)
        
        work_lay.addWidget(self.welcome_card)
        
        # State 1: Active Workspace Container
        self.active_workspace = QWidget()
        self.active_workspace.hide()
        aw_lay = QVBoxLayout(self.active_workspace)
        aw_lay.setContentsMargins(0, 0, 0, 0)
        aw_lay.setSpacing(14)
        
        # Horizontal Split (Description on left, Code Editor on right)
        editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_splitter.setStyleSheet("QSplitter::handle { background-color: rgba(148, 163, 184, 0.1); width: 1px; }")
        
        # Problem Details
        desc_widget = QWidget()
        dl = QVBoxLayout(desc_widget)
        dl.setContentsMargins(0, 0, 6, 0)
        dl.setSpacing(8)
        
        self.problem_title = QLabel("Problem Title")
        self.problem_title.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 800;")
        dl.addWidget(self.problem_title)
        
        meta_row = QHBoxLayout()
        self.diff_badge = QLabel("Easy")
        self.diff_badge.setStyleSheet("color: #10B981; background-color: rgba(16, 185, 129, 0.15); font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 4px;")
        self.topic_badge = QLabel("Topic: Array")
        self.topic_badge.setStyleSheet("color: #38BDF8; font-size: 11px; font-weight: bold;")
        meta_row.addWidget(self.diff_badge)
        meta_row.addWidget(self.topic_badge)
        meta_row.addStretch()
        dl.addLayout(meta_row)
        
        self.desc_browser = QTextBrowser()
        self.desc_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #FFFFFF;
                color: #E2E8F0;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                line-height: 1.4;
            }
        """)
        dl.addWidget(self.desc_browser)
        editor_splitter.addWidget(desc_widget)
        
        # Code Editor
        editor_widget = QWidget()
        el = QVBoxLayout(editor_widget)
        el.setContentsMargins(6, 0, 0, 0)
        el.setSpacing(8)
        
        el.addWidget(QLabel("Write Python Code:", styleSheet="color: #94A3B8; font-size: 12px; font-weight: bold;"))
        self.code_editor = QPlainTextEdit()
        self.code_editor.setFont(QFont("Consolas", 11) if sys.platform == "win32" else QFont("Monaco", 11))
        self.code_editor.setTabChangesFocus(False)
        self.code_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #FFFFFF;
                color: #38BDF8;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        el.addWidget(self.code_editor)
        editor_splitter.addWidget(editor_widget)
        
        aw_lay.addWidget(editor_splitter, 3) # takes more space
        
        # Console Output (terminal-like)
        console_widget = QWidget()
        cl = QVBoxLayout(console_widget)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(6)
        cl.addWidget(QLabel("Terminal Log & AI Review Output:", styleSheet="color: #94A3B8; font-size: 11px; font-weight: bold;"))
        
        self.console = QTextBrowser()
        self.console.setFont(QFont("Consolas", 10) if sys.platform == "win32" else QFont("Monaco", 10))
        self.console.setText("Output logs will appear here after running tests...")
        self.console.setStyleSheet("""
            QTextBrowser {
                background-color: #020617;
                color: #64748B;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        cl.addWidget(self.console)
        aw_lay.addWidget(console_widget, 1) # console takes less space
        
        # Actions Row
        actions = QHBoxLayout()
        actions.setSpacing(12)
        
        self.btn_run = QPushButton("⚡ Run Test Cases")
        self.btn_run.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_run.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; color: #0F172A; border: 1px solid #E2E8F0;
                border-radius: 8px; font-weight: bold; height: 36px; padding: 0 16px;
            }
            QPushButton:hover { background-color: #E2E8F0; }
        """)
        self.btn_run.clicked.connect(self._run_local_tests)
        
        self.timer_lbl = QLabel("⏱️ 30:00")
        self.timer_lbl.setStyleSheet("color: #0F172A; font-weight: bold; font-size: 14px; background: #FFFFFF; border-radius: 8px; padding: 0 15px;")
        actions.addWidget(self.timer_lbl)
        
        actions.addWidget(self.btn_run)
        
        self.btn_ai = QPushButton("🧠 Ask AI Mentor")
        self.btn_ai.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ai.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #EC4899);
                color: white; border: none; border-radius: 8px; font-weight: bold; height: 36px; padding: 0 20px;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777); }
        """)
        self.btn_ai.clicked.connect(self._get_ai_mentor_review)
        actions.addWidget(self.btn_ai)
        
        self.btn_submit = QPushButton("🚀 Submit Solution")
        self.btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #10B981; color: #020617; border: none;
                border-radius: 8px; font-weight: bold; height: 36px; padding: 0 20px;
            }
            QPushButton:hover { background-color: #059669; }
        """)
        self.btn_submit.clicked.connect(self._submit_solution)
        actions.addWidget(self.btn_submit)
        
        actions.addStretch()
        aw_lay.addLayout(actions)
        
        work_lay.addWidget(self.active_workspace)
        main_splitter.addWidget(self.workspace_stack)
        
        # Set proportions: Explorer takes 30%, workspace takes 70%
        main_splitter.setSizes([320, 800])
        main_layout.addWidget(main_splitter)
        
        # Load data
        self.refresh()

    def refresh(self):
        # Load all challenges
        self.challenges_list = code_lab_db.get_all_challenges()
        
        # Update progress stats
        stats = code_lab_db.get_challenge_statistics()
        total = stats["total"]
        solved = stats["solved"]
        self.progress_lbl.setText(f"Challenges Solved: {solved} / {total}")
        
        if total > 0:
            self.progress_bar.setValue(int(solved / total * 100))
        else:
            self.progress_bar.setValue(0)
            
        # Re-draw the explorer challenges list
        self._apply_filters()

    def _apply_filters(self):
        # Clear items in list layout
        for i in reversed(range(self.list_layout.count())):
            item = self.list_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            else:
                self.list_layout.removeItem(item)
                
        search_query = self.search_box.text().lower().strip()
        diff_filter = self.diff_combo.currentText()
        
        for challenge in self.challenges_list:
            title = challenge["title"].lower()
            topic = challenge["topic"].lower()
            diff = challenge["difficulty"]
            cid = challenge["id"]
            
            # Apply filters
            match_search = (not search_query) or (search_query in title) or (search_query in topic)
            match_diff = (diff_filter == "All Difficulties") or (diff_filter.lower() == diff.lower())
            
            if match_search and match_diff:
                card = ClickableCard(challenge, on_click=self._load_challenge, parent=self)
                
                header = QHBoxLayout()
                header.setContentsMargins(0, 0, 0, 0)
                
                # Title
                lbl_title = QLabel(challenge["title"])
                lbl_title.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: bold; background: transparent; border: none;")
                header.addWidget(lbl_title)
                header.addStretch()
                
                # Solved indicator dot
                dot_lbl = QLabel()
                dot_style = "color: #94A3B8; font-size: 14px;" # default new
                
                # Fetch last submission status
                last_sub = code_lab_db.get_last_submission(cid)
                if last_sub:
                    if last_sub["status"] == "Solved":
                        dot_lbl.setText("●")
                        dot_style = "color: #10B981; font-size: 14px;" # green
                    else:
                        dot_lbl.setText("●")
                        dot_style = "color: #F59E0B; font-size: 14px;" # orange (attempted)
                else:
                    dot_lbl.setText("○") # empty circle for new
                    
                dot_lbl.setStyleSheet(dot_style + "background: transparent; border: none;")
                header.addWidget(dot_lbl)
                
                card.internal_layout.addLayout(header)
                
                # Details row
                details = QHBoxLayout()
                details.setContentsMargins(0, 0, 0, 0)
                
                topic_lbl = QLabel(challenge["topic"])
                topic_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-weight: bold; background: transparent; border: none;")
                details.addWidget(topic_lbl)
                details.addStretch()
                
                color = "#10B981" if diff.lower() == "easy" else ("#F59E0B" if diff.lower() == "medium" else "#EF4444")
                diff_lbl = QLabel(diff)
                diff_lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: 800; background: transparent; border: none;")
                details.addWidget(diff_lbl)
                
                card.internal_layout.addLayout(details)
                self.list_layout.addWidget(card)
                
        self.list_layout.addStretch()

    def _load_challenge(self, challenge):
        self.active_challenge = challenge
        
        # Open Workspace Stack
        self.welcome_card.hide()
        self.active_workspace.show()
        
        # Populate problem metadata
        self.problem_title.setText(challenge["title"])
        self.topic_badge.setText(f"Topic: {challenge['topic']}")
        
        diff = challenge["difficulty"]
        self.diff_badge.setText(diff)
        color = "#10B981" if diff.lower() == "easy" else ("#F59E0B" if diff.lower() == "medium" else "#EF4444")
        bg_rgba = "rgba(16, 185, 129, 0.15)" if diff.lower() == "easy" else ("rgba(245, 158, 11, 0.15)" if diff.lower() == "medium" else "rgba(239, 68, 68, 0.15)")
        self.diff_badge.setStyleSheet(f"color: {color}; background-color: {bg_rgba}; font-size: 10px; font-weight: bold; padding: 2px 8px; border-radius: 4px;")
        
        # Set description text
        self.desc_browser.setHtml(challenge["description"])
        
        # Load user's last code submission if it exists, otherwise starter code
        last_sub = code_lab_db.get_last_submission(challenge["id"])
        if last_sub and last_sub.get("code"):
            self.code_editor.setPlainText(last_sub["code"])
            # Load AI feedback in terminal if it exists
            if last_sub.get("ai_review"):
                self.console.setText(last_sub["ai_review"])
                self.console.setStyleSheet("background-color: #020617; color: #E2E8F0; font-family: Consolas, monospace; font-size: 11px;")
            else:
                self.console.setText("Write your code and run tests or request AI review...")
                self.console.setStyleSheet("background-color: #020617; color: #64748B; font-family: Consolas, monospace; font-size: 11px;")
        else:
            self.code_editor.setPlainText(challenge["starter_code"])
            self.console.setText("Write your code and run tests or request AI review...")
            self.console.setStyleSheet("background-color: #020617; color: #64748B; font-family: Consolas, monospace; font-size: 11px;")

        # Start timer for 30 mins
        self.time_left = 1800
        self._update_timer()
        self.timer.start(1000)

    def _update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            self.timer_lbl.setText(f"⏱️ {mins:02d}:{secs:02d}")
        else:
            self.timer.stop()
            self._show_message("Time's Up!", "Thời gian làm bài đã hết!", is_warning=True)

    def _run_local_tests(self):
        if not self.active_challenge:
            return False
            
        code = self.code_editor.toPlainText()
        test_cases_json = self.active_challenge["test_cases"]
        
        self.console.setText("Running local test suite...")
        self.console.setStyleSheet("background-color: #020617; color: #38BDF8; font-family: Consolas, monospace; font-size: 11px;")
        
        # Quick process events to draw "running..." text
        QGuiApplication.processEvents()
        
        test_cases = json.loads(test_cases_json)
        
        # Capture standard out
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        try:
            # Create isolated local namespace
            local_scope = {}
            exec(code, {}, local_scope)
            
            # Retrieve the function defined by the user
            func = None
            for key, val in local_scope.items():
                if callable(val) and not key.startswith("__"):
                    func = val
                    break
                    
            if not func:
                sys.stdout = old_stdout
                self.console.setText("❌ Error: No function defined in code workspace.\nPlease define a python function matching the challenge.")
                self.console.setStyleSheet("background-color: #020617; color: #EF4444; font-family: Consolas, monospace; font-size: 11px;")
                return False
                
            # Execute cases
            passed_cases = 0
            for idx, tc in enumerate(test_cases):
                args = tc["input"]
                expected = tc["output"]
                
                # Clone parameters for safe in-place edits (e.g. string arrays)
                import copy
                cloned_args = copy.deepcopy(args)
                
                result = func(*cloned_args)
                
                # Handle in-place string arrays that return None but modify inputs
                if result is None and len(cloned_args) == 1:
                    result = cloned_args[0]
                    
                # Standardize structures for clean equivalence comparison
                if isinstance(result, tuple):
                    result = list(result)
                if isinstance(expected, tuple):
                    expected = list(expected)
                    
                if result != expected:
                    sys.stdout = old_stdout
                    console_out = redirected_output.getvalue()
                    err_msg = f"❌ Test Case {idx + 1} Failed!\n\nInput Params: {args}\nExpected Output: {expected}\nReturned Output: {result}\n"
                    if console_out:
                        err_msg += f"\nCaptured console stdout:\n{console_out}"
                    self.console.setText(err_msg)
                    self.console.setStyleSheet("background-color: #020617; color: #EF4444; font-family: Consolas, monospace; font-size: 11px;")
                    return False
                passed_cases += 1
                
            sys.stdout = old_stdout
            console_out = redirected_output.getvalue()
            success_msg = f"✅ Success: All {passed_cases} Test Cases Passed!\n"
            if console_out:
                success_msg += f"\nCaptured console stdout:\n{console_out}"
            self.console.setText(success_msg)
            self.console.setStyleSheet("background-color: #020617; color: #10B981; font-family: Consolas, monospace; font-size: 11px;")
            return True
            
        except Exception:
            sys.stdout = old_stdout
            tb = traceback.format_exc()
            self.console.setText(f"❌ Syntax or Runtime Exception:\n{tb}")
            self.console.setStyleSheet("background-color: #020617; color: #EF4444; font-family: Consolas, monospace; font-size: 11px;")
            return False

    def _get_ai_mentor_review(self):
        if not self.active_challenge:
            return
            
        # First, run local tests to check correctness
        passed = self._run_local_tests()
        
        self.console.setText("Querying AI Coding Mentor review...\n(Testing local Ollama LLM endpoint, falling back to structural analysis if offline)")
        self.console.setStyleSheet("background-color: #020617; color: #A78BFA; font-family: Consolas, monospace; font-size: 11px;")
        QGuiApplication.processEvents()
        
        code = self.code_editor.toPlainText()
        cid = self.active_challenge["id"]
        
        prompt = f"""
        You are an expert AI Coding Mentor. Analyze the following Python solution for the coding challenge '{cid}'.
        Test execution passed: {passed}
        
        Code:
        ```python
        {code}
        ```
        
        Please provide:
        1. Rating: (1 to 5 stars)
        2. Time Complexity: (e.g. O(N), O(N^2))
        3. Space Complexity: (e.g. O(1), O(N))
        4. Code Quality & optimization advice.
        Keep the response concise, constructive, and formatted in clear markdown.
        """
        
        ai_text = None
        # Try local Ollama service
        try:
            url = "http://localhost:11434/api/generate"
            payload = json.dumps({
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=2.0) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                ai_text = res_data.get("response", "")
        except Exception:
            # Fallback to local analysis
            pass
            
        if not ai_text:
            ai_text = self._analyze_code_structurally(cid, code, passed)
            
        self.console.setText(ai_text)
        self.console.setStyleSheet("background-color: #020617; color: #E2E8F0; font-family: Consolas, monospace; font-size: 11px;")
        
        # Save Attempt in submission table
        code_lab_db.save_submission(cid, code, "Attempted", ai_text, 0)
        self.refresh()

    def _analyze_code_structurally(self, challenge_id, code, passed):
        # Strip comments and strings for analysis
        cleaned = re.sub(r'#.*', '', code)
        cleaned = re.sub(r'""".*?"""', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"'''.*?'''", '', cleaned, flags=re.DOTALL)
        
        # Check nested loops
        has_nested = False
        lines = [l for l in cleaned.split('\n') if l.strip()]
        for idx, l in enumerate(lines):
            if ("for " in l or "while " in l) and idx + 1 < len(lines):
                indent = len(l) - len(l.lstrip())
                for next_l in lines[idx+1:]:
                    next_indent = len(next_l) - len(next_l.lstrip())
                    if next_indent <= indent:
                        break
                    if next_indent > indent and ("for " in next_l or "while " in next_l):
                        has_nested = True
                        break
                if has_nested:
                    break
                    
        # Check list/dict variables
        uses_dict = "dict(" in cleaned or "{" in cleaned or "set(" in cleaned
        uses_list = "list(" in cleaned or "[" in cleaned or ".append(" in cleaned
        
        time_comp = "O(1)"
        space_comp = "O(1)"
        score = 5
        suggestions = []
        
        if challenge_id == "sum-two-numbers":
            time_comp = "O(1)"
            space_comp = "O(1)"
            score = 5
            suggestions.append("🌟 Perfect! Your solution performs a basic addition in O(1) constant time and space.")
            
        elif challenge_id == "two-sum":
            if has_nested:
                time_comp = "O(N^2)"
                space_comp = "O(1)"
                score = 3
                suggestions.append("⚠️ You are using nested loops to check all pairs. This takes O(N^2) time.")
                suggestions.append("💡 Optimization: Use a Hash Map (Python `dict`) to store indices. This checks for matches in a single pass, reducing time complexity to O(N) at the expense of O(N) space.")
            else:
                time_comp = "O(N)"
                space_comp = "O(N)"
                score = 5
                suggestions.append("🌟 Excellent! Your solution uses a Hash Map to find the index target in linear time.")
                
        elif challenge_id == "reverse-string":
            if uses_list or uses_dict:
                time_comp = "O(N)"
                space_comp = "O(N)"
                score = 4
                suggestions.append("⚠️ Correct but allocating extra arrays consumes O(N) space.")
                suggestions.append("💡 Optimization: Use the two-pointer swap technique to reverse characters in-place, achieving O(1) space complexity.")
            else:
                time_comp = "O(N)"
                space_comp = "O(1)"
                score = 5
                suggestions.append("🌟 Excellent! You reversed the string in-place with O(1) space complexity.")
                
        elif challenge_id == "palindrome-number":
            if "str(" in cleaned:
                time_comp = "O(log N)"
                space_comp = "O(log N)"
                score = 4
                suggestions.append("⚠️ You converted the integer to a string. While simple, it requires O(log N) extra space.")
                suggestions.append("💡 Optimization: Try reversing the mathematically generated digits (using `% 10` and `// 10`) without string allocation.")
            else:
                time_comp = "O(log N)"
                space_comp = "O(1)"
                score = 5
                suggestions.append("🌟 Fantastic! You solved it mathematically with O(1) space complexity.")
                
        elif challenge_id == "valid-parentheses":
            if uses_list and (".pop(" in cleaned or "append(" in cleaned):
                time_comp = "O(N)"
                space_comp = "O(N)"
                score = 5
                suggestions.append("🌟 Perfect! You used a stack to match brackets in linear time.")
            else:
                time_comp = "O(N^2)"
                space_comp = "O(1)"
                score = 3
                suggestions.append("⚠️ Your matching algorithm might be suboptimal or missing stack constraints.")
                suggestions.append("💡 Optimization: Use a Stack list. Push open brackets, and pop to verify matches when a closed bracket is encountered.")
                
        if not passed:
            score = max(1, score - 3)
            status_eval = "❌ Code does not pass test cases. Correct the logic before submitting."
        else:
            status_eval = "✅ Code compiles and passes all test cases."
            
        stars = "⭐" * score
        
        report = f"### 🧠 AI Coding Mentor Feedback\n\n"
        report += f"**Status**: {status_eval}\n"
        report += f"**Review Rating**: {stars} ({score}/5)\n\n"
        report += f"#### Complexity Analysis:\n"
        report += f"- ⏱️ **Time Complexity**: `{time_comp}`\n"
        report += f"- 💾 **Space Complexity**: `{space_comp}`\n\n"
        report += f"#### Suggestions & Insights:\n"
        for sug in suggestions:
            report += f"- {sug}\n"
            
        if passed and score == 5:
            report += "\n- 🎉 Great job! Your code is fully optimal and matches professional standards."
            
        return report

    def _show_message(self, title, text, is_warning=False):
        msg_box = QMessageBox(self)
        if is_warning:
            msg_box.setIcon(QMessageBox.Icon.Warning)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
            }
            QLabel {
                color: #0F172A;
                font-size: 13px;
                min-width: 250px;
            }
            QPushButton {
                background-color: #10B981;
                color: #F8FAFC;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        msg_box.exec()

    def _submit_solution(self):
        if not self.active_challenge:
            return
            
        passed = self._run_local_tests()
        if not passed:
            self._show_message("Validation Error", "Code must pass all test cases before submitting.", is_warning=True)
            return
            
        code = self.code_editor.toPlainText()
        cid = self.active_challenge["id"]
        
        # Run AI analysis to save feedback
        ai_feedback = self._analyze_code_structurally(cid, code, True)
        
        # Save as Solved
        code_lab_db.save_submission(cid, code, "Solved", ai_feedback, 100)
        
        self._show_message("Success", "Challenge solved and submitted successfully!")
        self.console.setText(ai_feedback + "\n\n🚀 SUBMISSION SUCCESSFUL!")
        self.console.setStyleSheet("background-color: #020617; color: #10B981; font-family: Consolas, monospace; font-size: 11px;")
        
        # Refresh progress and list status
        self.refresh()

    def _open_add_challenge_dialog(self):
        dialog = AddChallengeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()
