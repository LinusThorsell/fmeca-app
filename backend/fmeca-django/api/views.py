from gc import get_objects
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from .models import *
from .serializers import *
from rest_framework import viewsets
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
# Create your views here.

permission = '__all__'

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permissions = permission

    # transaction is atomic - nothing is commited
    # to db until everything is guaranteed successful.
    # eliminates waste in case of failure
    @transaction.atomic
    def create(self, request):     
        request_data             = request.data
        project_name             = request_data['name']
        node_set                 = request_data.pop('node_set')
        application_set          = request_data.pop('application_set')
        application_instance_set = request_data.pop('application_instance_set')
        thread_set               = request_data.pop('thread_set')
        domain_border_set        = request_data.pop('domain_border_set')
        connection_set           = request_data.pop('connection_set')
        
        # some dictionaries to use later for performance gains and optimization
        node_object_list     = {}
        app_object_list      = {}
        app_inst_object_list = {}
        thread_object_list   = {}
        db_object_list       = {}
        
        # creates project object in db
        project_object = Project.objects.create(name=project_name)
        
        print("<--- PROJECT CREATED --->")

        # node_set
        for node in node_set:
            cpu_set = node.pop('cpu_set')
            # creates node object in given project - makes sure project links to same project
            node_object = Node.objects.create(**node, project=project_object)  
            # saves the object to list for later use
            node_object_list[node['name']] = node_object       
            for cpu in cpu_set:
                partition_set = cpu.pop('partition_set')
                # creates cpu object - important that it has the relation to the node object
                cpu_object = CPU.objects.create(**cpu, node=node_object)
                # saves the object to list for later use
                node_object_list[node['name'] + cpu['name']] = cpu_object
                for partition in partition_set:
                    # creates partition object - must link to cpu object
                    partition_object = Partition.objects.create(**partition, cpu=cpu_object)
                    # saves the object to list for later use
                    node_object_list[node['name'] + cpu['name'] + partition['name']] = partition_object
                    
        print("<--- NODES CREATED --->")

        # application_set
        for application in application_set:
            # creates applications - links them to project
            application_object = Application.objects.create(**application, project=project_object)
            # saves the object to list for later use
            app_object_list[application['name']] = application_object

        print("<--- APPLICATIONS CREATED --->")

        # application_instance_set
        for application_instance in application_instance_set:  
            # pops all data that is irrelevant for db - is used
            # to get the proper relations to other objects in the project
            node_name         = application_instance.pop('node_name')
            cpu_name          = application_instance.pop('cpu_name')
            partition_name    = application_instance.pop('partition_name')
            application_name  = application_instance['instance_of_application']
            instance_of       = application_instance.pop('instance_of')
            
            # initiates to null in-case they have no relation
            # to that perticular object
            node_object = None
            cpu_object = None
            partition_object = None
            application_object = None
 
            if node_name != None:
                node_object = node_object_list[node_name]
                    
            # first check if it is possible to get from object_list
            # since it is much faster performance. if node is null
            # but partition or cpu exit then get() is necessary
            if cpu_name != None and node_name != None:
                cpu_object = node_object_list[node_name + cpu_name]
            elif cpu_name != None:
                cpu_object = get_object_or_404(CPU.objects.all(), name=cpu_name, node=node_object)
            
            if partition_name != None and cpu_name != None and node_name != None:
                partition_object = node_object_list[node_name + cpu_name + partition_name]
            elif partition_name != None:
                partition_object = get_object_or_404(Partition.objects.all(), name=partition_name, cpu=cpu_object)
                      
            if application_name != None:
                application_object = app_object_list[application_name]
            
            # creates application instance with parameters given
            app_inst_object = ApplicationInstance.objects.create(**application_instance, 
                                        instance_of=application_object, cpu=cpu_object, 
                                        node=node_object, partition=partition_object, project=project_object)
            # saves the object to list for later use
            app_inst_object_list[application_instance['name']] = app_inst_object

        print("<--- APPLICATION INSTANCES CREATED --->")

        # thread_set
        for thread in thread_set:
            application_name   = thread.pop('application')
            port_set           = thread.pop('port_set')
            application_object = app_object_list[application_name]
            
            # creates thread object
            thread_object = Thread.objects.create(**thread, application=application_object, project=project_object)
            # saves the object to list for later use
            thread_object_list[thread['name']] = thread_object
            for port in port_set:
                # creates pacport object - must link to thread and set
                # domain border to null
                port_object = PacPort.objects.create(**port, thread=thread_object, domain_border=None, project=project_object)
                # saves the object to list for later use
                thread_object_list[thread['name'] + port['name']] = port_object
        
        print("<--- THREADS CREATED --->")

        # domain_borders
        for domain_border in domain_border_set:
            port_set = domain_border.pop('port_set')
            # create domain border
            domain_border_object = DomainBorder.objects.create(**domain_border, project=project_object)
            # saves the object to list for later use
            db_object_list[domain_border['name']] = domain_border_object
            for port in port_set:
                # creates pacport object - must link to domain border
                # and set thread to null
                port_object = PacPort.objects.create(**port, thread=None, 
                                                    domain_border=domain_border_object, project=project_object)
                # saves the object to list for later use
                db_object_list[domain_border['name'] + port['name']] = port_object

        print("<--- DOMAIN BORDERS CREATED --->")
        
        # connection_set
        for connection in connection_set:        
            provider_owner  = connection.pop('provider_owner')
            provider_thread = connection.pop('provider_thread')
            provider_port   = connection.pop('provider_port')
            requirer_owner  = connection.pop('requirer_owner')
            requirer_thread = connection.pop('requirer_thread')
            requirer_port   = connection.pop('requirer_port')

            # initiates all the values to null incase they dont exist
            provider_is_db          = connection.pop('provider_is_domainborder')
            requirer_is_db          = connection.pop('requirer_is_domainborder')
            provider_app_object     = None
            requirer_app_object     = None
            provider_db_object      = None
            requirer_db_object      = None
            provider_thread_object  = None
            requirer_thread_object  = None
            provider_port_object    = None
            requirer_port_object    = None
            
            # if provider port goes to a domain border decides if the
            # connection should save the domain border or the application
            # instance and thread
            if provider_is_db:
                provider_db_object      = db_object_list[provider_owner]
                provider_port_object    = db_object_list[provider_owner + provider_port]
            else:
                provider_app_object     = app_inst_object_list[provider_owner]
                provider_thread_object  = thread_object_list[provider_thread]
                provider_port_object    = thread_object_list[provider_thread + provider_port]  
                      
            # if requirer port goes to a domain border decides if the
            # connection should save the domain border or the application
            # instance and thread
            if requirer_is_db:
                requirer_db_object      = db_object_list[requirer_owner]
                requirer_port_object    = db_object_list[requirer_owner + requirer_port]
            else:
                requirer_app_object     = app_inst_object_list[requirer_owner]
                requirer_thread_object  = thread_object_list[requirer_thread]
                requirer_port_object    = thread_object_list[requirer_thread + requirer_port]

            # creates conneciton object with all parameters
            Connection.objects.create(**connection, project=project_object,
                                    provider_domain_border=provider_db_object,
                                    provider_app_instance=provider_app_object,
                                    provider_thread=provider_thread_object,
                                    provider_port=provider_port_object,
                                    requirer_domain_border=requirer_db_object,
                                    requirer_app_instance=requirer_app_object,
                                    requirer_thread=requirer_thread_object,
                                    requirer_port=requirer_port_object)
      
        print("<--- CONNECTIONS CREATED --->")

        # serializer =  serializer = self.get_serializer(data=project_name)
        # serializer.is_valid(raise_exception=True)
        # return Response(serializer.data)
        return Response({'name':project_name})

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permissions = permission

class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer
    permissions = permission

class PartitionViewSet(viewsets.ModelViewSet):
    queryset = Partition.objects.all()
    serializer_class = PartitionSerializer
    permissions = permission

class ApplicationViewSet(viewsets.ModelViewSet): 
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permissions = permission

class ApplicationInstanceViewSet(viewsets.ModelViewSet):
    queryset = ApplicationInstance.objects.all()
    serializer_class = ApplicationInstanceSerializer
    permissions = permission

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permissions = permission

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permissions = permission

class DomainBorderViewSet(viewsets.ModelViewSet):
    queryset = DomainBorder.objects.all()
    serializer_class = DomainBorderSerializer
    permissions = permission

class PacPortViewSet(viewsets.ModelViewSet):
    queryset = PacPort.objects.all()
    serializer_class = PacPortSerializer
    permissions = permission

#------------------------------------------------

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = CommentsContainer.objects.all()
    serializer_class = CommentsContainerSerializer
    permissions = permission

    # transaction is atomic - nothing is commited
    # to db until everything is guaranteed successful.
    # eliminates waste in case of failure
    @transaction.atomic
    def create(self, request):
        # Sends in a comments container that has a dictionary
        # with key value pairs of objects and comments.

        request_data = request.data
        comments_dict = request_data.pop('comments')
        request_data['comments'] = []

        project_instance = get_object_or_404(Project.objects.all(), name=request_data['project'])
        # create or update the container
        container_instance, created = CommentsContainer.objects.update_or_create(project=project_instance)

        if not created:
            # delete all the old comments if it already exist
            for i in KeyVal.objects.all().iterator():
                i.delete()

        # create the new ones
        for key, value in comments_dict.items():
            KeyVal.objects.create(key=key, comment=value, container=container_instance)

        # serializer =  serializer = self.get_serializer(data=request_data)
        # serializer.is_valid(raise_exception=True)

        return Response({'project':request_data['project']})
