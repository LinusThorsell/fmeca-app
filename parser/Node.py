class Node_Data_Class:
    def __init__(self,name,project, partitionset):
        self.name = name
        self.project = project
        self.partition_set = partitionset
    def reprJSON(self):
        return {"name":self.name,"partition_set":self.partition_set}
