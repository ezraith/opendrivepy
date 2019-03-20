from src.roadmap import RoadMap
import src.xmlparser


class OpenDrive(object):
    def __init__(self, file):
        parser = src.xmlparser.XMLParser(file)
        self.header = None
        self.roads = parser.parse_roads()
        self.controllers = list()
        self.junctions = parser.parse_junctions()
        self.junction_groups = list()
        self.stations = list()

        self.roadmap = RoadMap(self.roads)



