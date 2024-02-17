"""
https://stackoverflow.com/questions/34429632/resize-a-qgraphicsitem-with-the-mouse
"""

from enum import Enum
from PySide6.QtCore import Qt, QRectF


class Resizer(Enum):
    handleNW = 1
    handleN = 2
    handleNE = 3
    handleW = 4
    handleE = 5
    handleSW = 6
    handleS = 7
    handleSE = 8

    @staticmethod
    def size():
        return 8

    @staticmethod
    def offset():
        return -4

    @staticmethod
    def get_cursor(position):
        if position == Resizer.handleNW:
            return Qt.SizeFDiagCursor
        if position == Resizer.handleN:
            return Qt.SizeVerCursor
        if position == Resizer.handleNE:
            return Qt.SizeBDiagCursor
        if position == Resizer.handleW:
            return Qt.SizeHorCursor
        if position == Resizer.handleE:
            return Qt.SizeHorCursor
        if position == Resizer.handleSW:
            return Qt.SizeBDiagCursor
        if position == Resizer.handleS:
            return Qt.SizeVerCursor
        if position == Resizer.handleSE:
            return Qt.SizeFDiagCursor
        return None

    @staticmethod
    def regions(bounds: QRectF):
        sz = Resizer.size()

        resizer_regions = {
            Resizer.handleNW: QRectF(bounds.left(), bounds.top(), sz, sz),
            Resizer.handleN: QRectF(bounds.center().x() - sz / 2.0, bounds.top(), sz, sz),
            Resizer.handleNE: QRectF(bounds.right() - sz, bounds.top(), sz, sz),
            Resizer.handleW: QRectF(bounds.left(), bounds.center().y() - sz / 2.0, sz, sz),
            Resizer.handleE: QRectF(bounds.right() - sz, bounds.center().y() - sz / 2.0, sz, sz),
            Resizer.handleSW: QRectF(bounds.left(), bounds.bottom() - sz, sz, sz),
            Resizer.handleS: QRectF(bounds.center().x() - sz / 2.0, bounds.bottom() - sz, sz, sz),
            Resizer.handleSE: QRectF(bounds.right() - sz, bounds.bottom() - sz, sz, sz)
        }
        return resizer_regions
