import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

class Plot:
    def __init__(self, x_plot_range, y_plot_range):
        self.app = QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget(title="Debug signal")
        self.plot = self.win.addPlot(title="PPM (Trig.)")
        self.curve = self.plot.plot(pen='y')
        self.plot.setYRange(y_plot_range[0], y_plot_range[1])
        self.plot.setXRange(x_plot_range[0], x_plot_range[1])
        self.ptr = 0

    def update(self, data):
        self.curve.setData(data)

    def show(self):
        self.win.show()

    def hide(self):
        self.win.hide()

    def run(self):
        self.app.exec_()
