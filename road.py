

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

        self.road_xarr = list()
        self.road_yarr = list()

    def add_record(self, record):
        self.plan_view.append(record)



    def draw_road(self):
        for record in self.plan_view:
            record.graph()

            xarr, yarr = record.get_xyarr()
            self.road_xarr.extend(xarr)
            self.road_yarr.extend(yarr)


class RoadLink(object):
    def __init__(self, element_type, element_id, contact_point = None):
        self.element_type = element_type
        self.element_id = element_id
        self.contact_point = contact_point
