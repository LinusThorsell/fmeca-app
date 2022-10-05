from audioop import maxpp
from email.mime import application
from functools import partial
from logging import critical
from unicodedata import category
from django.db import models

# Create your models here.

class Project(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True)

class Node(models.Model):
    # id = models.BigAutoField(primary_key=True, default=0)
    name = models.CharField(max_length=50, default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")

class NodeFailure(models.Model):
    id = models.BigAutoField(primary_key=True, default=0)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    event = models.CharField(max_length=200)
    flight_phase = models.CharField(max_length=50)    
    comments = models.TextField(max_length=500, default="")

class Partition(models.Model):
    id = models.BigAutoField(primary_key=True, default=0)
    name = models.CharField(max_length=20, default="")
    node = models.ForeignKey(Node, on_delete=models.CASCADE, default="")

class PartitionFailure(models.Model):
    id = models.BigAutoField(primary_key=True, default=0)
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
    id = models.BigAutoField(primary_key=True, default=0)
    name = models.CharField(max_length=50, default="")
    partition_failure = models.ManyToManyField(PartitionFailure, default="")

class MaterialGroup(models.Model):
    materal_group = models.CharField(max_length=50)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default="")
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE, default="")
 