import cv2
import numpy as np
import tensorflow as tf
from arduino_Connection import arduino as ser
from model_utils import preprocess_image

model_path = r"D:\priv\Programming\ARCV2\Model"
model = tf.keras.models.load_model(model_path)

def send_command(command):
    ser.write(f"{command}\n".encode())

def start_ai_car(arduino_serial):

    video_url = "http://192.168.0.164:8080/video"
    cap = cv2.VideoCapture(video_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Define the region of interest
        height, width, _ = frame.shape
        roi_left = width // 3
        roi_right = width * 2 // 3
        roi_top = height // 3
        roi_bottom = height * 2 // 3

        # Draw the ROI rectangle on the frame
        cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)

        # Extract the region of interest from the frame
        roi_frame = frame[roi_top:roi_bottom, roi_left:roi_right]

        # Preprocess the frame for the model
        preprocessed_frame = preprocess_image(frame)
        preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)

        # Use the model's prediction to decide the direction to move
        prediction = model.predict(preprocessed_frame)
        predicted_label = np.argmax(prediction)

        # Preprocess the ROI frame for the model
        preprocessed_frame = preprocess_image(roi_frame)
        preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)

        if predicted_label == 1:
            send_command("forward_on")
        else:
            send_command("forward_off")
            send_command("right_off")
            send_command("left_off")


        # Show the processed video feed
        cv2.imshow("processed_frame", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
