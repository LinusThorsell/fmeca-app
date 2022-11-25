import time
import sys

#Make print of a certain color by adding color + string + endc
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
CRED = '\033[91m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
OKBLUE = '\033[94m'
HEADER = '\033[95m'
OKCYAN = '\033[96m'

debug = False
slow_mode = False


def error_print(string):
    print(CRED + string + ENDC)

def warning_print(string):
    print(WARNING + string + ENDC)

def success_print(string):
    print(OKGREEN + string + ENDC)

def blue_print(string):
    print(OKBLUE + string + ENDC)

def underline_print(string):
    print(UNDERLINE + string + ENDC)

def underline_print(string):
    print(UNDERLINE + string + ENDC)



#def test_print(string):
    #print(testblink+ "hrj" + ENDC)
    #while True:
         #print("hej")
    #     sys.stdout.write('\033[2K\033[1G')
    #     print("Hello world", end =" ")
         #time.sleep(1)

def rainbow_print(string):
    lines = string.split("\n")
    colors = [YELLOW, OKBLUE, OKGREEN, CRED, MAGENTA]
    for i in range(0, len(lines)):
        print(colors[i % len(colors)] + lines[i] + ENDC)

def rainbow_rainbow_print(string):
    colors = [YELLOW, OKBLUE, OKGREEN, CRED, MAGENTA]
    for i in range(0, len(string)):
        print(colors[i % len(colors)] + string[i] + ENDC, end = "")


def debug_print(object_to_be_printed, color = ENDC):
    global debug
    if(debug == True):
        print(color)
        print(object_to_be_printed)
        print(ENDC)
            
def debug_print_list(object_to_be_printed, color = ENDC):
    global debug
    if(debug == True):
        try:
            #if color != ENDC:
            for args in object_to_be_printed:
                string = color + str(args)
                print(string)
            print(ENDC)
            
        except Exception:
            error_print("Couldnt print the object in debug_print")