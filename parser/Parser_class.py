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
        
        # for children in raw_cpu_data:
        #     print("\t\t" + children.tag)
        #     if children.tag in self.functions:
        #         returnlist += self.functions[children.tag](children)
                
        return DataClass.Cpu(name,type,unitid,IOPRef,ACCSSyncMaster,domainBorder)

    def create_partition(self,raw_partition_data,node,cpu):
        name = raw_partition_data.get("name")
        isLTM = raw_partition_data.get("isLTM")
        partition_id = raw_partition_data.get("id")
        
        Partition = DataClass.Partition_Data_Class(name, isLTM, partition_id, node,cpu)
        
        for children in raw_partition_data:
            if children.tag in self.functions:
                #typ onödig men whatever
                if children.tag == "Application":
                    Partition.applications.append(self.functions[children.tag](children,node,cpu,name))        
        return  Partition


    def create_application(self, raw_application_data,node, cpu, partition):
        
        #<DipsApplication name="PoProvider_Applicationrt_Gateway_1" rampool="0x10000" instanceOf="port_gateway" affinity="0"/>
        name = raw_application_data.get("name")
        rampool = raw_application_data.get("rampool")
        instanceOf = raw_application_data.get("instanceOf")
        affinity = raw_application_data.get("affinity")
        application = DataClass.Application(name, rampool, instanceOf, affinity, node, cpu, partition)
        return application

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
            arg1 = arg2 = arg3 = arg4 = arg5 = arg6 = arg7 = ""
            if(child.tag == "ProviderPort"):
                temp_list += child.get('name').split(".")
                print(temp_list)
                #arg1,arg2, arg3 = somethinglist[0],somethinglist[1],somethinglist[2]#= child.get('name').split("."), child.get('name').split("."), child.get('name').split(".")
                
            elif(child.tag == "RequirerPort"):
                temp_list += child.get('name').split(".")
                print(temp_list)

                #arg4, arg5, arg6 = child.get('name').split("."), child.get('name').split("."), child.get('name').split(".")
                temp_list.append(child.get('identity'))
                
        DebugFile.debug_print(*temp_list, DebugFile.OKCYAN)

        return DataClass.Connection(*temp_list)


    def create_application_instance(self, raw_application_instance_data):
        name = raw_application_instance_data.get('name')
        instanceOf = raw_application_instance_data.get("instanceOf")
        return DataClass.Application_Instances(name, instanceOf)



    
    def get_connection_list(self, path):
        connectionlist = []
        if os.path.exists(path+"/connections"):
            for subdir, dirs, files in os.walk(path+"/connections"):
                for file in files:
                    if(file == "connections.xml"):
                        print(subdir + "/"+file)
                        connectionlist += self.get_connections(os.path.join(subdir,file))
        return connectionlist

    def get_threads(self, path):
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
                    thread.port_list.append(port)
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
                DebugFile.warning_print("Template instantiation in {0}".format(path))
        return returnlist    


    def get_applications_instances_list(self, path):
        application_instances = []
        if os.path.exists(path + "/application_instances.xml"):
            if os.path.isfile( path + "/application_instances.xml"):
                application_instances += self.get_application_instances(path + "/application_instances.xml")
        return application_instances
  

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
    def get_partitions(self,path):
        tree = ET.parse(path)
        root = tree.getroot()
        returnlist = []
        for partitions in root:
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
    
    