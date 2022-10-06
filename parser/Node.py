class Node_Data_Class:
    def __init__(self,name,partitionset):
        self.name = name
        self.partition_set = partitionset
    def reprJSON(self):
        return {"name":self.name,"partition_set":self.partition_set}

class Node_Set:
    def __init__(self,node_list):
        self.node_set = node_list
    def reprJSON(self):
        return {"node_set":self.node_set}