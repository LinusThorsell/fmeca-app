from dataclasses import field
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from .models import *
from rest_framework import serializers

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    # connection_reciver_set = ConnectionSerializer(many=True)
    # connection_provider_set = ConnectionSerializer(many=True)

    class Meta:
        model = Application
        fields = '__all__'

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
            Node.objects.create(project=project_instance, **node)
            for cpu in cpu_set:
                part_set = cpu.pop('partition_set')
                app_set = cpu.pop('application_set')
                CPU.objects.create(node=Node.objects.get(**node), **cpu)
                for application in app_set:
                    Application.objects.create(cpu=CPU.objects.get(**cpu), **application)
                for partition in part_set:
                    app2_set = partition.pop('application_set')
                    Partition.objects.create(cpu=CPU.objects.get(**cpu), **partition)
                    for application in app2_set:
                        Application.objects.create(cpu=CPU.objects.get(**cpu), **application)
        return project_instance





# class PartitionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Partition
#         fields = '__all__'

# class NodeSerializer(serializers.ModelSerializer):
#     partition_set = PartitionSerializer(many=True)

#     class Meta:
#         model = Node
#         fields = '__all__'

#     def create(self, validated_data):
#         partition_set = validated_data.pop('partition_set')
#         node_instance = Node.objects.create(**validated_data)
#         for partition in partition_set:
#             Partition.objects.create(node=node_instance, **partition)
#         return node_instance

# class ProjectSerializer(serializers.ModelSerializer):
#     node_set = NodeSerializer(many=True)

#     class Meta:
#         model = Project
#         fields = '__all__'

#     def create(self, validated_data):
#         node_set = validated_data.pop('node_set')   
#         project_instance = Project.objects.create(**validated_data)
#         for node in node_set:
#             node_id = node.get('id')
#             print(node_id)
#             Node.objects.get('node_id').update(project=project_instance)
#             # Node.objects.create(project=project_instance,**node)
#         return project_instance

# class NodeFailureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NodeFailure
#         fields = '__all__'


# class PartitionFailureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PartitionFailure
#         fields = '__all__'

# class ApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = '__all__'

# class MaterialGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MaterialGroup
#         field = '__all__'