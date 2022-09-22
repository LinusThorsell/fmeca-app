import xml.etree.ElementTree as ET
import sys, string

class Parser:

    def __init__(self):
        self._debug = False
        self._delete = False
        self._add = False
        self._arguments = []
        self._flags = {}
        self._nr_arguments = 0

    def delete(self,project):
        ##Tell the database to delete the project
        print("Vi är i delete, project = " + str(project))

    def add(self,path):
        ##Add this project given by the path to the database
        print("Vi är i add, path = " + str(path))

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
        previous_was_two_part_argument = False
        #for i in range(self._nr_arguments):
        i = 0
        while i < self._nr_arguments:
            temp_argument = self._arguments[i]
            if (temp_argument in self._flags):
                if self._flags[temp_argument] == 0:
                    self._functions[temp_argument]()
                    previous_was_two_part_argument = False
                elif self._flags[temp_argument] == 1:
                    if i+1 < self._nr_arguments:
                        #print("i == " + str(i) + " nr_arguments == " + str(self._nr_arguments) )
                        argument = self._arguments[i+1]
                    else:
                        print("Not enough arguments for the flag")
                        exit()
                    self._functions[temp_argument](argument)
                    previous_was_two_part_argument = True

            elif temp_argument not in self._flags and previous_was_two_part_argument:
                previous_was_two_part_argument = False
                i+=1
                continue
            else:
                print("The flag(s) you used is not valid!")
                print("The valid flags are:")
                for flags in self._flags:
                    print(flags)
                print("If the flag requires a path, you put the path right after the flag\n-flag -path")
                exit()
            i+=1

    ##If you want to add more flags and corresponding functions you simply
    ##add the flag and function to the dictionary below
    ##in self._flags we should have the flag and how many arguments we should
    ## have after that
    def initialize(self):
        self._flags = {"print":0,"add":1,"delete":1}
        self._functions = {"print":self.print,"add":self.add,"delete":self.delete}

    def get_arguments(self):
        nrarguments = len(sys.argv)
        if(nrarguments >= 1):
            self._arguments = sys.argv[1:nrarguments]
            self._nr_arguments = len(self._arguments)

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