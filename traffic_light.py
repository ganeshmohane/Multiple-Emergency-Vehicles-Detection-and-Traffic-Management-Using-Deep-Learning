# Traditional Traffic Light

import time

def print_colored(text, color):
    # ANSI escape codes for colors
    colors = {
        "red": "\033[91m",    # Red
        "green": "\033[92m",  # Green
        "orange": "\033[93m"  # Orange
    }
    reset = "\033[0m"  # Reset color

    print(f"{colors[color]}{text}{reset}")

def traffic_light():
    for i in range(0, 24):
        print('Traffic Light 🚥')
        if emg_detected:
            print_colored("Green light (Go for Emergency Vehicle 🚑)", "green")
        else :
            print_colored("Red light (Stop)", "red")
        time.sleep(6)

        print_colored("Green light (Go)", "green")
        time.sleep(6)

        print_colored("Orange light (Be ready)", "orange")
        time.sleep(2)

emg_detected = False
traffic_light()


