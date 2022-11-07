from audioop import maxpp
from email.mime import application
from email.policy import default
from functools import partial
from logging import critical
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Node(models.Model):
    name = models.CharField(max_length=50, blank=True)
    platform = models.CharField(max_length=50, blank=True, null=True)
    load_set_type = models.CharField(max_length=50, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    redundant = models.CharField(max_length=20, blank=True, null=True)
    sync_loss = models.CharField(max_length=20, blank=True, null=True)

class CPU(models.Model):
    type = models.CharField(max_length=10, default="")
    node = models.ForeignKey(Node, on_delete=models.CASCADE, blank=True, null=True)
    unit_id = models.CharField(max_length=10, blank=True, null=True)
    iop_ref = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=10, blank=True, null=True)
    accs_sync_master = models.CharField(max_length=10, blank=True, null=True)
    domain_border = models.CharField(max_length=20, blank=True, null=True)

class Partition(models.Model):
    name = models.CharField(max_length=20, blank=True)
    is_ltm = models.CharField(max_length=20, blank=True, null=True)
    fixed_start = models.BigIntegerField(default=None, null=True)
    partition_id = models.IntegerField(default=None, null=True)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, blank=True, null=True)
    # node = models.ForeignKey(CPU, on_delete=models.CASCADE, blank=True)

class Application(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, blank=True, null=True)
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE, blank=True, null=True)
    # node = models.ForeignKey(CPU, on_delete=models.CASCADE, blank=True)

class Connection(models.Model):
    requirer = models.ForeignKey(Application, related_name="connection_requirer_set", on_delete=models.CASCADE, blank=True, null=True)
    provider = models.ForeignKey(Application, related_name="connection_provider_set", on_delete=models.CASCADE, blank=True, null=True)

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
    
# class MaterialGroup(models.Model):
#     materal_group = models.CharField(max_length=50)
#     application = models.ForeignKey(Application, on_delete=models.CASCADE, default="")
#     partition = models.ForeignKey(Partition, on_delete=models.CASCADE, default="")
 
# {
#     "name": "dummy1",
#     "node_set": [{ 
#             "name":"test_node", 
#             "cpu_set":[{
#                 "name":"test_cpu",
#                 "application_set":[{
#                     "name":"test_application1"
#                 }],
#                 "partition_set":[{
#                     "name": "test_partition",
#                     "application_set":[{
#                         "name":"test_application2"
#                     }]      
#                 }]
#             }]
#    }]
# }

# {
#     "name": "dummy1",
#     "node_set": [{ 
#             "name":"test_node", 
#             "cpu_app_set":[{
#                 "name":"test_cpu",
#                 "application_set":[],
#                 "partition_set":[{
#                     "name": "test_partition",
#                     "partition_app_set":[]      
#                 }]
#             }]
#    }]
# }