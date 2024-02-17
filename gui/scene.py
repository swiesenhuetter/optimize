from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Signal


class Scene(QGraphicsScene):
    keyReleased = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyReleaseEvent(self, event):
        if self.keyReleased:
            self.keyReleased.emit(event.key())
        super().keyReleaseEvent(event)
