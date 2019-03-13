

class RoadMap(object):
    def __init__(self, roads):
        self.roads = roads

    # Finds the closest point on the roads to the given point
    def closest_point(self, q):
        min_dist = 100
        min_segment = None

        roads = self.roads
        for road in roads.values():
            # if road.in_range(q) is False:
            #     continue
            for segment in road.segments:
                if segment.min_distance(q) < min_dist:
                    min_segment = segment
                    min_dist = segment.min_distance(q)

        return min_segment.min_point(q), min_dist, min_segment

