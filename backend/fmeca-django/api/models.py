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

    def __str__(self):
        return self.name

class animal(models.Model):
    type = models.CharField(max_length=20)
    belongs_to = models.ForeignKey(Person, on_delete=models.CASCADE, default="")


# -----------------------------------------


class Project(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True)
    
    def __str__(self):
        return self.project_id

class Node(models.Model):
    node_id = models.CharField(max_length=50, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return self.node_id

class NodeFailure(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    event = models.CharField(max_length=200)
    flight_phase = models.CharField(max_length=50)    
    comments = models.TextField(max_length=500, default="")

    def __str__(self):
        return self.event

class Partition(models.Model):
    partition_id = models.CharField(max_length=20, primary_key=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.partition_id

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

    def __str__(self):
        return self.event 

    
class Application(models.Model):
    application_id = models.CharField(max_length=20, primary_key=True)
    partition_failure = models.ManyToManyField(PartitionFailure)
    material_group = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.application_id