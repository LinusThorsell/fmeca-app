from Parser_class import Parser
import sys, string, os
from os import path as OSPATH
from Encoder_Class import *
import DataClass
import Paths
import DebugFile
import platform
import xml.etree.ElementTree as ET
import fileinput

#CLI - Command Line Interface
#Handles the command line interface class and functions
#Finds the file paths where the data is located

class CLI:
    
    def __init__(self):
        self._delete = False
        self._add = False
        self._arguments = []
        self._flags = {}
        self._functions = {}
        self._nr_arguments = 0
        self._parser = Parser()
        self._encoder = Encoder()
        self._Paths = Paths.Paths()
        self._parser = Parser()
        self._parser.initialisation()
        self.delete_argument = ""
        self._add_path = None
        self._meta_path = None
        self._project_name = ""
        self.PRINT = False
        
    def delete(self,project):
        ##Tell the database to delete the project
        self.delete_argument = project
        self._delete = True
        self._functions = self._delete_functions

    def add(self):
        ##Add this project given by the path to the database
        self._add = True
        self._functions = self._add_functions
        
    def meta(self, meta_path):
        self._meta_path = meta_path
    
    def path(self, path_to_infrastructure):
        self._add_path = path_to_infrastructure
    
    def tag(self, project_name):
        self._project_name = project_name

    def debug(self):
        DebugFile.debug = True
        DebugFile.debug_print("DEBUG active")

    def send(self):
        DebugFile.send = True

    def get_paths(self):
        self._Paths.initial_path(self._add_path)
        self._Paths.get_paths(self._Paths.fc_path)
        self._Paths.get_paths(self._Paths.mc_path)

    def print_f(self):
        self.PRINT = True
        self._functions = self._print_functions

    def config_database(self, path):
        DebugFile.debug_print("Configuring database, path to file = " + str(path))
        tree = ET.parse(path)
        root = tree.getroot()
        attributes = {}

        for child in root:
            #print(child.tag)
            attributes[child.tag.upper()] = child.get("name")

        nr_prints = 6
        #print(attributes)
        DATABASES_V = False
        for line in fileinput.input("backend/fmeca-django/backend/settings.py", inplace=True):
            for key,value in attributes.items():
                if "DATABASES" in line:
                    DATABASES_V = True
               
                if DATABASES_V == True and nr_prints > 0:
                    if key in line :
                        line = '\t' +'\''+ str(key) +'\'' +  ":" + '\'' + str(value) +'\''+ "," + "\n"
                        nr_prints -=1
                        break
            print('{}'.format( line), end='') # for Python 3
        fileinput.close()

    def analyse_cli(self):
        #previous_was_two_part_argument = False
        #for i in range(self._nr_arguments):
        i = 0
        while i < self._nr_arguments: #or self._keep_alive:
            #argument_list = []
            temp_argument = self._arguments[i].lower()
            if (temp_argument in self._flags):
                nr_arguments = self._flags[temp_argument]
                argument_list = self._arguments[i+1:i+1+nr_arguments]
                if (self._flags[temp_argument] != len(argument_list)):
                    print("The Flag \"" + temp_argument + "\" does not have enough arguments, it expects " + str(nr_arguments) + " but " + str(len(argument_list)) + " were given" )
                else:
                    self._functions[temp_argument](*argument_list)
                i+=nr_arguments + 1
                """ if(not(i < self._nr_arguments) and self._keep_alive): 
                    self._arguments = input("parser: ")
                    self._arguments = self._arguments.split(" ")
                    self._nr_arguments = len(self._arguments)
                    i = 0 """
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
        self._flags = {"debug":0,"add":0,"remove":0,"-c":1, "-path":1, "-meta":1, "-tag":1,"print":0}
        self._functions = {"add":self.add,"remove":self.delete,"print":self.print_f}
        self._delete_functions = {"remove":self.delete, "-tag":self.tag,"-c":self.config_database,"debug":self.debug}
        self._add_functions = {"add":self.add,"-meta":self.meta,"-tag":self.tag, "-path":self.path,"-c":self.config_database,"debug":self.debug}
        self._print_functions = {"print":self.print_f,"-meta":self.meta,"-tag":self.tag, "-path":self.path}
        DebugFile.windows = False 
        if platform.system() == "windows":
            DebugFile.windows = True 
   
    def parsing(self):
            #Call function that posts to database
            DebugFile.debug_print("Call function: ADD to database")
            DebugFile.debug_print(self._add_path)
            self.get_paths()
            DebugFile.debug_print("PATHS:")
            DebugFile.debug_print(self._Paths._paths)
            Project_type = DataClass.Project_Data_Class(self._project_name)
            
            Connections = DataClass.ConnectionContainer(self._project_name)
            Applications = DataClass.ApplicationContainer(self._project_name)
            runorder = ["fc/hw_topology.xml", "mc/hw_topology.xml","fc/sw_topology.xml","mc/sw_topology.xml","functional_topology/fc","functional_topology/mc"]
            #runorder = ["functional_topology/fc","functional_topology/mc"]

            connectionlist =  []
            application_instances = []
            
            for temppath in runorder:
                for path in self._Paths._paths:
                    if temppath in path and "fc/hw_topology.xml" in temppath:
                        Project_type.filter(self._parser.get_nodes(path))
                    elif temppath in path and "mc/hw_topology.xml" in temppath:
                        Project_type.filter(self._parser.get_nodes(path))
                    elif temppath in path and "fc/sw_topology.xml" in temppath:
                        Project_type.insert_partitions(self._parser.get_partitions(path))
                    elif temppath in path and "mc/sw_topology.xml" in temppath:
                        Project_type.insert_applications(self._parser.get_cpu_applications(path))

                    #För connections: Kolla efter <Project>/infrastructure/functional_topology/ sedan fc eller mc
                    elif temppath in path and "functional_topology/fc" in temppath:
                        if os.path.exists(path+"/connections"):

                            for subdir, dirs, files in os.walk(path+"/connections"):
                                for file in files:
                                    if(file == "connections.xml"):
                                        print(subdir + "/"+file)
                                        connectionlist += self._parser.get_connections(os.path.join(subdir,file))

                        print("PATH ===== " ,path + "/application_instance.xml")
                        if os.path.exists(path + "/application_instances.xml"):
                            if os.path.isfile( path + "/application_instances.xml"):
                                application_instances += self._parser.get_application_instances(path + "/application_instances.xml")

                    #Search for connections directories
                    elif temppath in path and "functional_topology/mc" in temppath:
                        if os.path.exists(path+"/connections"):
                            for subdir, dirs, files in os.walk(path+"/connections"):
                                for file in files:
                                    if(file == "connections.xml"):
                                        print(subdir + "/"+file)
                                        connectionlist += self._parser.get_connections(os.path.join(subdir,file))
                        if os.path.exists(path + "/application_instances.xml"):
                            if os.path.isfile( path + "/application_instances.xml"):
                                application_instances += self._parser.get_application_instances(path + "/application_instances.xml")
            return Project_type

    def get_arguments(self):
        nrarguments = len(sys.argv)
        if(nrarguments >= 2):
            self._arguments = sys.argv[1:nrarguments]
            self._nr_arguments = len(self._arguments)
        DebugFile.debug_print("ArgumentList",self._arguments)
        if "add" in self._arguments and "delete" in self._arguments:
            print("Cant have both \"add\" and \"delete\" in the arguments")
            exit()
        elif "add" in self._arguments:
            self._functions = self._add_functions
        elif "delete" in self._arguments:
            self._functions = self._delete_functions      
    
    def add_and_delete(self):
        
        if(self._delete and self._project_name != ""):
            DebugFile.debug_print("Call function: DELETE from database")
            self._encoder.delete_from_database(self._project_name, "projects/")
        elif (self._add and self._add_path != None and self._project_name != ""):      
            Project_type = self.parsing()
            self.send()
            self._encoder.send_to_database(Project_type,"projects/")
            #self._encoder.send_to_database(Connections,"connections/")
            #self._encoder.send_to_database(Applications,"applications/")
        
        elif self.PRINT:
            self.debug()
            Project_type = self.parsing()
            self._encoder.send_to_database(Project_type,"projects/")
            #self._encoder.send_to_database(Connections,"connections/")
            #self._encoder.send_to_database(Applications,"applications/")
        
        else:
            print("bad")
            exit()
            