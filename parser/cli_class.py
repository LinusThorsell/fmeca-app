from parser_class import Parser
import sys, string, os
from os import path as OSPATH
from encoder_class import *
import dataclass as dataclass
import paths as paths
import debugfile as debugfile
import tests as tests
import xml.etree.ElementTree as ET

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
        self._Paths = paths.Paths()
        self._add_path = None
        self._meta_path = None
        self.PRINT = False
        self._project_name = ""
    
    #Tell the database to delete the given project
    def remove(self):
        self._remove = True
        self._functions = self._remove_functions

    #Add this project given by the path to the database
    def add(self):
        self._add = True
        self._functions = self._add_functions
    
    #Not implemented
    def meta(self, meta_path):
        self._meta_path = meta_path
    
    #Adds the path to folder containing the infrastructure folder
    def path(self, path_to_infrastructure):
        self._add_path = path_to_infrastructure
    
    #Change tag if one is provided
    def tag(self, project_name):
        self._project_name = project_name

    #Enable debug mode
    def debug(self):
        debugfile.debug = True
        debugfile.debug_print("DEBUG active")

    #Change the api adress of database
    def ip(self, url):
        self._encoder.config_api(url)

    #Should later send to database 
    def send(self):
        debugfile.send = True

    #Get paths from system.xml file
    def get_paths(self):
        self._Paths.initial_path(self._add_path)
        self._Paths.get_paths(self._Paths.fc_path)
        self._Paths.get_paths(self._Paths.mc_path)
        self._Paths.add__outer_folders_to_paths()

    #The parsed data will later be printed 
    def print_f(self):
        self.PRINT = True
        self._functions = self._print_functions

    #Config database adress, can be extened to do more
    def config_database(self, path):
        debugfile.debug_print("Configuring database, path to file = " + str(path))
        tree = ET.parse(path)
        root = tree.getroot()
        
        for child in root:
            if(child.tag == "IP"):
                ip = child.get("value")
            elif(child.tag == "PORT"):
                port = child.get("value")
        self.ip(ip + ":"  + port + "/")
        
    #Parse the commands and execute commands
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
        self._flags = {"debug":0,"add":0,"remove":0,"-c":1, "-path":1, "-meta":1, "-tag":1,"print":0, "-ip":1}
        self._functions = {"add":self.add,"remove":self.remove,"print":self.print_f}
        self._remove_functions = {"remove":self.remove, "-tag":self.tag,"-c":self.config_database,"debug":self.debug, "-ip":self.ip}
        self._add_functions = {"add":self.add,"-meta":self.meta,"-tag":self.tag, "-path":self.path,"-c":self.config_database,"debug":self.debug, "-ip":self.ip}
        self._print_functions = {"print":self.print_f,"-meta":self.meta,"-tag":self.tag, "-path":self.path}
        debugfile.windows = False 
    
    #Main parse funtion
    def parsing(self):
        #Call function that posts to database
        debugfile.debug_print("Call function: ADD to database")
        debugfile.debug_print(self._add_path)
        self.get_paths()
        debugfile.debug_print("PATHS:")
        debugfile.debug_print(self._Paths._paths)


        # The order we want to parse the files in
        runorder = []
        runorder += ["functional_topology/fc","functional_topology/mc"]
        runorder += ["fc/hw_topology.xml", "mc/hw_topology.xml","fc/sw_topology.xml","mc/sw_topology.xml"]
        runorder += [ "/applications/", "/domain_border"]
        
        
        # If no tag was specified use name from folder
        if(self._project_name == ""): 
            self._project_name = self._parser.get_project_name(self._add_path) 
        
        # Init containers
        self.Project_Type = dataclass.Project_Data_Class(self._project_name)

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
                elif temppath in path and "/domain_border" in temppath:
                    self._parser.get_all_domains(path,self.Project_Type.domain_border_set)

                    
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
                            
        #Remove duplicate applications  
        self.Project_Type.application_set = list(set(self.Project_Type.application_set))

        #Run tests that checks if all data refer to actual obejcts
        tests.run_all(self.Project_Type)

    #Make sure to only allow one of the main commands: print, add, remove
    #The subcommands avalible are depending on the main command
    def get_arguments(self):
        nrarguments = len(sys.argv)
        if(nrarguments >= 2):
            self._arguments = sys.argv[1:nrarguments]
            self._nr_arguments = len(self._arguments)
        debugfile.debug_print("ArgumentList",self._arguments)
        if sum([("add" in self._arguments), ("remove" in self._arguments), ("print" in self._arguments)]) != 1:
            debugfile.error_print("Can only have one of \"add\", \"remove\", \"print\" in the arguments")
            exit(1)
        elif "add" in self._arguments:
            self._functions = self._add_functions
        elif "remove" in self._arguments:
            self._functions = self._remove_functions      
    
    #Called by parser.py 
    def execute_commands(self):
        if(self._remove and self._project_name != ""):
            debugfile.debug_print("Call function: DELETE from database")
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
            debugfile.error_print("bad")
            exit()
            