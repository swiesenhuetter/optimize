from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QPainterPath
from gui.resizable_item import ResizableItem
from gui.resize import Resizer


class EllipseItem(QGraphicsEllipseItem):
    resizer = Resizer

    def __init__(self, x, y, w, h, num, parent=None):
        QGraphicsEllipseItem.__init__(self, x, y, w, h, parent)
        ResizableItem.__init__(self, num)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        ResizableItem.paint(self, painter, option, widget)

    def __repr__(self):
        return f"Resizable Ellipse({self.num}, x:{self.pos().x()}, y:{self.pos().y()})"

    def boundingRect(self):
        return ResizableItem.boundingRect(self)

    def get_resizer(self, point):
        return ResizableItem.get_resizer(self, point)

    def hoverMoveEvent(self, move_event):
        ResizableItem.hoverMoveEvent(self, move_event)

    def hoverLeaveEvent(self, move_event):
        ResizableItem.hoverLeaveEvent(self, move_event)

    def mousePressEvent(self, mouse_event):
        ResizableItem.mousePressEvent(self, mouse_event)

    def mouseMoveEvent(self, mouse_event):
        ResizableItem.mouseMoveEvent(self, mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        ResizableItem.mouseReleaseEvent(self, mouse_event)

    def interactive_resize(self, pos):
        ResizableItem.interactive_resize(self, pos)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.resizer_regions.values():
                path.addEllipse(shape)
        return path

