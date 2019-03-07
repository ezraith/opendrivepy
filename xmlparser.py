from lxml import etree
from road import Road
from roadgeometry import RoadGeometry, RoadLine, RoadSpiral, RoadArc
from junction import Junction, Connection
from matplotlib import pyplot as plt

class XMLParser(object):
    def __init__(self, file):
        self.xml = etree.parse(file)
        self.root = self.xml.getroot()
        self.opendrive = OpenDrive()
        self.header = self.root.find('header')


    # Parses all roads in the xodr and instantiates them into objects
    # Returns a list of Road objects
    def parse_roads(self):
        ret = list()

        for road in self.root.iter('road'):

            # Create the Road object
            new_road = Road(road.get('name'), road.get('length'), road.get('id'), road.get('junction'))

            plan_view = road.find('planView')
            for geometry in plan_view.iter('geometry'):
                record = geometry[0].tag

                s = float(geometry.get('s'))
                x = float(geometry.get('x'))
                y = float(geometry.get('y'))
                hdg = float(geometry.get('hdg'))
                length = float(geometry.get('length'))

                if record == 'line':
                    new_road.add_record(RoadLine(s, x, y, hdg, length))
                elif record == 'arc':
                    curvature = float(geometry[0].get('curvature'))
                    new_road.add_record(RoadArc(s, x, y, hdg, length, curvature))
                elif record == 'spiral':
                    curv_start = float(geometry[0].get('curvStart'))
                    curv_end = float(geometry[0].get('curvEnd'))
                    new_road.add_record(RoadSpiral(s, x, y, hdg, length, curv_start, curv_end))

            ret.append(new_road)

        return ret

    # TODO Add Priorities, JunctionGroups and LaneLinks
    def parse_junctions(self):
        ret = list()

        for junction in self.root.iter('junction'):
            new_junction = Junction(junction.get('name'), junction.get('id'))

            for connection in junction.iter('connection'):
                id = connection.get('id')
                incomingRoad = connection.get('incomingRoad')
                connectingRoad = connection.get('connectingRoad')
                contactPoint = connection.get('contactPoint')
                new_connection = Connection(id, incomingRoad, connectingRoad, contactPoint)

                new_junction.add_connection(new_connection)

            ret.append(new_junction)

        return ret
