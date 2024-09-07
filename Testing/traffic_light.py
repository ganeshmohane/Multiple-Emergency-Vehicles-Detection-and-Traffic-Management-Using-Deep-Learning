# How Traffic Light work is that it stays neutral between night 
# then continues from red to amber then green and then amber and whole loop continues


# Main issues with traditonal Traffic Lights - 
'''
Fixed timing: The timing for each light phase is often fixed, which can lead to inefficient traffic flow, especially during peak hours.
Limited adaptability: Traditional traffic lights are not able to adapt to changing traffic conditions in real time.
Inefficient resource allocation: The fixed timing of traditional traffic lights can result in inefficient allocation of resources, such as road space.
Susceptible to congestion: If traffic volume exceeds the capacity of the intersection, traditional traffic lights can become overwhelmed and lead to congestion.
'''


# Points - 
# 1. Adjust Traffic Light Timing optimizing it where it requires most
# 2. Detecting Emergency Vehicles & Adjusting Traffic Lights 
# 3. Intelligent Pedestrian Crossing - Using Camera or Button input
# 4. if someone using Google Map they can see Ambulances

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

