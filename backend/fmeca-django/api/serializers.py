
from dataclasses import field
from .models import *
from rest_framework import serializers
<<<<<<< HEAD

class PartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partition
        fields = '__all__'
=======
>>>>>>> master

class NodeSerializer(serializers.ModelSerializer):
    partition_set = PartitionSerializer(many=True)

    class Meta:
        model = Node
        fields = '__all__'

    def create(self, validated_data):
        partition_set = validated_data.pop('partition_set')
        node_instance = Node.objects.create(**validated_data)
        for partition in partition_set:
            Partition.objects.create(node=node_instance, **partition)
        return node_instance

class ProjectSerializer(serializers.ModelSerializer):
    node_set = NodeSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        node_set = validated_data.pop('node_set')
        project_instance = Project.objects.create(**validated_data)
        for node in node_set:
            Node.objects.create(project=project_instance,**node)
        return project_instance

class NodeFailureSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeFailure
        fields = '__all__'


class PartitionFailureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartitionFailure
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class MaterialGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialGroup
        field = '__all__'




