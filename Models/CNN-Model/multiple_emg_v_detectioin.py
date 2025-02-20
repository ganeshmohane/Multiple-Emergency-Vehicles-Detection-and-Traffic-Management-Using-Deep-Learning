import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model

# Load your model
model = load_model(r"C:\Users\Ganesh\Downloads\cnn3class.h5")  # Replace with your actual model path

# Define types of emergency vehicles with priorities
EMERGENCY_VEHICLE_PRIORITY = {
    'ambulance': 3,
    'fire_truck': 2,
    'police_car': 1
}

# Paths to video files for each lane
video_feeds = [
    r"C:\Users\Ganesh\Downloads\TestVideo.mp4",  # Replace with your actual video path for lane 1
    r"C:\Users\Ganesh\Downloads\TrimmedVideo.avi",  # Replace with your actual video path for lane 2
    r"C:\Users\Ganesh\Downloads\TrimmedVideo.avi",  # Replace with your actual video path for lane 3
    r"C:\Users\Ganesh\Downloads\TrimmedVideo.avi"   # Replace with your actual video path for lane 4
]

# Initialize video captures for each lane
video_captures = [cv2.VideoCapture(video) for video in video_feeds]

# Placeholder function for traffic signal control
def control_traffic_signal(lane, action):
    if action == 'green':
        print(f"Changing lane {lane} to green.")
    elif action == 'red':
        print(f"Changing lane {lane} to red.")

# Function to detect emergency vehicles
def detect_emergency_vehicle(frame):
    frame_resized = cv2.resize(frame, (128, 128))  # Resize to match the model input shape
    frame_array = np.expand_dims(frame_resized, axis=0)  # Add batch dimension
    prediction = model.predict(frame_array)
    
    # Decode prediction into vehicle type
    vehicle_type = np.argmax(prediction, axis=1)
    
    vehicle_dict = {0: 'ambulance', 1: 'fire_truck', 2: 'police_car', 3: 'none'}
    
    return vehicle_dict[vehicle_type[0]]

# Function to handle multiple emergency vehicle detections and prioritize based on rules
def prioritize_vehicles(detections):
    for vehicle in detections:
        lane = vehicle['lane']
        signal_state = vehicle['signal_state']
        print(f"Emergency vehicle detected: {vehicle['type']} in lane {lane}, distance: {vehicle['distance']}m.")
        
        if signal_state == 'red':
            print(f"Changing lane {lane} to green for emergency vehicle.")
            control_traffic_signal(lane, 'green')
            # Set all other lanes to red
            for other_lane in range(1, 5):
                if other_lane != lane:
                    control_traffic_signal(other_lane, 'red')
            time.sleep(10)  # Hold green for 10 seconds
            control_traffic_signal(lane, 'red')
            break  # Exit after processing one vehicle to prevent multiple signals

# Main loop for processing video feeds and controlling signals
def process_feeds():
    while True:
        detections = []
        
        for i, capture in enumerate(video_captures):
            ret, frame = capture.read()
            
            if not ret:
                continue  # Skip to the next feed if there's no frame
            
            vehicle_type = detect_emergency_vehicle(frame)
            
            if vehicle_type != 'none':
                # Simulate distance and signal state (replace with actual sensor data in real implementation)
                distance = np.random.randint(20, 200)  # Example: generate random distance
                signal_state = 'red'  # Simulate red signal, replace with real signal state
                detections.append({
                    'lane': i + 1,
                    'type': vehicle_type,
                    'distance': distance,
                    'signal_state': signal_state
                })
                
                # Display predicted classes on the frame
                cv2.putText(frame, f'Predicted Class: {vehicle_type}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Red text
                
                # Show the frame
                cv2.imshow(f'Lane {i + 1}', frame)

        if detections:
            prioritize_vehicles(detections)
        else:
            print("No emergency vehicles detected.")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Exit on 'q' key press

# Release video captures and clean up
def cleanup():
    for capture in video_captures:
        capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        process_feeds()
    except KeyboardInterrupt:
        print("Stopping traffic control system.")
        cleanup()
