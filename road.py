from point import EndPoint


class Road(object):
    def __init__(self, name, length, id, junction):
        self.name = name
        self.length = length
        self.id = id
        self.junction = junction
        self.predecessor = None
        self.successor = None
        self.type = list()
        self.plan_view = list()
        self.elevation_profile = None
        self.lateral_profile = None
        self.lanes = None

        # x, y coordinates that represent the road
        # Mainly used for graphics
        self.road_xarr = list()
        self.road_yarr = list()

        self.startPoint = None
        self.endPoint = None

    def draw_road(self):
        for record in self.plan_view:
            record.graph()

            xarr = record.xarr
            yarr = record.yarr
            self.road_xarr.extend(xarr)
            self.road_yarr.extend(yarr)

    # Updates the values of self.startPoint and self.endPoint based on the road array
    def update_endpoints(self):
        if self.plan_view is not None:
            x = self.plan_view[0].x
            y = self.plan_view[0].y
            self.startPoint = EndPoint(x, y, self.id, True)

            x = self.plan_view[-1].xarr[-1]
            y = self.plan_view[-1].yarr[-1]
            self.endPoint = EndPoint(x, y, self.id, False)


class RoadLink(object):
    def __init__(self, element_type, element_id, contact_point):
        self.element_type = element_type
        self.element_id = element_id
        self.contact_point = contact_point
