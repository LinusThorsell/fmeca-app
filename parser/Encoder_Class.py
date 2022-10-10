import json
    
import Project
import Node
import Partitions
import requests


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)




class Encoder:
    def __init__(self):
        self._headers = {"Content-Type":"application/json"}
        self._url = 'http://127.0.0.1:8000/'
        self.Project = ""
        #self.nodes = ""
        #self.partitions = ""
        
    def createProject(self,name,list):
        self.Project = Project.Project_Data_Class(name,list) 
    
    #partitioner till noder
    def add_nodes(self,node_list):
        #__node_list = []
        #for nodes in node_list:
        #    __node_list.append(Node.Node_Data_Class(nodes,""))
        #self.nodes = __node_list
        #self.Project.node_set = __node_list
        pass
    
    def add_partitions(self,partitions_list,dict):
        #_partitions_list = []
        #for partitions in partitions_list:
        #    _partitions_list.append(Partitions.Partitionset_Data_Class(partitions,dict[partitions]))
        #for nodes in Project.node_set:
        #    if nodes.name in dict:
        #        nodes.partitionset.append()
        #self.partitions = _partitions_list
        
        pass
    
    def send_to_database(self,object,folder):
        print("Är i send to database")
        string = json.dumps(object,cls=ComplexEncoder,indent=4)
        
        #print("Postar detta:",self._headers,string)
        #print("Till foldern: ",self._url + folder)
        print(string)
        #requests.post(self._url+ folder,string,headers=self._headers)
        #########

#def main():
    #Name = "Project"
    '''
    lista2 = []
    for i in range(5):
        lista2.append(LALALALLA_Data_Class("LALA"+str(i)))
    '''
    #partitionset = []
    #for i in range(5):
    #    partitionset.append(Partitionset_Data_Class("partition-"+str(i)))
    
    #lista = []
    #for i in range(5):
    #    lista.append(Node_Data_Class("Node-"+str(i),partitionset))
    #Data = Project_Data_Class(Name,lista)
    #string = json.dumps(Data,cls=ComplexEncoder,indent=4)

    #string = json.dumps(Data,cls=ProjectEncoder,indent=4)
    #print(string)