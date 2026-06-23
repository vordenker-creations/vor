from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QCheckBox, QComboBox, QMessageBox, QWidget, QScrollArea
)
from PyQt6.QtCore import Qt
from database import skill_tree_db

class NodeDialog(QDialog):
    def __init__(self, node_data=None, current_branch_name=None, parent=None):
        super().__init__(parent)
        self.node_data = node_data
        self.current_branch_name = current_branch_name
        self.is_edit = node_data is not None

        if self.is_edit:
            self.setWindowTitle(f"Edit Skill: {node_data.get('name')}")
        else:
            self.setWindowTitle("Add New Skill Node")

        self.resize(420, 520)
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
            QLineEdit, QComboBox, QSpinBox {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #38BDF8;
            }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: #F1F5F9;
                selection-background-color: #38BDF8;
                selection-color: #0F172A;
                border: 1px solid #334155;
            }
            QCheckBox {
                color: #94A3B8;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 16px;
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
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 1. Branch Selection (Disabled in edit mode to preserve branch structure)
        self.layout.addWidget(QLabel("Skill Branch:"))
        self.branch_combo = QComboBox()
        self.layout.addWidget(self.branch_combo)
        
        # Load branches
        self.branches = skill_tree_db.get_all_branches()
        for b in self.branches:
            self.branch_combo.addItem(b["name"])
        
        if self.is_edit:
            self.branch_combo.setCurrentText(node_data.get("branch_name", ""))
            self.branch_combo.setEnabled(False)
        elif current_branch_name:
            self.branch_combo.setCurrentText(current_branch_name)

        # 2. Node Name
        self.layout.addWidget(QLabel("Skill Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. React.js, NumPy, PyTorch")
        if self.is_edit:
            self.name_input.setText(node_data.get("name", ""))
        self.layout.addWidget(self.name_input)

        # 3. Prerequisite / Parent Skill Dropdown
        self.layout.addWidget(QLabel("Prerequisite (Parent) Skill:"))
        self.parent_combo = QComboBox()
        self.layout.addWidget(self.parent_combo)
        
        # Populate parents based on selected branch
        self.branch_combo.currentTextChanged.connect(self._populate_parents)
        self._populate_parents()

        # 4. Mastery
        self.layout.addWidget(QLabel("Mastery Level (0 - 100%):"))
        self.mastery_spin = QSpinBox()
        self.mastery_spin.setRange(0, 100)
        if self.is_edit:
            self.mastery_spin.setValue(int(node_data.get("mastery", 0)))
        else:
            self.mastery_spin.setValue(0)
        self.layout.addWidget(self.mastery_spin)

        # 5. Unlocked Checkbox
        self.unlocked_checkbox = QCheckBox("Unlocked / Available")
        if self.is_edit:
            self.unlocked_checkbox.setChecked(bool(node_data.get("unlocked", False)))
        else:
            self.unlocked_checkbox.setChecked(True)
        self.layout.addWidget(self.unlocked_checkbox)

        # 5.5. Related Projects
        if self.is_edit:
            self.layout.addWidget(QLabel("Related Portfolio Projects:"))
            
            # Fetch from portfolio_db
            related_projects = []
            try:
                from database import portfolio_db
                all_projects = portfolio_db.get_all_projects()
                for p in all_projects:
                    linked = [s.strip().lower() for s in p.get("skills", "").split(",") if s.strip()]
                    if self.node_data["name"].lower() in linked:
                        related_projects.append(p)
            except Exception as e:
                print(f"Error loading related projects: {e}")
                
            if related_projects:
                proj_scroll = QScrollArea()
                proj_scroll.setFixedHeight(80)
                proj_scroll_content = QWidget()
                proj_scroll_content.setStyleSheet("background: transparent;")
                proj_lay = QVBoxLayout(proj_scroll_content)
                proj_lay.setContentsMargins(5, 5, 5, 5)
                proj_lay.setSpacing(6)
                
                for p in related_projects:
                    lbl = QLabel(f"💼 {p['title']} ({p['progress']}% Complete)")
                    lbl.setStyleSheet("""
                        color: #E2E8F0;
                        font-size: 12px;
                        background-color: #1E293B;
                        border: 1px solid #334155;
                        border-radius: 6px;
                        padding: 4px 8px;
                    """)
                    proj_lay.addWidget(lbl)
                proj_lay.addStretch()
                proj_scroll.setWidget(proj_scroll_content)
                proj_scroll.setWidgetResizable(True)
                self.layout.addWidget(proj_scroll)
            else:
                none_lbl = QLabel("No portfolio projects associated with this skill.")
                none_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-style: italic;")
                self.layout.addWidget(none_lbl)

        # 6. Action buttons
        btn_box = QHBoxLayout()
        if self.is_edit:
            self.btn_submit = QPushButton("Save Changes")
            self.btn_submit.setObjectName("btnPrimary")
            self.btn_submit.clicked.connect(self._submit)
            
            self.btn_delete = QPushButton("Delete Skill")
            self.btn_delete.setObjectName("btnDelete")
            self.btn_delete.clicked.connect(self._delete)
            
            btn_box.addWidget(self.btn_submit)
            btn_box.addWidget(self.btn_delete)
        else:
            self.btn_submit = QPushButton("Add Skill")
            self.btn_submit.setObjectName("btnPrimary")
            self.btn_submit.clicked.connect(self._submit)
            
            self.btn_cancel = QPushButton("Cancel")
            self.btn_cancel.clicked.connect(self.reject)
            
            btn_box.addWidget(self.btn_submit)
            btn_box.addWidget(self.btn_cancel)
            
        self.layout.addLayout(btn_box)

    def _populate_parents(self):
        self.parent_combo.clear()
        self.parent_combo.addItem("None (Root Skill)", None)
        
        branch_name = self.branch_combo.currentText()
        if not branch_name:
            return
            
        nodes = skill_tree_db.get_nodes_by_branch(branch_name)
        
        # In edit mode, find current parent and exclude the node itself to avoid cycles
        current_parent_id = None
        if self.is_edit:
            current_parent_id = skill_tree_db.get_parent_node_id(self.node_data["id"])
            
        for node in nodes:
            # Exclude current node
            if self.is_edit and node["id"] == self.node_data["id"]:
                continue
            self.parent_combo.addItem(node["name"], node["id"])
            
        # Select current parent if in edit mode
        if self.is_edit and current_parent_id:
            for idx in range(self.parent_combo.count()):
                if self.parent_combo.itemData(idx) == current_parent_id:
                    self.parent_combo.setCurrentIndex(idx)
                    break

    def _submit(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Skill Name cannot be empty.")
            return

        branch_name = self.branch_combo.currentText()
        mastery = self.mastery_spin.value()
        unlocked = 1 if self.unlocked_checkbox.isChecked() else 0
        parent_node_id = self.parent_combo.currentData() # returns ID or None

        if self.is_edit:
            node_id = self.node_data["id"]
            success, msg = skill_tree_db.update_node(node_id, name, mastery, unlocked, parent_node_id, change_parent=True)
            if not success:
                QMessageBox.warning(self, "Cycle Dependency Error", msg)
                return
            QMessageBox.information(self, "Success", f"Skill '{name}' updated successfully.")
        else:
            skill_tree_db.add_node(branch_name, name, mastery, unlocked, parent_node_id)
            QMessageBox.information(self, "Success", f"Skill '{name}' added successfully.")

        self.accept()

    def _delete(self):
        name = self.node_data.get("name", "Skill")
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete skill '{name}'? This will also remove any of its connected paths.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            skill_tree_db.delete_node(self.node_data["id"])
            QMessageBox.information(self, "Success", f"Skill '{name}' deleted successfully.")
            self.accept()
