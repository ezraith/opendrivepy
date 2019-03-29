from __future__ import division, print_function, absolute_import


class Controller(object):
    def __init__(self, id, name, sequence, controls):
        # Attributes
        self.id = id
        self.name = name
        self.sequence = sequence

        # Elements
        self.controls = controls


class Control(object):
    def __init__(self, signal_id, type):
        # Attributes
        self.signal_id = signal_id
        self.type = type
