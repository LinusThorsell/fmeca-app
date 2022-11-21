debug = False
send = False

def debug_print(*object_to_be_printed):
    global debug
    if(debug == True):
        print(*object_to_be_printed)