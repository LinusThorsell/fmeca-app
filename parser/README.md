# Parser

## Prerequisites

First make sure that a rest api server is live in the backend. This is necessary \
because the parser send the parsed data in json format to endpoint in the api \
which in turn forwards it to the database.

## Commands and Arguments

#### Always start with:

_/parser.py_

#### Commands:

- **add** \
  _Adds project specified in _-path* with name in *-tag* to database specified in *-c\__ \
  _-c* <'path to config'> *-OPTIONAL* \ *-path* <'path to system infrastructure'> *-REQUIRED* \
   *-tag* <'project name'> *-OPTIONAL

- **remove** \
  _Removes the project specified in _-tag* from database* \
   _-c_ <'path to config'> _-OPTIONAL_ \
   _-tag_ <'project name'> _-REQUIRED_

- **print** \
  _Prints the data in the form it will be sent to the database_ \
  _-path_ <'path to system infrastructure'> \ _-REQUIRED_ *-tag* <'project name'> *-OPTIONAL

#### Example:

- **/parser/parser.py -c Linus_DB.xml add -path "Projects/Project_3/ -tag "projectname"**
- **/parser/parser.py remove -tag "projectname"**
- **/parser/parser.py print -tag "projectname-path "Projects/Project_3/ -tag "projectname"**
