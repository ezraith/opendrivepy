from src.point import EndPoint


class Road(object):
    def __init__(self, name, length, id, junction):
        self.name = name
        self.length = length
        self.id = id
        self.junction = junction
        self.predecessor = RoadLink
        self.successor = RoadLink
        self.type = list()
        self.plan_view = list()
        self.elevation_profile = None
        self.lateral_profile = None
        self.lanes = None

        # Points that represent the road
        self.points = list()

        self.start_point = EndPoint
        self.end_point = EndPoint

    def generate_points(self):
        for record in self.plan_view:
            self.points.extend(record.points)

    def draw_road(self):
        for record in self.plan_view:
            record.graph()

    # Updates the values of self.startPoint and self.endPoint based on the road array
    def update_endpoints(self):
        if len(self.points) == 0:
            self.generate_points()

        if self.plan_view is not None:
            x = self.points[0].x
            y = self.points[0].y
            self.start_point = EndPoint(x, y, self.id, 'start')

            x = self.points[-1].x
            y = self.points[-1].y
            self.end_point = EndPoint(x, y, self.id, 'end')


class RoadLink(object):
    def __init__(self, element_type, element_id, contact_point):
        self.element_type = element_type
        self.element_id = element_id
        self.contact_point = contact_point
