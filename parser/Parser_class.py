import xml.etree.ElementTree as ET
from os import path as OSPATH
import Encoder_Class
import DataClassNest
class Parser:
    def __init__(self):
        self.functions = {}

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
                print("Creating partition ")
                partitions.append(self.create_partition(child, node, cpu))
        return partitions 
    
    def create_applications_in_cpu(self,raw_partition_data):
        applications = []
        ref = raw_partition_data.get("ref")
        node, cpu = ref.split('.')
        print("node")
        for child in raw_partition_data:
            if child.tag == "Application":
                print("Creating application ")
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
            else:
                type = "mc"

            node = DataClassNest.Node(type,name,loadsetTypeRef,redundant,platformRef,syncLostBehavior)
        
            for cpu in raw_node_data:
                print("\t" + cpu.tag)
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
            print(node.tag)
            if node.tag in self.functions:
                print("Node tag is in functions")
                if(node.tag == "DCM" or node.tag == "PDCM"):
                    returnlist.append(self.functions[node.tag](node))
        print(returnlist)
        return returnlist        

    #retrieve all partions and add to list
    def get_partitions(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for partitions in root:
            print(partitions.tag)
            if partitions.tag in self.functions:
                print("Node tag is in functions")
                if (partitions.tag == "APP" or partitions == "IOP"):
                    #returnlist.append(self.functions[node.tag](partitions))
                    returnlist += self.create_partitions_in_cpu(partitions)
        return returnlist
    
    def get_cpu_applications(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for cpu in root:
            print(cpu.tag)
            if cpu.tag in self.functions:
                print("Node tag is in functions")
                if (cpu.tag == "PP"):
                    #returnlist.append(self.functions[node.tag](partitions))
                    returnlist += self.create_applications_in_cpu(cpu)
        return returnlist
    
    def initialisation(self):
        self.functions = {"PP":self.cpu,"PDCM":self.create_node,"DCM":self.create_node,"APP":self.cpu,"IOP":self.cpu,"Application":self.create_application}
    