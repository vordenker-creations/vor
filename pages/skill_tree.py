import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsTextItem, QGraphicsLineItem, QGraphicsDropShadowEffect,
    QFrame, QProgressBar, QSizePolicy
)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import (
    QColor, QPen, QBrush, QRadialGradient, QLinearGradient,
    QFont, QPainter, QPainterPath
)


# ==========================================
# DATA: Skill Tree Definitions
# ==========================================

SKILL_BRANCHES = {
    "Software Dev": {
        "color_start": "#06B6D4",  # Cyan
        "color_end":   "#3B82F6",  # Blue
        "nodes": [
            {"name": "Python",       "mastery": 90, "unlocked": True,  "x": -320, "y": -60},
            {"name": "C++",          "mastery": 75, "unlocked": True,  "x": -420, "y": -180},
            {"name": "Java",         "mastery": 60, "unlocked": True,  "x": -220, "y": -180},
            {"name": "Web Dev",      "mastery": 40, "unlocked": True,  "x": -320, "y": -300},
            {"name": "System Design","mastery": 0,  "unlocked": False, "x": -420, "y": -420},
            {"name": "DevOps",       "mastery": 0,  "unlocked": False, "x": -220, "y": -420},
        ],
        "edges": [(0,1),(0,2),(1,3),(2,3),(3,4),(3,5)]
    },
    "Artificial Intelligence": {
        "color_start": "#8B5CF6",  # Purple
        "color_end":   "#EC4899",  # Pink
        "nodes": [
            {"name": "Machine Learning","mastery": 80, "unlocked": True,  "x": 0, "y": -60},
            {"name": "Deep Learning",   "mastery": 55, "unlocked": True,  "x": -80, "y": -200},
            {"name": "Computer Vision", "mastery": 45, "unlocked": True,  "x": 80,  "y": -200},
            {"name": "NLP",             "mastery": 0,  "unlocked": False, "x": -80, "y": -340},
            {"name": "Reinforcement L.","mastery": 0,  "unlocked": False, "x": 80,  "y": -340},
            {"name": "AGI Research",    "mastery": 0,  "unlocked": False, "x": 0,   "y": -460},
        ],
        "edges": [(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)]
    },
    "Hardware & IoT": {
        "color_start": "#F59E0B",  # Amber
        "color_end":   "#EF4444",  # Red
        "nodes": [
            {"name": "Arduino",          "mastery": 85, "unlocked": True,  "x": 320, "y": -60},
            {"name": "ESP32",            "mastery": 70, "unlocked": True,  "x": 220, "y": -180},
            {"name": "Robotics",         "mastery": 65, "unlocked": True,  "x": 420, "y": -180},
            {"name": "FPV Drones",       "mastery": 35, "unlocked": True,  "x": 320, "y": -300},
            {"name": "FPGA Design",      "mastery": 0,  "unlocked": False, "x": 220, "y": -420},
            {"name": "Adv. Robotics",    "mastery": 0,  "unlocked": False, "x": 420, "y": -420},
        ],
        "edges": [(0,1),(0,2),(1,3),(2,3),(3,4),(3,5)]
    }
}

NODE_RADIUS = 38


# ==========================================
# COMPONENT: Skill Node (QGraphicsEllipseItem)
# ==========================================
class SkillNode(QGraphicsEllipseItem):
    def __init__(self, data, color_start, color_end, on_click=None):
        r = NODE_RADIUS
        super().__init__(-r, -r, r * 2, r * 2)
        self.data = data
        self.on_click = on_click
        self.unlocked = data["unlocked"]
        self.setPos(data["x"], data["y"])
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setZValue(10)

        if self.unlocked:
            # Glowing gradient fill
            grad = QRadialGradient(0, 0, r)
            c1 = QColor(color_start)
            c2 = QColor(color_end)
            grad.setColorAt(0, c1.lighter(130))
            grad.setColorAt(0.7, c1)
            grad.setColorAt(1, c2)
            self.setBrush(QBrush(grad))

            # Neon glow ring
            glow_pen = QPen(QColor(color_start))
            glow_pen.setWidth(3)
            self.setPen(glow_pen)
        else:
            # Dimmed / locked
            self.setBrush(QBrush(QColor("#1E293B")))
            dim_pen = QPen(QColor("#334155"))
            dim_pen.setWidth(2)
            self.setPen(dim_pen)

        # Text label
        self.label = QGraphicsTextItem(data["name"], self)
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)
        self.label.setFont(font)
        if self.unlocked:
            self.label.setDefaultTextColor(QColor("#FFFFFF"))
        else:
            self.label.setDefaultTextColor(QColor("#475569"))
        br = self.label.boundingRect()
        self.label.setPos(-br.width() / 2, -br.height() / 2)

    def hoverEnterEvent(self, event):
        if self.unlocked:
            self.setScale(1.15)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setScale(1.0)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.data)
        super().mousePressEvent(event)


# ==========================================
# COMPONENT: Skill Tree Canvas
# ==========================================
class SkillTreeCanvas(QGraphicsView):
    def __init__(self, on_node_click=None, parent=None):
        super().__init__(parent)
        self.on_node_click = on_node_click
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setStyleSheet("border: none; background: transparent;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-600, -550, 1200, 650)
        self.setScene(self.scene)

        self._build_tree()

    def _build_tree(self):
        for branch_name, branch in SKILL_BRANCHES.items():
            c1 = branch["color_start"]
            c2 = branch["color_end"]
            nodes_data = branch["nodes"]
            edges = branch["edges"]

            # Draw edges first (underneath)
            for i, j in edges:
                n1 = nodes_data[i]
                n2 = nodes_data[j]
                both_unlocked = n1["unlocked"] and n2["unlocked"]

                line = QGraphicsLineItem(n1["x"], n1["y"], n2["x"], n2["y"])
                if both_unlocked:
                    pen = QPen(QColor(c1))
                    pen.setWidth(2)
                    pen.setStyle(Qt.PenStyle.SolidLine)
                else:
                    pen = QPen(QColor("#1E293B"))
                    pen.setWidth(1)
                    pen.setStyle(Qt.PenStyle.DashLine)
                line.setPen(pen)
                line.setZValue(1)
                self.scene.addItem(line)

            # Draw nodes
            for nd in nodes_data:
                node = SkillNode(nd, c1, c2, on_click=self.on_node_click)
                self.scene.addItem(node)

            # Branch label
            root = nodes_data[0]
            lbl = QGraphicsTextItem(branch_name)
            lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            lbl.setDefaultTextColor(QColor("#64748B"))
            br = lbl.boundingRect()
            lbl.setPos(root["x"] - br.width() / 2, root["y"] + NODE_RADIUS + 12)
            self.scene.addItem(lbl)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


# ==========================================
# COMPONENT: Right Detail Panel
# ==========================================
class SkillDetailPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 200);
                border-radius: 20px;
                border: 1px solid rgba(148, 163, 184, 40);
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 36, 28, 36)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Node icon placeholder
        self.node_icon = QLabel("⬡")
        self.node_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.node_icon.setStyleSheet("font-size: 56px; color: #38BDF8; border: none; background: transparent;")
        layout.addWidget(self.node_icon)

        # Title
        self.title_lbl = QLabel("Select a Skill")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setStyleSheet("font-size: 22px; font-weight: 900; color: #F1F5F9; border: none; background: transparent; letter-spacing: -0.5px;")
        layout.addWidget(self.title_lbl)

        # Status label
        self.status_lbl = QLabel("Click a node to view details")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 13px; color: #94A3B8; border: none; background: transparent; font-weight: 600;")
        layout.addWidget(self.status_lbl)

        layout.addSpacing(10)

        # Progress section
        prog_title = QLabel("MASTERY")
        prog_title.setStyleSheet("font-size: 11px; font-weight: 800; color: #64748B; letter-spacing: 1px; border: none; background: transparent;")
        layout.addWidget(prog_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border-radius: 5px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B5CF6, stop:1 #06B6D4);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.progress_lbl = QLabel("0%")
        self.progress_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progress_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #CBD5E1; border: none; background: transparent;")
        layout.addWidget(self.progress_lbl)

        layout.addSpacing(10)

        # CTA Button
        self.btn_learn = QPushButton("⚡ Start Mission")
        self.btn_learn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_learn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #06B6D4);
                color: #FFFFFF;
                font-weight: 800;
                border-radius: 16px;
                padding: 16px;
                font-size: 15px;
                border: none;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #0891B2);
            }
        """)
        layout.addWidget(self.btn_learn)

        layout.addStretch()

    def update_detail(self, data):
        name = data["name"]
        mastery = data["mastery"]
        unlocked = data["unlocked"]

        self.title_lbl.setText(name)

        if unlocked:
            self.node_icon.setStyleSheet("font-size: 56px; color: #06B6D4; border: none; background: transparent;")
            self.node_icon.setText("◈")
            self.status_lbl.setText(f"{'Mastered' if mastery >= 80 else 'In Progress' if mastery > 0 else 'Not Started'}")
            self.status_lbl.setStyleSheet("font-size: 13px; color: #38BDF8; border: none; background: transparent; font-weight: 700;")
            self.progress_bar.setValue(mastery)
            self.progress_lbl.setText(f"{mastery}%")
            self.btn_learn.setText("⚡ Continue Learning" if mastery > 0 else "⚡ Start Mission")
            self.btn_learn.setEnabled(True)
            self.btn_learn.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #06B6D4);
                    color: #FFFFFF; font-weight: 800; border-radius: 16px;
                    padding: 16px; font-size: 15px; border: none;
                }
                QPushButton:hover {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #0891B2);
                }
            """)
        else:
            self.node_icon.setStyleSheet("font-size: 56px; color: #334155; border: none; background: transparent;")
            self.node_icon.setText("🔒")
            self.status_lbl.setText("Locked — Complete prerequisites")
            self.status_lbl.setStyleSheet("font-size: 13px; color: #475569; border: none; background: transparent; font-weight: 600;")
            self.progress_bar.setValue(0)
            self.progress_lbl.setText("0%")
            self.btn_learn.setText("🔒 Locked")
            self.btn_learn.setEnabled(False)
            self.btn_learn.setStyleSheet("""
                QPushButton {
                    background-color: #1E293B; color: #475569;
                    font-weight: 800; border-radius: 16px; padding: 16px;
                    font-size: 15px; border: 1px solid #334155;
                }
            """)


# ==========================================
# MAIN PAGE: AI SKILL TREE
# ==========================================
class SkillTreePage(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller

        self.setStyleSheet("background-color: #0F172A;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left area: Canvas + Overlay Title
        canvas_wrapper = QWidget()
        canvas_wrapper.setStyleSheet("background: transparent;")
        canvas_layout = QVBoxLayout(canvas_wrapper)
        canvas_layout.setContentsMargins(30, 30, 0, 30)
        canvas_layout.setSpacing(16)

        # Page header
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(10, 0, 10, 0)

        page_title = QLabel("AI Skill Tree")
        page_title.setStyleSheet("font-size: 28px; font-weight: 900; color: #F1F5F9; letter-spacing: -0.5px; border: none; background: transparent;")

        page_sub = QLabel("Navigate your learning journey")
        page_sub.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 600; border: none; background: transparent;")

        h_layout.addWidget(page_title)
        h_layout.addSpacing(16)
        h_layout.addWidget(page_sub)
        h_layout.addStretch()

        canvas_layout.addWidget(header)

        # Canvas
        self.detail_panel = SkillDetailPanel()
        self.canvas = SkillTreeCanvas(on_node_click=self._on_node_selected)
        canvas_layout.addWidget(self.canvas, 1)

        # Right panel
        right_wrapper = QWidget()
        right_wrapper.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right_wrapper)
        right_layout.setContentsMargins(20, 30, 30, 30)
        right_layout.addWidget(self.detail_panel)

        main_layout.addWidget(canvas_wrapper, 75)
        main_layout.addWidget(right_wrapper, 25)

    def _on_node_selected(self, data):
        self.detail_panel.update_detail(data)
