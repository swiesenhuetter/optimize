from PySide6.QtWidgets import QMainWindow
from gui.MainGraphicsView import ImageViewer
from PySide6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow WheelEvent")
        self.setCentralWidget(ImageViewer(parent=self))

        # window menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        load_bg = QAction("Load Background Image", self)
        no_bg = QAction("No Background Image", self)
        file_menu.addAction(load_bg)
        file_menu.addAction(no_bg)

        load_bg.triggered.connect(self.centralWidget().select_image)
        no_bg.triggered.connect(self.centralWidget().clear_image)

        menu_bar.addMenu(file_menu)

    def closeEvent(self, event):
        graphics_view = self.centralWidget()
        graphics_view.closeEvent(event)
        print("closeEvent")
        super().closeEvent(event)
