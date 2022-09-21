#!/usr/bin/env python3

from ctypes import sizeof
import sys, string
from parser_class import Parser

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

##För debug
if(string.ascii_lowercase(sys.argv[1]) == "print"):
    pass

##För att lägga till ett projekt i databasen
elif(string.ascii_lowercase(sys.argv[1]) == "add"):
    pass

elif(string.ascii_lowercase(sys.argv[1]) == "parse"):
    Parser.parse(sys.argv[2])

## För att ta bort ett projekt från databasen
elif(string.ascii_lowercase(sys.argv[1]) == "delete"):
    pass
elif string.ascii_lowercase(sys.argv[1] == "-c"):
    pass

##efter denna ska en path till en fil med databaskonfig vara sen
elif string.ascii_lowercase(sys.argv[1] == "-d"):
    pass

else:
    pass


if (__name__ == "__main__"):
    main()


#parser.py 
#print, add, -c ,-d, -path, pathen