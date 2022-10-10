class Partition_Data_Class:
    def __init__(self,name,node):
        self.name = name
        self.node = node
    def reprJSON(self):
        return {"name":self.name}