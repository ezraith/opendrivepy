# !/usr/bin/env python

from __future__ import division, absolute_import, print_function

import rospy
from srv import OnRoad
import matplotlib.pyplot as plt
from opendrivepy.opendrive import OpenDrive
from opendrivepy.point import Point


def handle_is_on_road(req):
    opendrive = OpenDrive(req.file)
    q = Point(req.x, req.y)

    # Drawing
    for road in opendrive.roads.values():
        road.draw_road()

    plt.plot(q.x, q.y, 'g+')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    return OnRoadResponse(opendrive.roadmap.is_on_road(q))


def is_on_road_server():
    rospy.init_node('is_on_road_server')
    srv = rospy.Service('is_on_road', OnRoad)
    print('is_on_road service initialized')
    rospy.spin()


if __name__ == '__main__':
    is_on_road_server()
