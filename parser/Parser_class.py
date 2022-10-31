import xml.etree.ElementTree as ET
from os import path as OSPATH
import Encoder_Class
import DataClass
class Parser:
    def __init__(self):
        self.functions = {}

    
    def get_project_name(self,path):
        print(path)
        temp = path.split("/")
        name = temp[0]
        return name

    def cpu(self,node,parentname):
        type = ""
        returnlist = []
        name = node.get("name")
        unitid = node.get("unitId")
        IOPRef = ""
        ACCSSyncMaster = ""
        if node.tag == "APP":
            type = "APP"
            IOPRef = node.get("IOPRef")
        elif node.tag == "IOP":
            type = "IOP"
            ACCSSyncMaster = node.get("ACCSSyncMaster")
        returnlist.append(DataClass.Cpu(name,parentname,type,unitid,IOPRef,ACCSSyncMaster))
        
        for children in node:
            print("\t\t" + children.tag)
            if children.tag in self.functions:
                returnlist += self.functions[children.tag](children)
                
        return returnlist
    
    def dcm(self,node):
            returnlist = []
            type = "DCM"
            name = node.get('name')
            loadsetTypeRef =node.get("loadsetTypeRef")
            platformRef = node.get("platformRef")
            synclostBehavior =node.get("syncLostBehavior")
            redundant =node.get("redundant")
            returnlist.append(DataClass.NodeFC(type,name,loadsetTypeRef,redundant,platformRef,synclostBehavior))    
            for children in node:
                print("\t" + children.tag)
                if children.tag in self.functions:
                    if children.tag == "APP" or children.tag == "IOP":
                        returnlist += self.functions[children.tag](children,name)
                    else:
                        returnlist += self.functions[children.tag](children)
            return returnlist
    
    def get_fc_nodes(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for node in root:
            print(node.tag)
            if node.tag in self.functions:
                print("Node tag is in functions")
                returnlist += self.functions[node.tag](node)
        return returnlist        

    #return a list of nodes
    def get_mc_nodes(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        nodes = []
        for i in root.findall('PDCM'):
            name = i.get('name')
            loadsetTypeRef = i.get("loadsetTypeRef")
            platformRef = i.get("platformRef")
            nodes.append(DataClass.NodeMC(name,loadsetTypeRef,platformRef))
        return nodes
    
    def get_partitions(self,path):
        return []
    
    def initialisation(self):
        self.functions = {"DCM":self.dcm,"APP":self.cpu,"IOP":self.cpu}
    
'''    
    #return a list of nodes
    def get_fc_nodes(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for node in root.findall('DCM'):
            print(node)
            name = node.get('name')
            loadsetTypeRef =node.get("loadsetTypeRef")
            platformRef = node.get("platformRef")
            synclostBehavior =node.get("syncLostBehavior")
            redundant =node.get("redundant")
            returnlist.append(DataClass.NodeFC(name,loadsetTypeRef,redundant,platformRef,synclostBehavior))    
            for children in node:
                
                
        return returnlist
    '''    
'''
    #För noder
    def fc_hw_topology(self,path,partitions_dict):
        path = 'Project_1/infrastructure/fc/hw_topology.xml'
        tree = ET.parse(path)
        root = tree.getroot()
        nodes = []
        for i in root.findall('DCM'):
            name = i.get('name')
            #print(name)
            if name in partitions_dict:
                
                nodes.append(Node.Node_Data_Class(name,"",partitions_dict[name]))
            #else:
            #    nodes.append()
        return nodes
        
    #För noder
    def mc_hw_topology(self,path,partitions_dict):
        path = 'Project_1/infrastructure/mc/hw_topology.xml'
        tree = ET.parse(path)
        root = tree.getroot()
        nodes = []
        for i in root.findall('PDCM'):
            name = i.get('name')
            #print(n
            if name in partitions_dict:        
                nodes.append(Node.Node_Data_Class(name,"",partitions_dict[name]))
            else: 
                print("HEJ")
        return nodes
    
    def get_fc_mc_hw(self,fc_hw_path,mc_hw_path,partitions):
        node_set = []
        node_set += self.fc_hw_topology(fc_hw_path,partitions)
        node_set += self.mc_hw_topology(mc_hw_path,partitions)
        
        return node_set
        #encoder.send_to_database(encoder.nodes,"nodes/")
        
    #Partitioner
    def fc_sw_topology(self,path,partition_dict):
        path = 'Project_1/infrastructure/fc/sw_topology.xml'
        tree = ET.parse(path)
        root = tree.getroot()
        ##Dictionary innehåller nodenamn och partition
        for i in root.findall('APP'):
            referenced_node = i.get("ref")
            templist = referenced_node.split(".")
            
            referenced_node = templist[0]        
            for partitions in i.findall("Partition"):
                name = partitions.get("name")
                Partition = Partitions.Partition_Data_Class(name,referenced_node)
                if referenced_node in partition_dict:
                    partition_dict[referenced_node].append(Partition)
                else:
                    partition_dict[referenced_node] = [Partition]
        #rget_fc_nodes('Project_1/infrastructure/fc/hw_topology.xml')eturn partitions #,dict

    #Partitioner
    def mc_sw_topology(self,path,partition_dict):

        partition_dict["TMC_PDCM1"] =  [Partitions.Partition_Data_Class("Dummy","TMC_PDCM1")]
        #return partition
    
    #Partitioner
    def get_fc_mc_sw(self,fc_sw_path,mc_sw_path,project):
        partition_dict = {}
        self.fc_sw_topology(fc_sw_path,partition_dict)
        self.mc_sw_topology(mc_sw_path,partition_dict)
        #partition_set += self.fc_sw_topology(fc_sw_path)
        #partition_set += self.mc_sw_topology(mc_sw_path)

        return partition_dict
    
    
    '''