import xml.etree.ElementTree as ET
import sys, string

#Command Line Interface
class CLI:
    
    def __init__(self):
        self._debug = False
        self._delete = False
        self._add = False
        self._arguments = []
        self._flags = {}
        self._functions = {}
        self._nr_arguments = 0

    def delete(self,project):
        ##Tell the database to delete the project
        print("Vi är i delete, project = " + str(project))
        self._delete = True

    def add(self,xml_file_path):
        ##Add this project given by the path to the database
        print("Vi är i add, path = " + str(xml_file_path))
        self._add = True
    
    def print(self):
        print("Vi är i print")
        self._debug = True

    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            print(child)
    
    def test_func_with_two_args(self, arg1, arg2):
        print("test_func_with_two_args")
    
    def send_to_database(self):
        pass

    def config_database(self,path):
        print("Configuring database, path to file = " + str(path))


    def analyse_cli(self):
        #previous_was_two_part_argument = False
        #for i in range(self._nr_arguments):
        i = 0
        while i < self._nr_arguments:
            #argument_list = []
            temp_argument = self._arguments[i].lower()
            if (temp_argument in self._flags):
                nr_arguments = self._flags[temp_argument]
                print("Nr argumets = " + str(nr_arguments))
                argument_list = self._arguments[i+1:i+1+nr_arguments]
                print(argument_list)
                if (self._flags[temp_argument] != len(argument_list)):
                    print("The Flag \"" + temp_argument + "\" does not have enough arguments, it expects " + str(nr_arguments) + " but " + str(len(argument_list)) + " were given" )
                else:
                    self._functions[temp_argument](*argument_list)
                i+=nr_arguments + 1
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
        self._flags = {"print":0,"add":1,"delete":1,"-c":1, "test":2}
        self._functions = {"print":self.print,"add":self.add,"delete":self.delete,"-c":self.config_database, "test":self.test_func_with_two_args}

    def get_arguments(self):
        nrarguments = len(sys.argv)
        if(nrarguments >= 2):
            self._arguments = sys.argv[1:nrarguments]
            self._nr_arguments = len(self._arguments)

        print(self._arguments)
        
    def add_and_delete(self):
        
        if(self._delete):
            print("Anropa funktionen som ska deletea ett projekt i databasen")
            
        if (self._add):
            ##anropa funktionen som ska posta till databasen
            print("Anropa funktionen som ska lägga till ett projekt i databasen databasen") 
        
        

