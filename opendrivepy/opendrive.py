from __future__ import division, print_function, absolute_import


from opendrivepy.roadmap import RoadMap
import opendrivepy.xmlparser


class OpenDrive(object):
    def __init__(self, file):
        parser = opendrivepy.xmlparser.XMLParser(file)
        self.header = None
        self.roads = parser.parse_roads()
        self.controllers = parser.parse_controllers()
        self.junctions = parser.parse_junctions()
        self.junction_groups = parser.parse_junction_group()
        self.stations = list()

        self.roadmap = RoadMap(self.roads)



