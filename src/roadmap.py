

class RoadMap(object):
    def __init__(self, roads, junctions):
        self.roads = roads
        self.junctions = junctions
        # TODO Collect all endpoints that end in a junction

        self.endpoints = list()
        self.junction_connections = dict()

        self.generate_endpoints()
        self.generate_junction_connections()

    # Pulls the endpoints from each non junction road and adds it to self.endpoints
    def generate_endpoints(self):
        for road in self.roads.values():
            if road.junction == "-1":
                self.endpoints.append(road.start_point)
                self.endpoints.append(road.end_point)

    # Generates a list of every EndPoint that is opposite to an endpoint in a junction
    def generate_junction_connections(self):
        # Create an empty list for each junction id
        for key in self.junctions:
            self.junction_connections[key] = list()

        for road in self.roads.values():
            # For every road that is inside a junction, both the predecessor and successor are EndPoints
            if road.junction != '-1':
                jkey = road.junction

                for road_link in (road.predecessor, road.successor):
                    contact_point = road_link.contact_point
                    id = road_link.element_id
                    endpoint = self.get_endpoint(id, contact_point)

                    self.junction_connections[jkey].append(endpoint)

        # Remove duplicate EndPoints from each junction_connection
        for key in self.junctions:
            self.junction_connections[key] = list(set(self.junction_connections[key]))

    # Returns the endpoint defined by road id and contact_point
    def get_endpoint(self, id, contact_point):
        if contact_point is 'start':
            return self.roads[id].start_point
        else:
            return self.roads[id].end_point

    def get_opposing_endpoint(self, endpoint):
        if endpoint.contact_point is 'start':
            return self.roads[endpoint.id].end_point
        else:
            return self.roads[endpoint.id].start_point

    # Determines the EndPoint with the smallest x-coordinate not in a junction
    def left_most_endpoint(self):
        if self.endpoints is not None:
            leftmost = self.endpoints[0]
            for point in self.endpoints:
                if point.x < leftmost.x:
                    leftmost = point
            return leftmost
        return None

    # Given a base point, returns the closest point to b with the ccw most heading
    def ccw_most_endpoint(self, base, is_first):
        connected_ep = list()

        # Extracts a list of Endpoints that are connected to the base point either directly or through a junction
        base_road = self.roads[base.id]
        print(base_road.id)

        for link in [base_road.successor, base_road.predecessor]:
            print(link.element_type, link.element_id, link.contact_point)
            if link.element_type == "junction":
                connected_ep.extend(self.junction_connections[link.element_id])
                print(link.element_type, [x.id for x in self.junction_connections[link.element_id]])
            else:
                ep = self.get_endpoint(link.element_id, link.contact_point)
                connected_ep.append(ep)

        # Run only during the first loop
        # Adds the opposing point to the list of possible endpoints
        if is_first:
            connected_ep.append(self.get_opposing_endpoint(base))
        else:
            # Might be an issue if the opposing endpoint is also in the junction?
            print([x.id for x in connected_ep])
            connected_ep.remove(self.get_opposing_endpoint(base))

        current = None

        for point in connected_ep:
            if current is None:
                if point != base:
                    current = point
            elif self.ccw_heading(base, current, point) is -1:
                current = point

        return current

    # Determines if the new point n is located counterclockwise to the heading established by base b and current c
    # Returns 1 if the new point is clockwise, collinear but farther or the same as c
    # Returns -1 if the new point is anticlockwise or collinear but closer to c
    def ccw_heading(self, b, c, n):
        ret = (n.y - b.y) * (c.x - n.x) - (n.x - b.x) * (c.y - n.y)
        # print("Ret: ", ret)
        # If the three points are collinear
        if ret == 0:
            bc2 = (b.x - c.x) ** 2 + (b.y - c.y) ** 2
            bn2 = (b.x - n.x) ** 2 + (b.y - n.y) ** 2
            print("bc2: ", bc2, "bn2", bn2)
            # If the new point is equal to the base point, its is not the next point on the hull
            if bn2 == 0:
                return 1
            # If the new point is closer to base than the current point
            elif bn2 < bc2:
                return -1
            else:
                return 1

        # If n is anticlockwise compared to heading formed by b and c
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

        # Adds the leftmost endpoint (smallest x) to the hull as the first point
        base = self.left_most_endpoint()
        hull.append(base)
        is_first = True

        while True:
            if len(hull) > 20:
                break

            next = self.ccw_most_endpoint(base, is_first)
            print("Next: ", next.x, next.y, next.id, next.contact_point)

            # In the case that the second point on the hull is the opposing endpoint, the first loop is run
            # watching for this special condition
            if is_first and base is self.get_opposing_endpoint(base):
                hull.append(next)
                base = next
                if base == hull[0]:
                    break
            else:
                hull.append(next)
                if next == hull[0]:
                    break
                base = self.get_opposing_endpoint(next)
                hull.append(base)
                if base == hull[0]:
                    break

            is_first = False


        print(hull)
        return hull


