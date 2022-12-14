import json
import dataclass as dataclass
import debugfile as debugfile
import requests
import threading
import time
import sys

##This class is used in json to and returns the object as a string assuming you have overloded the "reprJSON" memberfunction in the class you want to serialize
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

#This class is used to encode and send the project to database
class Encoder:
    def __init__(self):
        self._headers = {"Content-Type":"application/json"}
        self._url = 'http://127.0.0.1:8000/'
        self.Project = ""
        self.send_succeded = True
        self.project_already_exists = False
        self.sema = threading.Semaphore(0)
        self.finished_request = False
        self.finished_request_lock = threading.Lock()
        self.loading_steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.thread = ""


    def config_api(self,URL):
        debugfile.debug_print("Changing URL from {0} to {1}".format(self._url, URL))
        self._url = URL

    ##This function returns the object as a string
    def get_json(self,object):
        string = json.dumps(object,cls=ComplexEncoder,indent=4)
        return string
        
    ##This is a loading screen, this will be running using multithreading
    def loading_screen(self,string,color = debugfile.ENDC):
        many_steps = len(self.loading_steps)
        counter = 0
        while True:
            self.finished_request_lock.acquire()
            if self.finished_request == True:
                self.finished_request_lock.release()
                break
            self.finished_request_lock.release()
            print(("\r" + string + color + " {0}" + debugfile.ENDC).format(self.loading_steps[counter % many_steps]), end="" ,flush=True)
            time.sleep(0.33333)
            counter += 1
        self.sema.release()

    def set_finished_request(self,boolean : bool):
        self.finished_request_lock.acquire()
        self.finished_request = boolean
        self.finished_request_lock.release()

    def delete_from_database(self,project,folder):
        
        try:
            self.thread = threading.Thread(target=self.loading_screen,args=("Deleting from database",debugfile.CRED))
            self.thread.start()
            response = requests.delete(self._url + folder + project)
            self.set_finished_request(True)
            self.sema.acquire()
            if response.status_code == 204:
                debugfile.success_print("\rThe project \"{0}\" was succesfully removed at {1}".format(project,self._url + folder + project))
            elif response.status_code == 404:
                debugfile.error_print("\rError 404, There were no project with the name \"{0}\"".format(project))
            else:
                debugfile.error_print("\rUnhandled statuscode code: {0}".format(response.status_code))
        except requests.exceptions.ConnectionError:
            self.set_finished_request(True)
            self.sema.acquire()
            debugfile.error_print("\rWas not able to connect to database when trying to remove project \"{0}\"".format(project))
        
    def send_to_database(self,project_segment,folder):
        string = self.get_json(project_segment)
        
        debugfile.debug_print("Sending to: \n\n", self._url + folder)
        response = ""
        try:
            self.thread = threading.Thread(target=self.loading_screen,args=("Sending to database",debugfile.OKGREEN))
            self.thread.start()
            response = requests.post(self._url + folder,string,headers=self._headers)
            self.set_finished_request(True)
            self.sema.acquire()
            if response.status_code == 201:
                debugfile.success_print("\rThe project_segment was sucessfully sent to the database at {0}.".format(self._url+folder))
            elif response.status_code == 200:
                debugfile.success_print("\rThe project_segment was sucessfully sent to the database at {0}.".format(self._url+folder))
            elif response.status_code == 400:
                if "project with this name already exists" in response.text:
                    debugfile.error_print("\rError bad request: 400, project with this name already exists!")
                    debugfile.error_print("Aborting send to database and exiting program")
                    exit()                        
            elif response.status_code == 500:
                    debugfile.error_print("\rInternal server error when sending to {0}".format(self._url+folder))
                    exit()
            else:
                debugfile.warning_print("\rUnhandled status code {0}".format(response.status_code))
                exit()
        except requests.exceptions.ConnectionError:
            self.set_finished_request(True)
            self.sema.acquire()
            debugfile.error_print("\rFailed to connect to the database/API at " + (self._url + folder))

        except requests.exceptions.MissingSchema:
            self.set_finished_request(True)
            self.sema.acquire()
            debugfile.error_print("\rThe URL: {0} is not a valid URL.".format(self._url + folder))

        except Exception as e: 
            self.set_finished_request(True)
            self.sema.acquire()
            debugfile.error_print("\rSomething went wrong: {0}".format(e))

    def print_project(self,project_segment):
        string = self.get_json(project_segment)
        print(string)