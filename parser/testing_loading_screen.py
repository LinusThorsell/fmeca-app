import threading
import time
import sys
steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]

sema = threading.Semaphore(0)
#val_sema = threading.Semaphore(0)

stop = False

def loading_screen():
    #print("Press enter to stop the loading")    
    global steps
    global sema
    many_steps = len(steps)
    counter = 0
    time.sleep(1)
    while True and stop == False:
        #print(steps[counter % many_steps], end="" ,flush=True)
        sys.stdout.write("\r"+"Loading {0}".format(steps[counter % many_steps]))
        sys.stdout.flush()        
        time.sleep(0.5)
        counter += 1
    sema.release()
new_thread = threading.Thread(target=loading_screen)
new_thread.start()
input("Press any key to stop the thread\n")
stop = True
sema.acquire()