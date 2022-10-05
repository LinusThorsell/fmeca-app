class Project_Data_Class:
    def __init__(self,name):
        self.project_id = name
        self.nodeset = []
    def reprJSON(self):
        return {"project_id":self.project_id,"node_set":self.nodeset}
    
    
    
    
#class Project_Data_Class:
#    def __init__(self,name,list):
#        self.project_id = name
#        self.node_set = list
#    def reprJSON(self):
#        return {"project_id":self.project_id,"node_set":self.node_set}