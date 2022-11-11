import xml.etree.ElementTree as ET
from os import path as OSPATH
<<<<<<< HEAD
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
        self._headers = {"Content-Type": "application/json"}
        self._url = 'http://127.0.0.1:8000/'

    def send_project_name(self, path):
        temp = path.split("/")
        name = temp[0]

        x = {"project_id": "PROJEKT3"}
        y = {"project_id": "PROJEKT4"}
        lista = [x, y]
        string = json.dumps(x)
        # string = json.dumps(lista)


        # payload = {
        #         'project_id': 'Test20',
        #         'node_set': [
        #             {
        #                 "name": "FMC-0",
        #                 "partition_set": [
        #                     {
        #                         "name": "LTM-FMC"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "name": "FMC-1",
        #                 "partition_set": []
        #             },
        #             {
        #                 "name": "FMC-2",
        #                 "partition_set": []
        #             }
        #         ]
        # }

        payload = {
            'name': 'FMC',
            'platform': 'test',
            "load_set_type": 'test',
            'project': 'dummy-proj',
        }

        # payload = {
        #     "name": "FMC-0",
        #     "project": "test-project3",
        #     "partition_set": [
        #         {
        #         "name": "LTM-FMC",
        #         }
        #     ],
        # }

        print("Postar detta:", self._headers, string)
        requests.post(self._url + "projects/", json=payload,
                      headers = self._headers)

    def fc_hw_topology(self, path):
        # path = 'Project_1/infrastructure/fc/hw_topology.xml'
        tree=ET.parse(path)
        root=tree.getroot()
        for i in root.findall('DCM'):
            name=i.get('name')
            print(name)
            # add to database?

    def mc_hw_topology(self, path):
        tree=ET.parse(path)
        root=tree.getroot()
        for i in root.findall('DCM'):
            name=i.get('name')
            print(name)
            # add to database?

    def fc_sw_topology(self, path):
        # path = 'Project_1/infrastructure/fc/sw_topology.xml'
        tree=ET.parse(path)
        root=tree.getroot()
        for i in root.findall('APP'):
            name=i.get('ref')
            print(name)
            # add to database?
            # x = {""}

    def mc_sw_topology(self, path):
        # path = 'Project_1/infrastructure/fc/sw_topology.xml'
        tree=ET.parse(path)
        root=tree.getroot()
        for i in root.findall('APP'):
            name=i.get('ref')
            print(name)
            # add to database?
            # x = {""}

    def build_path(self, index):

        # print("The catalog")
        # print(self.catalogs[c])
        path=""
        dictionary=self.catalogs[index][1]

        # print("The content of the lists dictionary:")
        # print(self.catalogs[index][1])

        if "value" in dictionary:
            path=dictionary["value"]
        elif "dir" in dictionary:
            path=dictionary["dir"]
        elif "src" in dictionary:
            path=dictionary["src"]
        elif "conf" in dictionary:
            path=dictionary["conf"]
        else:
            return "nopath"

        if "[acs_src]" in path:
            path="nopath"
        else:
            while "[" and "]" in path:
                if(path.count("[") == 1 and "[root]" in path):
                    break
                for temp in self._dictionary:
                    if ("[" + temp + "]") in path:
                        path=path.replace(
                            "[" + temp + "]", self._dictionary[temp])
        dictionary["path"]=path

    def parsefunction(self, index):
        # print("PATH:")
        # print(self.catalogs[index][1])
        # print(self.catalogs[index][1]["path"])
        temppath=self.catalogs[index][1]["path"]
        if temppath == "nopath":
            return
        templist=temppath.split("/")

        newpath=""
        counter=3
        if len(templist) >= 3:
            while counter < len(templist):

                newpath += templist[counter]
                if counter+1 != len(templist):
                    newpath += "/"
                counter += 1
        else:
            return

        print(newpath)
        if os.path.exists(newpath):
            if ".xml" in newpath:
                print(ET.tostring(ET.parse(newpath).getroot(),
                      encoding="ISO-8859-1").decode('utf8'))
                tree=ET.parse(newpath)
                root=tree.getroot()
                curr_file=xml_file(newpath)

                for child in root:
                    # Store data
                    parsed_value=xml_data(child.tag)
                    parsed_value.data=child.attrib
                    curr_file.data.append(parsed_value)

                curr_file.xml=tree
                self.parsed_files.append(curr_file)
            elif os.path.isdir(newpath):
                print("Kollar igenom directories")
                for filename in os.scandir(newpath):
                    if filename.is_file():
                        # print("LALALALAL")
                        # print(filename.path)
                        print(ET.tostring(ET.parse(filename.path).getroot(),
                              encoding="ISO-8859-1").decode('utf8'))

    def initial_path(self, path):
        self.fc_path=path + "/fc/system.xml"
        self.mc_path=path + "/mc/system.xml"

    def parse_all(self, path):
        # Get all xml to parse
        print("Parsing the following files:")
        for path, subdirs, files in os.walk(path):
            for name in files:
                file_path=os.path.join(path, name)
                if "xml" in file_path:
                    print(file_path)
                    self.all_file_paths.append(file_path)

        # Parse all files
        for xml in self.all_file_paths:
            print("Now parsing: " + xml)
            try:
                tree=ET.parse(xml)
            except:
                print("File could not be parsed: " + xml)
                self.all_file_paths.remove(xml)

=======
import Encoder_Class
import DataClassNest
class Parser:
    def __init__(self):
        self.functions = {}
        self.debug = False


    def debug_print(self, string_to_print):
        if(self.debug):
            print(string_to_print)
            
    #retrieves the project name from the path
    def get_project_name(self,path):
        print(path)
        temp = path.split("/")
        name = temp[0]
        return name

    #creates a cpu datatype
    def cpu(self,raw_cpu_data):
    
        type = raw_cpu_data.tag
        name = raw_cpu_data.get("name")
        unitid = raw_cpu_data.get("unitId")
        IOPRef = raw_cpu_data.get("IOPRef")
        ACCSSyncMaster = raw_cpu_data.get("ACCSSyncMaster")
        domainBorder = raw_cpu_data.get("domainBorder")
        
        # for children in raw_cpu_data:
        #     print("\t\t" + children.tag)
        #     if children.tag in self.functions:
        #         returnlist += self.functions[children.tag](children)
                
        return DataClassNest.Cpu(name,type,unitid,IOPRef,ACCSSyncMaster,domainBorder)

    def create_partition(self,raw_partition_data,node,cpu):
        name = raw_partition_data.get("name")
        isLTM = raw_partition_data.get("isLTM")
        partition_id = raw_partition_data.get("id")
        
        Partition = DataClassNest.Partition_Data_Class(name, isLTM, partition_id, node,cpu)
        
        for children in raw_partition_data:
            if children.tag in self.functions:
                #typ onödig men whatever
                if children.tag == "Application":
                    Partition.applications.append(self.functions[children.tag](children,node,cpu,name))        
        return  Partition


    def create_application(self, raw_application_data,node, cpu, partition):
        
        #<DipsApplication name="Port_Gateway_1" rampool="0x10000" instanceOf="port_gateway" affinity="0"/>
        name = raw_application_data.get("name")
        rampool = raw_application_data.get("rampool")
        instanceOf = raw_application_data.get("instanceOf")
        affinity = raw_application_data.get("affinity")

        return DataClassNest.Application(name, rampool, instanceOf, affinity, node, cpu, partition)

    def create_partitions_in_cpu(self,raw_partition_data):
        partitions = []
        ref = raw_partition_data.get("ref")
        node, cpu = ref.split('.')
        for child in raw_partition_data:
            if child.tag == "Partition":
                partitions.append(self.create_partition(child, node, cpu))
        return partitions 
    
    def create_applications_in_cpu(self,raw_partition_data):
        applications = []
        ref = raw_partition_data.get("ref")
        node, cpu = ref.split('.')
        for child in raw_partition_data:
            if child.tag == "Application":
                applications.append(self.create_application(child, node, cpu, None))
        return applications 

    

    #create a single node, handle cpus related to node
    def create_node(self,raw_node_data):
            name = raw_node_data.get('name')
            loadsetTypeRef = raw_node_data.get("loadsetTypeRef")
            platformRef = raw_node_data.get("platformRef")
            syncLostBehavior = raw_node_data.get("syncLostBehavior")
            redundant = raw_node_data.get("redundant")
            type = ""
            if(raw_node_data.tag == "DCM"):
                type = "fc"
>>>>>>> 3bdf4ac69a7ef2ea33d6159968c1994bd1403b48
            else:
                type = "mc"

<<<<<<< HEAD
                root=tree.getroot()
                curr_file=xml_file(xml)

                for child in root:
                    # Store data
                    parsed_value=xml_data(child.tag)
                    parsed_value.data=child.attrib
                    curr_file.data.append(parsed_value)

                curr_file.xml=tree
                self.parsed_files.append(curr_file)

    def parse(self, path):
        # print("path = " + path)
        tree=ET.parse(path)
        root=tree.getroot()
        # parsed_data = []

        self.catalogs=[]
        for obj in root:
            #    print(obj.tag, obj.attrib)
            if(obj.tag == "idb" and ".xml" not in obj.attrib["value"]):
                self._dictionary[obj.attrib["key"]]=obj.attrib["value"]
            else:
                tuple=(obj.tag, obj.attrib)
                self.catalogs.append(tuple)
        # print("\n\n\n")

        # print("Content of self._dicitonary: ")
        # print(self._dictionary)
        # print("\n\n\n")
        # print("Content of catalogs: ")
        # print(self.catalogs)

        counter=0
        while counter < len(self.catalogs):
            self.build_path(counter)
            self.parsefunction(counter)
            counter += 1

        # print("KATALOGEN")
        # print(self.catalogs)
=======
            node = DataClassNest.Node(type,name,loadsetTypeRef,redundant,platformRef,syncLostBehavior)
        
            for cpu in raw_node_data:
                if cpu.tag in self.functions:
                    if cpu.tag == "APP" or cpu.tag == "IOP" or cpu.tag == "PP":
                        node.cpus.append(self.functions[cpu.tag](cpu)) 
            return node
            
            
    #retrieves all nodes(and cpus) from fc/hw_topology
    def get_nodes(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for node in root:
            if node.tag in self.functions:
                if(node.tag == "DCM" or node.tag == "PDCM"):
                    returnlist.append(self.functions[node.tag](node))
        return returnlist        

    #retrieve all partions and add to list
    def get_partitions(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for partitions in root:
            print(partitions.tag)
            if partitions.tag in self.functions:
                if (partitions.tag == "APP" or partitions == "IOP"):
                    #returnlist.append(self.functions[node.tag](partitions))
                    returnlist += self.create_partitions_in_cpu(partitions)
        return returnlist
    
    def get_cpu_applications(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for cpu in root:
            if cpu.tag in self.functions:
                if (cpu.tag == "PP"):
                    #returnlist.append(self.functions[node.tag](partitions))
                    returnlist += self.create_applications_in_cpu(cpu)
        return returnlist
    
    def initialisation(self):
        self.functions = {"PP":self.cpu,"PDCM":self.create_node,"DCM":self.create_node,"APP":self.cpu,"IOP":self.cpu,"Application":self.create_application}
    
    
>>>>>>> 3bdf4ac69a7ef2ea33d6159968c1994bd1403b48
