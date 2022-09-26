from email.mime import application
from functools import partial
from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    age = models.IntegerField()

class Project(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True)

class Node(models.Model):
    node_id = models.CharField(max_length=50, primary_key=True)

class NodeFailure(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    event = models.TextField(max_length=200)
    flight_phase = models.CharField(max_length=50)
    # maybe future refrence to PartitionFailure

class Partition(models.Model):
    partition_id = models.CharField(max_length=20, primary_key=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, default="")

class PartitionFailure(models.Model):
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE)
    
class Application(models.Model):
    application_id = models.CharField(max_length=20, primary_key=True)
    partition_failure = models.ManyToManyField(PartitionFailure)