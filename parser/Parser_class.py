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


    def build_path(self,c):
        path = self.catalogs[c]["dir"]
        print("In build path")
        print("pathe == " ,path)
        print(self.catalogs[c])
        templist = path.split("/")
        
        print(templist)
        
        rootinpath = False
        while "[" and "]" in path:# rootinpath == False:
            print("\n\n")
            print("path == ",path)
            if(path.count("[") == 1 and "[root]" in path): 
                break
            print("Dictionary == ", self._dictionary)
            for temp in self._dictionary:
                print(temp)
                print("[" + temp + "]")
                if ( "[" + temp + "]") in path:
                    path = path.replace("[" + temp + "]",self._dictionary[temp])

            time.sleep(2)
        print(path)
        return path

    def parse(self, path):
        print("path = " + path)
        tree = ET.parse(path)
        root = tree.getroot()
        #parsed_data = []
        
        self.catalogs = {}

        for obj in root:
            print(obj.tag, obj.attrib)
            if(obj.tag == "idb"):
                self._dictionary[obj.attrib["key"]] = obj.attrib["value"]
            else:
                self.catalogs[obj.tag] = obj.attrib
        print("\n\n\n")

        print("Content of self._dicitonary: ")
        print(self._dictionary)
        print("\n\n\n")
        print("Content of catalogs: ")
        print(self.catalogs)
        
        for c in self.catalogs:
            #print(c)
            if "dir" in self.catalogs[c]:
                self.build_path(c)
            
        
        
'''
    def replace_varible_with_value(self, s):
        while ']' in s:
        split_s = s.split('/')
        #print("S = ")
        #print(split_s)
        for  index, sub_s in enumerate(split_s):
            for line in self.data:
                if isinstance(line.data.get("key"), str) and line.data.get("key") in sub_s:
                    #print("Key = " + line.data.get("key"))
                    #print("Value = " + line.data.get("value"))
                    split_s[index] = line.data.get("value")
                    break
        #print(split_s)
        s = '/'.join(split_s)
        #print(done_s)
        
        return s

    def vaild_path_to_parse(self, value):
        path = self.replace_varible_with_value(value)
        print(path)
        if (OSPATH.exists(path)) and  "xml" in path:
            return path 
        else:
            return False
    def recursive_parser(self):
        print("PATHS:\n\n")
        for obj in self.data:
            for value in obj.data.values():
                print(value)
                path = self.vaild_path_to_parse(value)
                if (path):
                    print(path)
        print("\n\n\n")



    def build_path(self,c):
        path = self.catalogs[c]["dir"]
        print("In build path")
        print("pathe == " ,path)
        print(self.catalogs[c])
        templist = path.split("/")
        
        print(templist)
        
        
        #for values in self._dictionary:
        #    if "[" + values + "]" in templist:
        #        print("values in list == " + values)

        while "[" and "]" in templist:
            pass
        
        path = ""
        counter =0 
        while counter != len(templist):
            path += templist[counter]
            
            counter+=1
            if ( counter != len(templist)):
                path+= "/"
        print(path)
        return path'''