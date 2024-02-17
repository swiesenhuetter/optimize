from PySide6.QtWidgets import QMainWindow
from gui.MainGraphicsView import ImageViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow WheelEvent")
        self.setCentralWidget(ImageViewer(parent=self))
        # self.setGeometry(300, 300, 800, 600)

    def closeEvent(self, event):
        graphics_view = self.centralWidget()
        graphics_view.closeEvent(event)
        print("closeEvent")
        super().closeEvent(event)
