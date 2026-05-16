from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, 
                             QGraphicsItem, QFrame, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath

from .skill_node import SkillNode

class ConnectionItem(QGraphicsItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.setZValue(-1) # Behind nodes

    def boundingRect(self):
        if not self.start_item or not self.end_item:
            return QRectF()
        p1 = self.start_item.scenePos() + QPointF(self.start_item.widget().width(), self.start_item.widget().height()/2)
        p2 = self.end_item.scenePos() + QPointF(0, self.end_item.widget().height()/2)
        return QRectF(p1, p2).normalized().adjusted(-10, -10, 10, 10)

    def paint(self, painter, option, widget):
        if not self.start_item or not self.end_item:
            return
        
        p1 = self.start_item.scenePos() + QPointF(self.start_item.widget().width(), self.start_item.widget().height()/2)
        p2 = self.end_item.scenePos() + QPointF(0, self.end_item.widget().height()/2)
        
        path = QPainterPath()
        path.moveTo(p1)
        
        # Bezier curve for smooth connection
        ctrl1 = QPointF(p1.x() + 50, p1.y())
        ctrl2 = QPointF(p2.x() - 50, p2.y())
        path.cubicTo(ctrl1, ctrl2, p2)
        
        pen = QPen(QColor("#E2E8F0"), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(pen)
        painter.drawPath(path)

class RoadmapCanvas(QGraphicsView):
    node_selected = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 2000, 2000)
        self.setScene(self.scene)
        
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.setStyleSheet("background-color: #F8FAFC; border: none;")
        self.setup_mock_data()

    def setup_mock_data(self):
        # Center in scene
        start_x, start_y = 100, 400
        
        skills = [
            {"id": "python", "title": "Python Core", "icon": "🐍", "state": "completed", "mastery": 95, "pos": (100, 400)},
            {"id": "ds", "title": "Data Structures", "icon": "🌳", "state": "completed", "mastery": 88, "pos": (350, 300)},
            {"id": "algo", "title": "Algorithms", "icon": "🔢", "state": "in_progress", "mastery": 45, "pos": (350, 500)},
            {"id": "pytorch", "title": "PyTorch Deep Learning", "icon": "🔥", "state": "in_progress", "mastery": 32, "pos": (600, 400)},
            {"id": "cv", "title": "Computer Vision", "icon": "👁️", "state": "ai_priority", "mastery": 10, "pos": (850, 300)},
            {"id": "nlp", "title": "NLP Transformers", "icon": "💬", "state": "locked", "mastery": 0, "pos": (850, 500)},
        ]
        
        self.nodes = {}
        for s in skills:
            node_widget = SkillNode(s)
            node_widget.clicked.connect(self.node_selected.emit)
            proxy = self.scene.addWidget(node_widget)
            proxy.setPos(s["pos"][0], s["pos"][1])
            proxy.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.nodes[s["id"]] = proxy
            
        # Connections
        self.scene.addItem(ConnectionItem(self.nodes["python"], self.nodes["ds"]))
        self.scene.addItem(ConnectionItem(self.nodes["python"], self.nodes["algo"]))
        self.scene.addItem(ConnectionItem(self.nodes["ds"], self.nodes["pytorch"]))
        self.scene.addItem(ConnectionItem(self.nodes["algo"], self.nodes["pytorch"]))
        self.scene.addItem(ConnectionItem(self.nodes["pytorch"], self.nodes["cv"]))
        self.scene.addItem(ConnectionItem(self.nodes["pytorch"], self.nodes["nlp"]))

    def wheelEvent(self, event):
        zoom_in_factor = 1.1
        zoom_out_factor = 1 / zoom_in_factor
        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)
