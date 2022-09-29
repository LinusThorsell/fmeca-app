import xml.etree.ElementTree as ET
from os import path as OSPATH
import json
import os
class Parser:
    def __init__(self):
        self.data = []
        self.pure_data = []
        self._dictionary = {}
        
    def build_path(self,index):
        
        #print("The catalog")
        #print(self.catalogs[c])
        path = ""
        dictionary = self.catalogs[index][1]

        #print("The content of the lists dictionary:")
        #print(self.catalogs[index][1])
        
        if "value" in dictionary:
            path = dictionary["value"]
        elif "dir" in dictionary:
            path = dictionary["dir"]
        elif "src" in dictionary:
            path = dictionary["src"]
        elif "conf" in dictionary:
            path = dictionary["conf"]
        else:
            return "nopath"       
        
        
        if "[acs_src]" in path:
            path = "nopath"
        else:
            while "[" and "]" in path:         
                if(path.count("[") == 1 and "[root]" in path): 
                    break
                for temp in self._dictionary:
                    if ( "[" + temp + "]") in path:
                        path = path.replace("[" + temp + "]",self._dictionary[temp])
        dictionary["path"] = path

    def parsefunction(self,index):
        #print("PATH:")
        #print(self.catalogs[index][1])
        #print(self.catalogs[index][1]["path"])
        temppath = self.catalogs[index][1]["path"]
        if temppath == "nopath":
            return
        templist = temppath.split("/")
        
        newpath = ""
        counter = 3
        if len(templist) >= 3:       
            while counter < len(templist):
                
                newpath += templist[counter]
                if counter+1 != len(templist):
                    newpath += "/" 
                counter +=1
        else:
            return

        print(newpath)
        if os.path.exists(newpath):
            if ".xml" in newpath:
                print(ET.tostring(ET.parse(newpath).getroot(),encoding="ISO-8859-1").decode('utf8'))
            elif os.path.isdir(newpath):
                print("Kollar igenom directories")
                for filename in os.scandir(newpath):
                    if filename.is_file():
                        #print("LALALALAL")
                        #print(filename.path)
                        print(ET.tostring(ET.parse(filename.path).getroot(),encoding="ISO-8859-1").decode('utf8'))

            

    def initial_path(self,path):
        self.fc_path = path + "/fc/system.xml"
        self.mc_path = path + "/mc/system.xml"


    def parse(self, path):
        #print("path = " + path)
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
            self.build_path(counter)
            self.parsefunction(counter)
            counter +=1

        #print("KATALOGEN")
        #print(self.catalogs)