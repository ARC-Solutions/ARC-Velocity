import cv2
import numpy as np
import time
import tensorflow as tf
from keras.models import load_model
import concurrent.futures
from queue import Queue
import requests
from PIL import Image
from io import BytesIO
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.videoConnection import frame_url

# Create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Create a queue to hold the Futures returned by the executor
futures = Queue()

def fetch_latest_frame(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error fetching latest frame: {e}")
        return None

def preprocess_image(img, img_size=224):
    img_resized = cv2.resize(img, (img_size, img_size))
    img_normalized = img_resized.astype('float32') / 255.0
    return img_normalized

# Load the model
model_path = r"../../PreTrainedModel"
model = load_model(model_path)

# Define the frame URL
frame_url = frame_url

# Initialize the previous frame time for FPS calculation
prev_frame_time = time.time()

# Create a named window
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

while True:
    # Fetch the latest frame
    frame = fetch_latest_frame(frame_url)
    if frame is None:
        continue

    # Calculate FPS
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps_text = f"FPS: {fps:.2f}"

    # Define a region of interest
    height, width, _ = frame.shape
    roi_height = 100 # Adjust this to change the ROI height
    roi_width = 230  # Adjust this to change the ROI width
    roi_y = int(height * 0.6)+25
    roi_x = int((width - roi_width) / 2)
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    # Define a range for the gray color of the tape
    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 0])  # adjust the V value as needed based on your specific lighting conditions

    # Create a mask to highlight the line
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, lower, upper)
    highlighted_line = cv2.bitwise_and(roi, roi, mask=mask)

    # Draw a rectangle around the ROI
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

    # Preprocess the highlighted line for the model
    preprocessed_roi = preprocess_image(highlighted_line)
    preprocessed_roi = np.expand_dims(preprocessed_roi, axis=0)

    # Submit the task to the executor and store the Future in the queue
    future = executor.submit(model.predict, preprocessed_roi)
    futures.put(future)

    # Get the result of the earliest submitted task, ifit's done
    while not futures.empty():
        future = futures.queue[0]  # Peek at the first item
        if future.done():
            future = futures.get()  # Remove the first item
            prediction = future.result()
            predicted_label = np.argmax(prediction)
            print("Predicted label: ", predicted_label)
            if predicted_label == 0:
                print("forward")
            elif predicted_label == 1:
                print("left")
            elif predicted_label == 2:
                print("right")
            elif predicted_label == 3:
                print("no_tape")
        else:
            break  # No more completed tasks

    # Add FPS text to the frame
    cv2.putText(frame, fps_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop ends, destroy the window
cv2.destroyAllWindows()
