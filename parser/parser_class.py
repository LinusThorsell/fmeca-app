import xml.etree.ElementTree as ET
import sys, string

class Parser:

    def __init__(self):
        self._debug = False
        self._arguments = []

    def analyse_cli(self):
        nr_arguments = len(sys.argv)
        if(nr_arguments >= 1):
            self._arguments = sys.argv[1:nr_arguments-1]

        print(self._arguments)

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




#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

##För debug
if(sys.argv[1].lower == "print"):
    pass

##För att lägga till ett projekt i databasen
elif(string.ascii_lowercase(sys.argv[1]) == "add"):
    pass

elif(string.ascii_lowercase(sys.argv[1]) == "parse"):
    Parser.parse(sys.argv[2])

## För att ta bort ett projekt från databasen
elif(string.ascii_lowercase(sys.argv[1]) == "delete"):
    pass
elif string.ascii_lowercase(sys.argv[1] == "-c"):
    pass

##efter denna ska en path till en fil med databaskonfig vara sen
elif string.ascii_lowercase(sys.argv[1] == "-d"):
    pass

else:
    pass
