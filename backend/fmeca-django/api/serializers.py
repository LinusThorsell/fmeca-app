from dataclasses import field
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from .models import *
from rest_framework import serializers

class PacPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacPort
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
    application_set = ApplicationSerializer(many=True)

    class Meta:
        model = Partition
        fields = '__all__'

    # def create(self, validated_data):
    #     application_set = validated_data.pop('application_set')
    #     partition_instance, created = Partition.objects.update_or_create(**validated_data)
    #     cpu_ref = getattr(partition_instance, 'cpu')
    #     # node_ref = getattr(partition_instance, 'node')
    #     for application in application_set:
    #         Application.objects.create(partition_instance=partition_instance, cpu=cpu_ref, **application)

class CPUSerializer(serializers.ModelSerializer):
    partition_set = PartitionSerializer(many=True)
    application_set = ApplicationSerializer(many=True)

    class Meta:
        model = CPU
        fields = '__all__'

    # def create(self, validated_data):
    #     partition_set = validated_data.pop('partition_set')
    #     application_set = validated_data.pop('application_set')
    #     cpu_instance, created = CPU.objects.update_or_create(**validated_data)
    #     # node_ref = getattr(cpu_instance, 'node')
    #     for partition in partition_set:
    #         Partition.objects.create(cpu=cpu_instance, **partition)
    #     for application in application_set:
    #         Application.objects.create(cpu=cpu_instance, **application)
    #     return cpu_instance

class NodeSerializer(serializers.ModelSerializer):
    cpu_set = CPUSerializer(many=True)

    class Meta:
        model = Node
        fields = '__all__'

    # def create(self, validated_data):
    #     cpu = validated_data.pop('cpu_set')
    #     node_instance, created = Node.objects.update_or_create(**validated_data)
    #     for cpu in cpu_set:
    #         CPU.objects.create(node=node_instance, **cpu)
    #     return node_instance

class ProjectSerializer(serializers.ModelSerializer):
    node_set = NodeSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        node_set = validated_data.pop('node_set')
        project_instance, created = Project.objects.update_or_create(**validated_data)
        for node in node_set:
            cpu_set = node.pop('cpu_set')
            node_instance, created = Node.objects.update_or_create(project=project_instance, **node)
            for cpu in cpu_set:
                part_set = cpu.pop('partition_set')
                app_set = cpu.pop('application_set')
                cpu_instance, created = CPU.objects.update_or_create(node=node_instance, **cpu)
                for application in app_set:
                    application.pop('cpu')
                    Application.objects.update_or_create(cpu=cpu_instance, project=project_instance, **application)
                for partition in part_set:
                    app2_set = partition.pop('application_set')
                    Partition.objects.update_or_create(cpu=cpu_instance, **partition)
                    for application in app2_set:
                        application.pop('cpu')
                        Application.objects.update_or_create(cpu=cpu_instance, project=project_instance, **application)
        return project_instance

#---------------------------------------------------------------------

class GetApplicationIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'name']

#---------------------------------------------------------------------

class KeyValSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyVal
        fields = '__all__'

class DictSerializer(serializers.ModelSerializer):
    comments = KeyValSerializer(many=True)

    class Meta:
        model = CommentsDict
        fields = '__all__'

    def create(self, validated_data):
        comments = validated_data.pop('comments')
        dict_instance, created = CommentsDict.objects.update_or_create(**validated_data)
        for comment in comments:
            KeyVal.objects.all().update_or_create(dict_instance, **comment)
