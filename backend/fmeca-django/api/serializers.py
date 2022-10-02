
from dataclasses import field
from .models import *
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

# class ProjectSerializer(serializers.ModelSerializer, many=True):
#     node = NodeSerializer()

#     class Meta:
#         model = Project
#         fields = '__all__'

#     def create(self, validated_data):
#         node_data = validated_data.pop('node')
#         node.objects.create()
#         pass


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




