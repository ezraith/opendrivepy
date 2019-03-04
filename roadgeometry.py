import numpy as np
from matplotlib import pyplot as plt
import math

class RoadGeometry(object):
    def __init__(self, s, x, y, hdg, length):
        self.s = s
        self.x = x
        self.y = y
        self.hdg = hdg
        self.length = length
        self.xCoordinates = list()
        self.yCoordinates = list()


class RoadLine(RoadGeometry):
    def __init__(self, s, x, y, hdg, length):
        super(RoadLine, self).__init__(s, x, y, hdg, length)

    def graph(self):
        x = nprange(self.length)
        plt.plot(self.x + (x * math.cos(self.hdg)), self.y + (x * math.sin(self.hdg)), 'b-')


class RoadArc(RoadGeometry):
    def __init__(self, s, x, y, hdg, length, curvature):
        super(RoadArc, self).__init__(s, x, y, hdg, length)
        self.curvature = curvature

    def graph(self):
        x = np.array(range(0, self.length))

    def c


class RoadSpiral(RoadGeometry):
    def __init__(self, s, x, y, hdg, length, curvStart, curvEnd):
        super(RoadSpiral, self).__init__(s, x, y, hdg, length)
        self.curvStart = curvStart
        self.curvEnd = curvEnd

    def graph(self):
        x = np.array(range(0, self.length))


class RoadParamPoly3(RoadGeometry):
    def __init__(self, s, x, y, hdg, length, aU, bU, cU, dU, aV, bV, cV, dV):
        super(RoadParamPoly3, self).__init__(s, x, y, hdg, length)
        self.aU = aU
        self.bU = bU
        self.cU = cU
        self.dU = dU
        self.aV = aV
        self.bV = bV
        self.cV = cV
        self.dV = dV

    def graph(self):
        x = np.array(range(0, self.length))


def nprange(end):
    if end < 5:
        array = list(range(math.floor(end*10)))
        array = [x/10 for x in array]
        if math.floor(end) != end:
            array.append(end)
    else:
        array = list(range(math.floor(end)))
        if math.floor(end) != end:
            array.append(end)
    for x in range(len(array)):
        print(array[x])
    return np.array(array)

