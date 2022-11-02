# Classes the we want to represent in database


class Node:
    def __init__(self,type,name,loadsetTypeRef, redundant, platformRef, syncLostBehavior):
        self.type = type
        self.name = name
        self.loadsetTypeRef = loadsetTypeRef
        self.redundant = redundant
        self.platformRef = platformRef
        self.syncLostBehavior =  syncLostBehavior
        self.cpus = []
    def reprJSON(self):
        return {"name":self.name,"loadsetTypeRef":self.loadsetTypeRef,"redundant":self.redundant,
                "platformRef":self.platformRef,"syncLostBehavior":self.syncLostBehavior,"cpu_set":self.cpus}

class Cpu:
    def __init__(self,name,type, unitid, IOPRef, ACCSSyncMaster,domainBorder):
        self.name = name    #node of origin/parent node
        self.type = type    #"APP" or "IOP"
        self.unitid = unitid
        self.IOPRef = IOPRef
        self.ACCSSyncMaster = ACCSSyncMaster
        self.domainBorder = domainBorder
        self.applications = []
        self.partitions = []
    def reprJSON(self):
        return {"name":self.name,"type":self.type,"unitid":self.unitid,"IOPRef":self.IOPRef,
        "ACCSSyncMaster":self.ACCSSyncMaster,"domainBorder":self.domainBorder,"partition_set":self.partitions,"application_set":self.applications}


class Partition_Data_Class:
    def __init__(self,name,ltmbool,id, node,cpu):
        self.name = name
        self.isLTM = ltmbool
        #Denna va med i project 1... lol?
        #self.fixedStartNs = start
        self.partiton_id = id
        self.nodename = node
        self.cpuname = cpu
        self.applications = []
    def reprJSON(self):
        return {"name":self.name,"isLTM":self.isLTM,"id":self.partiton_id,"application_set":self.applications}

class Application:
    #<DipsApplication name="Port_Gateway_1" rampool="0x10000" instanceOf="port_gateway" affinity="0"/>
    def __init__(self,name, rampool, instanceOf, affinity,node,cpu,partition):
        self.name = name
        self.rampool = rampool
        self.instanceOf = instanceOf
        self.affinity = affinity
        self.nodename = node
        self.cpuname = cpu
        self.partitionname = partition
        # self.loadsetTypeRef = id
        # self.connectionProvider = connectionProvider
        # self.connectionRequirer = connectionRequirer
        # self.connectionId = connectionId
    def reprJSON(self):
        return {"name":self.name} #,"rampool":self.rampool,"instanceOf":self.instanceOf,"affinity":self.affinity}

#The lists should contain Objects of the Objects

class Project_Data_Class:
    def __init__(self,name):
        self.project_id = name
        self.node_set = []
    def reprJSON(self):
        return {"project_id":self.project_id,"node_set":self.node_set}
         
    def insert_partitions(self,partitionlist):
        for partition in partitionlist:
            for node in self.node_set:
                if partition.nodename == node.name:
                    for cpu in node.cpus:
                        if partition.cpuname == cpu.name:
                            cpu.partitions.append(partition)   
    
    def insert_applications(self,applicationlist):
        
        for application in applicationlist:
            print(1)
            for node in self.node_set:
                print(2)
                print("application.nodename =" + application.nodename + "== node.name" + node.name)
                if application.nodename == node.name:
                    for cpu in node.cpus:
                        print(3)
                        if application.cpuname == cpu.name:
                            print("Partitionsnamn == " ,application.partitionname)
                            if(application.partitionname == None):
                                cpu.applications.append(application)
                            #cpu.partitions.append(partition)  
    
    def filter(self,objectlist):
        
        for objecttype in objectlist:
            #if isinstance(object,Cpu):
            #    self.Cpu.append(object)
            if isinstance(objecttype, Node):
                self.node_set.append(objecttype)
            #elif isinstance(object, Partitions):
            #    self.Partitions.append(object)