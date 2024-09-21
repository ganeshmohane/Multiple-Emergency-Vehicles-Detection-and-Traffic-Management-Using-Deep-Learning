import cv2
import numpy as np
from keras.models import load_model

# Load your model
model = load_model(r"C:\Users\Ganesh\Downloads\cnn3class.h5")  # Replace with your actual model path

# Define the classes
desired_classes = ['ambulance', 'firetruck', 'police vehicle']

def predict_and_display(frame):
    # Preprocess the frame
    image_resized = cv2.resize(frame, (128, 128))  # Resize to match model input
    image_array = np.array(image_resized, dtype='float32') / 255.0
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    
    # Predict using the model
    predictions = model.predict(image_array)[0]
    
    # Get class names for predicted labels
    predicted_classes = [desired_classes[i] for i in range(len(predictions)) if predictions[i] > 0.5]  # Adjust threshold as needed
    
    return predicted_classes, predictions

# Open the video file
video_path = r"C:\Users\Ganesh\Downloads\TestVideo.mp4"  # Replace with your video path
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Get predictions for the current frame
    predicted_classes, predictions = predict_and_display(frame)

    # Display predicted classes
    cv2.putText(frame, f'Predicted Classes: {predicted_classes}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Red text
    
    # Show green light if any emergency vehicle is detected
    if predicted_classes:
        cv2.putText(frame, 'Green Light', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Green text

    # Show the frame
    cv2.imshow('Video Prediction', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
