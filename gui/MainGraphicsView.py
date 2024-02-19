from PySide6.QtWidgets import (QFileDialog,
                               QGraphicsView,
                               QGraphicsPixmapItem)

from PySide6.QtGui import (QPixmap, QPainter)
from PySide6.QtCore import QSettings, Qt
from gui.scene import Scene
from gui.ellipse_item import EllipseItem

org = "StephanW"
prog = "QGraphicsTest"


class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("QMainWindow Graphics Viewer")

        self.setRenderHint(QPainter.Antialiasing, True)

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
            w = settings.value("width")
            h = settings.value("height")
            num = settings.value("num")
            if None not in (x, y, w, h, num):
                movable_dot = EllipseItem(float(x), float(y), float(w), float(h), num)
                self.dots.append(movable_dot)
                self.scene().addItem(movable_dot)

        settings.endArray()
        settings.endGroup()
        if win_size:
            self.resize(win_size)

        self.setSceneRect(0, 0, self.width(), self.height())
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)

        self.background_item = QGraphicsPixmapItem()
        self.scene().addItem(self.background_item)

        if self.image_file_name:
            self.load_image(self.image_file_name)

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.load_image(file_name)

    def clear_image(self):
        self.background_item.setPixmap(QPixmap())
        self.image_file_name = ""

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        self.background_item.setPixmap(pixmap)
        self.background_item.setZValue(-1)
        self.image_file_name = file_name
        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.setSceneRect(0, 0, self.width(), self.height())

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
            dot = EllipseItem(pos.x() - 10, pos.y() - 10, 40, 40, len(self.dots) + 1)
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
        settings.remove("dots")
        settings.setValue("size", self.size())
        settings.beginWriteArray("dots")
        for i, dot in enumerate(self.dots):
            settings.setArrayIndex(i)
            pos = dot.pos()
            rect = dot.rect()
            settings.setValue("dot_x", rect.x() + pos.x())
            settings.setValue("dot_y", rect.y() + pos.y())
            settings.setValue("width", rect.width())
            settings.setValue("height", rect.height())
            settings.setValue("num", dot.num)
        settings.endArray()
        settings.endGroup()
        super().closeEvent(event)

