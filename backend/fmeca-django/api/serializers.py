
from dataclasses import field
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from .models import *
from rest_framework import serializers
<<<<<<< HEAD
=======

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
>>>>>>> f124b00244b3d4205cfe25ec69d65901fb58bfbe

class PartitionSerializer(serializers.ModelSerializer):
    application_set = ApplicationSerializer(many=True)

    class Meta:
        model = Partition
        fields = '__all__'

    def create(self, validated_data):
        application_set = validated_data.pop('application_set')
        partition_instance, created = Partition.objects.update_or_create(**validated_data)
        cpu_ref = getattr(partition_instance, 'cpu')
        # node_ref = getattr(partition_instance, 'node')
        for application in application_set:
            Application.objects.create(partition_instance=partition_instance, cpu=cpu_ref, **application)

class CPUSerializer(serializers.ModelSerializer):
    partition_set = PartitionSerializer(many=True)
    application_set = ApplicationSerializer(many=True)

    class Meta:
        model = CPU
        fields = '__all__'

    def create(self, validated_data):
        partition_set = validated_data.pop('partition_set')
        application_set = validated_data.pop('application_set')
        cpu_instance, created = CPU.objects.update_or_create(**validated_data)
        # node_ref = getattr(cpu_instance, 'node')
        for partition in partition_set:
            Partition.objects.create(cpu=cpu_instance, **partition)
        for application in application_set:
            Application.objects.create(cpu=cpu_instance, **application)
        return cpu_instance

class NodeSerializer(serializers.ModelSerializer):
    cpu_set = CPUSerializer(many=True)

    class Meta:
        model = Node
        fields = '__all__'

    def create(self, validated_data):
        cpu_set = validated_data.pop('cpu_set')
        node_instance, created = Node.objects.update_or_create(**validated_data)
        for cpu in cpu_set:
            CPU.objects.create(node=node_instance, **cpu)
        return node_instance

class ProjectSerializer(serializers.ModelSerializer):
    node_set = NodeSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        node_set = validated_data.pop('node_set')
        project_instance, created = Project.objects.update_or_create(**validated_data)
        for node in node_set:
            Node.objects.create(project=project_instance, **node)
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




# {
#     "name": "test",
#     "node_set": [{ 
#                            "name":"test_node", 
#                            "cpu_set":[{
#                                               "name":"test_cpu",
#                                               "application_set":[{"name":"test_app"}]
#                                            }],
#                            "partition_set":[{
#                                               "name": "test_partition",
#                                               "application_set":[{"name":"test_app2"}]      
#                                            }], 
#                        }]
# }