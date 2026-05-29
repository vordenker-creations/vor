from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QSizePolicy, QComboBox, QDialog, QLineEdit, QFormLayout, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QCursor
import datetime

from ui_core.components import CollapsiblePanel
from database import crud

class PlannerToolbar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(74)
        self.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(24)

        info_v = QVBoxLayout()
        info_v.setSpacing(2)
        info_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        title_h = QHBoxLayout()
        title_h.setSpacing(12)
        title = QLabel("Study Tasks")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none;")
        
        badge = QLabel("Academic mode")
        badge.setStyleSheet("font-size: 10px; font-weight: 800; color: #10B981; background: #F0FDF4; padding: 2px 8px; border-radius: 6px; border: 1px solid #BBF7D0;")
        
        title_h.addWidget(title); title_h.addWidget(badge); title_h.addStretch()
        
        summary = QLabel("View your manual classes and AI-recommended study sessions")
        summary.setStyleSheet("font-size: 11px; color: #64748B; font-weight: 600; border: none;")
        
        info_v.addLayout(title_h); info_v.addWidget(summary)
        layout.addLayout(info_v)
        layout.addStretch()
        
        # Filters and Sort
        self.filter_cb = QComboBox()
        self.filter_cb.addItems(["All Tasks", "Only Manual Classes", "Only AI Study Tasks"])
        self.filter_cb.setStyleSheet("background: white; border: 1px solid #E2E8F0; padding: 6px 12px; border-radius: 6px;")
        
        self.sort_cb = QComboBox()
        self.sort_cb.addItems(["Sort AI by Time", "Sort AI by Duration"])
        self.sort_cb.setStyleSheet("background: white; border: 1px solid #E2E8F0; padding: 6px 12px; border-radius: 6px;")
        
        # Add Button
        self.add_btn = QPushButton("+ Add Class")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet("background: #0F172A; color: white; border-radius: 6px; padding: 8px 16px; font-weight: bold;")
        
        layout.addWidget(self.filter_cb)
        layout.addWidget(self.sort_cb)
        layout.addWidget(self.add_btn)

class ClassDialog(QDialog):
    def __init__(self, data=None, is_ai=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Timetable Block")
        self.setStyleSheet("background-color: #FFFFFF; border-radius: 8px;")
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        self.title_le = QLineEdit()
        self.title_le.setStyleSheet("border: 1px solid #E2E8F0; padding: 6px; border-radius: 4px;")
        self.day_cb = QComboBox()
        self.day_cb.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_cb.setStyleSheet("border: 1px solid #E2E8F0; padding: 6px; border-radius: 4px;")
        
        self.start_cb = QComboBox()
        self.start_cb.addItems([str(i) for i in range(1, 11)])
        self.end_cb = QComboBox()
        self.end_cb.addItems([str(i) for i in range(1, 11)])
        
        self.room_le = QLineEdit()
        self.type_cb = QComboBox()
        self.type_cb.addItems(["class", "makeup", "self_study", "exam", "other", "study_task"])
        
        form.addRow("Title:", self.title_le)
        form.addRow("Day:", self.day_cb)
        form.addRow("Start Period:", self.start_cb)
        form.addRow("End Period:", self.end_cb)
        form.addRow("Room/Group:", self.room_le)
        form.addRow("Type:", self.type_cb)
        
        if data:
            self.title_le.setText(str(data.get("title", "")))
            self.day_cb.setCurrentText(data.get("day", "Monday"))
            self.start_cb.setCurrentText(str(data.get("period_start", 1)))
            self.end_cb.setCurrentText(str(data.get("period_end", 1)))
            self.room_le.setText(str(data.get("room", "") or data.get("group", "")))
            self.type_cb.setCurrentText(data.get("type", "study_task" if is_ai else "class"))
            
        layout.addLayout(form)
        
        btns = QHBoxLayout()
        
        if is_ai:
            self.assign_btn = QPushButton("Assign to Schedule")
            self.assign_btn.setStyleSheet("background: #10B981; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
            self.assign_btn.clicked.connect(self.accept_assign)
            btns.addWidget(self.assign_btn)
            
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

    def accept_assign(self):
        self.action = "assign"
        super().accept()

    def reject_delete(self):
        self.action = "delete"
        super().accept()
        
    def get_data(self):
        return {
            "title": self.title_le.text(),
            "day": self.day_cb.currentText(),
            "period_start": int(self.start_cb.currentText()),
            "period_end": int(self.end_cb.currentText()),
            "room": self.room_le.text(),
            "type": self.type_cb.currentText()
        }

class ClassBlock(QFrame):
    clicked = pyqtSignal(dict, bool) # bool indicates if it's an AI task
    completed = pyqtSignal(dict, bool)

    def __init__(self, data, is_ai=False, parent=None):
        super().__init__(parent)
        self.data = data
        self.is_ai = is_ai
        
        title = data.get("title", "Block")
        block_type = data.get("type", "class") if not is_ai else "study_task"
        
        if is_ai:
            dur = data.get("duration_min", 60)
            subtitle = f"{dur} mins"
        else:
            group = data.get("group", "")
            room = data.get("room", "")
            subtitle = f"Room: {room}" if room else f"Group: {group}" if group else ""
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        colors = {
            "class": ("#F0F9FF", "#0284C7", "#38BDF8"), # Blue
            "makeup": ("#FEF9C3", "#A16207", "#FBBF24"), # Yellow
            "self_study": ("#FAF5FF", "#7E22CE", "#A855F7"), # Purple
            "exam": ("#FEF2F2", "#B91C1C", "#F87171"), # Red
            "study_task": ("#F0FDF4", "#15803D", "#4ADE80"), # Green
            "other": ("#F8FAFC", "#475569", "#94A3B8") # Gray
        }
        bg, text, border = colors.get(block_type, colors["other"])
        
        is_completed, is_expired = self._check_status(data)
        text_decor = "line-through" if is_completed or is_expired else "none"
        if is_completed or is_expired:
            bg = "#F1F5F9" # Grayed out background
            text = "#94A3B8" # Grayed out text
            border = "#CBD5E1"
        
        self.setStyleSheet(f"background-color: {bg}; border-left: 4px solid {border}; border-radius: 8px;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)
        
        h_header = QHBoxLayout()
        h_header.setContentsMargins(0, 0, 0, 0)
        
        badge = QLabel(block_type.replace("_", " ").title())
        badge.setStyleSheet(f"color: {text}; font-size: 9px; font-weight: 800; text-transform: uppercase; border: 1px solid {border}; border-radius: 6px; padding: 4px 6px; background: rgba(255,255,255,0.7);")
        h_header.addWidget(badge, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        h_header.addStretch()
        
        chk = QCheckBox()
        chk.setStyleSheet(f"QCheckBox::indicator {{ width: 14px; height: 14px; border: 1px solid {border}; border-radius: 3px; background: white; }}")
        chk.setCursor(Qt.CursorShape.PointingHandCursor)
        chk.setChecked(is_completed)
        chk.clicked.connect(self._on_check)
        h_header.addWidget(chk, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            
        layout.addLayout(h_header)
        
        t_lbl = QLabel(title)
        t_lbl.setWordWrap(True)
        t_lbl.setStyleSheet(f"color: {text}; font-size: 11px; font-weight: 700; border: none; background: transparent; margin-top: 2px; text-decoration: {text_decor};")
        layout.addWidget(t_lbl, alignment=Qt.AlignmentFlag.AlignTop)
        
        if subtitle:
            s_lbl = QLabel(subtitle)
            s_lbl.setWordWrap(True)
            s_lbl.setStyleSheet(f"color: {text}; font-size: 10px; border: none; background: transparent; text-decoration: {text_decor};")
            layout.addWidget(s_lbl, alignment=Qt.AlignmentFlag.AlignTop)
            
        layout.addStretch()

    def _check_status(self, data):
        is_completed = data.get("completed", False)
        is_expired = False
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()
        today_idx = now.weekday()
        
        day_str = data.get("day", "Monday")
        block_day_idx = days.index(day_str) if day_str in days else 0
        
        if block_day_idx < today_idx:
            is_expired = True
        elif block_day_idx == today_idx:
            period_end = int(data.get("period_end", 1))
            if period_end <= 5:
                end_mins = 7 * 60 + period_end * 45
            else:
                end_mins = 13 * 60 + (period_end - 5) * 45
            
            current_mins = now.hour * 60 + now.minute
            if current_mins > end_mins:
                is_expired = True
                
        return is_completed, is_expired

    def mousePressEvent(self, event):
        self.clicked.emit(self.data, self.is_ai)

    def _on_check(self, checked=False):
        self.completed.emit(self.data, self.is_ai)



class SmartTaskPlanner(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("SmartTaskPlanner")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.center_workspace = QWidget()
        self.center_layout = QVBoxLayout(self.center_workspace)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)

        self.toolbar = PlannerToolbar()
        self.toolbar.add_btn.clicked.connect(self._add_class)
        self.toolbar.filter_cb.currentIndexChanged.connect(self.refresh)
        self.toolbar.sort_cb.currentIndexChanged.connect(self.refresh)
        self.center_layout.addWidget(self.toolbar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setSpacing(4)
        
        self.scroll.setWidget(self.grid_container)
        self.center_layout.addWidget(self.scroll, 1)

        self.main_layout.addWidget(self.center_workspace, 1)

        self.refresh()

    def _add_class(self):
        dialog = ClassDialog(parent=self)
        if dialog.exec():
            if dialog.action != "delete":
                new_data = dialog.get_data()
                self._update_sqlite(new_data, action="add")

    def _complete_class(self, block_data, is_ai):
        self._update_sqlite(block_data, action="complete", is_ai=is_ai)
        
    def _edit_class(self, block_data, is_ai):
        dialog = ClassDialog(data=block_data, is_ai=is_ai, parent=self)
        if dialog.exec():
            if dialog.action == "delete":
                self._update_sqlite(block_data, action="delete", is_ai=is_ai)
            elif dialog.action == "assign":
                updated_data = dialog.get_data()
                self._update_sqlite(block_data, action="delete", is_ai=True)
                self._update_sqlite(updated_data, action="add", is_ai=False)
            else:
                updated_data = dialog.get_data()
                self._update_sqlite(block_data, action="edit", new_data=updated_data, is_ai=is_ai)

    def _update_sqlite(self, target_data, action="add", new_data=None, is_ai=False):
        student = crud.get_current_student()
        if not student: return
        
        context = student.get("context", {})
        raw_input = context.get("raw_input", {})
        ai_plan = context.get("ai_plan", {})
        
        if not isinstance(raw_input, dict): raw_input = {}
        if not isinstance(raw_input.get("academic_context"), dict):
            raw_input["academic_context"] = {}
        timetable = raw_input["academic_context"].get("timetable_manual", [])
        if not isinstance(timetable, list): timetable = []
        
        if not is_ai:
            if action == "add":
                timetable.append(target_data)
            elif action == "delete":
                if target_data in timetable:
                    timetable.remove(target_data)
            elif action == "complete":
                for t in timetable:
                    if t.get("title") == target_data.get("title") and t.get("day") == target_data.get("day") and t.get("period_start") == target_data.get("period_start"):
                        t["completed"] = not t.get("completed", False)
                        break
            elif action == "edit":
                if target_data in timetable:
                    idx = timetable.index(target_data)
                    timetable[idx] = new_data
            raw_input["academic_context"]["timetable_manual"] = timetable
        else:
            weekly_plan = ai_plan.get("weekly_study_plan", [])
            if action == "delete":
                for dp in weekly_plan:
                    tasks = dp.get("tasks", [])
                    if target_data in tasks:
                        tasks.remove(target_data)
            elif action == "complete":
                for dp in weekly_plan:
                    tasks = dp.get("tasks", [])
                    for t in tasks:
                        if t.get("title") == target_data.get("title"):
                            t["completed"] = not t.get("completed", False)
                            break
            elif action == "edit":
                for dp in weekly_plan:
                    tasks = dp.get("tasks", [])
                    if target_data in tasks:
                        idx = tasks.index(target_data)
                        # Only update title/duration for AI tasks in this simple implementation
                        tasks[idx]["title"] = new_data["title"]
                        tasks[idx]["duration_min"] = (new_data["period_end"] - new_data["period_start"] + 1) * 45
            ai_plan["weekly_study_plan"] = weekly_plan

        crud.save_student_context(
            student_id=student["id"],
            raw_input_dict=raw_input,
            ai_plan_dict=ai_plan,
            ai_status=context.get("ai_status", "COMPLETED"),
            ai_last_error=context.get("ai_last_error"),
            is_dirty=1
        )
        self.refresh()

    def refresh(self):
        # Clear grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Headers
        empty_corner = QLabel("")
        self.grid_layout.addWidget(empty_corner, 0, 0)
        
        for col, day in enumerate(days):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #475569; font-weight: 700; font-size: 12px; padding: 8px; background: #F1F5F9; border-radius: 6px; border: 1px solid #E2E8F0;")
            self.grid_layout.addWidget(lbl, 0, col + 1)
            self.grid_layout.setColumnStretch(col + 1, 1)
            
        for period in range(1, 11):
            p_lbl = QLabel(f"Period {period}")
            p_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            p_lbl.setStyleSheet("color: #64748B; font-weight: 600; font-size: 11px; padding: 4px;")
            self.grid_layout.addWidget(p_lbl, period, 0)
            self.grid_layout.setRowMinimumHeight(period, 70)
            
            for col in range(1, 8):
                cell = QFrame()
                cell.setStyleSheet("background: transparent; border-bottom: 1px dashed #CBD5E1;")
                self.grid_layout.addWidget(cell, period, col)

        student = crud.get_current_student()
        if not student:
            return
            
        context = student.get("context", {})
        raw_input = context.get("raw_input", {})
        if not isinstance(raw_input, dict):
            raw_input = {}
        timetable_manual = raw_input.get("academic_context", {}).get("timetable_manual", []) if isinstance(raw_input.get("academic_context"), dict) else []
        ai_plan = context.get("ai_plan", {})
        if not isinstance(ai_plan, dict):
            ai_plan = {}
        weekly_plan = ai_plan.get("weekly_study_plan", [])
        
        filter_idx = self.toolbar.filter_cb.currentIndex()
        show_manual = filter_idx in [0, 1]
        show_ai = filter_idx in [0, 2]
        
        # Render manual timetable blocks
        if show_manual and isinstance(timetable_manual, list):
            for block in timetable_manual:
                if not isinstance(block, dict): continue
                day = block.get("day")
                if day not in days: continue
                col = days.index(day) + 1
                
                try: p_start = int(block.get("period_start", 1))
                except: p_start = 1
                try: p_end = int(block.get("period_end", 1))
                except: p_end = 1
                
                if p_start > p_end: p_start, p_end = p_end, p_start
                p_start = max(1, min(10, p_start))
                p_end = max(1, min(10, p_end))
                span = p_end - p_start + 1
                
                cb = ClassBlock(block, is_ai=False)
                cb.clicked.connect(self._edit_class)
                cb.completed.connect(self._complete_class)
                self.grid_layout.addWidget(cb, p_start, col, span, 1)
            
        if show_ai:
            row_ai_header = 12
            ai_lbl = QLabel("AI Recommended Study Tasks")
            ai_lbl.setStyleSheet("color: #0F172A; font-weight: 800; font-size: 15px; margin-top: 20px;")
            self.grid_layout.addWidget(ai_lbl, row_ai_header, 0, 1, 8)
            
            row_ai_content = 13
            tasks_by_day = {d: [] for d in days}
            if isinstance(weekly_plan, list):
                for day_plan in weekly_plan:
                    if isinstance(day_plan, dict):
                        day = day_plan.get("day")
                        if day in tasks_by_day:
                            tasks_by_day[day].extend(day_plan.get("tasks", []))
                        
            sort_idx = self.toolbar.sort_cb.currentIndex()
            
            for col, day in enumerate(days):
                tasks = tasks_by_day[day]
                if not tasks: continue
                
                # Sort tasks
                if sort_idx == 1:
                    tasks.sort(key=lambda x: int(x.get("duration_min", 0)) if isinstance(x, dict) else 0, reverse=True)
                
                t_container = QWidget()
                t_layout = QVBoxLayout(t_container)
                t_layout.setContentsMargins(0, 0, 0, 0)
                t_layout.setSpacing(4)
                
                for t in tasks:
                    if not isinstance(t, dict): continue
                    cb = ClassBlock(t, is_ai=True)
                    cb.clicked.connect(self._edit_class)
                    cb.completed.connect(self._complete_class)
                    t_layout.addWidget(cb)
                t_layout.addStretch()
                
                self.grid_layout.addWidget(t_container, row_ai_content, col + 1, Qt.AlignmentFlag.AlignTop)

