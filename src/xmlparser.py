from lxml import etree
from src.road import Road, RoadLink
from src.roadgeometry import RoadLine, RoadSpiral, RoadArc
from src.junction import Junction, Connection


class XMLParser(object):
    def __init__(self, file):
        self.xml = etree.parse(file)
        self.root = self.xml.getroot()
        #self.opendrive.header = self.root.find('header')

    # Parses all roads in the xodr and instantiates them into objects
    # Returns a list of Road objects
    def parse_roads(self):
        ret = dict()

        for road in self.root.iter('road'):

            # Create the Road object
            name = road.get('name')
            length = road.get('length')
            id = road.get('id')
            junction = road.get('junction')

            # Parses link for predecessor and successors
            # No support for neighbor is implemented
            link = road.find('link')
            predecessor = None
            successor = None
            if link is not None:
                xpredecessor = link.find('predecessor')
                if xpredecessor is not None:
                    element_type = xpredecessor.get('elementType')
                    element_id = xpredecessor.get('elementId')
                    contact_point = xpredecessor.get('contactPoint')
                    predecessor = (RoadLink(element_type, element_id, contact_point))

                xsuccessor = link.find('successor')
                if successor is not None:
                    element_type = xsuccessor.get('elementType')
                    element_id = xsuccessor.get('elementId')
                    contact_point = xsuccessor.get('contactPoint')
                    successor = (RoadLink(element_type, element_id, contact_point))

            # Parses planView for geometry records
            xplan_view = road.find('planView')
            plan_view = list()
            for geometry in xplan_view.iter('geometry'):
                record = geometry[0].tag

                s = float(geometry.get('s'))
                x = float(geometry.get('x'))
                y = float(geometry.get('y'))
                hdg = float(geometry.get('hdg'))
                length = float(geometry.get('length'))

                if record == 'line':
                    plan_view.append(RoadLine(s, x, y, hdg, length))
                elif record == 'arc':
                    curvature = float(geometry[0].get('curvature'))
                    plan_view.append(RoadArc(s, x, y, hdg, length, curvature))
                elif record == 'spiral':
                    curv_start = float(geometry[0].get('curvStart'))
                    curv_end = float(geometry[0].get('curvEnd'))
                    plan_view.append(RoadSpiral(s, x, y, hdg, length, curv_start, curv_end))

            new_road = Road(name, length, id, junction, predecessor, successor, plan_view)
            ret[new_road.id] = new_road

        return ret

    # TODO Add Priorities, JunctionGroups and LaneLinks
    def parse_junctions(self):
        ret = dict()

        for junction in self.root.iter('junction'):
            new_junction = Junction(junction.get('name'), junction.get('id'))

            for connection in junction.iter('connection'):
                id = connection.get('id')
                incoming_road = connection.get('incomingRoad')
                connecting_road = connection.get('connectingRoad')
                contact_point = connection.get('contactPoint')
                new_connection = Connection(id, incoming_road, connecting_road, contact_point)

                new_junction.connections.append(new_connection)

            ret[new_junction.id] = new_junction

        return ret
