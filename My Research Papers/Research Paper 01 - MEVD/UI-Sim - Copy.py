import time
from ultralytics import YOLO
import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk

# Load YOLO model
model_path = r"D:\Desktop\PROJs\Multiple Emergency Vehicles Detection and Traffic\SwiftPass-AI-Powered-Emergency-Traffic-Control\Model\YOLO-Trained-Model\content\runs\detect\train\weights\best.pt"
model = YOLO(model_path)

# Emergency vehicle classes
emergency_classes = ["ambulance", "police", "firetruck"]

# Initialize vehicle count and emergency vehicle count for each lane
lane_vehicle_counts = {f"lane{i+1}": {"vehicle_count": 0, "emg_vehicle_count": 0} for i in range(4)}

# Paths to images for each lane
lane_image_paths = {
    "lane1": "test_img3.jpg",
    "lane2": "test_img4.jpg",
    "lane3": "test_img5.jpg",
    "lane4": "test_img2.jpg"
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
        text=f"{lane_name.capitalize()} | Vehicles: {lane_vehicle_counts[lane_name]['vehicle_count']} | Emergency: {lane_vehicle_counts[lane_name]['emg_vehicle_count']}",
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

# Function to update UI with latest vehicle counts
def update_ui():
    for lane, info in lane_frames.items():
        info.config(text=f"{lane.capitalize()} | Vehicles: {lane_vehicle_counts[lane]['vehicle_count']} | Emergency: {lane_vehicle_counts[lane]['emg_vehicle_count']}")

        placeholder_image = Image.open(lane_image_paths[lane])
        placeholder_image = placeholder_image.resize((400, 300))
        img = ImageTk.PhotoImage(placeholder_image)
        img_labels[lane].config(image=img)
        img_labels[lane].image = img

    root.after(1000, update_ui)

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

# Main detection loop
def main_loop():
    for lane, image_path in lane_image_paths.items():
        detect_vehicles_for_lane(image_path, lane)
    root.after(2000, main_loop)

root.after(2000, main_loop)
root.after(1000, update_ui)
root.mainloop()