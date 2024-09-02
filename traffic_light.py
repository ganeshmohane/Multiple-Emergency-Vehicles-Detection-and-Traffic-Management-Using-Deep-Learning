# How Traffic Light work is that it stays neutral between night 
# then continues from red to amber then green and then amber and whole loop continues

import time

def traffic_light():
    if night:
        print("In Night almost all traffic lights are on idle mode")
        print("\033[5m\033[33m🟡 Orange : Alert\033[0m")
        exit()

    while day:    
        red(1)
        green(1)
        orange(1)
        swiftpass()
      
def red(n):
    print("\033[5m\033[31m🔴 Red : Stop\033[0m")
    time.sleep(n)
    
def green(n):
    print("\033[5m\033[32m🟢 Green : Go\033[0m")
    time.sleep(n)
    
def orange(n):
    print("\033[5m\033[33m🟡 Orange : Alert\033[0m")
    time.sleep(2)

def swiftpass():
    print("Emergency Vehicle Detected")
    print("🟢 Green : Safe Passage for emergency vehicles")
    time.sleep(6)
    orange(5)


day =  True
night = False
traffic_light()

