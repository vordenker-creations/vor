from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QFrame, QMessageBox, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import skill_tree_db

class MissionDialog(QDialog):
    def __init__(self, node_data, controller=None, parent=None):
        super().__init__(parent)
        self.node_data = node_data
        self.controller = controller
        self.navigation_target = None
        
        self.setWindowTitle(f"Skill Mission: {node_data.get('name')}")
        self.resize(500, 580)
        self.setStyleSheet("""
            QDialog {
                background-color: #0F172A;
                color: #F1F5F9;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: 800;
                color: #F1F5F9;
                letter-spacing: -0.5px;
            }
            QLabel#subtitle {
                font-size: 13px;
                color: #64748B;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #1E293B;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #475569;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #1E293B;
                color: #F1F5F9;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton#btnCode {
                border: 1px solid rgba(56, 189, 248, 0.4);
                color: #38BDF8;
            }
            QPushButton#btnCode:hover {
                background-color: rgba(56, 189, 248, 0.1);
            }
            QPushButton#btnInterview {
                border: 1px solid rgba(139, 92, 246, 0.4);
                color: #A78BFA;
            }
            QPushButton#btnInterview:hover {
                background-color: rgba(139, 92, 246, 0.1);
            }
            QPushButton#btnPlanner {
                border: 1px solid rgba(245, 158, 11, 0.4);
                color: #FBBF24;
            }
            QPushButton#btnPlanner:hover {
                background-color: rgba(245, 158, 11, 0.1);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header Info
        header_widget = QWidget()
        header_lay = QVBoxLayout(header_widget)
        header_lay.setContentsMargins(0, 0, 0, 0)
        header_lay.setSpacing(4)
        
        lbl_title = QLabel(f"⚡ {node_data.get('name')} Mission", objectName="title")
        lbl_sub = QLabel(f"Complete challenges to master this skill", objectName="subtitle")
        header_lay.addWidget(lbl_title)
        header_lay.addWidget(lbl_sub)
        layout.addWidget(header_widget)

        # Mastery percentage overview
        self.mastery_lbl = QLabel(f"Current Mastery: {node_data.get('mastery', 0)}%")
        self.mastery_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #38BDF8;")
        layout.addWidget(self.mastery_lbl)

        # Sub-tasks/Missions List Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Load missions
        self.missions = skill_tree_db.get_missions_by_node(node_id=node_data["id"], skill_name=node_data["name"])
        self.checkboxes = []

        for m in self.missions:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #1E293B;
                    border-radius: 12px;
                    border: 1px solid #334155;
                }
            """)
            item_lay = QHBoxLayout(item_frame)
            item_lay.setContentsMargins(15, 12, 15, 12)
            
            chk = QCheckBox(m["title"])
            chk.setChecked(bool(m["completed"]))
            chk.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Save mission reference
            chk.setProperty("mission_id", m["id"])
            
            self._update_checkbox_styling(chk)
            
            # Connect toggle event
            chk.toggled.connect(lambda checked, c=chk: self._on_checkbox_toggled(checked, c))
            
            item_lay.addWidget(chk)
            self.scroll_layout.addWidget(item_frame)
            self.checkboxes.append(chk)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)

        # Deep Links Section Title
        lbl_links = QLabel("CORE HUBS DEEP LINKS")
        lbl_links.setStyleSheet("font-size: 11px; font-weight: 800; color: #475569; letter-spacing: 1.5px;")
        layout.addWidget(lbl_links)

        # Deep Links row
        links_layout = QHBoxLayout()
        links_layout.setSpacing(10)

        btn_code = QPushButton("💻 Code Lab", objectName="btnCode")
        btn_code.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_code.clicked.connect(lambda: self._navigate_to("CodeAlgorithmLab"))
        links_layout.addWidget(btn_code)

        btn_interview = QPushButton("🤖 Interview", objectName="btnInterview")
        btn_interview.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_interview.clicked.connect(lambda: self._navigate_to("MockInterviews"))
        links_layout.addWidget(btn_interview)

        btn_planner = QPushButton("📅 Study Plan", objectName="btnPlanner")
        btn_planner.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_planner.clicked.connect(lambda: self._navigate_to("SmartTaskPlanner"))
        links_layout.addWidget(btn_planner)

        layout.addLayout(links_layout)

        # Bottom Close button
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def _update_checkbox_styling(self, chk):
        if chk.isChecked():
            chk.setStyleSheet("""
                QCheckBox {
                    color: #64748B;
                    font-size: 13px;
                    font-weight: 500;
                    text-decoration: line-through;
                }
            """)
        else:
            chk.setStyleSheet("""
                QCheckBox {
                    color: #E2E8F0;
                    font-size: 13px;
                    font-weight: 600;
                }
            """)

    def _on_checkbox_toggled(self, checked, chk):
        # Update styling
        self._update_checkbox_styling(chk)
        
        # Save to DB
        mission_id = chk.property("mission_id")
        completed = 1 if checked else 0
        skill_tree_db.update_mission_completed(mission_id, completed)
        
        # Recalculate node mastery
        completed_count = sum(1 for c in self.checkboxes if c.isChecked())
        total_count = len(self.checkboxes)
        new_mastery = int((completed_count / total_count) * 100) if total_count > 0 else 0
        
        # Update node in DB
        node_id = self.node_data["id"]
        node_name = self.node_data["name"]
        unlocked = 1 if self.node_data["unlocked"] else 0
        skill_tree_db.update_node(node_id, node_name, new_mastery, unlocked)
        self.node_data["mastery"] = new_mastery # keep local state synced
        
        # Update dialog label
        self.mastery_lbl.setText(f"Current Mastery: {new_mastery}%")

    def _navigate_to(self, target):
        self.navigation_target = target
        self.accept()
