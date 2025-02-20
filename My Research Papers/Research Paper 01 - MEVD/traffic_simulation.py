import time
from ultralytics import YOLO

# https://universe.roboflow.com/ganesh-lbmbj/indian-emergency-vehicles-dataset/model/1?youtube=https://www.youtube.com/watch?v%3DijLZBoAJ94s%26t%3D6s

# Load YOLO model
model_path = r"D:\Desktop\PROJs\Multiple Emergency Vehicles Detection and Traffic\SwiftPass-AI-Powered-Emergency-Traffic-Control\Model\YOLO-Trained-Model\content\runs\detect\train\weights\best.pt"
model = YOLO(model_path)

# Emergency vehicle classes
emergency_classes = ["ambulance", "police", "firetruck"]

# Initialize vehicle count and emergency vehicle count for each lane
lane_vehicle_counts = {f"lane{i+1}": {"vehicle_count": 0, "emg_vehicle_count": 0} for i in range(4)}

# Paths to images for each lane (replace with actual camera feeds)
lane_image_paths = {
    "lane1": r"D:\Desktop\Yolo Model Test\test_img3.jpg",
    "lane2": r"D:\Desktop\Yolo Model Test\test_img4.jpeg",
    "lane3": r"D:\Desktop\Yolo Model Test\test_img5.jpeg",
    "lane4": r"D:\Desktop\Yolo Model Test\test_img2.jpg"
}

# Function to detect vehicles and emergency vehicles for each lane
def detect_vehicles_for_lane(image_path, lane_name):
    results = model.predict(source=image_path, conf=0.25, save=True)
    vehicle_count = 0
    emg_vehicle_count = 0

    for box in results[0].boxes:
        vehicle_count += 1
        class_idx = int(box.cls.item())
        if results[0].names[class_idx] in emergency_classes:
            emg_vehicle_count += 1

    lane_vehicle_counts[lane_name]["vehicle_count"] = vehicle_count
    lane_vehicle_counts[lane_name]["emg_vehicle_count"] = emg_vehicle_count

    print(f"Lane {lane_name} - Detected {vehicle_count} vehicles, {emg_vehicle_count} emergency vehicles.")

# Function to show traffic light signals
def show_signals(lane_signals):
    print("\nCurrent Signal Status:")
    for idx, signal in enumerate(lane_signals):
        if signal == 'Red':
            print(f"Lane {idx + 1}: 🔴 Red : Stop")
        elif signal == 'Green':
            print(f"Lane {idx + 1}: 🟢 Green : Go")
        elif signal == 'Amber':
            print(f"Lane {idx + 1}: 🟡 Amber : Alert")
    print("")

# Function to simulate traffic lights
def traffic_light_simulation():
    num_lanes = 4
    base_timer = 5
    amber_time = 3

    while True:
        print("Updating traffic lights for a new cycle...")
        emergency_handled = False

        for i in range(num_lanes):
            current_lane = f"lane{i + 1}"
            vehicle_count = lane_vehicle_counts[current_lane]["vehicle_count"]
            green_time = base_timer + (vehicle_count * 2)
            # Add this print statement to show timings
            print(f"Lane {current_lane}: Base time = {base_timer}s, Added time = {vehicle_count * 2}s, Total green time = {green_time}s")

            if not emergency_handled:
                emergency_lanes = [
                    lane for lane, counts in lane_vehicle_counts.items()
                    if counts["emg_vehicle_count"] > 0
                ]
                if emergency_lanes:
                    emergency_lane = emergency_lanes[0]
                    print(f"Emergency detected! Giving priority to {emergency_lane}.")
                    show_signals(['Green' if lane == emergency_lane else 'Red' for lane in lane_vehicle_counts])
                    time.sleep(base_timer)
                    emergency_handled = True
                    continue

            # Default logic for normal lanes
            lane_signals = ['Red' for _ in range(num_lanes)]
            lane_signals[i] = 'Green'
            show_signals(lane_signals)
            time.sleep(green_time)

            lane_signals[i] = 'Amber'
            show_signals(lane_signals)
            time.sleep(amber_time)

# Main function
def main():
    while True:
        print("Starting vehicle detection for all lanes...")
        for lane, image_path in lane_image_paths.items():
            detect_vehicles_for_lane(image_path, lane)
        print("Detection complete. Starting traffic light simulation.")
        traffic_light_simulation()

if __name__ == "__main__":
    main()
