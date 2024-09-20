import time

# Define the traffic light and emergency vehicle priority algorithm functions
def emergency_vehicle_priority_algorithm(detected_vehicles):
    if len(detected_vehicles) == 0:
        return "No Emergency Vehicles Detected"

    if len(detected_vehicles) > 1:
        detected_vehicles = prioritize_vehicles(detected_vehicles)

    for vehicle in detected_vehicles:
        if is_next_signal_green(vehicle):
            continue
        else:
            change_signal_to_green(vehicle.lane, duration=10)
        continue_next_signal(vehicle)

    return "Emergency Vehicles Processed"

def prioritize_vehicles(vehicles):
    vehicles.sort(key=lambda x: (x.distance_to_intersection, x.severity, x.speed))
    return vehicles

def is_next_signal_green(vehicle):
    current_signal = get_current_signal_state(vehicle.lane)
    return current_signal == "green"

def change_signal_to_green(lane, duration):
    set_signal(lane, "green")
    print(f"Signal changed to green for lane {lane} for {duration} seconds")
    wait(duration)
    reset_signal(lane)

def continue_next_signal(vehicle):
    current_signal = get_current_signal_state(vehicle.lane)
    if current_signal != "green":
        reset_signal(vehicle.lane)

def get_current_signal_state(lane):
    return "red"  # Simplified assumption

def set_signal(lane, state):
    print(f"Setting signal for lane {lane} to {state}")

def reset_signal(lane):
    print(f"Resetting signal for lane {lane} to normal operation")
    set_signal(lane, "red")

def wait(duration):
    print(f"Waiting for {duration} seconds")
    time.sleep(duration)

# Vehicle class for simulation
class Vehicle:
    def __init__(self, lane, distance_to_intersection, severity, speed):
        self.lane = lane
        self.distance_to_intersection = distance_to_intersection
        self.severity = severity
        self.speed = speed

# Simple traffic light demonstration with emergency vehicle detection
def traffic_light_simulation():
    lanes = ["A", "B", "C", "D"]

    # Initial traffic light states
    for lane in lanes:
        set_signal(lane, "red")

    # Simulate normal traffic light operation
    print("Normal traffic light operation")
    time.sleep(2)
    for lane in lanes:
        set_signal(lane, "green")
        wait(2)
        set_signal(lane, "yellow")
        wait(1)
        set_signal(lane, "red")

    # Trigger emergency vehicle detection
    print("Emergency vehicle detected!")
    detected_vehicles = [Vehicle("A", 100, 5, 60)]  # Example vehicle detected
    emergency_vehicle_priority_algorithm(detected_vehicles)

    # Continue normal operation
    print("Resuming normal traffic operation")
    for lane in lanes:
        set_signal(lane, "green")
        wait(2)
        set_signal(lane, "yellow")
        wait(1)
        set_signal(lane, "red")

# Run the simulation
if __name__ == "__main__":
    traffic_light_simulation()
