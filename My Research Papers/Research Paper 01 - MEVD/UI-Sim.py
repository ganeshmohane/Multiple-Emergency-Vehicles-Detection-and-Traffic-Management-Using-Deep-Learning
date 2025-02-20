import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk

# Load YOLO model
model_path = r"D:\Desktop\PROJs\Multiple Emergency Vehicles Detection and Traffic\SwiftPass-AI-Powered-Emergency-Traffic-Control\Model\YOLO-Trained-Model\content\runs\detect\train\weights\best.pt"
model = YOLO(model_path)

# Emergency vehicle classes
emergency_classes = ["ambulance", "police", "firetruck"]

# Initialize vehicle count, emergency count, and signal status for each lane
lane_vehicle_counts = {
    f"lane{i+1}": {
        "vehicle_count": 0, 
        "emg_vehicle_count": 0, 
        "signal": "🔴 Red", 
        "time": "0 sec"
    } 
    for i in range(4)
}

# Paths to images for each lane
lane_image_paths = {
    "lane1": "test_img3.jpg",
    "lane2": "test_img.jpg",
    "lane3": "test_img2.jpg",
    "lane4": "test_img6.png"
}

# Tkinter UI Setup
root = tk.Tk()
root.title("Traffic Control System")
root.geometry("1200x800")

lane_frames = {}
img_labels = {}

# Function to create a frame for each lane
def create_lane_frame(lane_name, image_path, row, column):
    lane_frame = Frame(root, bd=2, relief="solid")
    lane_frame.grid(row=row, column=column, padx=30, pady=30, sticky="nsew")

    lane_info = Label(
        lane_frame,
        text=f"{lane_name.capitalize()} | Vehicles: {lane_vehicle_counts[lane_name]['vehicle_count']} | "
             f"Emergency: {lane_vehicle_counts[lane_name]['emg_vehicle_count']}\n"
             f"Signal: {lane_vehicle_counts[lane_name]['signal']} | Time: {lane_vehicle_counts[lane_name]['time']}",
        font=("Helvetica", 16),
        justify="left"
    )
    lane_info.pack()

    placeholder_image = Image.open(image_path)
    placeholder_image = placeholder_image.resize((400, 300))
    img = ImageTk.PhotoImage(placeholder_image)
    img_label = Label(lane_frame, image=img)
    img_label.image = img
    img_label.pack()

    lane_frames[lane_name] = lane_info
    img_labels[lane_name] = img_label

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

create_lane_frame("lane1", lane_image_paths["lane1"], 0, 0)
create_lane_frame("lane2", lane_image_paths["lane2"], 0, 1)
create_lane_frame("lane3", lane_image_paths["lane3"], 1, 0)
create_lane_frame("lane4", lane_image_paths["lane4"], 1, 1)

# Function to draw bounding boxes on detected vehicles
def draw_bounding_boxes(image_path, lane_name):
    image = cv2.imread(image_path)
    results = model.predict(source=image_path, conf=0.25)
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_idx = int(box.cls.item())
        label = results[0].names[class_idx]
        color = (0, 255, 0) if label not in emergency_classes else (0, 0, 255)
        
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Resize the image to match the original size (400x300)
    resized_image = cv2.resize(image, (400, 300))
    
    return resized_image

# Function to update UI with latest vehicle counts and signals
def update_ui():
    for lane, info in lane_frames.items():
        # Get the current signal
        signal = lane_vehicle_counts[lane]["signal"]
        
        # Define the color based on the signal
        signal_color = "green" if signal == "🟢 Green" else "red"
        
        info.config(
            text=f"{lane.capitalize()} | Vehicles: {lane_vehicle_counts[lane]['vehicle_count']} | "
                 f"Emergency: {lane_vehicle_counts[lane]['emg_vehicle_count']}\n"
                 f"Signal: {signal} | Time: {lane_vehicle_counts[lane]['time']}",
            fg=signal_color  # Set the text color to green or red based on the signal
        )

        # Display image with bounding boxes
        img_path = lane_image_paths[lane]
        img_with_boxes = draw_bounding_boxes(img_path, lane)
        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)))
        img_labels[lane].config(image=img)
        img_labels[lane].image = img

    root.after(1000, update_ui)



# Function to detect vehicles and emergency vehicles for each lane
def detect_vehicles_for_lane(image_path, lane_name):
    results = model.predict(source=image_path, conf=0.25)
    vehicle_count = 0
    emg_vehicle_count = 0

    for box in results[0].boxes:
        vehicle_count += 1
        class_idx = int(box.cls.item())
        if results[0].names[class_idx] in emergency_classes:
            emg_vehicle_count += 1

    lane_vehicle_counts[lane_name]["vehicle_count"] = vehicle_count
    lane_vehicle_counts[lane_name]["emg_vehicle_count"] = emg_vehicle_count

# Function to simulate traffic lights dynamically
# Function to simulate traffic lights dynamically with vehicle time calculation
def traffic_light_simulation(index=0):
    lanes = list(lane_vehicle_counts.keys())
    if index >= len(lanes):
        index = 0
    
    current_lane = lanes[index]
    
    # Calculate the time based on vehicle count, 1 second per vehicle with a max of 30 seconds
    vehicle_count = lane_vehicle_counts[current_lane]["vehicle_count"]
    max_time = 30
    time_for_current_lane = min(vehicle_count, max_time)
    
    # Update the signal and time for the current lane
    lane_vehicle_counts[current_lane]["signal"] = "🟢 Green"
    lane_vehicle_counts[current_lane]["time"] = f"{time_for_current_lane} sec"
    
    # Set all other lanes to Red
    for lane in lanes:
        if lane != current_lane:
            lane_vehicle_counts[lane]["signal"] = "🔴 Red"
            lane_vehicle_counts[lane]["time"] = "0 sec"
    
    # Switch to the next lane after the calculated time
    root.after(time_for_current_lane * 1000, lambda: traffic_light_simulation(index + 1))


# Main detection loop
def main_loop():
    for lane, image_path in lane_image_paths.items():
        detect_vehicles_for_lane(image_path, lane)
    root.after(2000, main_loop)

# Start the loops
root.after(2000, main_loop)
root.after(1000, update_ui)
root.after(1000, traffic_light_simulation)
root.mainloop()
