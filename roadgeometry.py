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
        r, x, y, array = self.generate_coords()
        print(r, x, y)
        for c in range(len(array)):
            print(array[c])
        xarr = np.array([r * math.cos(x) for x in array])

        yarr = np.array([r * math.sin(y) for y in array])
        print(xarr, yarr)
        plt.plot(x + xarr, y + yarr, 'b-')

    def generate_coords(self):
        radius = math.fabs(1/self.curvature)
        print(radius)
        circumference = radius * math.pi * 2
        angle = (self.length/circumference) * 2 * math.pi
        print(angle)
        # if clockwise, then curvature < 0
        if self.curvature > 0:
            #TODO Test the anticlockwise case for drawArc
            start_angle = self.hdg - (math.pi / 2)
            circlex = self.x + (math.cos(start_angle) * radius)
            circley = self.y + (math.sin(start_angle) * radius)

            array = list(range(61))
            return radius, circlex, circley, [start_angle + (angle * x / 60) for x in array]
        else:
            start_angle = self.hdg + (math.pi / 2)
            circlex = self.x - (math.cos(start_angle) * radius)
            circley = self.y - (math.sin(start_angle) * radius)
            array = list(range(61))
            return radius, circlex, circley, [start_angle - (angle * x / 60) for x in array]


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
    if end < 11:
        array = list(range(11))
        array = [end*x/10 for x in array]
    else:
        array = list(range(math.floor(end)))
        if math.floor(end) != end:
            array.append(end)
    return np.array(array)

