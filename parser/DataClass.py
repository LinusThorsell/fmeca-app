# Classes the we want to represent in database

class Project_Data_Class:
    def __init__(self,name):
        self.project_id = name
    def reprJSON(self):
        return {"project_id":self.project_id}


class Partition_Data_Class:
    def __init__(self,name,node):
        self.name = name
        self.node = node
    def reprJSON(self):
        return {"name":self.name}

class NodeFC:
    def __init__(self,name,loadsetTypeRef, redundant, platformRef, syncLostBehavior):
        self.name = name
        self.loadsetTypeRef = loadsetTypeRef
        self.redundant = redundant
        self.platformRef = platformRef
        self.syncLostBehavior =  syncLostBehavior
        self.Partitions = []


class NodeMC:
    def __init__(self,name,loadsetTypeRef,platformRef):
        self.name = name
        self.loadsetTypeRef = loadsetTypeRef
        self.platformRef = platformRef
        

#The lists should contain Objects of the Objects
class Project:
    def __init__(self,name):
        self.ProjectDataClass = Project_Data_Class(name)
        self.NodeFC = []
        self.NodeMC = []
        self.Partitions = []
        
    def add_NodeFC(self,NodeList):
        self.NodeFC += NodeList
        
    def add_NodeMC(self,NodeList):
        self.NodeMC += NodeList
            
    def add_Partitions(self,PartitionList):
        self.Partitions += PartitionList
        