from __future__ import division, print_function, absolute_import


class Header(object):
    def __init__(self, rev_major, rev_minor, name, version, date, north, south, east, west, vendor, geo_reference):

        # Attributes
        self.rev_major = int(rev_major)
        self.rev_minor = int(rev_minor)
        self.name = name
        self.version = float(version)
        self.date = date
        self.north = float(north)
        self.south = float(south)
        self.east = float(east)
        self.west = float(west)
        self.vendor = vendor

        # Elements
        self.geo_reference = geo_reference


class GeoReference(object):
    def __init__(self, proj4):
        self.proj4 = proj4

    def convert_coordinates(self):
        pass

