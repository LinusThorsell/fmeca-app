import xml.etree.ElementTree as ET
from os import path as OSPATH
import json
import os
import requests
class xml_file:
    def __init__(self, path):
        self.path = path
        self.data = []
        self.xml = None

    def get_values(self):
        return self.data.values()


class xml_data:
     def __init__(self, name):
        self.name = name
        self.data = {}
        self.children = []

class Parser:
    def __init__(self):
        self.data = []
        self.pure_data = []
        self._dictionary = {}
        self.all_file_paths = []
        self.parsed_files = []
        
    def send_project_name(self,path):
        url = 'http://127.0.0.1:8000/projects/'
        temp = path.split("/")
        name = temp[0]
        headers = {"Content-Type":"application/json"}
        x = {"project_id":name}
        string = json.dumps(x)
        print("Postar detta:",headers,string)
        requests.post(url,string,headers=headers)

    def fc_hw_topology(self,path):
        #path = 'Project_1/infrastructure/fc/hw_topology.xml'
        tree = ET.parse(path)
        root = tree.getroot()
        for i in root.findall('DCM'):
            name = i.get('name')
            print(name)
            #add to database?
            

    def fc_sw_topology(self,path):
        #path = 'Project_1/infrastructure/fc/sw_topology.xml'
        tree = ET.parse(path)
        root = tree.getroot()
        for i in root.findall('APP'):
            name = i.get('ref')
            print(name)
            #add to database?
            #x = {""}

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
                tree = ET.parse(newpath)
                root = tree.getroot()
                curr_file = xml_file(newpath)     
                
                for child in root:
                    # Store data
                    parsed_value = xml_data(child.tag)
                    parsed_value.data = child.attrib
                    curr_file.data.append(parsed_value)
                    
                curr_file.xml = tree
                self.parsed_files.append(curr_file)
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
    
    def get_values_from_xml(self, xml, element_to_search_for, value_to_search_for):
        tree = ET.parse(xml.path)
        root = tree.getroot()

        results = []
        elements = root.findall(element_to_search_for)
        for element in elements:
            results.append(element.get(value_to_search_for))
        return results


    def parse_all(self, path):
        # Get all xml to parse
        print("Parsing the following files:")
        for path, subdirs, files in os.walk(path):
            for name in files:
                file_path = os.path.join(path, name)
                if "xml" in file_path: 
                    print(file_path)
                    self.all_file_paths.append(file_path)


        # Parse all files
        for xml in self.all_file_paths:
            print("Now parsing: " + xml)
            try:
                 tree = ET.parse(xml)
            except:
                print("File could not be parsed: " + xml)
                self.all_file_paths.remove(xml)
  
            else:

                root = tree.getroot()
                curr_file = xml_file(xml)     
                
                for child in root:
                    # Store data
                    parsed_value = xml_data(child.tag)
                    parsed_value.data = child.attrib
                    curr_file.data.append(parsed_value)
                    
                curr_file.xml = tree
                self.parsed_files.append(curr_file)


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