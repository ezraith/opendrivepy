

class OpenDrive(object):
    def __init__(self):
        self.header = None
        self.roads = dict()
        self.controllers = list()
        self.junctions = dict()
        self.junction_groups = list()
        self.stations = list()

    # Setter for self.header
    def set_header(self, header):
        self.header = header

    # Setter for self.roads
    def set_roads(self, roads):
        self.roads = roads

    # Setter for self.junctions
    def set_junctions(self, junctions):
        self.junctions = junctions


