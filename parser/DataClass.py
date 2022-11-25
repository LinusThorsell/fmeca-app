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
        return {"name":self.name,"load_set_type":self.loadsetTypeRef,"redundant":self.redundant,
                "platform":self.platformRef,"sync_loss":self.syncLostBehavior,"cpu_set":self.cpus}

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
        return {"name":self.name,"type":self.type,"unit_id":self.unitid,"iop_ref":self.IOPRef,
        "accs_sync_master":self.ACCSSyncMaster,"domain_border":self.domainBorder,"partition_set":self.partitions,"application_set":self.applications}


class Partition_Data_Class:
    def __init__(self,name,ltmbool,id, node,cpu):
        self.name = name
        self.isLTM = ltmbool
        self.fixedStartNs = None
        self.partiton_id = id
        self.nodename = node
        self.cpuname = cpu
        self.applications = []
    def reprJSON(self):
        return {"name":self.name,"is_ltm":self.isLTM,"partition_id":self.partiton_id,
                "application_set":self.applications,"fixed_start":self.fixedStartNs}

class Application:
    def __init__(self,name, rampool, instanceOf, affinity,node,cpu,partition):
        self.name = name
        self.rampool = rampool
        self.instanceOf = instanceOf
        self.affinity = affinity
        self.nodename = node
        self.cpuname = cpu
        self.partitionname = partition

    def reprJSON(self):
        return {"name":self.name,"cpu":None} #,"rampool":self.rampool,"instanceOf":self.instanceOf,"affinity":self.affinity}

class Application_Instances:
    def __init__(self,name, instanceOf):
        self.name = name
        self.instanceOf = instanceOf
    
    def reprJSON(self):
        return {"name":self.name,"instanceof":self.instanceOf}
    
class ApplicationContainer:
    def __init__(self,project):
        self.applicationlist = []
        self.project_name = project
    def add_project_name(self,name):
        self.project_name = name
    def reprJSON(self):
        return {"project_name":self.project_name,"applicationlist":self.applicationlist}

class ThreadContainer:
    def __init__(self,project):
        self.project = project
        self.thread_set = []
    def reprJSON(self):
        return {"project_name":self.project,"thread_set":self.thread_set}
class Threads:
    def __init__(self,name,application, rategroup):
        self.name = name
        self.application = application
        self.rategroup = rategroup
        self.port_list = []
    def reprJSON(self):
        return {"name":self.name,"application":self.application, "rategroup":self.rategroup,"port_list":self.port_list}

class DomainBorder:
    def __init__(self, name):
        self.name = name
        self.port_list = []


class PacPorts:
    def __init__(self,name, interface, role):
        self.name = name
        self.interface = interface
        self.role = role
    def reprJSON(self):
        return {"name":self.name,"interface":self.interface,"role":self.role}

class Connection:
    
    def __init__(self, Provider_owner, Provider_thread, Provider_port,provider_is_domainborder,
        Requirer_owner, Requirer_thread, Requirer_port,requirer_is_domainborder, identity):
        self.Provider_owner = Provider_owner
        self.Provider_thread = Provider_thread
        self.Provider_port = Provider_port
        self.Provider_is_domainborder = provider_is_domainborder

        self.Requirer_is_domainborder = requirer_is_domainborder
        self.Requirer_owner = Requirer_owner
        self.Requirer_thread =  Requirer_thread
        self.Requirer_port = Requirer_port
        self.identity = identity
        
    def reprJSON(self):
        return {"provider_owner":self.Provider_owner,"provider_thread":self.Provider_thread,
                "provider_port":self.Provider_port,"provider_is_domainborder":self.Provider_is_domainborder,
                "requirer_owner":self.Requirer_owner,"requirer_thread":self.Requirer_thread,
                "requirer_port":self.Requirer_port,"requirer_is_domainborder":self.Requirer_is_domainborder,
                "identity":self.identity} 

class ConnectionContainer:
    def __init__(self,projectname):
        self.project_name = projectname
        self.connectionlist = []
    
    def reprJSON(self):
        return {"project_name":self.project_name,"connectionlist":self.connectionlist}

class Project_Data_Class:
    def __init__(self,name):
        self.name = name
        self.node_set = []
        self.Applications = []
    def reprJSON(self):
        return {"name":self.name,"node_set":self.node_set}
         
    def insert_partitions(self,partitionlist):
        for partition in partitionlist:
            for node in self.node_set:
                if partition.nodename == node.name:
                    for cpu in node.cpus:
                        if partition.cpuname == cpu.name:
                            cpu.partitions.append(partition)   
    
    def insert_applications(self,applicationlist):
        for application in applicationlist:
            for node in self.node_set:
                if application.nodename == node.name:
                    for cpu in node.cpus:
                        if application.cpuname == cpu.name:
                            if(application.partitionname == None):
                                cpu.applications.append(application)
                                self.Applications.append(application)
    
    def filter(self,objectlist):
        
        for objecttype in objectlist:
            #if isinstance(object,Cpu):
            #    self.Cpu.append(object)
            if isinstance(objecttype, Node):
                self.node_set.append(objecttype)
            #elif isinstance(object, Partitions):
            #    self.Partitions.append(object)