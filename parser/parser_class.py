from ssl import ALERT_DESCRIPTION_UNEXPECTED_MESSAGE
import xml.etree.ElementTree as ET
import sys, string

class Parser:

    def __init__(self):
        self._debug = False
        self._arguments = []
        self._flags = {}

    def get_arguments(self):
        nr_arguments = len(sys.argv)
        if(nr_arguments >= 1):
            self._arguments = sys.argv[1:nr_arguments]
        print(self._arguments)

    def delete(self):
        print("Vi är i delete")

    def add(self):
        print("Vi är i add")

    def print(self):
        print("Vi är i print")

    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            print(child)
    
    def send_to_database(self):
        pass

    def analyse_cli(self):
        
        for arguments in self._arguments:
            temp_argument = arguments.lower()
            print(temp_argument)
            if(temp_argument in self._flags):
                self.flags[temp_argument]()
            else:
                print("The flag(s) you used is not valid!")
                print("The valid flags are:")
                for flags in self._flags:
                    print(flags)
                exit()
    
    ##If you want to add more flags and corresponding functions you simply
    ##add the flag and function to the dictionary below
    def initialize_flags(self):
        self._flags = {"print":self.print,"add":self.add,"delete":self.delete}





#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

##För debug
if(sys.argv[1].lower == "print"):
    pass

##För att lägga till ett projekt i databasen
elif(sys.argv[1].lower == "add"):
    pass

elif(sys.argv[1].lower == "parse"):
    Parser.parse(sys.argv[2])

## För att ta bort ett projekt från databasen
elif(sys.argv[1].lower == "delete"):
    pass
elif (sys.argv[1].lower == "-c"):
    pass

##efter denna ska en path till en fil med databaskonfig vara sen
elif (sys.argv[1].lower== "-d"):
    pass

else:
    pass
