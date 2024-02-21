from PySide6.QtWidgets import QAbstractGraphicsShapeItem, QGraphicsItem


from PySide6.QtGui import (QColor,
                           QPainterPath,
                           QFont)

from PySide6.QtCore import (Qt,
                            QPoint,
                            QPointF)

from gui.resize import Resizer


class ResizableItem(QAbstractGraphicsShapeItem):
    resizer = Resizer

    def __init__(self, num: int):
        self.num = num
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setBrush(QColor(0, 0, 255, 255))
        self.resizer_regions = {}
        self.resizer_regions = Resizer.regions(self.boundingRect())
        self.resizer_selected = None
        self.mouse_pos = None
        self.mouse_press_rect = None

    def paint(self, painter, option, widget):
        text = str(self.num)
        # text to center of the dot
        shape_rect = self.rect()
        font = QFont("Arial", 13)
        font.setBold(True)
        painter.setFont(font)
        text_rect = painter.fontMetrics().boundingRect(text)
        # make center of text and center of shape the same (sometimes need 1 pixel left - why?)
        text_rect.moveCenter(shape_rect.center().toPoint() - QPoint(1, 0))
        painter.setBrush(QColor(Qt.black))
        ext_rct = text_rect.adjusted(-3, -3, 3, 3)
        path = QPainterPath()
        path.addRoundedRect(ext_rct, 5, 5)
        painter.fillPath(path, QColor(Qt.cyan))
        painter.setPen(QColor(Qt.blue))
        painter.drawText(text_rect, 0, text)

    def __repr__(self):
        return f"ResizableItem ({self.num}, x:{self.pos().x()}, y:{self.pos().y()})"

    def mouseMoveEvent(self, event):
        # if alt is pressed, resize the dot
        if event.modifiers() == Qt.AltModifier:
            self.setRect(self.rect().x(), self.rect().y(), event.pos().x(), event.pos().y())
            print(f"mouseMoveEvent: {self.pos()}")
        super().mouseMoveEvent(event)

    def boundingRect(self):
        # bounding rect of the shape (including the resize handles).
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
        QAbstractGraphicsShapeItem.hoverMoveEvent(self, move_event)

    def hoverLeaveEvent(self, move_event):
        self.setCursor(Qt.ArrowCursor)
        QAbstractGraphicsShapeItem.hoverLeaveEvent(self, move_event)

    def mousePressEvent(self, mouse_event):
        self.resizer_selected = self.get_resizer(mouse_event.pos())
        if self.resizer_selected:
            self.mouse_pos = mouse_event.pos()
            self.mouse_press_rect = self.boundingRect()
        QAbstractGraphicsShapeItem.mousePressEvent(self, mouse_event)

    def mouseMoveEvent(self, mouse_event):
        if self.resizer_selected is not None:
            self.interactive_resize(mouse_event.pos())
        else:
            QAbstractGraphicsShapeItem.mouseMoveEvent(self, mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        QAbstractGraphicsShapeItem.mouseReleaseEvent(self, mouse_event)
        self.resizer_selected = None
        self.mouse_pos = None
        self.mouse_press_rect = None
        self.update()

    def interactive_resize(self, pos):
        offset = Resizer.size() + Resizer.offset()
        bounding_rect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.resizer_selected == Resizer.handleN:
            from_y = self.mouse_press_rect.top()
            to_y = from_y + pos.y() - self.mouse_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setTop(to_y)
            rect.setTop(bounding_rect.top() + offset)
        elif self.resizer_selected == Resizer.handleS:
            from_y = self.mouse_press_rect.bottom()
            to_y = from_y + pos.y() - self.mouse_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setBottom(to_y)
            rect.setBottom(bounding_rect.bottom() - offset)
        elif self.resizer_selected == Resizer.handleW:
            from_x = self.mouse_press_rect.left()
            to_x = from_x + pos.x() - self.mouse_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setLeft(to_x)
            rect.setLeft(bounding_rect.left() + offset)
        elif self.resizer_selected == Resizer.handleE:
            from_x = self.mouse_press_rect.right()
            to_x = from_x + pos.x() - self.mouse_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setRight(to_x)
            rect.setRight(bounding_rect.right() - offset)
        elif self.resizer_selected == Resizer.handleNW:
            from_x = self.mouse_press_rect.left()
            to_x = from_x + pos.x() - self.mouse_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setLeft(to_x)
            rect.setLeft(bounding_rect.left() + offset)
            from_y = self.mouse_press_rect.top()
            to_y = from_y + pos.y() - self.mouse_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setTop(to_y)
            rect.setTop(bounding_rect.top() + offset)
        elif self.resizer_selected == Resizer.handleNE:
            from_x = self.mouse_press_rect.right()
            to_x = from_x + pos.x() - self.mouse_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setRight(to_x)
            rect.setRight(bounding_rect.right() - offset)
            from_y = self.mouse_press_rect.top()
            to_y = from_y + pos.y() - self.mouse_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setTop(to_y)
            rect.setTop(bounding_rect.top() + offset)
        elif self.resizer_selected == Resizer.handleSW:
            from_x = self.mouse_press_rect.left()
            to_x = from_x + pos.x() - self.mouse_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setLeft(to_x)
            rect.setLeft(bounding_rect.left() + offset)
            from_y = self.mouse_press_rect.bottom()
            to_y = from_y + pos.y() - self.mouse_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setBottom(to_y)
            rect.setBottom(bounding_rect.bottom() - offset)
        elif self.resizer_selected == Resizer.handleSE:
            from_x = self.mouse_press_rect.right()
            to_x = from_x + pos.x() - self.mouse_pos.x()
            diff.setX(to_x - from_x)
            bounding_rect.setRight(to_x)
            rect.setRight(bounding_rect.right() - offset)
            from_y = self.mouse_press_rect.bottom()
            to_y = from_y + pos.y() - self.mouse_pos.y()
            diff.setY(to_y - from_y)
            bounding_rect.setBottom(to_y)
            rect.setBottom(bounding_rect.bottom() - offset)
        else:
            return

        self.setRect(rect)
        self.resizer_regions = Resizer.regions(self.boundingRect())



"""
    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.resizer_regions.values():
                path.addEllipse(shape)
        return path

"""