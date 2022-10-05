import json
    
class Partitionset_Data_Class:
    def __init__(self,namn):
        self.name = namn
    def reprJSON(self):
        return {"name":self.name}

class Node_Data_Class:
    def __init__(self,namn,partitioner):
        self.name = namn
        self.partition_set = partitioner
    def reprJSON(self):
        return {"name":self.name,"partition_set":self.partition_set}

class Project_Data_Class:
    def __init__(self,namn,lista):
        self.project_id = namn
        self.node_set = lista
    def reprJSON(self):
        return {"project_id":self.project_id,"node_set":self.node_set}


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class Encoder:
    def __init__(self):
        self.Project = ""
        
    def createProject(self,name):
        self.Project = Project_Data_Class(name,[]) 
    
    def send_to_database(self):
        string = json.dumps(self.Project,cls=ComplexEncoder,indent=4)
        #########

def main():
    Name = "Project"
    '''
    lista2 = []
    for i in range(5):
        lista2.append(LALALALLA_Data_Class("LALA"+str(i)))
    '''
    partitionset = []
    for i in range(5):
        partitionset.append(Partitionset_Data_Class("partition-"+str(i)))
    
    lista = []
    for i in range(5):
        lista.append(Node_Data_Class("Node-"+str(i),partitionset))
    Data = Project_Data_Class(Name,lista)
    string = json.dumps(Data,cls=ComplexEncoder,indent=4)

    #string = json.dumps(Data,cls=ProjectEncoder,indent=4)
    print(string)
    
#main()


#{
#    "name":"Project"
#    "nodes":
#    [
#        {
#            "Node_1",
#           "Node-2",
#            "Node-3"
#            }
#    ]
#    "something":"True"
#}

'''

class LALALALLA_Data_Class:
    def __init__(self,namn):
        self.name = namn
    def reprJSON(self):
        return {"name":self.name}
       

'''