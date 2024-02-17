from PySide6.QtWidgets import (QApplication,
                               QFileDialog,
                               QGraphicsView,
                               QGraphicsPixmapItem,
                               QGraphicsEllipseItem)

from PySide6.QtGui import QPixmap, QColor, QPainterPath
from PySide6.QtCore import QSettings, Qt, QRectF
from gui.scene import Scene
from gui.resize import Resizer

org = "StephanW"
prog = "QGraphicsTest"


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
        self.set_resizer_regions()

    def set_resizer_regions(self):
        bounds = self.boundingRect()
        sz = Resizer.size()

        self.resizer_regions = {
            Resizer.handleNW: QRectF(bounds.left(), bounds.top(), sz, sz),
            Resizer.handleN: QRectF(bounds.center().x() - sz / 2.0, bounds.top(), sz, sz),
            Resizer.handleNE: QRectF(bounds.right() - sz, bounds.top(), sz, sz),
            Resizer.handleW: QRectF(bounds.left(), bounds.center().y() - sz / 2.0, sz, sz),
            Resizer.handleE: QRectF(bounds.right() - sz, bounds.center().y() - sz / 2.0, sz, sz),
            Resizer.handleSW: QRectF(bounds.left(), bounds.bottom() - sz, sz, sz),
            Resizer.handleS: QRectF(bounds.center().x() - sz / 2.0, bounds.bottom() - sz, sz, sz),
            Resizer.handleSE: QRectF(bounds.right() - sz, bounds.bottom() - sz, sz, sz)
        }

    def paint(self, painter, option, widget):
        painter.setPen(QColor(0, 255, 255, 255))
        # number inside the dot
        painter.drawText(self.rect(), 0, str(self.num))
        super().paint(painter, option, widget)

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


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()

        scene = Scene(self)
        self.setScene(scene)
        scene.keyReleased.connect(self.key_released)

        settings = QSettings(org, prog)
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", self.size()))
        self.image_file_name = settings.value("file_name", "")
        win_size = settings.value("size", self.size())
        num_pts = settings.beginReadArray("dots")
        self.dots = []
        for i in range(num_pts):
            settings.setArrayIndex(i)
            x = settings.value("dot_x")
            y = settings.value("dot_y")
            num = settings.value("num")
            if None not in (x, y, num):
                movable_dot = DraggableDot(float(x), float(y), 20, 20, num)
                self.dots.append(movable_dot)
                self.scene().addItem(movable_dot)

        settings.endArray()
        settings.endGroup()
        if win_size:
            self.resize(win_size)

        self.setSceneRect(0, 0, self.width(), self.height())
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)
        if not self.image_file_name:
            self.image_file_name = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")[0]

        pixmap = QPixmap(self.image_file_name)

        # background image
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.image_item.setZValue(-1)
        # self.scene().addItem(self.image_item)
        self.setWindowTitle("QMainWindow WheelEvent")

    def key_released(self, key):
        if key == Qt.Key_Delete:

            subset_to_remove = [(i, dot) for i, dot in enumerate(self.dots) if dot.isSelected()]

            for i, dot in subset_to_remove:
                if dot.isSelected():
                    self.scene().removeItem(dot)

            for index, _ in sorted(subset_to_remove, reverse=True):
                del self.dots[index]

    def mousePressEvent(self, event):
        # right click to add a dot
        if event.button() == Qt.RightButton:
            pos = event.position()
            dot = DraggableDot(pos.x() - 10, pos.y() - 10, 40, 40, len(self.dots) + 1)
            self.dots.append(dot)
            self.scene().addItem(dot)
        else:
            super().mousePressEvent(event)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        zoom_factor = 1 + (angle/1000)
        self.scale(zoom_factor, zoom_factor)

    def closeEvent(self, event):
        settings = QSettings(org, prog)
        settings.beginGroup("MainWindow")
        # file_name = self.image_file_name
        settings.setValue("file_name", self.image_file_name)
        settings.setValue("size", self.size())
        settings.beginWriteArray("dots")
        for i, dot in enumerate(self.dots):
            settings.setArrayIndex(i)
            pos = dot.pos()
            rect = dot.rect()
            settings.setValue("dot_x", rect.x() + pos.x())
            settings.setValue("dot_y", rect.y() + pos.y())
            settings.setValue("num", dot.num)
        settings.endArray()
        settings.endGroup()
        super().closeEvent(event)
        print("closeEvent")


if __name__ == "__main__":
    app = QApplication([])
    win = ImageViewer()
    win.show()
    app.exec()
