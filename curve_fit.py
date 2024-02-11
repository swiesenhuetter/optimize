import os
import numpy as np
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QWidget,
                               QVBoxLayout,
                               QSpinBox)

from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.ax.set_aspect('equal')
        self.setParent(parent)
        self.num_points = 20
        self.spline_points = 500

    def set_spline_points(self, val):
        self.spline_points = val


    def set_resolution(self, val):
        self.num_points = val

    def paintEvent(self, event):
        # ERASE THE CANVAS
        self.ax.clear()

        # recompute the data
        phi = np.linspace(0, 2.0 * np.pi, self.num_points, endpoint=True)
        r = 1.0 + np.cos(phi)  # polar coords
        x, y = r * np.cos(phi), r * np.sin(phi)  # convert to cartesian

        tck, u = splprep([x, y], s=0, k=3)
        new_u = np.linspace(0.0, 1.0, self.spline_points, endpoint=True)
        new_points = splev(new_u, tck)
        knots, control_points, degree = tck
        self.ax.plot(x, y, 'bo-')
        self.ax.plot(control_points[0], control_points[1], 'go')
        self.ax.plot(new_points[0], new_points[1], 'r-')
        self.fig.canvas.draw()
        super().paintEvent(event)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 with Matplotlib")
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.canvas = PlotCanvas(self)
        layout.addWidget(self.canvas)

        spl_pts_spin = QSpinBox()
        spl_pts_spin.setFixedWidth(100)
        spl_pts_spin.setRange(1, 1000)
        spl_pts_spin.setSingleStep(10)
        spl_pts_spin.setValue(500)
        spl_pts_spin.valueChanged.connect(self.canvas.set_spline_points)
        layout.addWidget(spl_pts_spin)

        res_spin = QSpinBox()
        res_spin.setFixedWidth(100)
        res_spin.setRange(4, 100)
        res_spin.setValue(20)
        res_spin.valueChanged.connect(self.canvas.set_resolution)
        layout.addWidget(res_spin)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        settings = QSettings("StephanW", "CurveFitting")
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", self.size()))
        settings.endGroup()

    def paintEvent(self, event):
        super().paintEvent(event)

    def closeEvent(self, event):
        settings = QSettings("StephanW", "CurveFitting")
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.endGroup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    win = MainWin()
    win.show()
    app.exec()
