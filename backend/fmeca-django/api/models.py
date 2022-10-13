from audioop import maxpp
from email.mime import application
from email.policy import default
from functools import partial
from logging import critical
from unicodedata import category
from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

# class Node(models.Model):
#     name = models.CharField(max_length=50, default="")

class Node(models.Model):
    name = models.CharField(max_length=50, default="")
    platform = models.CharField(max_length=50, default="")
    load_set_type = models.CharField(max_length=50, default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")

class NodeFC(models.Model):
    redundant = models.CharField(max_length=20, default="false")
    sync_loss = models.CharField(max_length=50, default="")
    node = models.OneToOneField(Node, on_delete=models.CASCADE)

class NodeMC(models.Model):
    node = models.OneToOneField(Node, on_delete=models.CASCADE)


# class NodeFC(models.Model):
#     name = models.CharField(max_length=50, default="")
#     platform = models.CharField(max_length=50, default="")
#     load_set_type = models.CharField(max_length=50, default="")
#     redundant = models.CharField(max_length=20, default="false")
#     sync_loss = models.CharField(max_length=50, default="")
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")

# class NodeMC(models.Model):
#     name = models.CharField(max_length=50, default="")
#     platform = models.CharField(max_length=50, default="")
#     load_set_type = models.CharField(max_length=50, default="")
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, default="")

class CPU(models.Model):
    type = models.CharField(max_length=50, default="")
    node = models.OneToOneField(Node, on_delete=models.CASCADE)
    # nodeFC = models.ForeignKey(NodeFC, on_delete=models.CASCADE, null=True)
    # nodeMC = models.ForeignKey(NodeMC, on_delete=models.CASCADE, null=True)

    # @property
    # def node(self):
    #     if self.nodeFC.name == None:
    #         return self.nodeMC
    #     return self.nodeFC

class Partition(models.Model):
    name = models.CharField(max_length=20, default="")
    is_ltm = models.CharField(max_length=20, default="")
    fixed_start = models.BigIntegerField(default=None)
    partition_id = models.IntegerField(default=None)
    node = models.ForeignKey(NodeFC, on_delete=models.CASCADE, default="")
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, default="")

class Application(models.Model):
    id = models.BigAutoField(primary_key=True, default=0)
    name = models.CharField(max_length=50, default="")
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, default="")
    node = models.ForeignKey(Node, on_delete=models.CASCADE, default="")

# class Connection(models.Model):
#     requirer = models.ForeignKey(Application, on_delete=models.CASCADE, default="")
#     provider = models.ForeignKey(Application, on_delete=models.CASCADE, default="")

# class NodeFailure(models.Model):
#     id = models.BigAutoField(primary_key=True, default=0)
#     node = models.ForeignKey(Node, on_delete=models.CASCADE)
#     event = models.CharField(max_length=200)
#     flight_phase = models.CharField(max_length=50)    
#     comments = models.TextField(max_length=500, default="")

# class PartitionFailure(models.Model):
#     id = models.BigAutoField(primary_key=True, default=0)
#     partition = models.ForeignKey(Partition, on_delete=models.CASCADE)
#     failure_mode_effect = models.TextField(max_length=100, default="")
#     subsystem_effect = models.TextField(max_length=100, default="")
#     aircraft_level_effect = models.TextField(max_length=100, default="")
#     event = models.CharField(max_length=50, default="")
#     mission = models.CharField(max_length=50, default="")
#     category = models.CharField(max_length=50, default="")
#     criticality = models.CharField(max_length=50, default="")
#     comments = models.TextField(max_length=500, default="")
    
# class Application(models.Model):
#     id = models.BigAutoField(primary_key=True, default=0)
#     name = models.CharField(max_length=50, default="")
#     partition_failure = models.ManyToManyField(PartitionFailure, default="")

# class MaterialGroup(models.Model):
#     materal_group = models.CharField(max_length=50)
#     application = models.ForeignKey(Application, on_delete=models.CASCADE, default="")
#     partition = models.ForeignKey(Partition, on_delete=models.CASCADE, default="")
 