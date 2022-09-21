import xml.etree.ElementTree as ET
import sys, string

class Parser:

    def __init__(self):
        self._debug = False
        self._arguments = []
        self._flags = {}

    def delete(self):
        print("Vi är i delete")

    def add(self):
        print("Vi är i add")

    def print(self):
        print("Vi är i print")
        self._debug = True

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
                if(self._flags[temp_argument] == 0):
                    self._functions[temp_argument]()
                if(self._flags[temp_argument] == 1):
                    pass
                    #self._functions[temp_argument](arg)
            else:
                print("The flag(s) you used is not valid!")
                print("The valid flags are:")
                for flags in self._flags:
                    print(flags)
                print("If the flag requires a path, you put the path right after the flag\n-flag -path")
                exit()
    
    ##If you want to add more flags and corresponding functions you simply
    ##add the flag and function to the dictionary below
    ##in self._flags we should have the flag and how many arguments we should
    ## have after that
    def initialize(self):
        self._flags = {"print":0,"add":0,"delete":0}
        self._functions = {"print":self.print,"add":self.add,"delete":self.delete}

    def get_arguments(self):
        nr_arguments = len(sys.argv)
        if(nr_arguments >= 1):
            self._arguments = sys.argv[1:nr_arguments]
        print(self._arguments)


'''
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
'''