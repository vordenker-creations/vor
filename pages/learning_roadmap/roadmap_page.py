import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QProgressBar,
                             QDialog, QComboBox, QSlider, QFormLayout, QSpinBox,
                             QLineEdit, QTextEdit, QGraphicsDropShadowEffect, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QColor, QFont, QCursor, QPainter, QPen, QLinearGradient, QBrush, QRadialGradient
from database import crud
from core.config import (COLOR_BG_APP, COLOR_BG_CARD, COLOR_PRIMARY, 
                         COLOR_PRIMARY_LIGHT, COLOR_TEXT_MAIN, COLOR_TEXT_SUB, 
                         COLOR_BORDER, COLOR_SUCCESS, FONT_MAIN)
from ui_core.components import SaaSCard, AnimatedProgressBar, CountUpLabel

class AIInsightCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent); self.setFixedHeight(150)
        self.glow = QGraphicsDropShadowEffect(self); self.glow.setBlurRadius(20); self.glow.setColor(QColor(15, 23, 42, 20)); self.glow.setOffset(0, 8); self.setGraphicsEffect(self.glow)
        l = QHBoxLayout(self); l.setContentsMargins(35, 25, 35, 25); l.setSpacing(25)
        ic = QFrame(); ic.setFixedSize(64, 64); ic.setStyleSheet("background: rgba(255, 255, 255, 0.1); border-radius: 32px;"); il = QLabel("✨"); il.setStyleSheet("font-size: 30px;"); icl = QVBoxLayout(ic); icl.setAlignment(Qt.AlignmentFlag.AlignCenter); icl.addWidget(il); l.addWidget(ic)
        tc = QVBoxLayout(); tc.setSpacing(6); h = QLabel("AI STRATEGIC INSIGHT"); h.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 900; letter-spacing: 1.5px;")
        self.cnt = QLabel("You are in the top 20% of learners. Completing 'Robotics' next will increase job match by 45%."); self.cnt.setWordWrap(True); self.cnt.setStyleSheet("color: white; font-size: 15px; font-weight: 600;")
        tc.addWidget(h); tc.addWidget(self.cnt); l.addLayout(tc, stretch=1)
        self.btn = QPushButton("Auto-Schedule Next Step"); self.btn.setFixedHeight(48); self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet("background: white; color: #0F172A; border-radius: 12px; padding: 0 25px; font-weight: 800; border: none;")
        l.addWidget(self.btn)
    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing); r = self.rect()
        bg = QLinearGradient(0, 0, r.width(), r.height()); bg.setColorAt(0, QColor("#1E293B")); bg.setColorAt(1, QColor("#0F172A"))
        p.setBrush(QBrush(bg)); p.setPen(Qt.PenStyle.NoPen); p.drawRoundedRect(r, 16, 16)
        h1 = QRadialGradient(r.width()*0.1, r.height()*0.1, r.width()*0.5); h1.setColorAt(0, QColor(255,255,255,20)); h1.setColorAt(1, QColor(255,255,255,0))
        p.setBrush(QBrush(h1)); p.drawRoundedRect(r, 16, 16)

class MilestoneDialog(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent); self.setWindowTitle("Edit Milestone"); self.setStyleSheet(f"background-color: {COLOR_BG_CARD}; border-radius: 16px;"); self.setMinimumWidth(480)
        l = QVBoxLayout(self); l.setContentsMargins(30, 30, 30, 30); l.setSpacing(25); h = QLabel("Milestone Configuration"); h.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {COLOR_TEXT_MAIN};"); l.addWidget(h)
        f = QFormLayout(); f.setSpacing(18); style = f"border: 1px solid {COLOR_BORDER}; padding: 12px; border-radius: 10px; background: #F8FAFC;"
        self.tle = QLineEdit(); self.tle.setStyleSheet(style); self.scb = QComboBox(); self.scb.addItems(["not_started", "in_progress", "completed"]); self.scb.setStyleSheet(style)
        self.psp = QSpinBox(); self.psp.setRange(0, 100); self.psp.setFixedHeight(45); self.psp.setStyleSheet(style); self.ite = QTextEdit(); self.ite.setFixedHeight(120); self.ite.setStyleSheet(style)
        f.addRow("Title", self.tle); f.addRow("Status", self.scb); f.addRow("Progress", self.psp); f.addRow("Notes", self.ite); l.addLayout(f)
        bs = QHBoxLayout(); self.sbtn = QPushButton("Save"); self.sbtn.setFixedHeight(48); self.sbtn.setStyleSheet("background: #2563EB; color: white; font-weight: 700; border-radius: 10px;")
        self.dbtn = QPushButton("Delete"); self.dbtn.setFixedHeight(48); self.dbtn.setStyleSheet("background: #FEE2E2; color: #EF4444; border-radius: 10px; font-weight: 700;")
        cbtn = QPushButton("Cancel"); cbtn.setFixedHeight(48); cbtn.setStyleSheet("background: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; border-radius: 10px; font-weight: 700;")
        cbtn.clicked.connect(self.reject); self.sbtn.clicked.connect(self.accept); self.dbtn.clicked.connect(self.reject_delete)
        bs.addWidget(cbtn); bs.addStretch(); bs.addWidget(self.dbtn); bs.addWidget(self.sbtn); l.addLayout(bs)
        if data: self.tle.setText(data.get("title", "")); self.scb.setCurrentText(data.get("status", "not_started")); self.psp.setValue(int(data.get("progress_pct", 0))); self.ite.setPlainText(data.get("ai_insight", ""))
        self.action = "cancel"
    def reject_delete(self): self.action = "delete"; self.accept()
    def get_data(self): return {"title": self.tle.text(), "status": self.scb.currentText(), "progress_pct": self.psp.value(), "ai_insight": self.ite.toPlainText()}

class KPICard(QFrame):
    def __init__(self, title, value, icon_char, parent=None):
        super().__init__(parent); self.setFixedSize(220, 110); self.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
        s = QGraphicsDropShadowEffect(self); s.setBlurRadius(15); s.setColor(QColor(15, 23, 42, 10)); s.setOffset(0, 4); self.setGraphicsEffect(s)
        l = QVBoxLayout(self); l.setContentsMargins(22, 18, 22, 18); l.setSpacing(6); t = QHBoxLayout(); tl = QLabel(title.upper())
        tl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 800; letter-spacing: 0.8px; border: none; background: transparent;"); il = QLabel(icon_char); il.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        t.addWidget(tl); t.addStretch(); t.addWidget(il); l.addLayout(t); self.vlbl = CountUpLabel(parent=self); self.vlbl.setStyleSheet("color: #0F172A; font-size: 26px; font-weight: 900; border: none; background: transparent;")
        try: float(value); self.vlbl.set_target(value)
        except: self.vlbl.setText(str(value)); self.vlbl.timer.stop()
        l.addWidget(self.vlbl)

class TimelineItem(QWidget):
    def __init__(self, is_last=False, is_first=False, is_active=False, is_prev_active=False, parent=None):
        super().__init__(parent); self.setFixedWidth(50); self.is_last = is_last; self.is_first = is_first; self.is_active = is_active; self.is_prev_active = is_prev_active
    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing); cx = self.width() // 2
        # Continuous vertical line ABOVE the dot (from previous node)
        if not self.is_first:
            lc = QColor(COLOR_SUCCESS) if self.is_prev_active else QColor("#CBD5E1")
            p.setPen(QPen(lc, 2)); p.drawLine(cx, 0, cx, 25)
        # Continuous vertical line BELOW the dot (to next node)
        if not self.is_last:
            lc = QColor(COLOR_SUCCESS) if self.is_active else QColor("#CBD5E1")
            p.setPen(QPen(lc, 2)); p.drawLine(cx, 40, cx, self.height())
        # Dot itself
        c = COLOR_SUCCESS if self.is_active else "#CBD5E1"
        p.setBrush(QColor(c)); p.setPen(Qt.PenStyle.NoPen); p.drawEllipse(cx - 7, 25, 14, 14)
        if self.is_active: p.setBrush(Qt.BrushStyle.NoBrush); p.setPen(QPen(QColor(c), 1.5)); p.drawEllipse(cx - 12, 20, 24, 24)

# Sub-task placeholder data keyed by milestone title keywords
_SUBTASK_DATA = {
    "default": [
        (True,  "Complete Calculus 1"),
        (False, "Master Object-Oriented Programming"),
        (False, "Data Structures and Algorithms project"),
    ]
}

class SubTaskChecklist(QWidget):
    """Compact, read-only checklist previewing sub-tasks inside a milestone card."""
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #F8FAFC; border-radius: 10px; border: none;")
        layout = QVBoxLayout(self); layout.setContentsMargins(16, 12, 16, 12); layout.setSpacing(8)
        lbl = QLabel("SUB-TASKS"); lbl.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: 800; letter-spacing: 1px; border: none; background: transparent;"); layout.addWidget(lbl)
        for done, text in items:
            row = QHBoxLayout(); row.setSpacing(10)
            icon = QLabel("✓" if done else "○")
            icon.setFixedWidth(18)
            if done: icon.setStyleSheet("color: #10B981; font-size: 14px; font-weight: 900; border: none; background: transparent;")
            else: icon.setStyleSheet("color: #CBD5E1; font-size: 14px; font-weight: 600; border: none; background: transparent;")
            task_lbl = QLabel(text)
            if done: task_lbl.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600; text-decoration: line-through; border: none; background: transparent;")
            else: task_lbl.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 600; border: none; background: transparent;")
            row.addWidget(icon); row.addWidget(task_lbl); row.addStretch(); layout.addLayout(row)

class RoadmapCard(QWidget):
    clicked = pyqtSignal(dict)
    def __init__(self, data, is_last=False, is_first=False, is_prev_active=False, parent=None):
        super().__init__(parent); self.data = data; l = QHBoxLayout(self); l.setContentsMargins(0,0,0,0); l.setSpacing(0)
        s = data.get("status", "not_started").lower(); active = "progress" in s or "completed" in s
        self.timeline = TimelineItem(is_last=is_last, is_first=is_first, is_active=active, is_prev_active=is_prev_active); l.addWidget(self.timeline)
        self.card = SaaSCard(); self.card.setCursor(Qt.CursorShape.PointingHandCursor); cl = self.card.internal_layout; cl.setSpacing(20)
        tm = QHBoxLayout(); cat = "AI" if "AI" in data.get("title", "") else "DEV"; tag = QLabel(f"🤖 {cat}")
        tag.setStyleSheet(f"color: {COLOR_PRIMARY}; background: rgba(56,189,248,0.08); padding: 5px 12px; border-radius: 12px; font-size: 11px; font-weight: 800; border: 1px solid rgba(56,189,248,0.2);")
        bc = COLOR_SUCCESS if "completed" in s else (COLOR_PRIMARY if "progress" in s else COLOR_TEXT_SUB)
        badge = QLabel(s.replace("_"," ").title()); badge.setStyleSheet(f"color: {bc}; background: rgba({QColor(bc).red()},{QColor(bc).green()},{QColor(bc).blue()},0.06); padding: 5px 12px; border-radius: 12px; font-size: 11px; font-weight: 800; border: 1px solid rgba({QColor(bc).red()},{QColor(bc).green()},{QColor(bc).blue()},0.15);")
        tm.addWidget(tag); tm.addStretch(); tm.addWidget(badge); cl.addLayout(tm)
        tl = QLabel(data.get("title", "Milestone")); tl.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 22px; font-weight: 800;"); tl.setWordWrap(True); cl.addWidget(tl)
        if data.get("ai_insight"):
            il = QLabel(data.get("ai_insight")); il.setWordWrap(True); il.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 14px; line-height: 1.6;"); cl.addWidget(il)
        # Sub-task Checklist Preview
        subtasks = _SUBTASK_DATA.get("default", [])
        if subtasks: cl.addWidget(SubTaskChecklist(subtasks))
        f = QHBoxLayout(); f.setSpacing(25); pc = QVBoxLayout(); pc.setSpacing(10); ph = QHBoxLayout()
        pt = QLabel("PROGRESS"); pt.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;")
        pv = QLabel(f"{data.get('progress_pct', 0)}%"); pv.setStyleSheet(f"color: {COLOR_TEXT_MAIN}; font-size: 11px; font-weight: 900;")
        ph.addWidget(pt); ph.addStretch(); ph.addWidget(pv); pc.addLayout(ph); self.bar = AnimatedProgressBar(color=COLOR_PRIMARY); self.bar.setValue(int(data.get('progress_pct', 0))); pc.addWidget(self.bar); f.addLayout(pc, stretch=2)
        dl = QLabel("📅 Q4 2026"); dl.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 12px; font-weight: 600;"); f.addWidget(dl, stretch=1)
        vb = QPushButton("Details →"); vb.setStyleSheet(f"background: transparent; color: {COLOR_PRIMARY}; font-weight: 800; font-size: 14px; border: none;")
        f.addWidget(vb, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight); cl.addLayout(f); l.addWidget(self.card)
    def mousePressEvent(self, event): self.clicked.emit(self.data)

class LearningRoadmapPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent); self.controller = controller; self.setObjectName("LearningRoadmapPage"); self.setStyleSheet("background-color: #F8FAFC;")
        self.main_layout = QVBoxLayout(self); self.main_layout.setContentsMargins(0, 0, 0, 0); self.main_layout.setSpacing(0); self._setup_header()
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame); self.scroll.setStyleSheet("background: transparent;")
        self.cntr = QWidget(); self.clyt = QVBoxLayout(self.cntr); self.clyt.setContentsMargins(0, 0, 0, 0); self.clyt.setSpacing(0); self.clyt.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ais = QWidget(); al = QVBoxLayout(self.ais); al.setContentsMargins(16, 16, 16, 12); self.aic = AIInsightCard(); al.addWidget(self.aic); self.clyt.addWidget(self.ais)
        self.kpis = QWidget(); self.kpl = QHBoxLayout(self.kpis); self.kpl.setContentsMargins(16, 12, 16, 12); self.kpl.setSpacing(25); self.clyt.addWidget(self.kpis)
        self.cnts = QWidget(); self.cnl = QVBoxLayout(self.cnts); self.cnl.setContentsMargins(16, 16, 16, 16); self.cnl.setSpacing(0); self.cnl.setAlignment(Qt.AlignmentFlag.AlignTop); self.clyt.addWidget(self.cnts)
        self.scroll.setWidget(self.cntr); self.main_layout.addWidget(self.scroll, stretch=1); self.refresh()
    def _setup_header(self):
        h = QFrame(); h.setFixedHeight(84); h.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        l = QHBoxLayout(h); l.setContentsMargins(16, 0, 16, 0); i = QVBoxLayout(); i.setSpacing(4); i.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        t = QLabel("Academic Roadmap"); t.setStyleSheet("font-size: 20px; font-weight: 800; color: #0F172A; border: none; background: transparent;"); s = QLabel("AI-driven strategic journey mapping"); s.setStyleSheet("font-size: 13px; font-weight: 500; color: #64748B; border: none; background: transparent;")
        i.addWidget(t); i.addWidget(s); l.addLayout(i); l.addStretch(); cs = QHBoxLayout(); cs.setSpacing(15)
        style = "background: white; border: 1px solid #E2E8F0; padding: 8px 16px; border-radius: 8px; font-weight: 600; color: #0F172A;"
        self.fcb = QComboBox(); self.fcb.addItems(["All Milestones", "Not Started", "In Progress", "Completed"]); self.fcb.setStyleSheet(style); self.fcb.currentIndexChanged.connect(self.refresh)
        self.scb = QComboBox(); self.scb.addItems(["Default Order", "Sort by Progress"]); self.scb.setStyleSheet(style); self.scb.currentIndexChanged.connect(self.refresh)
        self.aibtn = QPushButton("✨ AI Auto-Plan"); self.aibtn.setFixedHeight(36); self.aibtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.aibtn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B5CF6, stop:1 #3B82F6); color: white; border-radius: 8px; padding: 0 20px; font-weight: 700; border: none;")
        ai_glow = QGraphicsDropShadowEffect(); ai_glow.setBlurRadius(16); ai_glow.setColor(QColor(139, 92, 246, 70)); ai_glow.setOffset(0, 4); self.aibtn.setGraphicsEffect(ai_glow)
        self.aibtn.clicked.connect(self._ai_auto_plan)
        self.abtn = QPushButton("+ Add Milestone"); self.abtn.setFixedHeight(36); self.abtn.setCursor(Qt.CursorShape.PointingHandCursor); self.abtn.setStyleSheet("background: #0F172A; color: white; border-radius: 8px; padding: 0 20px; font-weight: 700; border: none;"); self.abtn.clicked.connect(self._add_milestone)
        cs.addWidget(self.fcb); cs.addWidget(self.scb); cs.addWidget(self.aibtn); cs.addWidget(self.abtn); l.addLayout(cs); self.main_layout.addWidget(h)
    def _ai_auto_plan(self):
        # Placeholder for future AI Auto-Plan API call
        pass
    def _add_milestone(self):
        d = MilestoneDialog(parent=self)
        if d.exec() and d.action != "delete": self._update_sqlite(None, d.get_data(), action="add")
    def _edit_milestone(self, data):
        d = MilestoneDialog(data=data, parent=self)
        if d.exec():
            if d.action == "delete": self._update_sqlite(data, None, action="delete")
            else: self._update_sqlite(data, d.get_data(), action="edit")
    def _update_sqlite(self, old, new, action="edit"):
        s = crud.get_current_student(); ctx = s.get("context", {}); p = ctx.get("ai_plan", {})
        rm = p.get("academic_roadmap", [])
        if action == "add": rm.append(new)
        elif action == "delete": rm = [m for m in rm if m.get("title") != old.get("title")]
        elif action == "edit":
            for m in rm:
                if m.get("title") == old.get("title"): m.update(new); break
        p["academic_roadmap"] = rm; crud.save_student_context(student_id=s["id"], raw_input_dict=ctx.get("raw_input", {}), ai_plan_dict=p, ai_status=ctx.get("ai_status", "COMPLETED"), is_dirty=1); self.refresh()
    def refresh(self):
        for l in [self.cnl, self.kpl]:
            while l.count():
                item = l.takeAt(0)
                if item.widget(): item.widget().deleteLater()
        s = crud.get_current_student(); 
        if not s: return
        p = s.get("context", {}).get("ai_plan")
        if not p: self._render_empty_state("AI plan not generated."); return
        rm = p.get("academic_roadmap", [])
        if not rm: self._render_empty_state("No milestones found."); return
        tot = len(rm); cmp = len([m for m in rm if "completed" in m.get("status", "").lower()]); foc = "None"
        for m in rm:
            if "progress" in m.get("status", "").lower(): foc = m.get("title", "")[:12] + "..."; break
        self.kpl.addWidget(KPICard("Milestones", tot, "📊")); self.kpl.addWidget(KPICard("Completed", cmp, "✅")); self.kpl.addWidget(KPICard("Active Focus", foc, "🎯")); self.kpl.addStretch()
        fi = self.fcb.currentIndex(); si = self.scb.currentIndex(); fl = [m for m in rm if isinstance(m, dict)]
        if fi == 1: fl = [m for m in fl if m.get("status") == "not_started"]
        elif fi == 2: fl = [m for m in fl if "progress" in m.get("status", "").lower()]
        elif fi == 3: fl = [m for m in fl if "completed" in m.get("status", "").lower()]
        if si == 1: fl.sort(key=lambda x: int(x.get("progress_pct", 0)), reverse=True)
        if not fl: self._render_empty_state("No matching milestones."); return
        for i, m in enumerate(fl):
            s_prev = fl[i-1].get("status", "not_started").lower() if i > 0 else ""
            prev_active = "progress" in s_prev or "completed" in s_prev
            c = RoadmapCard(m, is_last=(i == len(fl) - 1), is_first=(i == 0), is_prev_active=prev_active); c.clicked.connect(self._edit_milestone); self.cnl.addWidget(c)
    def _render_empty_state(self, msg):
        l = QLabel(msg); l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setStyleSheet(f"color: {COLOR_TEXT_SUB}; font-size: 16px; padding: 60px;"); self.cnl.addWidget(l)
