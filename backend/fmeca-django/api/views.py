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

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permissions = permission

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