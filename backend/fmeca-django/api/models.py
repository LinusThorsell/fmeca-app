from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    age = models.IntegerField()

class Project(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True)


class Partition(models.Model):
    partition_id = models.CharField(max_length=50, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Application(models.Model):
    application_id = models.CharField(max_length=50, primary_key=True)
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE)

    failure_mode_effect = models.CharField(max_length=50)
    flight_phase = models.CharField(max_length=50)
    aircraft_level_effect  = models.TextField(max_length=500)
    mission = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

class Subsystem(models.Model):
    material_group = models.CharField(max_length=50, primary_key=True)
    effect = models.TextField(max_length=200)
    comment = models.TextField(max_length=500)



