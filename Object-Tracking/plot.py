from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys

class Visualizer(object):
    def __init__(self, n=1, size=(640, 360)):
        self.traces = []
        self.data = dict()
        self.app = QtWidgets.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 15
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, size[0], size[1])
        self.w.setBackgroundColor((50, 50, 50, 128))
        
        self.w.show()

        # create the background grids
        self.xsize = 10
        self.ysize = 10
        self.zsize = 3
        self.xlim = [-self.xsize / 2, self.xsize / 2]
        self.ylim = [-self.ysize / 2, self.ysize / 2]
        self.zlim = [-self.zsize / 2, self.zsize / 2]
        gx = gl.GLGridItem(size=pg.Vector(self.zsize, self.ysize, 0))
        gx.setSpacing(1, 1, 1)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-self.xsize / 2, 0, 0)
        self.w.addItem(gx)
        gy = gl.GLGridItem(size=pg.Vector(self.xsize, self.zsize, 0))
        gy.setSpacing(1, 1, 1)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -self.ysize / 2, 0)
        self.w.addItem(gy)
        gz = gl.GLGridItem(size=pg.Vector(self.xsize, self.ysize, 0))
        gz.setSpacing(1, 1, 1)
        gz.translate(0, 0, -self.zsize / 2)
        self.w.addItem(gz)

        for i in range(n):
            self.traces.append(gl.GLLinePlotItem(pos=np.array([[0, 0, 0]]), color=pg.glColor((0, 1)), width=3, antialias=True))
            self.w.addItem(self.traces[i])

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec()

    def set_plotdata(self, index, points, color, width):
        self.traces[index].setData(pos=points, color=color, width=width)

    def add_point(self, index, point):
        point[0] = (point[0] - (self.xlim[0] + self.xlim[1]) / 2) / (self.xlim[1] - self.xlim[0]) * self.xsize
        point[1] = (point[1] - (self.ylim[0] + self.ylim[1]) / 2) / (self.ylim[1] - self.ylim[0]) * self.ysize
        point[2] = (point[2] - (self.zlim[0] + self.zlim[1]) / 2) / (self.zlim[1] - self.zlim[0]) * self.zsize
        if index not in self.data:
            self.data[index] = np.array([point])
        else:
            self.data[index] = np.concatenate((self.data[index], np.array([point])), axis=0)
        self.set_plotdata(index, self.data[index], self.traces[index].color, self.traces[index].width)

    def set_xlim(self, xlim):
        self.xlim = xlim
    
    def set_ylim(self, ylim):
        self.ylim = ylim

    def set_zlim(self, zlim):
        self.zlim = zlim

    def set_color(self, index, color):
        self.traces[index].setData(color=pg.colorTuple(QtGui.QColor(color[0], color[1], color[2], color[3])))

class VisualizerExample(object):
    def __init__(self):
        self.traces = dict()
        self.app = QtWidgets.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, 1280, 720)
        self.w.show()

        # create the background grids
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.w.addItem(gz)

        self.n = 50
        self.m = 1000
        self.y = np.linspace(-10, 10, self.n)
        self.x = np.linspace(-10, 10, self.m)
        self.phase = 0

        for i in range(self.n):
            yi = np.array([self.y[i]] * self.m)
            d = np.sqrt(self.x ** 2 + yi ** 2)
            z = 10 * np.cos(d + self.phase) / (d + 1)
            pts = np.vstack([self.x, yi, z]).transpose()
            self.traces[i] = gl.GLLinePlotItem(pos=pts, color=pg.glColor(
                (i, self.n * 1.3)), width=(i + 1) / 10, antialias=True)
            self.w.addItem(self.traces[i])

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec()

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    def update(self):
        for i in range(self.n):
            yi = np.array([self.y[i]] * self.m)
            d = np.sqrt(self.x ** 2 + yi ** 2)
            z = 10 * np.cos(d + self.phase) / (d + 1)
            pts = np.vstack([self.x, yi, z]).transpose()
            self.set_plotdata(
                name=i, points=pts,
                color=pg.glColor((i, self.n * 1.3)),
                width=(i + 1) / 10
            )
            self.phase -= .003

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    v = Visualizer()
    v.animation()