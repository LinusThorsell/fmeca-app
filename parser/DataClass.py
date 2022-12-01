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
        self.partition_set = []
    def reprJSON(self):
        return {"name":self.name,"type":self.type,"unit_id":self.unitid,"iop_ref":self.IOPRef,
        "accs_sync_master":self.ACCSSyncMaster,"domain_border":self.domainBorder,"partition_set":self.partition_set}


class Partition_Data_Class:
    def __init__(self,name,ltmbool,id, node,cpu):
        self.name = name
        self.isLTM = ltmbool
        self.fixedStartNs = None
        self.partiton_id = id
        self.nodename = node
        self.cpuname = cpu  
    
    
    def reprJSON(self):
        return {"name":self.name,"is_ltm":self.isLTM,"partition_id":self.partiton_id,"fixed_start":self.fixedStartNs}

class Application_Instance:
    def __init__(self,name, application):
        # Retrieved when parsing application_instances.xml for either mc or fc
    
        self.name = name
        self.instanceOfApplication = application
        # Below attributes are known after parsing sw_topology.xml
        self.rampool = None
        self.instanceOf =  None
        self.affinity = None
        self.nodename = None
        self.cpuname = None
        self.partitionname = None
    
    def __eq__(self, other):
        if(isinstance(other, str)):
            return self.name == other 
        elif(isinstance(other, Application_Instance)):
            return self.name == other.name
        else:
            return False

    def reprJSON(self):
        return {"name":self.name, "instance_of_application":self.instanceOfApplication,"rampool":self.rampool,"instance_of":self.instanceOf,"affinity":self.affinity,
        "node_name":self.nodename, "cpu_name":self.cpuname,"partition_name":self.partitionname}

class Application:
    def __init__(self,name, automatedTestLevel = None):
        self.name = name
        self.automatedTestLevel = automatedTestLevel
    def __eq__(self, other):
        return self.name == other.name 
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return self.name
    def reprJSON(self):
        return {"name":self.name, "automated_test_level":self.automatedTestLevel}
    # Application also have thread but those are sent separately to the database  
class Threads:
    def __init__(self,name,application, rategroup):
        self.name = name
        self.application = application
        self.rategroup = rategroup
        self.port_set = []
    def reprJSON(self):
        return {"name":self.name,"application":self.application, "rategroup":self.rategroup,"port_set":self.port_set}

class DomainBorder:
    def __init__(self, name):
        self.name = name 
        self.port_set = []
    def reprJSON(self):
        return {"name":self.name,"port_set":self.port_set}
    
class PacPorts:
    def __init__(self,name, interface, role, provider = None):
        self.name = name
        self.interface = interface
        self.role = role
        self.provider = provider
    def reprJSON(self):
        return {"name":self.name,"interface":self.interface,"role":self.role, "provider":self.provider}

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
class Project_Data_Class:
    def __init__(self,name):
        self.name = name
        self.application_set =  []
        self.application_instance_set = []
        self.node_set = []
        self.thread_set = []
        self.domain_border_set = []
        self.connection_set = []
    def reprJSON(self):
        return {"name":self.name,"application_set": self.application_set,"application_instance_set":self.application_instance_set,"node_set":self.node_set,
                "thread_set":self.thread_set,"domain_border_set":self.domain_border_set,"connection_set":self.connection_set}
         
    def insert_partitions(self,partition_set):
        for partition in partition_set:
            for node in self.node_set:
                if partition.nodename == node.name:
                    for cpu in node.cpus:
                        if partition.cpuname == cpu.name:
                            cpu.partition_set.append(partition)   
    
    def insert_applications(self,application_set):
        for application in application_set:
            for node in self.node_set:
                if application.nodename == node.name:
                    for cpu in node.cpus:
                        if application.cpuname == cpu.name:
                            if(application.partitionname == None):
                                cpu.application_set.append(application)
                                self.Applications.append(application)
    
    def filter(self,objectlist):
        for objecttype in objectlist:
            #if isinstance(object,Cpu):
            #    self.Cpu.append(object)
            if isinstance(objecttype, Node):
                self.node_set.append(objecttype)
            #elif isinstance(object, Partitions):
            #    self.Partitions.append(object)