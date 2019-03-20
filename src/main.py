import matplotlib.pyplot as plt
from src.opendrive import OpenDrive
from src.point import Point

opendrive = OpenDrive('examples/Crossing8Course.xodr')
for road in opendrive.roads.values():
    road.draw_road()
        # plt.xlim(-210, 210)
        # plt.ylim(-90, 90)

q = Point(-10, 0)
segment = opendrive.roadmap.closest_point(q)
point = segment.min_point(q)
distance = segment.min_distance(q)
plt.plot(q.x, q.y, 'g+')
plt.plot(point.x, point.y, 'r+')
plt.gca().set_aspect('equal', adjustable='box')
print(distance)
plt.show()
