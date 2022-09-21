import xml.etree.ElementTree as ET

class Parser:

    def __init__(self):
        _debug = False
        

    def analyse_cli(self):
        pass

    def delete(self):
        pass

    def add(self):
        pass

    def print(self):
        pass

    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            print(child)
    
    def send_to_database(self):
        pass