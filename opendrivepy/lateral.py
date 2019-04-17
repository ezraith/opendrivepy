from __future__ import division, print_function, absolute_import


class LateralProfile(object):
    def __init__(self):
        self.superelevations = list()
        self.crossfalls = list()
        self.shapes = list()


class SuperElevation(object):
    def __init__(self, s, a, b, c, d):
        self.s = s
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class CrossFall(object):
    def __init__(self, side, s, a, b, c, d):
        self.side = side
        self.s = s
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class Shape(object):
    def __init__(self, s, t, a, b, c, d):
        self.s = s
        self.t = t
        self.a = a
        self.b = b
        self.c = c
        self.d = d

