from __future__ import division, absolute_import, print_function

import matplotlib.pyplot as plt
from opendrivepy.opendrive import OpenDrive
from opendrivepy.point import Point

opendrive = OpenDrive('examples/Crossing8Course.xodr')

opendrive.roads['500'].draw_road()
plt.show()

for road in opendrive.roads.values():
    road.draw_road()
        # plt.xlim(-210, 210)
        # plt.ylim(-90, 90)

q = Point(-10, 0)
segment, right, left = opendrive.roadmap.closest_point(q)
point = segment.min_point(q)
distance = segment.min_distance(q)
plt.plot(q.x, q.y, 'g+')
plt.plot(point.x, point.y, 'r+')
#plt.ylim((15, -15))
#plt.xlim(198, 202)
plt.gca().set_aspect('equal', adjustable='box')
print(distance)
print(right, left)
plt.show()
