from audioop import maxpp
from email.mime import application
from functools import partial
from logging import critical
from unicodedata import category
from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    age = models.IntegerField()

class Project(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True)

class Node(models.Model):
    node_id = models.CharField(max_length=50, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class NodeFailure(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    event = models.TextField(max_length=200)
    flight_phase = models.CharField(max_length=50)    
    comments = models.TextField(max_length=500, default="")

class Partition(models.Model):
    partition_id = models.CharField(max_length=20, primary_key=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, default="")

class PartitionFailure(models.Model):
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE)
    failure_mode_effect = models.TextField(max_length=100, default="")
    subsystem_effect = models.TextField(max_length=100, default="")
    aircraft_level_effect = models.TextField(max_length=100, default="")
    event = models.CharField(max_length=50, default="")
    mission = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    criticality = models.CharField(max_length=50, default="")
    comments = models.TextField(max_length=500, default="")

    
class Application(models.Model):
    application_id = models.CharField(max_length=20, primary_key=True)
    partition_failure = models.ManyToManyField(PartitionFailure)
    material_group = models.CharField(max_length=20, default="")