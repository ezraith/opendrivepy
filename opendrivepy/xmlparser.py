from __future__ import division, print_function, absolute_import


from lxml import etree
from opendrivepy.header import Header, GeoReference
from opendrivepy.road import Road, RoadLink, RoadType, RoadSpeed
from opendrivepy.roadgeometry import RoadLine, RoadSpiral, RoadArc
from opendrivepy.elevation import Elevation, ElevationProfile
from opendrivepy.lateral import LateralProfile, SuperElevation, CrossFall, Shape
from opendrivepy.junction import Junction, Connection
from opendrivepy.signal import Signal, SignalDependency, LaneValidity
from opendrivepy.lane import Lanes, Lane, LaneLink, LaneSection, LaneWidth
from opendrivepy.controller import Controller, Control
from opendrivepy.junctiongroup import JunctionGroup, JunctionReference


class XMLParser(object):
    def __init__(self, file):
        self.xml = etree.parse(file)
        self.root = self.xml.getroot()

    def parse_header(self):
        xheader = self.root.find('header')
        rev_major = xheader.get('revMajor')
        rev_minor = xheader.get('revMinor')
        name = xheader.get('name')
        version = xheader.get('version')
        date = xheader.get('date')
        north = xheader.get('north')
        south = xheader.get('south')
        east = xheader.get('east')
        west = xheader.get('west')
        vendor = xheader.get('vendor')

        # TODO Figure out how to read CTYPE data
        geo_reference = GeoReference("")

        return Header(rev_major, rev_minor, name, version, date, north, south, east, west, vendor, geo_reference)

    # Parses all roads in the xodr and instantiates them into objects
    # Returns a list of Road objects
    def parse_roads(self):
        ret = dict()

        for road in self.root.iter('road'):

            # Create the Road object
            name = road.get('name')
            length = road.get('length')
            id = road.get('id')
            junction = road.get('junction')

            # Parses link for predecessor and successors
            # No support for neighbor is implemented
            link = road.find('link')
            predecessor = None
            successor = None
            if link is not None:
                xpredecessor = link.find('predecessor')
                if xpredecessor is not None:
                    element_type = xpredecessor.get('elementType')
                    element_id = xpredecessor.get('elementId')
                    contact_point = xpredecessor.get('contactPoint')
                    predecessor = (RoadLink(element_type, element_id, contact_point))

                xsuccessor = link.find('successor')
                if xsuccessor is not None:
                    element_type = xsuccessor.get('elementType')
                    element_id = xsuccessor.get('elementId')
                    contact_point = xsuccessor.get('contactPoint')
                    successor = (RoadLink(element_type, element_id, contact_point))

            # Parses planView for geometry records
            xplan_view = road.find('planView')
            plan_view = list()
            for geometry in xplan_view.iter('geometry'):
                record = geometry[0].tag

                s = float(geometry.get('s'))
                x = float(geometry.get('x'))
                y = float(geometry.get('y'))
                hdg = float(geometry.get('hdg'))
                length = float(geometry.get('length'))

                if record == 'line':
                    plan_view.append(RoadLine(s, x, y, hdg, length))
                elif record == 'arc':
                    curvature = float(geometry[0].get('curvature'))
                    plan_view.append(RoadArc(s, x, y, hdg, length, curvature))
                elif record == 'spiral':
                    curv_start = float(geometry[0].get('curvStart'))
                    curv_end = float(geometry[0].get('curvEnd'))
                    plan_view.append(RoadSpiral(s, x, y, hdg, length, curv_start, curv_end))

            # Parses ElevationProfile
            xelevation_profile = road.find('elevationProfile')
            elevation_profile = None
            if xelevation_profile is not None:
                elevation_profile = ElevationProfile()
                for xelevation in xelevation_profile.iter('elevation'):
                    s = xelevation.get('s')
                    a = xelevation.get('a')
                    b = xelevation.get('b')
                    c = xelevation.get('c')
                    d = xelevation.get('d')
                    new_elevation = Elevation(s, a, b, c, d)
                    elevation_profile.elevations.append(new_elevation)

            # Parses LateralProfile
            xlateral_profile = road.find('lateralProfile')
            lateral_profile = None
            if xlateral_profile is not None:
                lateral_profile = LateralProfile()

                for xsuperelevation in xlateral_profile.iter('superelevation'):
                    s = xsuperelevation.get('s')
                    a = xsuperelevation.get('a')
                    b = xsuperelevation.get('b')
                    c = xsuperelevation.get('c')
                    d = xsuperelevation.get('d')
                    new_superelevation = SuperElevation(s, a, b, c, d)
                    lateral_profile.superelevations.append(new_superelevation)
                    
                for xcrossfall in xlateral_profile.iter('crossfall'):
                    side = xcrossfall.get('side')
                    s = xcrossfall.get('s')
                    a = xcrossfall.get('a')
                    b = xcrossfall.get('b')
                    c = xcrossfall.get('c')
                    d = xcrossfall.get('d')
                    new_crossfall = CrossFall(side, s, a, b, c, d)
                    lateral_profile.crossfalls.append(new_crossfall)

                for xshape in xlateral_profile.iter('shape'):
                    s = xshape.get('s')
                    t = xshape.get('t')
                    a = xshape.get('a')
                    b = xshape.get('b')
                    c = xshape.get('c')
                    d = xshape.get('d')
                    new_shape = CrossFall(s, t, a, b, c, d)
                    lateral_profile.shapes.append(new_shape)

            # Parses RoadType and Road Speed
            types = list()
            for xtype in road.iter('type'):
                s = xtype.get('s')
                type = xtype.get('type')

                speeds = list()

                for xspeed in xtype.iter('speed'):
                    max = xspeed.get('max')
                    unit = xspeed.get('unit')

                    new_speed = RoadSpeed(max, unit)
                    speeds.append(new_speed)

                new_type = RoadType(s, type, speeds)
                types.append(new_type)

            # Parses signals for signal
            xsignals = road.find('signals')
            signals = self.parse_signal(xsignals)

            # Parse lanes for lane
            xlanes = road.find('lanes')

            # TODO Adapt LaneSection for multiple lane records
            # Lane Sections
            xlane_section = xlanes.find('laneSection')

            # Center Lane
            center = list()
            xcenter = xlane_section.find('center')
            if xcenter is not None:
                xlane = xcenter.find('lane')
                center.append(self.parse_lane(xlane))

            # Left Lanes
            left = list()
            xleft = xlane_section.find('left')
            if xleft is not None:
                for xlane in xleft.iter('lane'):
                    left.append(self.parse_lane(xlane))

            # Right Lanes
            right = list()
            xright = xlane_section.find('right')
            if xright is not None:
                for xlane in xright.iter('lane'):
                    right.append(self.parse_lane(xlane))

            lane_section = LaneSection(left, center, right)

            lanes = Lanes(lane_section)

            new_road = Road(name, length, id, junction, predecessor, successor, types, plan_view, elevation_profile, lateral_profile, lanes, signals)
            ret[new_road.id] = new_road

        return ret

    def parse_signal(self, xsignals):

        signals = dict()

        for xsignal in xsignals.iter('signal'):
            s = xsignal.get('s')
            t = xsignal.get('t')
            id = xsignal.get('id')
            name = xsignal.get('name')
            dynamic = xsignal.get('dynamic')
            orientation = xsignal.get('orientation')
            z_offset = xsignal.get('zOffset')
            country = xsignal.get('country')
            type = xsignal.get('type')
            subtype = xsignal.get('subtype')
            value = xsignal.get('value')
            unit = xsignal.get('unit')
            height = xsignal.get('height')
            width = xsignal.get('width')
            text = xsignal.get('text')
            h_offset = xsignal.get('hOffset')
            pitch = xsignal.get('pitch')
            roll = xsignal.get('roll')

            new_signal = Signal(s, t, id, name, dynamic, orientation, z_offset, country, type, subtype,
                                value, unit, height, width, text, h_offset, pitch, roll)

            signals[id] = new_signal

        return signals

    def parse_lane(self, xlane):

        # Attributes
        id = int(xlane.get('id'))
        type = xlane.get('type')
        level = xlane.get('level')

        # Lane Links
        xlink = xlane.find('link')
        predecessor = None
        successor = None

        if xlink is not None:
            xpredecessor = xlink.find('predecessor')
            if xpredecessor is not None:
                link_id = int(xpredecessor.get('id'))
                predecessor = LaneLink(link_id)

            xsuccessor = xlink.find('successor')
            if xsuccessor is not None:
                link_id = int(xsuccessor.get('id'))
                successor = LaneLink(link_id)

        # Width
        width = None
        xwidth = xlane.find('width')
        if xwidth is not None:
            s_offset = float(xwidth.get('sOffset'))
            a = float(xwidth.get('a'))
            b = float(xwidth.get('b'))
            c = float(xwidth.get('c'))
            d = float(xwidth.get('d'))
            width = LaneWidth(s_offset, a, b, c, d)

        return Lane(id, type, level, predecessor, successor, width)

    # TODO Add Priorities, JunctionGroups and LaneLinks
    def parse_junctions(self):
        ret = dict()

        for junction in self.root.iter('junction'):
            new_junction = Junction(junction.get('name'), junction.get('id'))

            for connection in junction.iter('connection'):
                id = connection.get('id')
                incoming_road = connection.get('incomingRoad')
                connecting_road = connection.get('connectingRoad')
                contact_point = connection.get('contactPoint')
                new_connection = Connection(id, incoming_road, connecting_road, contact_point)

                new_junction.connections.append(new_connection)

            ret[new_junction.id] = new_junction

        return ret

    def parse_controllers(self):
        ret = dict()

        for xcontroller in self.root.getchildren():

            # Filter all non controller elements of the root node
            if xcontroller.tag != "controller":
                continue

            # Attributes
            name = xcontroller.get('name')
            id = xcontroller.get('id')
            sequence = xcontroller.get('sequence')

            # Control Element
            controls = dict()
            for xcontrol in xcontroller.iter('control'):
                # Attributes
                signal_id = xcontrol.get('signalId')
                type = xcontrol.get('type')

                new_control = Control(signal_id, type)
                controls[new_control.signal_id] = new_control

            new_controller = Controller(id, name, sequence, controls)

            ret[id] = new_controller

        return ret

    def parse_junction_group(self):
        ret = dict()

        for xjunction_group in self.root.iter('junctionGroup'):

            # Attributes
            name = xjunction_group.get('name')
            id = xjunction_group.get('id')
            type = xjunction_group('type')

            # Elements
            junction_references = list()
            for xjunction_reference in xjunction_group.iter('junctionReference'):

                junction = xjunction_reference.get('junction')

                new_junction_reference = JunctionReference(junction)
                junction_references.append(new_junction_reference)

            new_junction_group = JunctionGroup(name, id, type, junction_references)

            ret[id] = new_junction_group

        return ret

