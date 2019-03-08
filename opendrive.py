

class OpenDrive(object):
    def __init__(self):
        self.header = None
        self.roads = dict()
        self.controllers = list()
        self.junctions = dict()
        self.junction_groups = list()
        self.stations = list()

    def left_most_endpoint(self):
        if self.roads is not None:
            leftmost = self.roads[0].start_point
            for road in self.roads.values():
                if road.start_point.x < leftmost.x:
                    leftmost = road.start_point
                if road.end_point.x < leftmost.x:
                    leftmost = road.end_point

            return leftmost

        return None

    def is_connected(self, p1, p2):
        # Check if the two endpoints belong to the same road
        if p1.id == p2.id:
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




