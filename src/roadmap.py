

class RoadMap(object):
    def __init__(self, roads, junctions):
        self.roads = roads
        self.junctions = junctions

        self.endpoints = list()

    def get_endpoints(self):
        for road in self.roads.values():
            self.endpoints.append(road.start_point)
            self.endpoints.append(road.end_point)

    def left_most_endpoint(self):
        if self.endpoints is not None:
            leftmost = self.endpoints[0]
            for point in self.endpoints:
                if point.x < leftmost.x:
                    leftmost = point
            return leftmost
        return None

    # Given a base point, returns the closest point to b with the ccw most heading
    def ccw_most_endpoint(self, base):
        current = None

        for point in self.endpoints:

            if current is None:
                if self.is_connected(base, point):
                    current = point
            elif self.ccw_heading(base, current, point) is -1:
                print("Base: ", base.x, base.y, base.id, base.contact_point)
                print("Point: ", point.x, point.y, point.id, point.contact_point)
                print("CCW: ", self.ccw_heading(base, current, point))
                print("Current: ", current.x, current.y, current.id, current.contact_point)
                current = point
        print("Current: ", current.x, current.y, current.id, current.contact_point)

        return current

    def is_connected(self, p1, p2):
        # Check if the two endpoints belong to the same road
        if p1.id is not p2.id and p1.contact_point is not p2.contact_point:
            return True

        flag1 = False
        road1 = self.roads[p1.id]
        for link in (road1.predecessor, road1.successor):

            # Checks the junction for possible connections if the road is connected to a junction
            if link.element_type == 'junction':
                flag1 = self.is_junction_connected(p1, p2, link.element_id)
                if flag1:
                    break

            # Checks predecessor and successor for id and contact_point match
            elif link.element_id == p2.id and link.contact_point == p2.contact_point:
                flag1 = True
                break

        if flag1 is False:
            return False

        road2 = self.roads[p2.id]
        for link in (road2.predecessor, road2.successor):
            if link.element_type == 'junction':
                if self.is_junction_connected(p2, p1, link.element_id):
                    return True
            elif link.element_id == p1.id and link.contact_point == p1.contact_point:
                return True

        return False

    def is_junction_connected(self, p1, p2, id):
        connections = self.junctions[id].connections
        for connection in connections:
            if (connection.incoming_road == p1.id
                    and connection.connecting_road == p2.id
                    and connection.contact_point == p1.contact_point):

                return True

        return False

    # Determines if the new point n is located counterclockwise to the heading established by base b and current c
    # Returns 1 if the new point is clockwise, collinear but farther or the same as c
    # Returns -1 if the new point is anticlockwise or collinear but closer to c
    def ccw_heading(self, b, c, n):
        ret = (n.y - b.y) * (c.x - n.x) - (n.x - b.x) * (c.y - n.y)
        print("Ret: ", ret)
        # If the three points are collinear
        if ret == 0:
            bc2 = (b.x - c.x) ** 2 + (b.y - c.y) ** 2
            bn2 = (b.x - n.x) ** 2 + (b.y - n.y) ** 2
            print("bc2: ", bc2, "bn2", bn2)
            # If the new point is equal to the base point, its is not the next point on the hull
            if bn2 == 0:
                return 1
            elif bn2 < bc2:
                return -1
            else:
                return 1

        elif ret < 0:
            return -1
        else:
            return 1

    # Uses the gift wrapping algorithm/Jarvis's March to find the convex hull
    # ,then shrink wraps it to fit existing roads
    def shrink_convex_hull(self):

        # Stores the points that make up the vertices of the shrink hull
        hull = list()

        # If there exists less than 3 endpoints, than the boundary is just the existing endpoints
        if len(self.endpoints) < 3:
            print("Less than 3 endpoint!")
            return self.endpoints

        base = self.left_most_endpoint()
        hull.append(base)

        while True:
            next = self.ccw_most_endpoint(base)
            print("Next: ", next.x, next.y, next.id, next.contact_point)
            hull.append(next)
            base = next

            if base == hull[0]:
                break

        return hull
        


