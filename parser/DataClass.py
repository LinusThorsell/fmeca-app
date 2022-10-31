# Classes the we want to represent in database

class Project_Data_Class:
    def __init__(self,name):
        self.project_id = name
    def reprJSON(self):
        return {"project_id":self.project_id}


class Partition_Data_Class:
    def __init__(self,name,node):
        self.name = name
        self.node = node    #parent node
    def reprJSON(self):
        return {"name":self.name}

class Node:
    def __init__(self,type,name,load_set_type, redundant, platform, sync_loss):
        self.type = type
        self.name = name
        self.load_set_type = load_set_type
        self.redundant = redundant
        self.platform = platform
        self.sync_loss =  sync_loss
        self.type = type
    
    

class NodeFC:
    def __init__(self,type,name,loadsetTypeRef, redundant, platformRef, syncLostBehavior):
        self.type = type
        self.name = name
        self.loadsetTypeRef = loadsetTypeRef
        self.redundant = redundant
        self.platformRef = platformRef
        self.syncLostBehavior =  syncLostBehavior
    def reprJSON(self):
        return {"name":self.name,"loadsetTypeRef":self.loadsetTypeRef,"redundant":self.redundant,"platformRef":self.platformRef,"syncLostBehavior":self.syncLostBehavior}


class NodeMC:
    def __init__(self,name,loadsetTypeRef,platformRef):
        self.name = name
        self.loadsetTypeRef = loadsetTypeRef
        self.platformRef = platformRef
    def reprJSON(self):
        return {"name":self.name,"loadsetTypeRef":self.loadsetTypeRef,"platformRef":self.platformRef}

class Application:
    def __init__(self,name, id, connectionProvider, connectionRequirer, connectionId):
        self.name = name
        self.loadsetTypeRef = id
        self.connectionProvider = connectionProvider
        self.connectionRequirer = connectionRequirer
        self.connectionId = connectionId
        
class Cpu:
    def __init__(self,name,node,type, unitid, IOPRef, ACCSSyncMaster):
        self.name = name
        self.node = node    #node of origin/parent node
        self.type = type    #"APP" or "IOP"
        self.unitid = unitid
        self.IOPRef = IOPRef
        self.ACCSSyncMaster = ACCSSyncMaster
    def reprJSON(self):
        return {"name":self.name,"node":self.node,"type":self.type,"unitid":self.unitid,"IOPRef":self.IOPRef,"ACCSSyncMaster":self.ACCSSyncMaster}



#The lists should contain Objects of the Objects
class Project:
    def __init__(self,name):
        self.ProjectDataClass = Project_Data_Class(name)
        self.Cpu = []
        self.NodeFC = []
        self.NodeMC = []
        self.Partitions = []

        
    def filter(self,objectlist):
        
        for object in objectlist:
            if isinstance(object,Cpu):
                self.Cpu.append(object)
            elif isinstance(object, NodeFC):
                self.NodeFC.append(object)
            elif isinstance(object, NodeMC):
                self.NodeMC.append(object)
            elif isinstance(object, Partitions):
                self.Partitions.append(object)
