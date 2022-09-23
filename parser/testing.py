#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()
parsed_data = []
dictionary = {}



# Parse paths from system.xml
# Check if path exists
# Check if file is xml
# If so parse file


print("\n\n\n")
for obj in root:
    print(obj.tag, obj.attrib)
    if(obj.tag == "idb"):
        dictionary[obj.attrib["key"]] = obj.attrib["value"]
#    for s in obj.data.items():
#        print(s[0] + " " + s[1])
print("\n\n\n")

print(dictionary)
