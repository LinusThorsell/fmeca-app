import xml.etree.ElementTree as ET
import os.path
from os import path as OSPATH


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
        
        
    def parse(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        #parsed_data = []

        for obj in root:
            print(obj.tag, obj.attrib)
            if(obj.tag == "idb"):
                self._dictionary[obj.attrib["key"]] = obj.attrib["value"]
        print("\n\n\n")

        print("Content of self._dicitonary: ")
        print(self._dictionary)
        print("\n\n\n")

        '''
        for child in root:
            #print(child.tag)
            pure_value = xml_data(child.tag)
            parsed_value = xml_data(child.tag)
            pure_value.data[child.attrib.get("key")] = child.attrib.get("value")
            parsed_value.name = child.tag
            parsed_value.data = child.attrib
            #print(child.attrib)
            # for obj in child.attrib.items():
            #     #print("    " + obj[0] + " = " + obj[1])
            #     parsed_value.data[obj[0]] = obj[1]
            self.data.append(parsed_value)
            self.pure_data.append(pure_value)
        print("Pure data")
        for obj in self.pure_data:
            print(obj.data)
        counter =0
        '''
        #while counter < 

                



'''
try:
    f = open("filename.txt")
    # Do something with the file
except IOError:
    print("File not accessible")
finally:
    f.close()
'''