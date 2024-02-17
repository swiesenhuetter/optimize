from PySide6.QtWidgets import QApplication
from gui.main_win import MainWindow


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
