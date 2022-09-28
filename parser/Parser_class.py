from logging import root
import xml.etree.ElementTree as ET
import os.path
from os import path as OSPATH
import time

class xml_data:
     def __init__(self, name):
        self.name = name
        self.data = {}        

class Parser:
    def __init__(self):
        self.data = []
        self.pure_data = []
        self._dictionary = {}
        
    def get_keys(self):
        pass

    def get_values(self):
        pass

    def build_path(self,index):
        
        #print("The catalog")
        #print(self.catalogs[c])
        path = ""
        dictionary = self.catalogs[index][1]

        print("The content of the lists dictionary:")
        print(self.catalogs[index][1])
        
        if("value" in dictionary):
            path = dictionary["value"]
        elif "dir" in dictionary:
            path = dictionary["dir"]
        elif "src" in dictionary:
            path = dictionary["src"] ##fix this
        else:
            return "nopath"       
        
        templist = path.split("/")
        
        #print(templist)
        
        rootinpath = False
        while "[" and "]" in path:
            if(path.count("[") == 1 and "[root]" in path): 
                break
            for temp in self._dictionary:
                if ( "[" + temp + "]") in path:
                    path = path.replace("[" + temp + "]",self._dictionary[temp])
        #print(path)
        return path

    def parsefunction(self,path):
        print("PATH:")
        print(path)

    def parse(self, path):
        print("path = " + path)
        tree = ET.parse(path)
        root = tree.getroot()
        #parsed_data = []
        
        self.catalogs = []
        for obj in root:
        #    print(obj.tag, obj.attrib)
            if(obj.tag == "idb" and ".xml" not in obj.attrib["value"]):
                self._dictionary[obj.attrib["key"]] = obj.attrib["value"]
            else:
                tuple = (obj.tag,obj.attrib)
                self.catalogs.append(tuple)
        #print("\n\n\n")

        #print("Content of self._dicitonary: ")
        #print(self._dictionary)
        #print("\n\n\n")
        #print("Content of catalogs: ")
        #print(self.catalogs)
    
        counter = 0
        while counter < len(self.catalogs):
            path = self.build_path(counter)
            self.parsefunction(path)
            counter +=1