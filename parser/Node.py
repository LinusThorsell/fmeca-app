class Node_Data_Class:
    def __init__(self,namn,project):
        self.name = namn
        self.project = project
    def reprJSON(self):
        return {"name":self.name,"project":self.project}

class Node_Set:
    def __init__(self,nodeset):
        self.nodes = nodeset
    def reprJSON(self):
        return {"node_set":self.nodes}
    
    
    
#class Node_Data_Class:
#    def __init__(self,namn,partitioner):
#        self.name = namn
#        self.partition_set = partitioner
#    def reprJSON(self):
#        return {"name":self.name,"partition_set":self.partition_set}
#        return {"name":self.name}
 