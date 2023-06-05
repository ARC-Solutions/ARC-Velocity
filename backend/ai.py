import cv2
import numpy as np
from arduino_Connection import arduino as ser
import time
from keras.models import load_model
import threading
import queue
import os
import sys
import requests
from PIL import Image
from io import BytesIO
import concurrent.futures

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.videoConnection import frame_url

def send_command(command, impulse_duration=0.1):
    ser.write(f"{command}\n".encode())
    time.sleep(impulse_duration)
    ser.write(f"{command}_off\n".encode())

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

def start_ai_car(arduino_serial):
    model_path = "../PreTrainedModel"
    model = load_model(model_path)

    impulse_duration = 0.05  # Adjust this value to control the duration of the impulses
    prev_frame_time = time.time()

    # Create a ThreadPoolExecutor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    # Create a queue to hold the Futures returned by the executor
    futures = queue.Queue()

    while True:
        # Fetch the latest frame
        frame_future = executor.submit(fetch_latest_frame, frame_url)
        futures.put(frame_future)

        # Get the result of the earliest submitted task, if it's done
        while not futures.empty():
            future = futures.queue[0]  # Peek at the first item
            if future.done():
                future = futures.get()  # Remove the first item
                frame = future.result()
                if frame is None:
                    continue

                # Calculate FPS
                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time
                fps_text = f"FPS: {fps:.2f}"

                # Define a region of interest
                height, width, _ = frame.shape
                roi_height = 100  # Adjust this to change the ROI height
                roi_width = 230  # Adjust this to change the ROI width
                roi_y = int(height * 0.6)+25
                roi_x = int((width - roi_width) / 2)
                roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

                # Define a range for the gray color of the tape
                lower =np.array([0, 0, 0])
                upper = np.array([160, 160, 140])  # adjust the V value as needed based on your specific lighting conditions

                # Create a mask to highlight the line
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_roi, lower, upper)
                highlighted_line = cv2.bitwise_and(roi, roi, mask=mask)

                # Check the percentage of white pixels in the ROI
                white_pixel_percentage = (np.sum(mask > 0) / (roi_height * roi_width)) * 100
                white_pixel_threshold = 5  # Adjust this threshold to your preference

                # Preprocess the ROI for the model
                preprocessed_roi = preprocess_image(roi)
                preprocessed_roi = np.expand_dims(preprocessed_roi, axis=0)

                # Use the model's prediction to decide the direction to move
                prediction_future = executor.submit(model.predict, preprocessed_roi)
                futures.put(prediction_future)

                while not futures.empty():
                    future = futures.queue[0]  # Peek at the first item
                    if future.done():
                        future = futures.get()  # Remove the first item
                        prediction = future.result()
                        predicted_label = np.argmax(prediction)
                        print(predicted_label)
                        action_text = ""
                        if white_pixel_percentage < white_pixel_threshold:
                            if predicted_label == 0:  # forward
                                send_command("forward_on", impulse_duration)
                                print("forward_on")
                                action_text = "forward"
                            elif predicted_label == 1:  # left
                                send_command("left_on", impulse_duration)
                                action_text = "left"
                                print("left_on")
                            elif predicted_label == 2:  # right
                                send_command("right_on", impulse_duration)
                                action_text = "right"
                                print("right_on")
                            elif predicted_label == 3:
                                action_text = "no_tape"
                                print("no_tape")
                        else:  # stop or any other action
                            send_command("forward_off")
                            send_command("right_off")
                            send_command("left_off")
                            action_text = "stop"

                        # Add action text to the frame
                        cv2.putText(frame, fps_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                                    cv2.LINE_AA)
                        cv2.putText(highlighted_line, action_text, (0, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                        # Combine the original frame with the highlighted_line
                        frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width] = highlighted_line
                        cv2.imshow("processed_frame", frame)

                        # Break the loop when the 'q' key is pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        break  # No more completed tasks

    cv2.destroyAllWindows()

start_ai_car(ser)
