import numpy as np
from scipy.special import fresnel
from matplotlib import pyplot as plt
from math import pi, sin, cos, sqrt, fabs, floor


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
        plt.plot(self.x + (x * cos(self.hdg)), self.y + (x * sin(self.hdg)), 'b-')


class RoadArc(RoadGeometry):
    def __init__(self, s, x, y, hdg, length, curvature):
        super(RoadArc, self).__init__(s, x, y, hdg, length)
        self.curvature = curvature

    def graph(self):
        r, x, y, array = self.generate_coords()
        xarr = np.array([r * cos(x) for x in array])
        yarr = np.array([r * sin(y) for y in array])
        plt.plot(x + xarr, y + yarr, 'b-')

    def generate_coords(self):
        radius = fabs(1/self.curvature)
        circumference = radius * pi * 2
        angle = (self.length/circumference) * 2 * pi
        # if clockwise, then curvature < 0
        if self.curvature > 0:
            # TODO Test the anticlockwise case for drawArc
            start_angle = self.hdg - (pi / 2)
            circlex = self.x + (cos(start_angle) * radius)
            circley = self.y + (sin(start_angle) * radius)

            array = list(range(61))
            return radius, circlex, circley, [start_angle + (angle * x / 60) for x in array]
        else:
            start_angle = self.hdg + (pi / 2)
            circlex = self.x - (cos(start_angle) * radius)
            circley = self.y - (sin(start_angle) * radius)
            array = list(range(61))
            return radius, circlex, circley, [start_angle - (angle * x / 60) for x in array]


class RoadSpiral(RoadGeometry):
    def __init__(self, s, x, y, hdg, length, curvstart, curvend):
        super(RoadSpiral, self).__init__(s, x, y, hdg, length)
        self.curvStart = curvstart
        self.curvEnd = curvend
        self.cDot = (curvend-curvstart)/length
        self.spiralS = curvstart/self.cDot

    def graph(self):
        xarr = []
        yarr = []
        arr = nprange(self.length)
        xarr, yarr = self.evaluate_spiral(10)
        print(xarr)
        print(yarr)
        plt.plot(xarr, yarr, '-b')

    def odr_spiral(self, s):
        a = 1 / sqrt(fabs(self.cDot))
        a *= sqrt(pi)

        y, x = fresnel(s / a)

        x *= a
        y *= a

        if self.cDot < 0:
            y *= -1

        t = s * s * self.cDot * 0.5
        return x, y, t

    def base_spiral(self, n):
        ox, oy, theta = self.odr_spiral(self.spiralS)
        sinRot = sin(theta)
        cosRot = cos(theta)
        xcoords = list()
        ycoords = list()
        for i in range(n):
            tx, ty, ttheta = self.odr_spiral((i * self.length / n) + self.spiralS)

            dx = tx - ox
            dy = ty - oy
            xcoords.append(dx * cosRot + dy * sinRot)
            ycoords.append(dy * cosRot - dx * sinRot)

        return xcoords, ycoords

    def evaluate_spiral(self, n):
        xarr, yarr = self.base_spiral(n)
        sinRot = sin(self.hdg)
        cosRot = cos(self.hdg)
        for i in range(n):
            tmpX = self.x + cosRot * xarr[i] - sinRot * yarr[i]
            tmpY = self.y + cosRot * yarr[i] + sinRot * xarr[i]
            xarr[i] = tmpX
            yarr[i] = tmpY

        return xarr, yarr

    # def evaluate_spiral(self, n):
    #     if self.curvStart == 0:
    #         r_end = fabs(1/self.curvEnd)
    #         a = 1/sqrt(2 * self.length * r_end)
    #         dys, dxs = fresnel(n*a)
    #         dx = dxs/a
    #         dy = dys/a*-1
    #         dxr = dx * cos(self.hdg) - dy * sin(self.hdg)
    #         dyr = dx * sin(self.hdg) + dy * cos(self.hdg)
    #         return self.x + dxr, self.y + dyr
    #
    # def evaluate_spiral2(self,n):
    #     if (fabs(self.curvEnd) > 1.00e-15) and (fabs(self.curvStart)<=1.00e-15):
    #         normal = True
    #         curv = self.curvEnd
    #         a = 1/sqrt(2*(1/fabs(curv)*self.length))
    #         denormalize = 1/a
    #         mRotCos = cos(self.hdg)
    #         mRotSin = sin(self.hdg)
    #     else:
    #         normal = False
    #         curv = self.curvStart
    #         a = 1 / sqrt(2 * (1 / fabs(curv) * self.length))
    #         denormalize = 1/a
    #         L = (self.length*a)/sqrt(pi/2)
    #         endY, endX = fresnel(L)
    #         if curv < 0:
    #             endY*=-endY
    #         endX*=(1/a)/sqrt(pi/2)
    #         endY*=(1/a)/sqrt(pi/2)
    #         differenceAngle = L*L*sqrt(pi/2)*sqrt(pi/2)
    #         if curv < 0:
    #             diffAngle = self.hdg - differenceAngle-pi
    #         else:
    #             diffAngle = self.hdg + differenceAngle-pi
    #         mRotCos = cos(diffAngle)
    #         mRotSin = sin(diffAngle)
    #
    #     if normal:
    #         l = (n - self.s)*a/sqrt(pi/2)
    #     else:
    #         l = (self.s - n)*a/sqrt(pi/2)
    #     tmpY, tmpX = fresnel(l)
    #
    #     if curv < 0:
    #         tmpY *= -tmpY
    #
    #     tmpX *= denormalize * sqrt(pi/2)
    #     tmpY *= denormalize * sqrt(pi/2)
    #
    #     l = (n-self.s)*a
    #     tangentangle = l*l
    #     if curv < 0:
    #         tangentangle = -tangentangle
    #     rHdg = self.hdg+tangentangle
    #
    #     if not normal:
    #         tmpX-=endX
    #         tmpY-=endX
    #         tmpY = -tmpY
    #
    #     rX = self.x + tmpX * mRotCos - tmpY * mRotSin
    #     rY = self.y + tmpY * mRotCos + tmpX * mRotSin
    #
    #     return rX, rY
    #
    # def evaluate_spiral3(self, n):
    #     xarr, yarr = self.base_spiral((self.curvEnd - self.curvStart)/ self.length, n)
    #     sinRot = sin(self.hdg)
    #     cosRot = cos(self.hdg)
    #     for i in range(n):
    #         xarr[i] = self.x + cosRot*xarr[i] + sinRot*yarr[i]
    #         yarr[i] = self.y + cosRot*yarr[i] - sinRot*xarr[i]
    #
    #     return xarr, yarr
    #
    # def odr_spiral(self, s, cdot):
    #     a = sqrt(pi/abs(cdot))
    #     y, x = fresnel(s/a)
    #     return x*a, y*a * (x > 0 - x < 0), s * s * cdot/2
    #
    # def base_spiral(self, cDot, n):
    #     ox, oy, theta = self.odr_spiral(self.curvStart/cDot, cDot)
    #     sinRot = sin(theta)
    #     cosRot = cos(theta)
    #     xcoords = list()
    #     ycoords = list()
    #     for i in range(n):
    #         tx, ty, ttheta = self.odr_spiral((i * self.length/n) + self.curvStart/cDot, cDot)
    #
    #         dx = tx - ox
    #         dy = ty - oy
    #         xcoords.append(dx)
    #         ycoords.append(dy)
    #
    #     return xcoords, ycoords

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
        array = list(range(floor(end)))
        if floor(end) != end:
            array.append(end)
    return np.array(array)
