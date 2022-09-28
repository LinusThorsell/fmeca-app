import xml.etree.ElementTree as ET
from os import path as OSPATH

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

        print("The content of the lists dictionary:")
        print(self.catalogs[index][1])
        
        if "value" in dictionary:
            path = dictionary["value"]
        elif "dir" in dictionary:
            path = dictionary["dir"]
        elif "src" in dictionary:
            path = dictionary["src"]
        else:
            return "nopath"       
        
        while "[" and "]" in path:
            if(path.count("[") == 1 and "[root]" in path): 
                break
            for temp in self._dictionary:
                if ( "[" + temp + "]") in path:
                    path = path.replace("[" + temp + "]",self._dictionary[temp])
        dictionary["path"] = path

    def parsefunction(self,index):
        print("PATH:")
        print(self.catalogs[index][1]["path"])

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
            self.build_path(counter)
            self.parsefunction(counter)
            counter +=1

        print("KATALOGEN")
        print(self.catalogs)