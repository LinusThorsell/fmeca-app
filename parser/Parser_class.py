import xml.etree.ElementTree as ET
from os import path as OSPATH
import Encoder_Class
import DataClass
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
    def cpu(self,node,parentname):
        returnlist = []
        type = node.tag
        name = node.get("name")
        unitid = node.get("unitId")
        IOPRef = node.get("IOPRef")
        ACCSSyncMaster = node.get("ACCSSyncMaster")
        domainBorder = node.get("domainBorder")
        returnlist.append(DataClass.Cpu(name,parentname,type,unitid,IOPRef,ACCSSyncMaster,domainBorder))
        
        for children in node:
            print("\t\t" + children.tag)
            if children.tag in self.functions:
                returnlist += self.functions[children.tag](children)
                
        return returnlist

    
    
    #creates node of dcm type
    def dcm(self,node,project_id):
            returnlist = []
            type = "DCM"
            name = node.get('name')
            loadsetTypeRef =node.get("loadsetTypeRef")
            platformRef = node.get("platformRef")
            synclostBehavior =node.get("syncLostBehavior")
            redundant =node.get("redundant")
            returnlist.append(DataClass.NodeFC(project_id,type,name,loadsetTypeRef,redundant,platformRef,synclostBehavior))    
            for children in node:
                print("\t" + children.tag)
                if children.tag in self.functions:
                    if children.tag == "APP" or children.tag == "IOP":
                        returnlist += self.functions[children.tag](children,name)
                    else:
                        returnlist += self.functions[children.tag](children)
            return returnlist
        

    
    #retrieves all nodes(and cpus) from fc/hw_topology
    def get_fc_nodes(self,path,project_id):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for node in root:
            print(node.tag)
            if node.tag in self.functions:
                print("Node tag is in functions")
                if node.tag != "DCM":
                    returnlist += self.functions[node.tag](node)
                else:
                    returnlist += self.functions[node.tag](node,project_id)
        return returnlist        

    #retrieves all nodes(and cpus) from mc/hw_topology
    def get_mc_nodes(self,path,project_id):
        tree = ET.parse(path)
        root = tree.getroot()
        nodes = []
        for i in root.findall('PDCM'):
            name = i.get('name')
            loadsetTypeRef = i.get("loadsetTypeRef")
            platformRef = i.get("platformRef")
            nodes.append(DataClass.NodeMC(project_id,name,loadsetTypeRef,platformRef))
        return nodes
    

    def get_partitions(self,path):
        return []
    
    def initialisation(self):
        self.functions = {"DCM":self.dcm,"APP":self.cpu,"IOP":self.cpu}
    
