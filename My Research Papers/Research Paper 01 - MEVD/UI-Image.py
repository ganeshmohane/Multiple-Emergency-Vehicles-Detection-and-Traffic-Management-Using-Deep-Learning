import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk

# Create main window
root = tk.Tk()
root.title("Traffic Control System")
root.geometry("1200x800")  # Bigger window for better visibility

# Example data for each lane (you can later update this dynamically)
lane_data = {
    "lane1": {"signal": "🟢 Green", "comment": "Emg Detected", "time": "10 sec"},
    "lane2": {"signal": "🔴 Red", "comment": "No Emg", "time": "20 sec"},
    "lane3": {"signal": "🟡 Amber", "comment": "Emg Detected", "time": "15 sec"},
    "lane4": {"signal": "🟢 Green", "comment": "No Emg", "time": "12 sec"},
}

# Function to create a frame for each lane
def create_lane_frame(lane_name, image_path, row, column):
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

    # Placeholder Image or Video Frame
    placeholder_image = Image.open(image_path)  # Use image or video feed here
    placeholder_image = placeholder_image.resize((400, 300))  # Bigger size for better visibility
    img = ImageTk.PhotoImage(placeholder_image)
    img_label = Label(lane_frame, image=img)
    img_label.image = img
    img_label.pack()

    # Traffic Light Label (Static for now)
    traffic_light = Label(lane_frame, text=lane_data[lane_name]['signal'], fg="green", font=("Helvetica", 24))
    traffic_light.pack()

# Adjust grid to expand with window size
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Creating 4 corners for 4 lanes (Using test images, replace with video feed later)
create_lane_frame("lane1", "test_img.jpg", 0, 0)  # Top-Left Corner
create_lane_frame("lane2", "test_img2.jpg", 0, 1)  # Top-Right Corner
create_lane_frame("lane3", "test_img3.jpg", 1, 0)  # Bottom-Left Corner
create_lane_frame("lane4", "test_img4.jpg", 1, 1)  # Bottom-Right Corner

# Start the Tkinter main loop
root.mainloop()
