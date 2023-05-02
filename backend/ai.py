import cv2
import numpy as np
from arduino_Connection import arduino as ser
import time
from keras.models import load_model
import threading
import queue

def send_command(command, impulse_duration=0.1):
    ser.write(f"{command}\n".encode())
    time.sleep(impulse_duration)
    ser.write(f"{command}_off\n".encode())

def preprocess_image(img, img_size=224):
    img_resized = cv2.resize(img, (img_size, img_size))
    img_normalized = img_resized.astype('float32') / 255.0
    return img_normalized


def capture_frames(cap, frame_queue, stop_capture):
    while not stop_capture.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_queue.full():
            frame_queue.get()

        frame_queue.put((ret, frame))


def start_ai_car(arduino_serial):
    video_url = "http://192.168.0.164:8080/video"
    cap = cv2.VideoCapture(video_url)

    model_path = "/mnt/d/priv/Programming/ARCV2/PreTrainedModel"
    model = load_model(model_path)

    impulse_duration = 0.05  # Adjust this value to control the duration of the impulses
    prev_frame_time = time.time()

    # Create a queue to store frames and an event to signal when to stop capturing frames
    frame_queue = queue.Queue(maxsize=1)
    stop_capture = threading.Event()

    # Initialize the frame_queue and start the capture thread
    frame_queue = queue.Queue()
    capture_thread = threading.Thread(target=capture_frames, args=(cap, frame_queue, stop_capture))
    capture_thread.start()

    while True:
        if frame_queue.empty():
            continue

        ret, frame = frame_queue.get()
        if not ret:
            break

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        new_width = 96
        new_height = 128
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

        # Calculate FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps_text = f"FPS: {fps:.2f}"

        # Define a region of interest
        height, width, _ = frame.shape
        roi_height = 100  # Adjust this to change the ROI height
        roi_width = 300  # Adjust this to change the ROI width
        roi_y = int(height * 0.6)
        roi_x = int((width - roi_width) / 2)
        roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

        # Define a range for the gray color of the tape
        lower = np.array([0, 0, 40])
        upper = np.array([220, 80, 220])

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
        prediction = model.predict(preprocessed_roi)
        predicted_label = np.argmax(prediction)

        action_text = ""
        if white_pixel_percentage >= white_pixel_threshold:
            if predicted_label == 0:  # forward
                send_command("forward_on", impulse_duration)
                action_text = "forward"
            elif predicted_label == 1:  # left
                send_command("left_on", impulse_duration)
                action_text = "left"
            elif predicted_label == 2:  # right
                send_command("right_on", impulse_duration)
                action_text = "right"
        else:  # stop or any other action
            send_command("forward_off")
            send_command("right_off")
            send_command("left_off")
            action_text = "stop"

        # Add action text to the frame
        cv2.putText(frame, fps_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
        cv2.putText(highlighted_line, action_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Combine the original frame with the highlighted_line
        frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width] = highlighted_line
        cv2.imshow("processed_frame", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_capture.set()
            break

    capture_thread.join()
    cap.release()
    cv2.destroyAllWindows()
