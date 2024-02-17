from PySide6.QtWidgets import (QApplication,
                               QFileDialog,
                               QGraphicsView,
                               QGraphicsPixmapItem,
                               QGraphicsEllipseItem)

from PySide6.QtGui import (QColor,
                           QPainterPath,
                           QFont)

from PySide6.QtCore import QSettings, Qt, QRectF, QPoint
from gui.resize import Resizer



class DraggableDot(QGraphicsEllipseItem):
    resizer = Resizer

    def __init__(self, x, y, w, h, num, parent=None):
        super().__init__(x, y, w, h, parent)
        self.num = num
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)
        self.setBrush(QColor(0, 0, 255, 255))
        self.resizer_regions = {}
        self.resizer_regions = Resizer.regions(self.boundingRect())

    def paint(self, painter, option, widget):
        text = str(self.num)
        # text to center of the dot
        shape_rect = self.rect()
        painter.setFont(QFont("Arial", 10))
        text_rect = painter.fontMetrics().boundingRect(text)
        # make center of text and center of shape the same (sometimes need 1 pixel left - why?)
        text_rect.moveCenter(shape_rect.center().toPoint() - QPoint(1, 0))
        super().paint(painter, option, widget)
        painter.setPen(QColor(Qt.yellow))
        painter.setPen(QColor(Qt.yellow))
        painter.drawRect(text_rect)
        painter.drawText(text_rect, 0, text)

    def __repr__(self):
        return f"DraggableDot({self.num}, x:{self.pos().x()}, y:{self.pos().y()})"

    def mouseMoveEvent(self, event):
        # if alt is pressed, resize the dot
        if event.modifiers() == Qt.AltModifier:
            self.setRect(self.rect().x(), self.rect().y(), event.pos().x(), event.pos().y())
            print(f"mouseMoveEvent: {self.pos()}")
        super().mouseMoveEvent(event)

    def itemChange(self, change, value):
        # if change == QGraphicsEllipseItem.ItemPositionHasChanged:
        #     print(f"ItemPositionHasChanged: {self.pos()}")
        return super().itemChange(change, value)

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = Resizer.size() + Resizer.offset()
        return self.rect().adjusted(-o, -o, o, o)

    def get_resizer(self, point):
        for region, rect in self.resizer_regions.items():
            if rect.contains(point):
                return region
        return None

    def hoverMoveEvent(self, move_event):
        if self.isSelected():
            handle = self.get_resizer(move_event.pos())
            cursor = Qt.ArrowCursor if handle is None else self.resizer.get_cursor(handle)
            self.setCursor(cursor)
        super().hoverMoveEvent(move_event)

    def hoverLeaveEvent(self, move_event):
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(move_event)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.resizer_regions.values():
                path.addEllipse(shape)
        return path

