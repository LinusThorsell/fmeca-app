import xml.etree.ElementTree as ET
from os import path as OSPATH
import os
import DataClass

import DebugFile
class Parser:
    def __init__(self):
        self.functions = {}
            
    #Retrieves the project name from the path
    def get_project_name(self,path):
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
        return DataClass.Cpu(name,type,unitid,IOPRef,ACCSSyncMaster,domainBorder)

    def add_info_where_applicaion_instance_is_running(self,Project,children,node,cpu,parititon):
        for instance in Project.application_instance_set:
            if(instance.name == children.get("name")):
                instance.rampool = children.get("rampool")
                instance.instanceOf = children.get("instanceOf")
                instance.affinity = children.get("affinity")
                instance.cpuname = cpu
                instance.nodename = node
                instance.partitionname = parititon
                return
        DebugFile.error_print("Error: Application {0} was schuled but is not defined ".format( children.get("name")))
                
                
    def create_application(self,Project ,raw_application_data,node, cpu, partition):
        name = raw_application_data.get("name")
        rampool = raw_application_data.get("rampool")
        instanceOf = raw_application_data.get("instanceOf")
        affinity = raw_application_data.get("affinity")
        application = DataClass.Application(name, rampool, instanceOf, affinity, node, cpu, partition)
        return application

    def create_partitions_in_cpu(self,Project,raw_partition_data):
        partitions = []
        ref = raw_partition_data.get("ref")
        node, cpu = ref.split('.')
        for child in raw_partition_data:
            if child.tag == "Partition":
                partitions.append(self.create_partition(Project,child, node, cpu))
        return partitions 
    
    def create_applications_in_cpu(self,project,raw_partition_data):
        applications = []
        ref = raw_partition_data.get("ref")
        node, cpu = ref.split('.')
        for child in raw_partition_data:
            if child.tag == "Application":
                self.add_info_where_applicaion_instance_is_running(project,child, node, cpu, None)
        return applications 

    def create_partition(self,Project,raw_partition_data,node,cpu):
        name = raw_partition_data.get("name")
        isLTM = raw_partition_data.get("isLTM")
        partition_id = raw_partition_data.get("id")
        
        Partition = DataClass.Partition_Data_Class(name, isLTM, partition_id, node,cpu)
        
        for children in raw_partition_data:
            if children.tag in self.functions:
                #typ onödig men whatever
                if children.tag == "Application":
                    #
                    self.add_info_where_applicaion_instance_is_running(Project,children,node,cpu,name)
                    #Partition.application_set.append(self.functions[children.tag](Project,children,node,cpu,name))        
        return  Partition

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

            node = DataClass.Node(type,name,loadsetTypeRef,redundant,platformRef,syncLostBehavior)
        
            for cpu in raw_node_data:
                if cpu.tag in self.functions:
                    if cpu.tag == "APP" or cpu.tag == "IOP" or cpu.tag == "PP":
                        node.cpus.append(self.functions[cpu.tag](cpu)) 
            return node
    
    def create_connection(self, raw_connection_data):
        temp_list = []

        for child in raw_connection_data:
            if(child.tag == "ProviderPort"):
                providerport_list = child.get('name').split(".")
                temp_list += providerport_list
                if(len(providerport_list) == 3):
                    temp_list.append(False) ## Is not domainborder
                elif(len(providerport_list) == 2):
                    temp_list.insert(1,None) # Thread parmeter is not valid
                    temp_list.append(True) ## Is domainborder
                
            elif(child.tag == "RequirerPort"):
                requirerport_list = child.get('name').split(".")
                temp_list += requirerport_list
                if(len(requirerport_list) == 3):
                    temp_list.append(False)
                elif(len(requirerport_list) == 2):
                    temp_list.insert(5,None) # Thread parmeter is not valid
                    temp_list.append(True) # Is domainborder
                
                temp_list.append(child.get('identity'))
                
        #DebugFile.debug_print(temp_list, DebugFile.OKCYAN)

        return DataClass.Connection(*temp_list)

    def get_domainborders(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        domain_borders = []
        if("domainborder" in root.tag.lower()):
            domain_borders.append(DataClass.DomainBorder(root.get("name")))
        return domain_borders


    def get_domain_border_ports(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        port_dict = {}
        for child in root:
            if(child.tag == "PacPort"):
                port = DataClass.PacPorts(child.get("name"), child.get("interface"),child.get("role"),child.get("provider"))
                if child.get("domainBorder") in port_dict:
                    port_dict[child.get("domainBorder")].append(port)
                else:
                    port_dict[child.get("domainBorder")] = [port]
                     
        return port_dict


    def get_all_domains(self, path, container):
        domainborders = []
        pacports = {} ## "key":lista
        if os.path.exists(path):
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    #print("File in files {0}".format(file))
                    #print("Subdir {0}".format(subdir))
                    if(subdir == (path + "/border")):
                        #print("Subidr= {0}".format(subdir))
                        #DebugFile.debug_print(subdir + "/"+file)
                        domainborders += self.get_domainborders(os.path.join(subdir,file))
                    elif (subdir == (path + "/config")):
                        tempdict = self.get_domain_border_ports(os.path.join(subdir,file))
                        for key,value in tempdict.items():
                            if key in pacports:
                                pacports[key] += value
                            else:
                                pacports[key] = value
                    elif (subdir == (path + "/continous_contracts")):
                        pass
                        #pacports += self._parser.get_domain_border_ports(os.path.join(subdir,file))
                    elif (subdir == (path + "/event_contracts")):
                        pass
                        #pacports += self._parser.get_domain_border_ports(os.path.join(subdir,file))
                    else:
                        pass
                        #DebugFile.debug_print("Unhandled directories under domain_border",DebugFile.WARNING)

            #{"Domain_border":PacPort, ...}
            container += domainborders
            ##Put the ports in domaiborders
            #for key,value in tempdict.items():
            for Domainborder in container:
                if Domainborder.name in pacports:
                    Domainborder.port_set += pacports[Domainborder.name]



    def create_application_instance(self, raw_application_instance_data):
        name = raw_application_instance_data.get('name')
        instanceOf = raw_application_instance_data.get("instanceOf")
        return DataClass.Application_Instance(name, instanceOf)

    def get_connection_list(self, path):
        connectionlist = []
        if os.path.exists(path+"/connections"):
            for subdir, dirs, files in os.walk(path+"/connections"):
                for file in files:
                    if(file == "connections.xml"):
                        #DebugFile.debug_print(subdir + "/"+file)
                        connectionlist += self.get_connections(os.path.join(subdir,file))
        return connectionlist
    
    def get_threads(self, path):
        threads = []
        for subdir, dirs, files in os.walk(path):
            for file in files:
                #DebugFile.debug_print(file)
                if(file == "application.xml"):
                    #DebugFile.debug_print(subdir + "/"+file)
                    threads += self.get_thread(os.path.join(subdir,file))
        return threads

    def get_thread(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        application = "unknown"
        returnlist = []
        application = root.get("name")
        for child in root:
            #if(child.tag == "Application"):
            #    application = child.get("name")
            if(child.tag == "PeriodicThread"):
                thread = DataClass.Threads(child.get("name"),application, child.get("rateGroup"))
                for second_child in child:
                    port = DataClass.PacPorts(second_child.get("name"), second_child.get("interface"), second_child.get("role"))
                    thread.port_set.append(port)
                returnlist.append(thread)
        return returnlist

    def get_connections(self, path):
        # Return all connections in path
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for child in root:
            if(child.tag == "Connection"):
                returnlist.append(self.create_connection(child))
            elif child.tag == "TemplateInstantiation":
                pass
                #DebugFile.debug_print("Template instantiation in {0}".format(path), DebugFile.WARNING)
        return returnlist 


    def get_all_applications(self, path):
        application = []
        application_instances = []
        if os.path.exists(path + "/application_instances.xml"):
            if os.path.isfile( path + "/application_instances.xml"):
                application += self.get_application(path + "/application_instances.xml")
                application_instances += self.get_application_instances(path + "/application_instances.xml")

        return application,application_instances



    def get_applications_instances_list(self, path):
        application_instances = []
        if os.path.exists(path + "/application_instances.xml"):
            if os.path.isfile( path + "/application_instances.xml"):
                application_instances += self.get_application_instances(path + "/application_instances.xml")
        return application_instances

    
    def get_applications_list(self, path):
        returnlist = []
        if os.path.exists(path + "/application_instances.xml"):
            if os.path.isfile( path + "/application_instances.xml"):
                returnlist = self.get_applications(path + "/application_instances.xml")
        return returnlist

    def get_applications(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        set_of_application_names = set()
        returnlist = []
        for child in root:
            if(child.tag == "ApplicationInstance"):
                set_of_application_names.add(child.get("instanceOf"))

        for app in set_of_application_names:
           print(app)
           returnlist.append(DataClass.Application(app))
        return returnlist
  
    def get_application_instances(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for child in root:
            if(child.tag == "ApplicationInstance"):
                returnlist.append(self.create_application_instance(child))
        return returnlist  

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
    def get_partitions(self,Project,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for partitions in root:
            if partitions.tag in self.functions:
                if (partitions.tag == "APP" or partitions == "IOP"):
                    #returnlist.append(self.functions[node.tag](partitions))
                    returnlist += self.create_partitions_in_cpu(Project,partitions)
        return returnlist


    
    def get_cpu_applications(self,project,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for cpu in root:
            if cpu.tag in self.functions:
                if (cpu.tag == "PP"):
                    #returnlist.append(self.functions[node.tag](partitions))
                    returnlist += self.create_applications_in_cpu(project,cpu)
        return returnlist 
    
    def initialisation(self):
        self.functions = {"PP":self.cpu,"PDCM":self.create_node,"DCM":self.create_node,"APP":self.cpu,"IOP":self.cpu,"Application":self.create_application}
    
    