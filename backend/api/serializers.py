from dataclasses import field
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from .models import *
from rest_framework import serializers

class PacPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacPort
        fields = '__all__'

class DomainBorderSerializer(serializers.ModelSerializer):
    pacport_set = PacPortSerializer(many=True)
    class Meta:
        model = DomainBorder
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    pacport_set = PacPortSerializer(many=True)

    class Meta:
        model = Thread
        fields = '__all__'

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class ApplicationInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationInstance
        fields = '__all__'


class PartitionSerializer(serializers.ModelSerializer):
    application_instance_set = ApplicationInstanceSerializer(many=True)

    class Meta:
        model = Partition
        fields = '__all__'

class CPUSerializer(serializers.ModelSerializer):
    partition_set = PartitionSerializer(many=True)
    application_instance_set = ApplicationInstanceSerializer(many=True)

    class Meta:
        model = CPU
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    cpu_set = CPUSerializer(many=True)

    class Meta:
        model = Node
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    node_set = NodeSerializer(many=True)
    application_set = ApplicationSerializer(many=True)
    thread_set = ThreadSerializer(many=True)
    domainborder_set = DomainBorderSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

#---------------------------------------------------------------------

class KeyValSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyVal
        fields = '__all__'

class CommentsContainerSerializer(serializers.ModelSerializer):
    comments = KeyValSerializer(many=True)

    class Meta:
        model = CommentsContainer
        fields = '__all__'

    def create(self, validated_data):
        return CommentsContainer.objects.create(**validated_data)