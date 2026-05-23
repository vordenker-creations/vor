import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar,
                             QDialog, QComboBox, QSlider, QFormLayout, QSpinBox,
                             QLineEdit, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor
from database import crud

class MilestoneDialog(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Milestone")
        self.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        self.title_le = QLineEdit()
        self.title_le.setStyleSheet("border: 1px solid #E2E8F0; padding: 6px; border-radius: 4px;")
        
        self.status_cb = QComboBox()
        self.status_cb.addItems(["not_started", "in_progress", "completed"])
        self.status_cb.setStyleSheet("border: 1px solid #E2E8F0; padding: 6px; border-radius: 4px;")
        
        self.progress_sp = QSpinBox()
        self.progress_sp.setRange(0, 100)
        self.progress_sp.setSuffix("%")
        self.progress_sp.setStyleSheet("border: 1px solid #E2E8F0; padding: 6px; border-radius: 4px;")
        
        self.insight_te = QTextEdit()
        self.insight_te.setFixedHeight(80)
        self.insight_te.setStyleSheet("border: 1px solid #E2E8F0; padding: 6px; border-radius: 4px;")
        
        form.addRow("Title:", self.title_le)
        form.addRow("Status:", self.status_cb)
        form.addRow("Progress:", self.progress_sp)
        form.addRow("Notes/Insight:", self.insight_te)
        
        if data:
            self.title_le.setText(data.get("title", ""))
            self.status_cb.setCurrentText(data.get("status", "not_started"))
            self.progress_sp.setValue(int(data.get("progress_pct", 0)))
            self.insight_te.setPlainText(data.get("ai_insight", ""))
            
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet("background: #0F172A; color: white; padding: 8px; border-radius: 4px;")
        self.save_btn.clicked.connect(self.accept)
        
        self.del_btn = QPushButton("Delete")
        self.del_btn.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 4px;")
        self.del_btn.clicked.connect(self.reject_delete)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btns.addWidget(self.save_btn)
        btns.addWidget(self.del_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)
        
        self.action = "cancel"

    def reject_delete(self):
        self.action = "delete"
        self.accept()
        
    def get_data(self):
        return {
            "title": self.title_le.text(),
            "status": self.status_cb.currentText(),
            "progress_pct": self.progress_sp.value(),
            "ai_insight": self.insight_te.toPlainText()
        }

class RoadmapCard(QFrame):
    clicked = pyqtSignal(dict)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 1px solid #94A3B8;
                background-color: #F8FAFC;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        
        title = data.get("title", "Milestone")
        status = data.get("status", "not_started")
        progress = data.get("progress_pct", 0)
        insight = data.get("ai_insight", "")
        
        status_clean = status.replace("_", " ").title()
        color = "#10B981" if "completed" in status.lower() else ("#38BDF8" if "progress" in status.lower() else "#94A3B8")
        
        header = QHBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #0F172A; font-size: 18px; font-weight: 700; border: none; background: transparent;")
        title_lbl.setWordWrap(True)
        
        badge = QLabel(status_clean)
        badge.setStyleSheet(f"color: {color}; background: {color}15; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; border: none;")
        
        header.addWidget(title_lbl, stretch=1)
        header.addWidget(badge)
        layout.addLayout(header)
        
        if progress > 0 or "progress" in status.lower():
            p_layout = QVBoxLayout()
            p_layout.setSpacing(4)
            p_lbl = QLabel(f"Progress: {progress}%")
            p_lbl.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 500; border: none; background: transparent;")
            
            bar = QProgressBar()
            bar.setFixedHeight(6)
            bar.setValue(int(progress))
            bar.setTextVisible(False)
            bar.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border: none; border-radius: 3px; }} QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}")
            
            p_layout.addWidget(p_lbl)
            p_layout.addWidget(bar)
            layout.addLayout(p_layout)
            
        if insight:
            insight_lbl = QLabel(insight)
            insight_lbl.setWordWrap(True)
            insight_lbl.setStyleSheet("color: #475569; font-size: 14px; line-height: 1.5; border: none; background: #F8FAFC; padding: 12px; border-radius: 8px;")
            layout.addWidget(insight_lbl)

    def mousePressEvent(self, event):
        self.clicked.emit(self.data)

class LearningRoadmapPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("LearningRoadmapPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_header()
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(24)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll.setWidget(self.content_container)
        self.main_layout.addWidget(self.scroll, stretch=1)
        
        self.refresh()
        
    def _setup_header(self):
        header = QFrame()
        header.setFixedHeight(84)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(32, 0, 32, 0)
        
        info = QVBoxLayout()
        info.setSpacing(4)
        info.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title = QLabel("Academic Roadmap")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        
        sub = QLabel("Your AI-generated long-term study milestones")
        sub.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none;")
        
        info.addWidget(title)
        info.addWidget(sub)
        layout.addLayout(info)
        layout.addStretch()
        
        self.filter_cb = QComboBox()
        self.filter_cb.addItems(["All Milestones", "Not Started", "In Progress", "Completed"])
        self.filter_cb.setStyleSheet("background: white; border: 1px solid #E2E8F0; padding: 6px 12px; border-radius: 6px;")
        self.filter_cb.currentIndexChanged.connect(self.refresh)
        
        self.sort_cb = QComboBox()
        self.sort_cb.addItems(["Default Order", "Sort by Progress (High->Low)"])
        self.sort_cb.setStyleSheet("background: white; border: 1px solid #E2E8F0; padding: 6px 12px; border-radius: 6px;")
        self.sort_cb.currentIndexChanged.connect(self.refresh)
        
        self.add_btn = QPushButton("+ Add Milestone")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet("background: #0F172A; color: white; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        self.add_btn.clicked.connect(self._add_milestone)
        
        layout.addWidget(self.filter_cb)
        layout.addWidget(self.sort_cb)
        layout.addWidget(self.add_btn)
        
        self.main_layout.addWidget(header)
        
    def _add_milestone(self):
        dialog = MilestoneDialog(parent=self)
        if dialog.exec():
            if dialog.action != "delete":
                new_data = dialog.get_data()
                self._update_sqlite(None, new_data, action="add")
                
    def _edit_milestone(self, data):
        dialog = MilestoneDialog(data=data, parent=self)
        if dialog.exec():
            if dialog.action == "delete":
                self._update_sqlite(data, None, action="delete")
            else:
                updated_info = dialog.get_data()
                self._update_sqlite(data, updated_info, action="edit")

    def _update_sqlite(self, old_data, new_data, action="edit"):
        student = crud.get_current_student()
        if not student: return
        
        context = student.get("context", {})
        ai_plan = context.get("ai_plan", {})
        if not isinstance(ai_plan, dict): ai_plan = {}
        
        roadmap = ai_plan.get("academic_roadmap", [])
        if not isinstance(roadmap, list): roadmap = []
        
        if action == "add":
            roadmap.append(new_data)
        elif action == "delete":
            for i, m in enumerate(roadmap):
                if isinstance(m, dict) and m.get("title") == old_data.get("title"):
                    roadmap.pop(i)
                    break
        elif action == "edit":
            for i, m in enumerate(roadmap):
                if isinstance(m, dict) and m.get("title") == old_data.get("title"):
                    roadmap[i]["title"] = new_data["title"]
                    roadmap[i]["status"] = new_data["status"]
                    roadmap[i]["progress_pct"] = new_data["progress_pct"]
                    roadmap[i]["ai_insight"] = new_data["ai_insight"]
                    break
                
        ai_plan["academic_roadmap"] = roadmap
        
        crud.save_student_context(
            student_id=student["id"],
            raw_input_dict=context.get("raw_input", {}),
            ai_plan_dict=ai_plan,
            ai_status=context.get("ai_status", "COMPLETED"),
            ai_last_error=context.get("ai_last_error"),
            is_dirty=1
        )
        self.refresh()
        
    def refresh(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        student = crud.get_current_student()
        if not student:
            self._render_empty_state("No student session found.")
            return
            
        context = student.get("context", {})
        ai_plan = context.get("ai_plan")
        
        if not ai_plan or not isinstance(ai_plan, dict):
            self._render_empty_state("AI plan not generated yet. Please generate insights from the Dashboard.")
            return
            
        roadmap = ai_plan.get("academic_roadmap", [])
        if not roadmap or not isinstance(roadmap, list):
            self._render_empty_state("No roadmap milestones found in your AI plan.")
            return
            
        filter_idx = self.filter_cb.currentIndex()
        sort_idx = self.sort_cb.currentIndex()
        
        filtered_roadmap = []
        for r in roadmap:
            if not isinstance(r, dict): continue
            st = r.get("status", "not_started").lower()
            if filter_idx == 1 and st != "not_started": continue
            if filter_idx == 2 and st != "in_progress": continue
            if filter_idx == 3 and "completed" not in st: continue
            filtered_roadmap.append(r)
            
        if sort_idx == 1:
            filtered_roadmap.sort(key=lambda x: int(x.get("progress_pct", 0)), reverse=True)
            
        if not filtered_roadmap:
            self._render_empty_state("No milestones match your current filters.")
            return
            
        for r in filtered_roadmap:
            card = RoadmapCard(r)
            card.clicked.connect(self._edit_milestone)
            self.content_layout.addWidget(card)
            
    def _render_empty_state(self, message):
        lbl = QLabel(message)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #94A3B8; font-size: 15px; font-style: italic; margin-top: 40px;")
        self.content_layout.addWidget(lbl)
