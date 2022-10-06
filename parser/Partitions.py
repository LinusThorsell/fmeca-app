
#class Partition_Data_Class:
#    def __init__(self,name,node):
#        self.name = name
#        self.referenced_node = node
#    def reprJSON(self):
#        return {"name":self.name,"node":self.referenced_node}

#class Partitionset_Class:
#    def __init__(self,partitionset):
#            self.partitions = partitionset
#    def reprJSON(self):
#        return {"partition_set":self.partitions}

    
class Partition_Data_Class:
    def __init__(self,name,node):
        self.name = name
        #self.referenced_node = node
        #self.apps = []
    def reprJSON(self):
        return {"name":self.name}
    
class Partition_Set:
    def __init__(self,partition_list):
        self.partition_set = partition_list
    def reprJSON(self):
        return {"partition_set":self.partition_set}