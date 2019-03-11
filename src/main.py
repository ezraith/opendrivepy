import matplotlib.pyplot as plt
from src.xmlparser import XMLParser
from src.opendrive import OpenDrive

parser = XMLParser('examples/Crossing8Course.xodr')
roads = parser.parse_roads()
for road in roads.values():
    road.update_endpoints()
    # road.draw_road()
        # plt.xlim(-210, 210)
        # plt.ylim(-90, 90)
# plt.show()
junctions = parser.parse_junctions()

opendrive = OpenDrive()
opendrive.roads = roads
opendrive.junctions = junctions

opendrive.generate_roadmap()
roadmap = opendrive.roadmap

hull = opendrive.roadmap.shrink_convex_hull()
for point in hull:
    print(point.x, point.y, point.id, point.contact_point)
    plt.plot(point.x, point.y, 'r+')

plt.show()
