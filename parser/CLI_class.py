import xml.etree.ElementTree as ET
import os.path
from Parser_class import Parser
import sys, string, os
from os import path as OSPATH
from Encoder_Class import *
import DataClass
import Paths
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
        self._all_parser = 0
        self._keep_alive = False
        self._parser = Parser()
        self._encoder = Encoder()
        self._Paths = Paths.Paths()
        self._parser = Parser()
    
    def delete(self,project):
        ##Tell the database to delete the project
        print("Vi är i delete, project = " + str(project))
        self._delete = True

    def add(self,xml_file_path):
        ##Add this project given by the path to the database
        print("Vi är i add, path = " + str(xml_file_path))
        self._add = True
        self._add_path = xml_file_path
        
    
    def print(self):
        print("Vi är i print")
        self._debug = True
    

    def parse_all(self, path):
        self._all_parser = Parser()
        self._all_parser.parse_all(path)
    

    def get_paths(self):
        self._Paths.initial_path(self._add_path)
        self._Paths.get_paths(self._Paths.fc_path)
        self._Paths.get_paths(self._Paths.mc_path)
    
    
    
    def send_to_database(self):
        pass

    def config_database(self,path):
        print("Configuring database, path to file = " + str(path))
    
    def analyse_cli(self):
        #previous_was_two_part_argument = False
        #for i in range(self._nr_arguments):
        i = 0
        while i < self._nr_arguments or self._keep_alive:
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
                if(not(i < self._nr_arguments) and self._keep_alive): 
                    self._arguments = input("parser: ")
                    self._arguments = self._arguments.split(" ")
                    self._nr_arguments = len(self._arguments)
                    i = 0

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
        self._flags = {"print":0,"add":1,"delete":1,"-c":1, "test":2, "-kp":0, "quit":0, "parse":1,"print_xml":1, "ls":0, "find":2, "get":3}
        self._functions = {"print":self.print,"add":self.add,"delete":self.delete,"-c":self.config_database}

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
            print(self._add_path)
            self.get_paths()
            print("PATHS:")
            print(self._Paths._paths)
            Project_type = DataClass.Project(self._parser.get_project_name(self._add_path))
            
            #Assumes right path to fc/hw_topology
            Project_type.add_NodeFC(self._parser.get_fc_nodes('Project_1/infrastructure/fc/hw_topology.xml'))
            
            #Assumes right path to mc/hw_topology
            Project_type.add_NodeMC(self._parser.get_mc_nodes('Project_1/infrastructure/mc/hw_topology.xml'))
            
            #Assumes right path to fc/sw_topology
            Project_type.add_Partitions(self._parser.get_partitions('Project_1/infrastructure/fc/sw_topology.xml'))



            self._encoder.send_to_database(Project_type.ProjectDataClass,"projects/")
            
            for nodes in Project_type.NodeFC:
                self._encoder.send_to_database(nodes,"node-fc/")
            for nodes in Project_type.NodeMC:
                self._encoder.send_to_database(nodes,"node-mc/")
            for partitions in Project_type.Partitions:
                self._encoder.send_to_database(partitions,"partitions/")