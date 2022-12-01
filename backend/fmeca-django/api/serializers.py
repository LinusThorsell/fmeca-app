from dataclasses import field
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from .models import *
from rest_framework import serializers

class PacPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacPort
        fields = '__all__'

class DomainBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainBorder
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    # pacport_set = PacPortSerializer(many=True)

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

class ApplicationSerializer(serializers.ModelSerializer):
    # reciver_set = ConnectionSerializer(many=True)
    # provider_set = ConnectionSerializer(many=True)
    # thread_set = ThreadSerializer(many=True)

    class Meta:
        model = Application
        fields = '__all__'

    def update(self, **validated_data):
        pass

class PartitionSerializer(serializers.ModelSerializer):
    # application_set = ApplicationSerializer(many=True)

    class Meta:
        model = Partition
        fields = '__all__'

class CPUSerializer(serializers.ModelSerializer):
    # partition_set = PartitionSerializer(many=True)
    # application_set = ApplicationSerializer(many=True)

    class Meta:
        model = CPU
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    # cpu_set = CPUSerializer(many=True)

    class Meta:
        model = Node
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # node_set = NodeSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data.pop('node_set')
    #     return Project.objects.get(**validated_data)

# class ProjectSerializer(serializers.ModelSerializer):
#     node_set = NodeSerializer(many=True)

#     class Meta:
#         model = Project
#         fields = '__all__'

#     # def create(self, validated_data):
#     #     node_set = validated_data.pop('node_set')
#     #     project_instance, created = Project.objects.update_or_create(**validated_data)
#     #     for node in node_set:
#     #         cpu_set = node.pop('cpu_set')
#     #         node_instance, created = Node.objects.update_or_create(project=project_instance, **node)
#     #         for cpu in cpu_set:
#     #             part_set = cpu.pop('partition_set')
#     #             app_set = cpu.pop('application_set')
#     #             cpu_instance, created = CPU.objects.update_or_create(node=node_instance, **cpu)
#     #             for application in app_set:
#     #                 application.pop('cpu')
#     #                 Application.objects.update_or_create(cpu=cpu_instance, project=project_instance, **application)
#     #             for partition in part_set:
#     #                 app2_set = partition.pop('application_set')
#     #                 Partition.objects.update_or_create(cpu=cpu_instance, **partition)
#     #                 for application in app2_set:
#     #                     application.pop('cpu')
#     #                     Application.objects.update_or_create(cpu=cpu_instance, project=project_instance, **application)
#     #     return project_instance

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