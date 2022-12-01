from Parser_class import Parser
import sys, string, os
from os import path as OSPATH
from Encoder_Class import *
import DataClass
import DebugFile

    # Check if all application instances have some application they are instances of
def test_application_instances(Project):
    failed = True
    found = False
    for instance in Project.application_instance_set:
        for applications in Project.application_set:
            if instance.instanceOfApplication == applications.name:
                found = True
        if(not found):
            failed = True
            DebugFile.warning_print("Did not find application for instance {0}".format(instance.name))
            found = False
    
    if (failed):
        return 0
    else:
        return 1
            
    # Check if all threads in refer to an actual application
def test_threads_refer_to_application(Project):
    failed = False
    found = False
    for thread in Project.thread_set:
        for app in Project.application_set:
            if(thread.application == app.name):
                found = True
                break
        if(not found):
            failed = True
            DebugFile.warning_print("Did not find application for thread {0}".format(thread.name))
        else:
            found = False
            
    if (failed):
        return 0
    else:
        return 1

    # Check if all ports in connections exist
def test_connection_ports(Project):     
    found = False
    failed = False
    bad_connections =  [] #bad connections == connections that doesnt have any existing ports
    for connection in Project.connection_set:
        if connection.Provider_thread != None:
            for thread in Project.thread_set:
                for port in thread.port_set:
                    if connection.Provider_port == port.name:
                        found = True         
        else:
            for domain_border in Project.domain_border_set:
                for port in domain_border.port_set:
                    if connection.Provider_port == port.name:
                        found = True
        
        if(not found):
            failed = True
            DebugFile.warning_print("{0} port not found, removing connections".format(connection.Provider_port))
            bad_connections.append(connection)
        else:
            found = False
        
    for connection in bad_connections:
        Project.connection_set.remove(connection)
    
    if (failed):
        return 0
    else:
        return 1
    # If connection have port from application intance check if intance exists
def test_connection_application_instances(Project): 
        pass
    # found = False
    # failed = False
    # bad_connections =  [] 

    # self.Provider_owner = Provider_owner
    # self.Provider_thread = Provider_thread
    # self.Provider_port = Provider_port
    # self.Provider_is_domainborder = provider_is_domainborder

    # self.Requirer_is_domainborder = requirer_is_domainborder
    # self.Requirer_owner = Requirer_owner
    # self.Requirer_thread =  Requirer_thread
    # self.Requirer_port = Requirer_port
    # self.identity = identity

    # for connection in Project.connection_set:
    #     if(not connection.Provider_is_domainborder):
    #         if connection.Provider_owner
            



    
            
tests = [test_application_instances,test_connection_ports,test_threads_refer_to_application]         
        
def run_all(Project):
    DebugFile.blue_print("Running tests")
    counter = 0
    i = 0
    while i < len(tests):
        counter += tests[i](Project)
        i+=1
    #counter += test_application_instances(Project)
    #counter += test_threads_refer_to_application(Project)
    #counter += test_connection(Project)
    if (counter == len(tests)):
        DebugFile.success_print("{0} of {1} tests were successful".format(counter,len(tests)))
    elif counter > 0:
        DebugFile.warning_print("Only {0} of the {1} tests passed".format(counter,len(tests)))
    else:
        DebugFile.error_print("NO TESTS PASSED!")
