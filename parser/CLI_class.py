#import xml.etree.ElementTree as ET
#import os.path
from Parser_class import Parser
import sys, string, os
from os import path as OSPATH
from Encoder_Class import *
import DataClass
import Paths
#Command Line Interface

import DebugFile
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
        
    def delete(self,project):
        ##Tell the database to delete the project
        self.delete_argument = project
        self._delete = True

    def add(self,xml_file_path):
        ##Add this project given by the path to the database
        self._add = True
        self._add_path = xml_file_path

    def debug(self):
        DebugFile.debug = True
        DebugFile.debug_print("DEBUG active")

    
    def get_paths(self):
        self._Paths.initial_path(self._add_path)
        self._Paths.get_paths(self._Paths.fc_path)
        self._Paths.get_paths(self._Paths.mc_path)

    def config_database(self,path):
        print("Configuring database, path to file = " + str(path))
    
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
        self._flags = {"debug":0,"add":1,"delete":1,"-c":1}
        self._functions = {"debug":self.debug,"add":self.add,"delete":self.delete,"-c":self.config_database}

    def get_arguments(self):
        nrarguments = len(sys.argv)
        if(nrarguments >= 2):
            self._arguments = sys.argv[1:nrarguments]
            self._nr_arguments = len(self._arguments)
        DebugFile.debug_print("ArgumentList",self._arguments)
        
    def add_and_delete(self):
        
        if(self._delete):
            DebugFile.debug_print("Call function: DELETE from database")
            self._encoder.delete_from_database(self.delete_argument, "projects/")
            
        if (self._add):
            #Call function that posts to database
            DebugFile.debug_print("Call function: ADD to database")
            DebugFile.debug_print(self._add_path)
            self.get_paths()
            DebugFile.debug_print("PATHS:")
            DebugFile.debug_print(self._Paths._paths)
            Project_type = DataClass.Project_Data_Class(self._parser.get_project_name(self._add_path))
            
            #Behöver göra om detta i framtiden, funkar for now
            runorder = ["fc/hw_topology.xml", "mc/hw_topology.xml","fc/sw_topology.xml","mc/sw_topology.xml"]
            
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

            
            self._encoder.send_to_database(Project_type,"projects/")


