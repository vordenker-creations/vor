import json
import re
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QComboBox, QMessageBox, QScrollArea, QWidget, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import code_lab_db

class AddChallengeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Programming Challenge")
        self.resize(520, 720)
        self.test_cases_rows = []

        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F1F5F9;
            }
            QLabel {
                color: #94A3B8;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #38BDF8;
            }
            QScrollArea {
                border: 1px solid #334155;
                background-color: #1E293B;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton#btnPrimary {
                background-color: #38BDF8;
                color: #0F172A;
                border: none;
            }
            QPushButton#btnPrimary:hover {
                background-color: #0EA5E9;
            }
        """)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        main_scroll.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 1. Challenge Title
        self.layout.addWidget(QLabel("Challenge Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g. Find Maximum Number")
        self.layout.addWidget(self.title_input)

        # 2. Topic/Category
        self.layout.addWidget(QLabel("Topic/Category:"))
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("e.g. Array, Math, String")
        self.layout.addWidget(self.topic_input)

        # 3. Difficulty
        self.layout.addWidget(QLabel("Difficulty Level:"))
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["Easy", "Medium", "Hard"])
        self.layout.addWidget(self.diff_combo)

        # 4. Description (HTML supported)
        self.layout.addWidget(QLabel("Description (HTML supported):"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Write details here... e.g. Given a list <code>nums</code>, return the largest number.")
        self.desc_input.setMinimumHeight(100)
        self.layout.addWidget(self.desc_input)

        # 5. Starter Code
        self.layout.addWidget(QLabel("Starter Code Template:"))
        self.starter_input = QTextEdit()
        self.starter_input.setFont(QFont("Consolas", 11))
        self.starter_input.setPlaceholderText("def find_max(nums):\n    # Write your code here\n    pass")
        self.starter_input.setMinimumHeight(120)
        self.layout.addWidget(self.starter_input)

        # 6. Test Cases Section
        self.layout.addWidget(QLabel("Test Cases (Inputs must be JSON Lists; Outputs JSON values):"))
        
        # Header Row
        header_widget = QWidget()
        header_lay = QHBoxLayout(header_widget)
        header_lay.setContentsMargins(0, 0, 0, 0)
        header_lay.setSpacing(8)
        lbl_in = QLabel("Input Args (JSON List)")
        lbl_in.setStyleSheet("color: #64748B; font-size: 11px;")
        lbl_out = QLabel("Expected Output (JSON)")
        lbl_out.setStyleSheet("color: #64748B; font-size: 11px;")
        header_lay.addWidget(lbl_in, 2)
        header_lay.addWidget(lbl_out, 1)
        header_lay.addSpacing(44) # spacer for delete button alignment
        self.layout.addWidget(header_widget)

        # Container for dynamic test case rows
        self.cases_container = QWidget()
        self.cases_layout = QVBoxLayout(self.cases_container)
        self.cases_layout.setContentsMargins(0, 0, 0, 0)
        self.cases_layout.setSpacing(8)
        self.layout.addWidget(self.cases_container)

        # Add Test Case button
        self.btn_add_case = QPushButton("➕ Add Test Case")
        self.btn_add_case.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_case.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                color: #38BDF8;
                border: 1px dashed #334155;
            }
            QPushButton:hover {
                background-color: #243249;
                border: 1px dashed #38BDF8;
            }
        """)
        self.btn_add_case.clicked.connect(self.add_test_case_row)
        self.layout.addWidget(self.btn_add_case)

        # Add first row by default
        self.add_test_case_row()

        main_scroll.setWidget(scroll_content)
        outer_layout.addWidget(main_scroll)

        # Dialog Action Buttons Footer
        footer = QFrame()
        footer.setStyleSheet("QFrame { background-color: #0F172A; border-top: 1px solid #334155; }")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        footer_layout.setSpacing(12)
        
        footer_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        self.btn_cancel.clicked.connect(self.reject)
        footer_layout.addWidget(self.btn_cancel)
        
        self.btn_save = QPushButton("Save Challenge")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #38BDF8;
                color: #0F172A;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0EA5E9;
            }
        """)
        self.btn_save.clicked.connect(self.accept)
        footer_layout.addWidget(self.btn_save)
        
        outer_layout.addWidget(footer)

    def add_test_case_row(self, input_val="", output_val=""):
        row_widget = QWidget()
        row_lay = QHBoxLayout(row_widget)
        row_lay.setContentsMargins(0, 0, 0, 0)
        row_lay.setSpacing(8)
        
        input_input = QLineEdit()
        input_input.setPlaceholderText("e.g. [[1, 5, 3]] or [2, 3]")
        input_input.setText(input_val)
        
        output_input = QLineEdit()
        output_input.setPlaceholderText("e.g. 5")
        output_input.setText(output_val)
        
        btn_del = QPushButton("🗑️")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.setFixedWidth(36)
        btn_del.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        
        row_lay.addWidget(input_input, 2)
        row_lay.addWidget(output_input, 1)
        row_lay.addWidget(btn_del)
        
        self.cases_layout.addWidget(row_widget)
        
        row_data = {
            "widget": row_widget,
            "input": input_input,
            "output": output_input
        }
        self.test_cases_rows.append(row_data)
        
        btn_del.clicked.connect(lambda: self.remove_test_case_row(row_data))

    def remove_test_case_row(self, row_data):
        if len(self.test_cases_rows) <= 1:
            QMessageBox.warning(self, "Validation Error", "You must keep at least 1 test case.")
            return
            
        self.test_cases_rows.remove(row_data)
        row_data["widget"].deleteLater()

    def accept(self):
        title = self.title_input.text().strip()
        topic = self.topic_input.text().strip()
        diff = self.diff_combo.currentText()
        desc = self.desc_input.toPlainText().strip()
        starter = self.starter_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Validation Error", "Challenge Title cannot be empty.")
            return
        if not topic:
            QMessageBox.warning(self, "Validation Error", "Topic cannot be empty.")
            return
        if not desc:
            QMessageBox.warning(self, "Validation Error", "Description cannot be empty.")
            return
        if not starter:
            QMessageBox.warning(self, "Validation Error", "Starter Code cannot be empty.")
            return
            
        parsed_cases = []
        for idx, row in enumerate(self.test_cases_rows):
            in_text = row["input"].text().strip()
            out_text = row["output"].text().strip()
            
            if not in_text or not out_text:
                QMessageBox.warning(self, "Validation Error", f"Test case {idx + 1} has empty fields.")
                return
                
            try:
                in_json = json.loads(in_text)
                if not isinstance(in_json, list):
                    QMessageBox.warning(
                        self, 
                        "Validation Error", 
                        f"Test case {idx + 1} Input must be a valid JSON List (representing function arguments).\nExample: [2, 3] or [[1, 5, 3]]"
                    )
                    return
            except Exception:
                QMessageBox.warning(self, "Validation Error", f"Test case {idx + 1} Input is not valid JSON.\nExample: [2, 3] or [\"hello\"]")
                return
                
            try:
                out_json = json.loads(out_text)
            except Exception:
                QMessageBox.warning(self, "Validation Error", f"Test case {idx + 1} Expected Output is not valid JSON.\nExample: 5 or \"olleh\" or true")
                return
                
            parsed_cases.append({
                "input": in_json,
                "output": out_json
            })
            
        base_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        if not base_id:
            base_id = "custom-challenge"
            
        challenge_id = base_id
        counter = 1
        while code_lab_db.get_challenge_by_id(challenge_id) is not None:
            challenge_id = f"{base_id}-{counter}"
            counter += 1
            
        try:
            code_lab_db.add_custom_challenge(
                challenge_id,
                title,
                topic,
                diff,
                desc,
                starter,
                json.dumps(parsed_cases)
            )
            QMessageBox.information(self, "Success", f"Challenge '{title}' added successfully!")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save challenge to database:\n{str(e)}")
