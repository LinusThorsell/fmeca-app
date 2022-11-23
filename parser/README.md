# Parser
## Prerequisites 

First make sure that a rest api server is live in the backend. This is necessary \
because the parser send the parsed data in json format to endpoint in the api \
which  in turn forwards it to the database.

## Commands and Arguments

#### Always start with: 
_/parser.py_

#### Commands:

<<<<<<< HEAD
debug
Args(0)
Explanation:
Prints information to terminal


=======
- **add** \
_Adds project specified in _-path_ with name in _-tag_ to database specified in _-c__ \
_-c_ <'path to config'> _-OPTIONAL_ \ _-path_ <'path to system infrastructure'> _-REQUIRED_ \
 _-tag_ <'project name'> _-REQUIRED_

- **remove** \
_Removes the project specified in _-tag_ from database_ \
 _-c_ <'path to config'> _-OPTIONAL_ \
 _-tag_ <'project name'> _-REQUIRED_

- **print** \
_Prints the data in the form it will be sent to the database_ \
_-path_ <'path to system infrastructure'> _-REQUIRED_ 
 
#### Example:
 
 - */parser/parser.py -c Linus_DB.xml -path "Project 2"/infrastructure -tag "name"*
>>>>>>> master
