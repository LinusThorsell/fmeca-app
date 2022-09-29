from gc import get_objects
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import PersonSerializer, ProjectSerializer
from rest_framework import viewsets
# from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers
# from rest_framework import viewsets
# from rest_framework import permissions

# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permissions = ['__all__']



# class ProjectViewSet(view.ModelViewSet):
#     queryset = Project.objects.all()




# @api_view(['GET'])
# def PersonList(request):
#     persons = Person.objects.all()
#     serializers = PersonSerializer(persons, many=True)
#     return Response(serializers.data)



# @api_view(['GET', 'POST', 'DELETE'])
# def FmecaProject(request):
#     projects = Project.objects.all()
#     serializers = ProjectSerializer(projects, many=True)
#     return Response(serializers.data)