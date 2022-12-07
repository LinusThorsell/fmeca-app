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
        
        project_object = Project.objects.create(name=project_name)

        print("<--- PROJECT CREATED --->")

        # node_set
        for node in node_set:
            cpu_set = node.pop('cpu_set')
            node_object= Node.objects.create(**node, project=project_object)           
            for cpu in cpu_set:
                partition_set = cpu.pop('partition_set')
                cpu_object = CPU.objects.create(**cpu, node=node_object)
                for partition in partition_set:
                    partition_object = Partition.objects.create(**partition, cpu=cpu_object)       

        print("<--- NODES CREATED --->")

        # application_set
        for application in application_set:
            Application.objects.create(**application, project=project_object)

        print("<--- APPLICATIONS CREATED --->")

        # application_instance_set
        for application_instance in application_instance_set:  
            node_name        = application_instance.pop('node_name')
            cpu_name         = application_instance.pop('cpu_name')
            partition_name   = application_instance.pop('partition_name')
            instanceof_name  = application_instance['instance_of_application']
            instance_of      = application_instance.pop('instance_of')
            
            node_object = None
            cpu_object = None
            partition_object = None
            application_object = None

            if node_name != None:
                node_object = get_object_or_404(Node.objects.all(), name=node_name, project=project_object)
            if cpu_name != None:
                cpu_object = get_object_or_404(CPU.objects.all(), name=cpu_name, node=node_object)      
            if instanceof_name != None:
                instanceof_object = get_object_or_404(Application.objects.all(), name=instanceof_name, project=project_object)
            if partition_name != None:
                partition_object = Partition.objects.get(name=partition_name, cpu=cpu_object)
            
            ApplicationInstance.objects.create(**application_instance, instance_of=instanceof_object, cpu=cpu_object, 
                                        node=node_object, partition=partition_object, project=project_object)

        print("<--- APPLICATION INSTANCES CREATED --->")

        # thread_set
        for thread in thread_set:
            application_name   = thread.pop('application')
            port_set           = thread.pop('port_set')
            application_object = get_object_or_404(Application.objects.all(), name=application_name, project=project_object)
            thread_object = Thread.objects.create(**thread, application=application_object, project=project_object)
            for port in port_set:
                PacPort.objects.create(**port, thread=thread_object, domain_border=None, project=project_object)
        
        print("<--- THREADS CREATED --->")

        # domain_borders
        for domain_border in domain_border_set:
            port_set = domain_border.pop('port_set')
            domain_border_object = DomainBorder.objects.create(**domain_border, project=project_object)
            for port in port_set:
                PacPort.objects.create(**port, thread=None, domain_border=domain_border_object, project=project_object)

        print("<--- DOMAIN BORDERS CREATED --->")
        
        # connection_set
        for connection in connection_set:        
            provider_owner = connection.pop('provider_owner')
            provider_thread = connection.pop('provider_thread')
            provider_port = connection.pop('provider_port')
            requirer_owner = connection.pop('requirer_owner')
            requirer_thread = connection.pop('requirer_thread')
            requirer_port = connection.pop('requirer_port')

            provider_is_db = connection.pop('provider_is_domainborder')
            requirer_is_db = connection.pop('requirer_is_domainborder')
            provider_thread_object = None
            requirer_thread_object = None
            provider_port_object = None
            requirer_port_object = None
            
            if provider_is_db:
                provider_owner = None
            else:  
                provider_thread_object = get_object_or_404(Thread.objects.all(), name=provider_thread, project=project_object)
                provider_port_object = get_object_or_404(PacPort.objects.all(), 
                                    name=provider_port, thread=provider_thread_object, project=project_object)   
                application_object = getattr(thread_object, 'application')
                application_name = getattr(application_object, 'name')
                provider_owner = get_object_or_404(ApplicationInstance.objects.all(), name=application_name, project=project_object)
            
            if requirer_is_db:
                requirer_owner = None
            else:
                requirer_thread_object = get_object_or_404(Thread.objects.all(), name=requirer_thread, project=project_object)
                requirer_port_object = get_object_or_404(PacPort.objects.all(), 
                                    name=requirer_port, thread=requirer_thread_object, project=project_object)
                application_object = getattr(thread_object, 'application')
                application_name = getattr(application_object, 'name')
                requirer_owner = get_object_or_404(ApplicationInstance.objects.all(), name=application_name, project=project_object)

            Connection.objects.create(**connection, provider_app=provider_owner, provider_port=provider_port_object, 
                                    requirer_app=requirer_owner, requirer_port=requirer_port_object, project=project_object)
      
        print("<--- CONNECTIONS CREATED --->")
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

    def create(self, request):
        request_data = request.data
        comments_dict = request_data.pop('comments')
        request_data['comments'] = []

        # todo fix update defaults
        project_instance = get_object_or_404(Project.objects.all(), name=request_data['project'])
        container_instance, created = CommentsContainer.objects.update_or_create(project=project_instance)
        if created:
            for key, value in comments_dict.items():
                KeyVal.objects.create(key=key, comment=value, container=container_instance)

        serializer =  serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
