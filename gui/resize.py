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
