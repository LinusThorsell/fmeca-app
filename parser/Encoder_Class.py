import json
import DataClass
#from CLI_class import debug_print
import DebugFile
import requests

#from CLI_class import debug_print
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
    
    def delete_from_database(self,project,folder):
        
        print("Deleting project: ",self._url+folder+project)
        
        response = requests.delete(self._url+folder+project)
        DebugFile.debug_print("Response from delete = ",response.text)
    
    def send_to_database(self,object,folder):
        string = json.dumps(object,cls=ComplexEncoder,indent=4)
        DebugFile.debug_print(string)
        DebugFile.debug_print("Sending to: \n\n", self._url+ folder)
        response = requests.post(self._url+ folder,string,headers=self._headers)
        DebugFile.debug_print("Response from send = ",response.text)