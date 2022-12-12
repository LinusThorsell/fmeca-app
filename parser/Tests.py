from Parser_class import Parser
import sys, string, os
from os import path as OSPATH
from Encoder_Class import *
import DataClass
import DebugFile

    # Check if all application instances have some application they are instances of
def test_application_instances(Project):
    success = True
    found = False
    for instance in Project.application_instance_set:
        for applications in Project.application_set:
            if instance.instanceOfApplication == applications.name:
                found = True
        if(not found):
            success = False
            DebugFile.debug_print("Did not find application for instance {0}".format(instance.name))
            found = False
    
    return success
            
    # Check if all threads in refer to an actual application
def test_threads_refer_to_application(Project):
    success = True
    found = False
    for thread in Project.thread_set:
        for app in Project.application_set:
            if(thread.application == app.name):
                found = True
                break
        if(not found):
            success = False
            DebugFile.debug_print("Did not find application for thread {0}".format(thread.name))
        else:
            found = False
    return success


    # Check if all ports in connections exist and removes bad connections
def test_connection_ports(Project):     
    success = True
    bad_connections =  [] #bad connections = connections that doesnt have any existing ports   

    for connection in Project.connection_set:
        owner_found = False
        port_found = False

        # Provider
        if connection.Provider_is_domainborder:
            owner_found = True
            for domain_border in Project.domain_border_set:
                for port in domain_border.port_set:
                    if connection.Provider_port == port.name:
                        port_found = True
            if(not owner_found):
                DebugFile.debug_print("{0} domain_border not found, removing connection".format(connection.Provider_owner))
            elif(not port_found):
                DebugFile.debug_print("{0} port not found, removing connection".format(connection.Provider_port))

        else:

            if connection.Provider_owner in Project.application_instance_set:
                owner_found = True

            for thread in Project.thread_set:
                for port in thread.port_set:
                    if connection.Provider_port == port.name:
                        port_found = True  
            
            if(not owner_found):
                DebugFile.debug_print("{0} application instance not found, removing connection".format(connection.Provider_owner))
            elif(not port_found):
                DebugFile.debug_print("{0} port not found, removing connection".format(connection.Provider_port))
        
        if(not owner_found or not port_found):
            success = False
            bad_connections.append(connection)

        owner_found = False
        port_found = False

        # Requirer
        if connection.Requirer_is_domainborder:
            for domain_border in Project.domain_border_set:
                owner_found = True
                for port in domain_border.port_set:
                    if connection.Requirer_port == port.name:
                        port_found = True

            if(not owner_found):
                DebugFile.debug_print("{0} domain_border not found, removing connection".format(connection.Requirer_owner))
            elif(not port_found):
                DebugFile.debug_print("{0} port not found, removing connection".format(connection.Requirer_port))

        else:

            if connection.Requirer_owner in Project.application_instance_set:
                owner_found = True

            for thread in Project.thread_set:
                for port in thread.port_set:
                    if connection.Requirer_port == port.name:
                        port_found = True  
            
            if(not owner_found):
                DebugFile.debug_print("{0} application instance not found, removing connection".format(connection.Requirer_owner))
            elif(not port_found):
                DebugFile.debug_print("{0} port not found, removing connection".format(connection.Requirer_port))
        
        if(not owner_found or not port_found):
            success = False
            if(connection not in bad_connections):
                bad_connections.append(connection)

    for connection in bad_connections:
        Project.connection_set.remove(connection)

    return success
    
#     # If connection have port from application intance check if intance exists
# def test_connection_application_instances(Project): 
#     success = True
#     bad_connections =  [] 

#     for connection in Project.connection_set:
#         if(not connection.Provider_is_domainborder):
#             if not connection.Provider_owner in Project.application_instance_set:
#                 success = False
#                 DebugFile.debug_print("Did not found application_instance {0} that a connection refers to".format(connection.Provider_owner)) 
#         if(not connection.Requirer_is_domainborder):
#             if not connection.Requirer_owner in Project.application_instance_set:
#                 success = False
#                 DebugFile.debug_print("Did not found application_instance {0} that a connection  refers to".format(connection.Requirer_owner))       
#     return success

tests = [test_application_instances,test_threads_refer_to_application,test_connection_ports]         
        
def run_all(Project):
    DebugFile.debug_print("Running tests", DebugFile.BLUE)
    counter = 0
    i = 0
    while i < len(tests):
        counter += tests[i](Project)
        i+=1
    #counter += test_application_instances(Project)
    #counter += test_threads_refer_to_application(Project)
    #counter += test_connection(Project)
    if (counter == len(tests)):
        DebugFile.debug_print("{0} of {1} tests were successful".format(counter,len(tests)),  DebugFile.OKGREEN)
    elif counter > 0:
        DebugFile.debug_print("Only {0} of the {1} tests passed".format(counter,len(tests)), DebugFile.YELLOW)
    else:
        DebugFile.debug_print("NO TESTS PASSED!", DebugFile.CRED)
