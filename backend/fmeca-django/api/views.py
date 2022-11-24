from gc import get_objects
from django.shortcuts import render, get_object_or_404
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

    def create(self, request):
        request_data = request.data
        project_name = request_data.pop('project_name')
        application_name = request_data.pop('application_name')
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

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permissions = permission

    def create(self, request):
        pass


#------------------------------------------------

# Problem:
# Get id from application with application name and project name
# class GetApplicationID(viewsets.ReadOnlyModelViewSet):
#     queryset = Application.objects.all()
#     serializer_class = GetApplicationIDSerializer
#     http_method_names = ['get']
#     permissions = permission

#     def retrieve(self, request):
#         queryset = Application.objects.all()
#         application = get_object_or_404(queryset, name=request.name, project=request.project)
#         serializer = GetApplicationIDSerializer(application)
#         return Response(serializer.data)

#------------------------------------------------

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = CommentsDict.objects.all()
    serializer_class = DictSerializer
    permissions = permission