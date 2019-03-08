

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class EndPoint(Point):
    def __init__(self, x, y, id, contact_point):
        super(EndPoint, self).__init__(x, y)
        self.id = id
        self.contact_point = contact_point


