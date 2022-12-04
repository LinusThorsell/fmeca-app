import json
import DataClass
import DebugFile
import requests
import threading
import time
import sys
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
        self.send_succeded = True
        self.project_already_exists = False
        self.sema = threading.Semaphore(0)
        self.finished_request = False
        self.finished_request_lock = threading.Lock()
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.thread = ""
    
    def config_api(self,URL):
        self._url = URL

    def get_json(self,object):
        string = json.dumps(object,cls=ComplexEncoder,indent=4)
        return string
        
    def loading_screen(self,string):
    #print("Press enter to stop the loading")    
        many_steps = len(self.steps)
        counter = 0
        while True:
            self.finished_request_lock.acquire()
            if self.finished_request == True:
                self.finished_request_lock.release()
                break
            self.finished_request_lock.release()
            #print(steps[counter % many_steps], end="" ,flush=True)
            sys.stdout.write("\r"+string + " {0}".format(self.steps[counter % many_steps]))
            sys.stdout.flush()        
            time.sleep(0.5)
            counter += 1
        self.sema.release()

    def set_finished_request_and_wait_for_thread(self,boolean):
        self.finished_request_lock.acquire()
        self.finished_request = boolean
        self.finished_request_lock.release()
        self.sema.acquire()

    def delete_from_database(self,project,folder):
        
        try:
            self.thread = threading.Thread(target=self.loading_screen,args=("Deleting from database",))
            self.thread.start()
            response = requests.delete(self._url + folder + project)
            if response.status_code == 204:
                self.set_finished_request_and_wait_for_thread(True)
                DebugFile.success_print("\rThe project \"{0}\" was succesfully removed at {1}".format(project,self._url + folder + project))
            elif response.status_code == 404:
                self.set_finished_request_and_wait_for_thread(True)

                DebugFile.error_print("\rError 404, There were no project with the name \"{0}\"".format(project))
            else:
                self.set_finished_request_and_wait_for_thread(True)
                DebugFile.error_print("\rUnhandled statuscode code: {0}".format(response.status_code))
        except requests.exceptions.ConnectionError:
            self.set_finished_request_and_wait_for_thread(True)
            DebugFile.error_print("\rWas not able to connect to database when trying to remove project \"{0}\"".format(project))
        
    def send_to_database(self,project_segment,folder):
        string = self.get_json(project_segment)
        
        DebugFile.debug_print("Sending to: \n\n", self._url + folder)
        response = ""
        try:
            self.thread = threading.Thread(target=self.loading_screen,args=("Sending to database",))
            self.thread.start()
            response = requests.post(self._url + folder,string,headers=self._headers)
            print("Hej")
            if response.status_code == 201:
                self.set_finished_request_and_wait_for_thread(True)
                DebugFile.success_print("\rThe project_segment was sucessfully sent to the database at {0}.".format(self._url+folder))
            elif response.status_code == 400:
                self.set_finished_request_and_wait_for_thread(True)
                if "project with this name already exists" in response.text:
                    DebugFile.error_print("\rError bad request: 400, project with this name already exists!")
                    DebugFile.error_print("Aborting send to database and exiting program")
                    exit()                        
            elif response.status_code == 500:
                    self.set_finished_request_and_wait_for_thread(True)
                    DebugFile.error_print("\rInternal server error when sending to {0}".format(self._url+folder))
                    exit()
            else:
                self.set_finished_request_and_wait_for_thread(True)
                DebugFile.warning_print("\rUnhandled status code {0}".format(response.status_code))
                exit()
        except requests.exceptions.ConnectionError:
            self.set_finished_request_and_wait_for_thread(True)
            DebugFile.error_print("\rFailed to connect to the database/API at " + (self._url + folder))

        except Exception as e: 
            self.set_finished_request_and_wait_for_thread(True)
            DebugFile.error_print("\rSomething went wrong: {0}".format(e))

    def print_project(self,project_segment):
        string = self.get_json(project_segment)
        print(string)