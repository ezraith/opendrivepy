from src.roadmap import RoadMap

class OpenDrive(object):
    def __init__(self):
        self.header = None
        self.roads = dict()
        self.controllers = list()
        self.junctions = dict()
        self.junction_groups = list()
        self.stations = list()

        self.roadmap = None

    def generate_roadmap(self):
        self.roadmap = RoadMap(self.roads, self.junctions)


