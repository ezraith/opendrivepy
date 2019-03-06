from lxml import etree

class XMLParser(object):
    def __init__(self, file):
        self.xml = etree.parse(file)
        self.opendrive = xml.getroot()
        for element in opendrive.iter('header'):
            self.header = element
            break



