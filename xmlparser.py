from lxml import etree
from road import Road
from roadgeometry import RoadGeometry, RoadLine, RoadSpiral, RoadArc
from matplotlib import pyplot as plt

class XMLParser(object):
    def __init__(self, file):
        self.xml = etree.parse(file)
        self.opendrive = xml.getroot()
        self.header = opendrive.find('header')


    def parse_roads(self):
        ret = list()

        for road in opendrive.iter('road'):

            new_road = Road(road.get('name'), road.get('length'), road.get('id'), road.get('junction'))

            plan_view = road.find('planView')

            for geometry in road.iter('geometry'):
                record = geometry[0].tag

                s = float(geometry.get('s'))
                x = float(geometry.get('x'))
                y = float(geometry.get('y'))
                hdg = float(geometry.get('hdg'))
                length = float(geometry.get('length'))

                if record == 'line':
                    new_road.add_plan(RoadLine(s, x, y, hdg, length))
                elif record == 'arc':
                    curvature = float(geometry[0].get('curvature'))
                    new_road.add_plan(RoadArc(s, x, y, hdg, length, curvature))
                elif record == 'spiral':
                    curv_start = float(geometry[0].get('curvStart'))
                    curv_end = float(geometry[0].get('curvEnd'))
                    new_road.add_plan(RoadSpiral(s, x, y, hdg, length, curv_start, curv_end))

            ret.append(new_road)

        return ret

# Crossing8Course.xodr
xml = etree.parse("Crossing8Course.xodr")
print(etree.tostring(xml))

opendrive = xml.getroot()
print(opendrive.tag)
header = opendrive.find('header')
print(header.tag)

parser = XMLParser('test.xodr')
roads = parser.parse_roads()
for road in roads:
    road.draw_road()
plt.show()


