import DebugFile
debug = False

def debug_print(*object_to_be_printed):
    global debug
    if(DebugFile.debug == True):
        print(*object_to_be_printed)