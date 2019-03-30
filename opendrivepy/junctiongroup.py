from __future__ import division, print_function, absolute_import


class JunctionGroup(object):
    def __init__(self, name, id, type, junction_references):
        # Attributes
        self.name = name
        self.id = id
        self.type = type

        # Elements
        self.junction_references = junction_references


class JunctionReference(object):
    def __init__(self, junction):
        # Attributes
        self.junction = junction  # ID of the junction

