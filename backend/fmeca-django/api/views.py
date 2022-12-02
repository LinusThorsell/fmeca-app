from gc import get_objects
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets
# from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers
# Create your views here.

# {
#     "name":"dummy1",
#     "node_set":[{
#         "name":"testnode",
#         "cpu_set":[{
#             "name":"testcpu",
#             "application_set":[],
#             "partition_set":[]
#         }]
#     }]
# }

permission = '__all__'

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permissions = permission

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

# need to send application_name and project_name for the viewset
# to figure out which application to connect the instance to
class ApplicationInstanceViewSet(viewsets.ModelViewSet):
    queryset = ApplicationInstance.objects.all()
    serializer_class = ApplicationInstanceSerializer
    permissions = permission

    def create(self, request):
        request_data = request.data
        application_name = request_data.pop('application_name')
        project_name = request_data.pop('project_name')
        project_instance = get_object_or_404(Project.objects.all(), name=project_name)
        application_instance = get_object_or_404(Application.objects.all(), name=application_name, project=project_instance)
        application_id = getattr(application_instance, 'id')
        
        request_data['application'] = application_id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permissions = permission

# need to send application_name and project_name for the viewset
# to figure out which application to connect the thread to
class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permissions = permission

    def create(self, request):
        request_data = request.data
        application_name = request_data.pop('application_name')
        project_name = request_data.pop('project_name')
        project_instance = get_object_or_404(Project.objects.all(), name=project_name)
        application_instance = get_object_or_404(Application.objects.all(), name=application_name, project=project_instance)
        application_id = getattr(application_instance, 'id')
        
        request_data['application'] = application_id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

class PacPortViewSet(viewsets.ModelViewSet):
    queryset = PacPort.objects.all()
    serializer_class = PacPortSerializer
    permissions = permission

# {
#     "name": "",
#     "application_name": "LTM_FMC",
#     "project_name": "linus1"
# }

#------------------------------------------------

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = CommentsContainer.objects.all()
    serializer_class = CommentsContainerSerializer
    permissions = permission

    def create(self, request):
        request_data = request.data
        comments_dict = request_data.pop('comments')
        request_data['comments'] = []

        project_instance = get_object_or_404(Project.objects.all(), name=request_data['project'])
        container_instance = CommentsContainer.objects.create(project=project_instance)
        for key, value in comments_dict.items():
            KeyVal.objects.create(key=key, comment=value, container=container_instance)

        serializer =  serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
