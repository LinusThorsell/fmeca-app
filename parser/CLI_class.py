from Parser_class import Parser
import sys, string, os
from os import path as OSPATH
from Encoder_Class import *
import DataClass
import Paths
import DebugFile
import Tests
import platform
import xml.etree.ElementTree as ET
import fileinput
import time
#CLI - Command Line Interface
#Handles the command line interface class and functions
#Finds the file paths where the data is located

class CLI:
    def __init__(self):
        self._remove = False
        self._add = False
        self._arguments = []
        self._flags = {}
        self._functions = {}
        self._nr_arguments = 0
        self._parser = Parser()
        self._encoder = Encoder()
        self._Paths = Paths.Paths()
        self._add_path = None
        self._meta_path = None
        self._project_name = ""
        self.PRINT = False
        
    def remove(self):
        #Tell the database to delete the given projec
        self._remove = True
        self._functions = self._remove_functions

    def add(self):
        #Add this project given by the path to the database
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
            attributes[child.tag.upper()] = child.get("name")

        nr_prints = 6
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
        i = 0
        while i < self._nr_arguments:
            temp_argument = self._arguments[i].lower()
            if (temp_argument in self._flags):
                nr_arguments = self._flags[temp_argument]
                argument_list = self._arguments[i+1:i+1+nr_arguments]
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

    #If you want to add more flags and corresponding functions you simply
    #add the flag and function to the dictionary below
    #in self._flags we should have the flag and how many arguments we should
    # have after that
    def initialize(self):
        self._flags = {"debug":0,"add":0,"remove":0,"-c":1, "-path":1, "-meta":1, "-tag":1,"print":0}
        self._functions = {"add":self.add,"remove":self.remove,"print":self.print_f}
        self._remove_functions = {"remove":self.remove, "-tag":self.tag,"-c":self.config_database,"debug":self.debug}
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


        # The order we want to parse the files in
        runorder = []
        runorder += ["functional_topology/fc","functional_topology/mc"]
        runorder += ["fc/hw_topology.xml", "mc/hw_topology.xml","fc/sw_topology.xml","mc/sw_topology.xml"]
        runorder += [ "/applications/", "/domain_border"]
        
        
        # If no tag was specified use name from folder
        if(self._project_name == ""): 
            self._project_name = self._parser.get_project_name(self._add_path) 
        
        # Init containers
        self.Project_Type = DataClass.Project_Data_Class(self._project_name)

        # Parse files by order specified by runorder list
        for temppath in runorder:
            for path in self._Paths._paths:
                if temppath in path and "fc/hw_topology.xml" in temppath:
                    self.Project_Type.filter(self._parser.get_nodes(path))
                elif temppath in path and "mc/hw_topology.xml" in temppath:
                    self.Project_Type.filter(self._parser.get_nodes(path))
                elif temppath in path and "fc/sw_topology.xml" in temppath:
                    self.Project_Type.insert_partitions(self._parser.get_partitions(self.Project_Type,path))
                elif temppath in path and "mc/sw_topology.xml" in temppath:
                    self.Project_Type.insert_applications(self._parser.get_cpu_applications(self.Project_Type,path))
                elif temppath in path and "functional_topology/fc" in temppath:
                    self.Project_Type.connection_set += self._parser.get_connection_list(path)
                    self.Project_Type.application_set += self._parser.get_applications_list(path)
                    self.Project_Type.application_instance_set += self._parser.get_applications_instances_list(path)
                elif temppath in path and "functional_topology/mc" in temppath:
                    self.Project_Type.application_set += self._parser.get_applications_list(path)
                    self.Project_Type.application_instance_set += self._parser.get_applications_instances_list(path)
                    self.Project_Type.connection_set += self._parser.get_connection_list(path)
                elif temppath in path and "/applications/" in temppath:
                    self.Project_Type.thread_set += self._parser.get_threads(path)
                    #self.Threads.thread_set += self._parser.get_threads(path)
                elif temppath in path and "/domain_border" in temppath:
                    self._parser.get_all_domains(path,self.Project_Type.domain_border_set)
                    #self._parser.get_all_domains(path,self.DomainBorder)

         #-----------------------------------------------------------------------------
                    
        # Adding domainborder to connection
        for connection in self.Project_Type.connection_set:
            if connection.Provider_is_domainborder:
                for db in self.Project_Type.domain_border_set:
                    for port in db.port_set:
                        if port.name == connection.Provider_port:
                            connection.Provider_owner = db.name
            if connection.Requirer_is_domainborder:
                for db in self.Project_Type.domain_border_set:
                    for port in db.port_set:
                        if port.name == connection.Requirer_port:
                            connection.Requirer_owner = db.name
                            

        self.Project_Type.application_set = list(set(self.Project_Type.application_set))
        Tests.run_all(self.Project_Type)

    def get_arguments(self):
        nrarguments = len(sys.argv)
        if(nrarguments >= 2):
            self._arguments = sys.argv[1:nrarguments]
            self._nr_arguments = len(self._arguments)
        DebugFile.debug_print("ArgumentList",self._arguments)
        if sum([("add" in self._arguments), ("remove" in self._arguments), ("print" in self._arguments)]) != 1:
            DebugFile.error_print("Can only have one of \"add\", \"remove\", \"print\" in the arguments")
            exit(1)
        elif "add" in self._arguments:
            self._functions = self._add_functions
        elif "remove" in self._arguments:
            self._functions = self._remove_functions      
    
    def add_and_remove(self):
        
        if(self._remove and self._project_name != ""):
            DebugFile.debug_print("Call function: DELETE from database")
            self._encoder.delete_from_database(self._project_name, "projects/")
        elif (self._add and self._add_path != None and self._project_name != ""):      
            self.parsing()
            


            self._encoder.Project = self._project_name
            self._encoder.send_to_database(self.Project_Type,"projects/")
        
        elif self.PRINT:
            self.debug()
            self.parsing()
            
            self._encoder.Project = self._project_name
            self._encoder.print_project(self.Project_Type)
        else:
            DebugFile.error_print("bad")
            exit()
            