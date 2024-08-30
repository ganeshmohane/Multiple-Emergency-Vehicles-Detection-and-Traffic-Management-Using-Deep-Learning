# How Traffic Light work is that it stays neutral between night 
# then continues from red to amber then green and then amber and whole loop continues

import time

def traffic_light():
    if night:
        print("In Night almost all traffic lights are on ideal mode")
        print("🟡 Orange : Alert")
        exit()

    while day:    
        print("🔴 Red : Stop")
        amber(3)
        print("🟢 Green : Go")
        amber(5)

def amber(n):
    time.sleep(n)
    print("🟡 Orange : Alert")
    time.sleep(2)
    # if emg_vehicle:
    #     swiftpass()
        # amber(2)
        

def swiftpass():
    print("🟢 Green : Safe Passage for emeregency vehicles")
    time.sleep(6)

day = True  
night = False
emg_vehicle = True
traffic_light()

