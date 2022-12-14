import xml.etree.ElementTree as ET

#Parse the paths form system.xml
class Paths:
    def __init__(self):
        self.catalogs = []
        self._paths = set()
        self._dictionary = {}
    
    def build_full_path(self,index):
        path = ""
        dictionary = self.catalogs[index][1]
        
        if "value" in dictionary:
            path = dictionary["value"]
        elif "dir" in dictionary:
            path = dictionary["dir"]
        elif "src" in dictionary:
            path = dictionary["src"]
        elif "conf" in dictionary:
            path = dictionary["conf"]
        else:
            return "nopath"       
        
        if "[acs_src]" in path:
            path = "nopath"
        else:
            while "[" and "]" in path:         
                if(path.count("[") == 1 and "[root]" in path): 
                    break
                for temp in self._dictionary:
                    if ( "[" + temp + "]") in path:
                        path = path.replace("[" + temp + "]",self._dictionary[temp])
        dictionary["path"] = path

    def build_relative_paths(self,index):
        temppath = self.catalogs[index][1]["path"]
        if temppath == "nopath":
            return
        templist = temppath.split("/")
        
        newpath = ""
        counter = 3
        if len(templist) >= 3:       
            while counter < len(templist):
                
                newpath += templist[counter]
                if counter+1 != len(templist):
                    newpath += "/" 
                counter +=1
        else:
            return

        self._paths.add(newpath)

    def initial_path(self,path):
        self._inital_path = path
        self.fc_path = path + "infrastructure/fc/system.xml"
        self.mc_path = path + "infrastructure/mc/system.xml"
        
    def get_paths(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        for obj in root:
            if(obj.tag == "idb" and ".xml" not in obj.attrib["value"]):
                self._dictionary[obj.attrib["key"]] = obj.attrib["value"]
            else:
                tuple = (obj.tag,obj.attrib)
                self.catalogs.append(tuple)
    
        counter = 0
        while counter < len(self.catalogs):
            self.build_full_path(counter)
            self.build_relative_paths(counter)
            counter +=1
        
    def add__outer_folders_to_paths(self):
        splited_path = self._inital_path.split("/")
        many_subdir_and_files = len(splited_path)
        tempset = set()
        splited_path.pop()
        splited_path.pop()
        for paths in self._paths:
            string = "/"
            string = string.join(splited_path)
            string += "/" + paths           
            tempset.add(string)
    
        self._paths = tempset

        
                
            