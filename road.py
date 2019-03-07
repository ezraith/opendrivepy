

class Road(object):
    def __init__(self, name, length, id, junction):
        self.name = name
        self.length = length
        self.id = id
        self.junction = junction
        self.link = None
        self.type = list()
        self.plan_view = list()
        self.elevation_profile = None
        self.lateral_profile = None
        self.lanes = None

        self.road_xarr = list()
        self.road_yarr = list()

    def add_plan(self, record):
        self.plan_view.append(record)

    def draw_road(self):
        for record in self.plan_view:
            record.graph()

            xarr, yarr = record.get_xyarr()
            self.road_xarr.extend(xarr)
            self.road_yarr.extend(yarr)


