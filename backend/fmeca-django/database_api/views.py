from django.shortcuts import render
from .models import *
# from rest_framework import viewsets
# from rest_framework import permissions
from .serializers import PersonSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def PersonList(request):
    persons = Person.objects.all()
    serializers = PersonSerializer(persons, many=True)
    return Response(serializers.data)