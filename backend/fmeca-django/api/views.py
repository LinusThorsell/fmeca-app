from gc import get_objects
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets
# from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers
# from rest_framework import viewsets
# from rest_framework import permissions

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

# --------------------------------------------------


# class NodeFailureViewSet(viewsets.ModelViewSet):
#     queryset = NodeFailure.objects.all()
#     serializer_class = NodeFailureSerializer 
#     permissions = permission

# class PartitionFailureViewSet(viewsets.ModelViewSet):
#     queryset = PartitionFailure.objects.all()
#     serializer_class = PartitionFailureSerializer
#     permissions = permission

# class MaterialGroupViewSet(viewsets.ModelViewSet):
#     queryset = MaterialGroup.objects.all()
#     serializer_class = MaterialGroupSerializer
#     permissions = permission