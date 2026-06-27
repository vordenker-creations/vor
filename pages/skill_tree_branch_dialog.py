from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QColorDialog, QMessageBox, QComboBox, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import skill_tree_db

class BranchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Skill Branches")
        self.resize(450, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                color: #0F172A;
            }
            QLabel {
                color: #475569;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit, QComboBox {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #2563EB;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #0F172A;
                selection-background-color: #EFF6FF;
                selection-color: #2563EB;
                border: 1px solid #CBD5E1;
            }
            QPushButton {
                background-color: #F1F5F9;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
            QPushButton#btnPrimary {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
            }
            QPushButton#btnPrimary:hover {
                background-color: #1D4ED8;
            }
            QPushButton#btnDelete {
                background-color: #EF4444;
                color: #FFFFFF;
                border: none;
            }
            QPushButton#btnDelete:hover {
                background-color: #DC2626;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Tab or Dropdown selection for Action
        self.action_label = QLabel("Select Action:")
        self.layout.addWidget(self.action_label)

        self.action_combo = QComboBox()
        self.action_combo.addItems(["Add New Branch", "Edit/Delete Existing Branch"])
        self.action_combo.currentIndexChanged.connect(self._toggle_action_view)
        self.layout.addWidget(self.action_combo)

        # ==========================================
        # VIEW 1: Add New Branch
        # ==========================================
        self.add_widget = QWidget()
        add_lay = QVBoxLayout(self.add_widget)
        add_lay.setContentsMargins(0, 0, 0, 0)
        add_lay.setSpacing(12)

        add_lay.addWidget(QLabel("Branch Name:"))
        self.add_name_input = QLineEdit()
        self.add_name_input.setPlaceholderText("e.g. Frontend Development")
        add_lay.addWidget(self.add_name_input)

        # Colors selection
        color_row1 = QHBoxLayout()
        self.color_start_val = "#38BDF8"
        self.btn_color_start = QPushButton("Pick Start Color")
        self.btn_color_start.clicked.connect(lambda: self._pick_color("start"))
        self.color_start_lbl = QLabel("Color: █")
        self.color_start_lbl.setStyleSheet(f"color: {self.color_start_val}; font-size: 16px;")
        color_row1.addWidget(self.btn_color_start)
        color_row1.addWidget(self.color_start_lbl)
        add_lay.addLayout(color_row1)

        color_row2 = QHBoxLayout()
        self.color_end_val = "#3B82F6"
        self.btn_color_end = QPushButton("Pick End Color")
        self.btn_color_end.clicked.connect(lambda: self._pick_color("end"))
        self.color_end_lbl = QLabel("Color: █")
        self.color_end_lbl.setStyleSheet(f"color: {self.color_end_val}; font-size: 16px;")
        color_row2.addWidget(self.btn_color_end)
        color_row2.addWidget(self.color_end_lbl)
        add_lay.addLayout(color_row2)

        self.btn_add_submit = QPushButton("Add Branch")
        self.btn_add_submit.setObjectName("btnPrimary")
        self.btn_add_submit.clicked.connect(self._submit_add)
        add_lay.addWidget(self.btn_add_submit)

        self.layout.addWidget(self.add_widget)

        # ==========================================
        # VIEW 2: Edit/Delete Existing Branch
        # ==========================================
        self.edit_widget = QWidget()
        edit_lay = QVBoxLayout(self.edit_widget)
        edit_lay.setContentsMargins(0, 0, 0, 0)
        edit_lay.setSpacing(12)

        edit_lay.addWidget(QLabel("Select Branch to Edit/Delete:"))
        self.branch_combo = QComboBox()
        self.branch_combo.currentIndexChanged.connect(self._load_branch_details)
        edit_lay.addWidget(self.branch_combo)

        edit_lay.addWidget(QLabel("New Name (Rename):"))
        self.edit_name_input = QLineEdit()
        edit_lay.addWidget(self.edit_name_input)

        # Colors selection
        color_row3 = QHBoxLayout()
        self.edit_color_start_val = "#FFFFFF"
        self.btn_edit_color_start = QPushButton("Pick Start Color")
        self.btn_edit_color_start.clicked.connect(lambda: self._pick_color("edit_start"))
        self.edit_color_start_lbl = QLabel("Color: █")
        self.edit_color_start_lbl.setStyleSheet(f"color: {self.edit_color_start_val}; font-size: 16px;")
        color_row3.addWidget(self.btn_edit_color_start)
        color_row3.addWidget(self.edit_color_start_lbl)
        edit_lay.addLayout(color_row3)

        color_row4 = QHBoxLayout()
        self.edit_color_end_val = "#FFFFFF"
        self.btn_edit_color_end = QPushButton("Pick End Color")
        self.btn_edit_color_end.clicked.connect(lambda: self._pick_color("edit_end"))
        self.edit_color_end_lbl = QLabel("Color: █")
        self.edit_color_end_lbl.setStyleSheet(f"color: {self.edit_color_end_val}; font-size: 16px;")
        color_row4.addWidget(self.btn_edit_color_end)
        color_row4.addWidget(self.edit_color_end_lbl)
        edit_lay.addLayout(color_row4)

        # Action buttons
        btn_box = QHBoxLayout()
        self.btn_edit_submit = QPushButton("Save Changes")
        self.btn_edit_submit.setObjectName("btnPrimary")
        self.btn_edit_submit.clicked.connect(self._submit_edit)
        
        self.btn_delete = QPushButton("Delete Branch")
        self.btn_delete.setObjectName("btnDelete")
        self.btn_delete.clicked.connect(self._submit_delete)
        
        btn_box.addWidget(self.btn_edit_submit)
        btn_box.addWidget(self.btn_delete)
        edit_lay.addLayout(btn_box)

        self.layout.addWidget(self.edit_widget)
        self.edit_widget.hide()

        # Load initial branches list
        self._refresh_branches()

    def _toggle_action_view(self, index):
        if index == 0:
            self.edit_widget.hide()
            self.add_widget.show()
        else:
            self.add_widget.hide()
            self._refresh_branches()
            self.edit_widget.show()

    def _refresh_branches(self):
        self.branches = skill_tree_db.get_all_branches()
        self.branch_combo.clear()
        for b in self.branches:
            self.branch_combo.addItem(b["name"], b)
        self._load_branch_details()

    def _load_branch_details(self):
        b = self.branch_combo.currentData()
        if b:
            self.edit_name_input.setText(b["name"])
            self.edit_color_start_val = b["color_start"]
            self.edit_color_end_val = b["color_end"]
            self.edit_color_start_lbl.setStyleSheet(f"color: {self.edit_color_start_val}; font-size: 16px;")
            self.edit_color_end_lbl.setStyleSheet(f"color: {self.edit_color_end_val}; font-size: 16px;")

    def _pick_color(self, target):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if target == "start":
                self.color_start_val = hex_color
                self.color_start_lbl.setStyleSheet(f"color: {hex_color}; font-size: 16px;")
            elif target == "end":
                self.color_end_val = hex_color
                self.color_end_lbl.setStyleSheet(f"color: {hex_color}; font-size: 16px;")
            elif target == "edit_start":
                self.edit_color_start_val = hex_color
                self.edit_color_start_lbl.setStyleSheet(f"color: {hex_color}; font-size: 16px;")
            elif target == "edit_end":
                self.edit_color_end_val = hex_color
                self.edit_color_end_lbl.setStyleSheet(f"color: {hex_color}; font-size: 16px;")

    def _submit_add(self):
        name = self.add_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Branch Name cannot be empty.")
            return

        success = skill_tree_db.add_branch(name, self.color_start_val, self.color_end_val)
        if success:
            QMessageBox.information(self, "Success", f"Branch '{name}' added successfully!")
            self.add_name_input.clear()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Branch Name already exists.")

    def _submit_edit(self):
        b = self.branch_combo.currentData()
        if not b:
            return
        
        new_name = self.edit_name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Validation Error", "Branch Name cannot be empty.")
            return

        success = skill_tree_db.update_branch(b["name"], new_name, self.edit_color_start_val, self.edit_color_end_val)
        if success:
            QMessageBox.information(self, "Success", "Branch updated successfully!")
            self._refresh_branches()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Could not update branch. Check if the name collides.")

    def _submit_delete(self):
        b = self.branch_combo.currentData()
        if not b:
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete branch '{b['name']}'? All its nodes and connections will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            skill_tree_db.delete_branch(b["name"])
            QMessageBox.information(self, "Success", "Branch deleted successfully!")
            self._refresh_branches()
            self.accept()
