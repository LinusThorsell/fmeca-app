import json
import DataClass
import DebugFile
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
    
    def config_api(self,URL):
        self._url = URL

    def get_json(self,object):
        string = json.dumps(object,cls=ComplexEncoder,indent=4)
        return string
        
    
    def delete_from_database(self,project,folder):
        
        print("Deleting project: ",self._url + folder + project)
        
        response = requests.delete(self._url + folder + project)
        if response.status_code == 204:
            DebugFile.success_print("The project \"{0}\" was succesfully removed".format(project))
        elif response.status_code == 404:
            DebugFile.error_print("Error 404, There were no project with the name \"{0}\"".format(project))
        else:
            DebugFile.error_print("Unhandled statuscode code: {0}".format(response.status_code))
            DebugFile.warning_print("The response was:\n + {0}".format(response.text))
    
    def send_to_database(self,project_segment,folder):
        string = self.get_json(project_segment)
        #DebugFile.debug_print(string)
        DebugFile.debug_print("Sending to: \n\n", self._url + folder)
        response = ""
        try:
            response = requests.post(self._url + folder,string,headers=self._headers)
            if response.status_code == 201:
                DebugFile.success_print("The project_segment was sucessfully sent to the database.")
            elif response.status_code == 400:
                if "project with this name already exists" in response.text:
                    DebugFile.error_print("Error bad request: 400, project with this name already exists!")
            else:
                DebugFile.warning_print("Unhandled status code {0}".format(response.status_code))
        except requests.exceptions.ConnectionError:
            DebugFile.error_print("Failed to connect to the database/API at " + (self._url + folder))

        except Exception as e: 
            DebugFile.error_print("Something went wrong: {0}".format(e))


    def print_project(self,project_segment):
        string = self.get_json(project_segment)
        print(string)