import xml.etree.ElementTree as ET
class Paths:
    def __init__(self):
        self.catalogs = []
        self._paths = set()
        self._dictionary = {}
    
    def build_full_path(self,index):
        #print("The catalog")
        #print(self.catalogs[c])
        path = ""
        dictionary = self.catalogs[index][1]

        #print("The content of the lists dictionary:")
        #print(self.catalogs[index][1])
        
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
        #print(path)
        dictionary["path"] = path

    def build_relative_paths(self,index):
        #print("PATH:")
        #print(self.catalogs[index][1])
        #print(self.catalogs[index][1]["path"])
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

        #print(newpath)
        self._paths.add(newpath)

    def initial_path(self,path):
        self.fc_path = path + "infrastructure/fc/system.xml"
        self.mc_path = path + "infrastructure/mc/system.xml"
        
    def get_paths(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        
        #self.catalogs = []
        for obj in root:
        #    print(obj.tag, obj.attrib)
            if(obj.tag == "idb" and ".xml" not in obj.attrib["value"]):
                self._dictionary[obj.attrib["key"]] = obj.attrib["value"]
            else:
                tuple = (obj.tag,obj.attrib)
                self.catalogs.append(tuple)
        #print("\n\n\n")

        #print("Content of self._dicitonary: ")
        #print(self._dictionary)
        #print("\n\n\n")
        #print("Content of catalogs: ")
        #print(self.catalogs)
    
        counter = 0
        while counter < len(self.catalogs):
            self.build_full_path(counter)
            self.build_relative_paths(counter)
            counter +=1

        #print("KATALOGEN")
        #print(self.catalogs)