import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk
import cv2

# Create main window
root = tk.Tk()
root.title("Traffic Control System")
root.geometry("1200x800")

# Example data for each lane (you can update this dynamically later)
lane_data = {
    "lane1": {"signal": "🟢 Green", "comment": "Emg Detected", "time": "10 sec"},
    "lane2": {"signal": "🔴 Red", "comment": "No Emg", "time": "20 sec"},
    "lane3": {"signal": "🟡 Amber", "comment": "Emg Detected", "time": "15 sec"},
    "lane4": {"signal": "🟢 Green", "comment": "No Emg", "time": "12 sec"},
}

# Video Sources (Change these to your video file paths or use camera indexes)
video_sources = {
    "lane1": "D:\Desktop\Yolo Model Test\Outputs\TestVideo.avi",
    "lane2": "D:\Desktop\Yolo Model Test\Outputs\TestVideo.avi",
    "lane3": "D:\Desktop\Yolo Model Test\Outputs\TestVideo.avi",
    "lane4": "D:\Desktop\Yolo Model Test\Outputs\TestVideo.avi",
    #"lane4": "TestVideo/lane4.mp4"
}

# Dictionary to hold video capture objects
video_caps = {}

# Function to create a frame for each lane with video feed
def create_lane_frame(lane_name, video_path, row, column):
    # Lane Frame
    lane_frame = Frame(root, bd=2, relief="solid")
    lane_frame.grid(row=row, column=column, padx=30, pady=30, sticky="nsew")

    # Lane Info Label
    lane_info = Label(
        lane_frame,
        text=f"{lane_name.capitalize()} | Current Signal: {lane_data[lane_name]['signal']}\n"
             f"Comment: {lane_data[lane_name]['comment']}\n"
             f"Dynamic Time: {lane_data[lane_name]['time']}",
        font=("Helvetica", 16),
        justify="left"
    )
    lane_info.pack()

    # Video Frame Label (For displaying video)
    video_label = Label(lane_frame)
    video_label.pack()

    # Traffic Light Label (Static for now)
    traffic_light = Label(lane_frame, text=lane_data[lane_name]['signal'], fg="green", font=("Helvetica", 24))
    traffic_light.pack()

    # Initialize Video Capture Object
    cap = cv2.VideoCapture(video_path)
    video_caps[lane_name] = (cap, video_label)

# Function to update video frames
def update_videos():
    for lane_name, (cap, video_label) in video_caps.items():
        ret, frame = cap.read()
        if ret:
            # Resize frame for display
            frame = cv2.resize(frame, (400, 300))
            # Convert frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to ImageTk
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            # Update the label with the new frame
            video_label.config(image=img)
            video_label.image = img
        else:
            # Restart video when it ends
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Repeat after 30 ms
    root.after(30, update_videos)

# Adjust grid to expand with window size
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Creating 4 corners for 4 lanes (Using video feeds)
create_lane_frame("lane1", video_sources["lane1"], 0, 0)  # Top-Left Corner
create_lane_frame("lane2", video_sources["lane2"], 0, 1)  # Top-Right Corner
create_lane_frame("lane3", video_sources["lane3"], 1, 0)  # Bottom-Left Corner
create_lane_frame("lane4", video_sources["lane4"], 1, 1)  # Bottom-Right Corner

# Start video update loop
update_videos()

# Start the Tkinter main loop
root.mainloop()

# Release all video captures on exit
for cap, _ in video_caps.values():
    cap.release()
