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
from database import skill_tree_db

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
            # Dimmed / locked (Light Mode)
            self.setBrush(QBrush(QColor("#F8FAFC")))
            dim_pen = QPen(QColor("#CBD5E1"))
            dim_pen.setWidth(2)
            self.setPen(dim_pen)

        # Text label
        self.label = QGraphicsTextItem(data["name"], self)
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)
        self.label.setFont(font)
        if self.unlocked:
            self.label.setDefaultTextColor(QColor("#FFFFFF"))
        else:
            self.label.setDefaultTextColor(QColor("#64748B"))
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
        # Fetch structured data from SQLite database
        self.branches_data = skill_tree_db.load_skill_branches_structured()

        for branch_name, branch in self.branches_data.items():
            c1 = branch["color_start"]
            c2 = branch["color_end"]
            nodes_data = branch["nodes"]
            edges = branch["edges"]

            # Draw edges first (underneath)
            for i, j in edges:
                if i < len(nodes_data) and j < len(nodes_data):
                    n1 = nodes_data[i]
                    n2 = nodes_data[j]
                    both_unlocked = n1["unlocked"] and n2["unlocked"]

                    line = QGraphicsLineItem(n1["x"], n1["y"], n2["x"], n2["y"])
                    if both_unlocked:
                        pen = QPen(QColor(c1))
                        pen.setWidth(2)
                        pen.setStyle(Qt.PenStyle.SolidLine)
                    else:
                        pen = QPen(QColor("#CBD5E1"))
                        pen.setWidth(2)
                        pen.setStyle(Qt.PenStyle.DashLine)
                    line.setPen(pen)
                    line.setZValue(1)
                    self.scene.addItem(line)

            # Draw nodes
            for nd in nodes_data:
                # Inject branch_name context to node data
                nd["branch_name"] = branch_name
                node = SkillNode(nd, c1, c2, on_click=self.on_node_click)
                self.scene.addItem(node)

            # Branch label (only if nodes exist)
            if nodes_data:
                root = nodes_data[0]
                lbl = QGraphicsTextItem(branch_name)
                lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                lbl.setDefaultTextColor(QColor("#475569"))
                br = lbl.boundingRect()
                lbl.setPos(root["x"] - br.width() / 2, root["y"] + NODE_RADIUS + 12)
                self.scene.addItem(lbl)

        # Dynamic Scene Rect calculation
        rect = self.scene.itemsBoundingRect()
        if not rect.isNull():
            padding = 150
            rect.adjust(-padding, -padding, padding, padding)
            
            # Ensure minimum size to prevent excessive zooming on few nodes
            min_width = 800
            min_height = 600
            if rect.width() < min_width:
                dx = (min_width - rect.width()) / 2
                rect.adjust(-dx, 0, dx, 0)
            if rect.height() < min_height:
                dy = (min_height - rect.height()) / 2
                rect.adjust(0, -dy, 0, dy)
                
            self.scene.setSceneRect(rect)
        else:
            self.scene.setSceneRect(-600, -550, 1200, 650)

    def refresh_scene(self):
        self.scene.clear()
        self._build_tree()
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


# ==========================================
# COMPONENT: Right Detail Panel
# ==========================================
class SkillDetailPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_page = parent
        self.selected_node_data = None
        self.setFixedWidth(300)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 24px;
                border: 1px solid #E2E8F0;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(18, 55, 105, 20))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 30, 28, 30)
        layout.setSpacing(16)
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
        self.title_lbl.setStyleSheet("font-size: 22px; font-weight: 900; color: #0F172A; border: none; background: transparent; letter-spacing: -0.5px;")
        layout.addWidget(self.title_lbl)

        # Status label
        self.status_lbl = QLabel("Click a node to view details")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 13px; color: #64748B; border: none; background: transparent; font-weight: 600;")
        layout.addWidget(self.status_lbl)

        layout.addSpacing(5)

        # Progress section
        prog_title = QLabel("MASTERY")
        prog_title.setStyleSheet("font-size: 11px; font-weight: 800; color: #94A3B8; letter-spacing: 1px; border: none; background: transparent;")
        layout.addWidget(prog_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #F1F5F9;
                border-radius: 5px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38BDF8, stop:1 #0284C7);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.progress_lbl = QLabel("0%")
        self.progress_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progress_lbl.setStyleSheet("font-size: 14px; font-weight: 800; color: #0F172A; border: none; background: transparent;")
        layout.addWidget(self.progress_lbl)

        layout.addSpacing(5)

        # CTA Button
        self.btn_learn = QPushButton("⚡ Start Mission")
        self.btn_learn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_learn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38BDF8, stop:1 #0284C7);
                color: #FFFFFF;
                font-weight: 800;
                border-radius: 16px;
                padding: 14px;
                font-size: 15px;
                border: none;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0284C7, stop:1 #0369A1);
            }
        """)
        self.btn_learn.clicked.connect(self._on_learn_click)
        layout.addWidget(self.btn_learn)

        # Edit Skill Button
        self.btn_edit_skill = QPushButton("✏️ Edit Skill Details")
        self.btn_edit_skill.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_skill.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #0F172A;
                font-weight: bold;
                border-radius: 16px;
                padding: 12px;
                font-size: 14px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover {
                background-color: #F8FAFC;
            }
        """)
        self.btn_edit_skill.clicked.connect(self._on_edit_click)
        self.btn_edit_skill.hide()
        layout.addWidget(self.btn_edit_skill)

        layout.addStretch()

    def update_detail(self, data):
        self.selected_node_data = data
        name = data["name"]
        mastery = data["mastery"]
        unlocked = data["unlocked"]

        self.title_lbl.setText(name)
        self.btn_edit_skill.show()

        if unlocked:
            self.node_icon.setStyleSheet("font-size: 56px; color: #38BDF8; border: none; background: transparent;")
            self.node_icon.setText("◈")
            self.status_lbl.setText(f"{'Mastered' if mastery >= 80 else 'In Progress' if mastery > 0 else 'Not Started'}")
            self.status_lbl.setStyleSheet("font-size: 13px; color: #38BDF8; border: none; background: transparent; font-weight: 700;")
            self.progress_bar.setValue(mastery)
            self.progress_lbl.setText(f"{mastery}%")
            self.btn_learn.setText("⚡ Continue Learning" if mastery > 0 else "⚡ Start Mission")
            self.btn_learn.setEnabled(True)
            self.btn_learn.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #38BDF8, stop:1 #0284C7);
                    color: #FFFFFF; font-weight: 800; border-radius: 16px;
                    padding: 14px; font-size: 15px; border: none;
                }
                QPushButton:hover {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0284C7, stop:1 #0369A1);
                }
            """)
        else:
            self.node_icon.setStyleSheet("font-size: 56px; color: #CBD5E1; border: none; background: transparent;")
            self.node_icon.setText("🔒")
            self.status_lbl.setText("Locked — Complete prerequisites")
            self.status_lbl.setStyleSheet("font-size: 13px; color: #94A3B8; border: none; background: transparent; font-weight: 600;")
            self.progress_bar.setValue(0)
            self.progress_lbl.setText("0%")
            self.btn_learn.setText("🔒 Locked")
            self.btn_learn.setEnabled(False)
            self.btn_learn.setStyleSheet("""
                QPushButton {
                    background-color: #F1F5F9; color: #94A3B8;
                    font-weight: 800; border-radius: 16px; padding: 14px;
                    font-size: 15px; border: none;
                }
            """)

    def _on_edit_click(self):
        if self.parent_page and self.selected_node_data:
            self.parent_page._on_edit_node(self.selected_node_data)

    def _on_learn_click(self):
        if self.parent_page and self.selected_node_data:
            self.parent_page._on_start_mission(self.selected_node_data)


# ==========================================
# MAIN PAGE: AI SKILL TREE
# ==========================================
class SkillTreePage(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller

        self.setStyleSheet("background-color: #F8FAFC;")

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

        title_v = QVBoxLayout()
        title_v.setSpacing(4)
        
        page_title = QLabel("AI Skill Tree")
        page_title.setStyleSheet("font-size: 28px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px; border: none; background: transparent;")

        page_sub = QLabel("Navigate your learning journey")
        page_sub.setStyleSheet("font-size: 14px; color: #64748B; font-weight: 600; border: none; background: transparent;")

        title_v.addWidget(page_title)
        title_v.addWidget(page_sub)
        
        h_layout.addLayout(title_v)
        h_layout.addStretch()

        # Action Buttons in Header
        btn_style = """
            QPushButton {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 700;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F8FAFC;
            }
        """
        
        self.btn_manage_branches = QPushButton("📁 Branches")
        self.btn_manage_branches.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_manage_branches.setStyleSheet(btn_style)
        self.btn_manage_branches.clicked.connect(self._on_manage_branches)
        h_layout.addWidget(self.btn_manage_branches)

        self.btn_add_node = QPushButton("➕ Add Skill")
        self.btn_add_node.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_node.setStyleSheet(btn_style)
        self.btn_add_node.clicked.connect(self._on_add_node)
        h_layout.addWidget(self.btn_add_node)

        self.btn_manage_paths = QPushButton("🔗 Connect Paths")
        self.btn_manage_paths.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_manage_paths.setStyleSheet(btn_style)
        self.btn_manage_paths.clicked.connect(self._on_manage_paths)
        h_layout.addWidget(self.btn_manage_paths)

        canvas_layout.addWidget(header)

        # Canvas
        self.detail_panel = SkillDetailPanel(parent=self)
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

    def _on_edit_node(self, node_data):
        from pages.skill_tree_node_dialog import NodeDialog
        dlg = NodeDialog(node_data=node_data, parent=self)
        if dlg.exec():
            self.refresh()

    def _on_add_node(self):
        from pages.skill_tree_node_dialog import NodeDialog
        branch_name = None
        if self.detail_panel.selected_node_data:
            branch_name = self.detail_panel.selected_node_data.get("branch_name")
        dlg = NodeDialog(current_branch_name=branch_name, parent=self)
        if dlg.exec():
            self.refresh()

    def _on_manage_branches(self):
        from pages.skill_tree_branch_dialog import BranchDialog
        dlg = BranchDialog(parent=self)
        if dlg.exec():
            self.refresh()

    def _on_manage_paths(self):
        from pages.skill_tree_edge_dialog import EdgeDialog
        branch_name = None
        if self.detail_panel.selected_node_data:
            branch_name = self.detail_panel.selected_node_data.get("branch_name")
        dlg = EdgeDialog(current_branch_name=branch_name, parent=self)
        if dlg.exec():
            self.refresh()

    def _on_start_mission(self, node_data):
        from pages.skill_tree_mission_dialog import MissionDialog
        dlg = MissionDialog(node_data=node_data, controller=self.controller, parent=self)
        if dlg.exec():
            if dlg.navigation_target:
                if self.controller and hasattr(self.controller, "show_page"):
                    self.controller.show_page(dlg.navigation_target)
            self.refresh()

    def refresh(self):
        self.canvas.refresh_scene()
        
        # Reset detail panel
        self.detail_panel.selected_node_data = None
        self.detail_panel.title_lbl.setText("Select a Skill")
        self.detail_panel.status_lbl.setText("Click a node to view details")
        self.detail_panel.progress_bar.setValue(0)
        self.detail_panel.progress_lbl.setText("0%")
        self.detail_panel.node_icon.setStyleSheet("font-size: 56px; color: #38BDF8; border: none; background: transparent;")
        self.detail_panel.node_icon.setText("⬡")
        self.detail_panel.btn_learn.setText("⚡ Start Mission")
        self.detail_panel.btn_learn.setEnabled(True)
        self.detail_panel.btn_edit_skill.hide()
