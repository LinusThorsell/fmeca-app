
class Partition_Data_Class:
    def __init__(self,name,node):
        self.name = name
        #self.apps = []
        self.referenced_node = node
    def reprJSON(self):
        return {"name":self.name,"node":self.referenced_node}

class Partitionset_Class:
    def __init__(self,partitionset):
            self.partitions = partitionset
    def reprJSON(self):
        return {"partition_set":self.partitions}


    
#class Partitionset_Data_Class:
#    def __init__(self,name):
#        self.name = name
#        #self.apps = []
#    def reprJSON(self):
#        return {"name":self.name}