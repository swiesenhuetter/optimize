from PySide6.QtWidgets import (QApplication,
                               QFileDialog,
                               QGraphicsView,
                               QGraphicsScene,
                               QGraphicsPixmapItem,
                               QGraphicsEllipseItem)

from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import QSettings, Qt

org = "StephanW"
prog = "QGraphicsTest"


class DraggableDot(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, num, parent=None):
        super().__init__(x, y, w, h, parent)
        self.num = num
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.ItemIsFocusable, True)
        self.setBrush(QColor(0, 0, 255, 255))

    def paint(self, painter, option, widget):
        painter.setPen(QColor(0, 255, 255, 255))
        # number inside the dot
        painter.drawText(self.rect(), 0, str(self.num))
        super().paint(painter, option, widget)

    def __repr__(self):
        return f"DraggableDot({self.num}, x:{self.pos().x()}, y:{self.pos().y()})"

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))

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

    def mousePressEvent(self, event):
        # right click to add a dot
        if event.button() == Qt.RightButton:
            pos = event.position()
            dot = DraggableDot(pos.x() - 10, pos.y() - 10, 20, 20, len(self.dots) + 1)
            self.dots.append(dot)
            self.scene().addItem(dot)
        else:
            super().mousePressEvent(event)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        zoomFactor = 1 + (angle/1000)
        self.scale(zoomFactor, zoomFactor)

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
