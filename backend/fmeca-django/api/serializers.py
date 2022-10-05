
from dataclasses import field
from .models import *
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


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

class PartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partition
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




