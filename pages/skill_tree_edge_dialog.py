from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt
from database import skill_tree_db

class EdgeDialog(QDialog):
    def __init__(self, current_branch_name=None, parent=None):
        super().__init__(parent)
        self.current_branch_name = current_branch_name
        self.setWindowTitle("Manage Skill Connections")
        self.resize(450, 400)
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
            QComboBox {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #38BDF8;
            }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: #F1F5F9;
                selection-background-color: #38BDF8;
                selection-color: #0F172A;
                border: 1px solid #334155;
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
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 1. Action Type Selection
        self.layout.addWidget(QLabel("Select Action:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems(["Add Connection Path", "Remove Connection Path"])
        self.action_combo.currentIndexChanged.connect(self._toggle_action_view)
        self.layout.addWidget(self.action_combo)

        # 2. Branch selection (all actions need a branch context)
        self.layout.addWidget(QLabel("Skill Branch:"))
        self.branch_combo = QComboBox()
        self.branch_combo.currentIndexChanged.connect(self._on_branch_changed)
        self.layout.addWidget(self.branch_combo)

        # ==========================================
        # VIEW 1: Add Connection
        # ==========================================
        self.add_widget = QWidget()
        add_lay = QVBoxLayout(self.add_widget)
        add_lay.setContentsMargins(0, 0, 0, 0)
        add_lay.setSpacing(12)

        add_lay.addWidget(QLabel("Prerequisite Skill (From):"))
        self.source_combo = QComboBox()
        add_lay.addWidget(self.source_combo)

        add_lay.addWidget(QLabel("Next Skill (To):"))
        self.target_combo = QComboBox()
        add_lay.addWidget(self.target_combo)

        self.btn_add_submit = QPushButton("Add Connection")
        self.btn_add_submit.setObjectName("btnPrimary")
        self.btn_add_submit.clicked.connect(self._submit_add)
        add_lay.addWidget(self.btn_add_submit)

        self.layout.addWidget(self.add_widget)

        # ==========================================
        # VIEW 2: Delete Connection
        # ==========================================
        self.delete_widget = QWidget()
        delete_lay = QVBoxLayout(self.delete_widget)
        delete_lay.setContentsMargins(0, 0, 0, 0)
        delete_lay.setSpacing(12)

        delete_lay.addWidget(QLabel("Select Connection to Remove:"))
        self.edge_combo = QComboBox()
        delete_lay.addWidget(self.edge_combo)

        self.btn_delete_submit = QPushButton("Remove Connection")
        self.btn_delete_submit.setObjectName("btnDelete")
        self.btn_delete_submit.clicked.connect(self._submit_delete)
        delete_lay.addWidget(self.btn_delete_submit)

        self.layout.addWidget(self.delete_widget)
        self.delete_widget.hide()

        # Load branches
        self.branches = skill_tree_db.get_all_branches()
        for b in self.branches:
            self.branch_combo.addItem(b["name"])
        
        if current_branch_name:
            self.branch_combo.setCurrentText(current_branch_name)

        self._on_branch_changed()

    def _toggle_action_view(self, index):
        if index == 0:
            self.delete_widget.hide()
            self.add_widget.show()
        else:
            self.add_widget.hide()
            self.delete_widget.show()
        self._on_branch_changed()

    def _on_branch_changed(self):
        branch_name = self.branch_combo.currentText()
        if not branch_name:
            return

        self.nodes = skill_tree_db.get_nodes_by_branch(branch_name)
        
        # Populate Source and Target Combos (Add mode)
        self.source_combo.clear()
        self.target_combo.clear()
        for node in self.nodes:
            self.source_combo.addItem(node["name"], node["id"])
            self.target_combo.addItem(node["name"], node["id"])

        # Populate Edges Combo (Delete mode)
        self.edge_combo.clear()
        edges = skill_tree_db.get_edges_by_branch(branch_name)
        
        # We need a dictionary to map node IDs to their names
        node_map = {n["id"]: n["name"] for n in self.nodes}
        for edge in edges:
            src_name = node_map.get(edge["source_node_id"], f"ID {edge['source_node_id']}")
            tgt_name = node_map.get(edge["target_node_id"], f"ID {edge['target_node_id']}")
            self.edge_combo.addItem(f"{src_name} ➔ {tgt_name}", edge["id"])

    def _submit_add(self):
        branch_name = self.branch_combo.currentText()
        source_id = self.source_combo.currentData()
        target_id = self.target_combo.currentData()

        if source_id == target_id:
            QMessageBox.warning(self, "Validation Error", "A skill cannot be connected to itself.")
            return

        if not source_id or not target_id:
            QMessageBox.warning(self, "Validation Error", "Invalid skills selected.")
            return

        res = skill_tree_db.add_edge(branch_name, source_id, target_id)
        if res:
            QMessageBox.information(self, "Success", "Connection path added successfully!")
            self._on_branch_changed()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "This connection already exists or creates a cyclic dependency loop.")

    def _submit_delete(self):
        edge_id = self.edge_combo.currentData()
        if not edge_id:
            QMessageBox.warning(self, "Validation Error", "No connection selected to remove.")
            return

        reply = QMessageBox.question(
            self, "Confirm Remove",
            "Are you sure you want to remove this connection path?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            skill_tree_db.delete_edge(edge_id)
            QMessageBox.information(self, "Success", "Connection path removed successfully!")
            self._on_branch_changed()
            self.accept()
