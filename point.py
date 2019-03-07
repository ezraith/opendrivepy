

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class EndPoint(Point):
    def __init__(self, x, y, id, is_start):
        super(EndPoint, self).__init__(x, y)
        self.id = id
        self.is_start = is_start


