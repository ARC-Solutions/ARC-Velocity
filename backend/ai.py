import cv2
import numpy as np
import tensorflow as tf
from arduino_Connection import arduino as ser
import time

model_path = r"D:\priv\Programming\ARCV2\Model"
model = tf.keras.models.load_model(model_path)


def send_command(command, speed=None):
    ser.write(f"{command}\n".encode())
    if speed is not None:
        time.sleep(speed)
        ser.write(f"{command}_off\n".encode())


def start_ai_car(arduino_serial):
    video_url = "http://192.168.0.164:8080/video"
    cap = cv2.VideoCapture(video_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

            # Define a range for the gray color of the tape
            lower_gray = np.array([0, 0, 40])
            upper_gray = np.array([180, 40, 200])

            # Preprocess the frame for the model
            preprocessed_frame = preprocess_image(frame)
            preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)

            # Use the model's prediction to decide the direction to move
            prediction = model.predict(preprocessed_frame)
            predicted_label = np.argmax(prediction)

            # Replace the existing rule-based decision-making code with the model's prediction
            if predicted_label == 0:  # forward
                send_command("forward_on")
            elif predicted_label == 1:  # left
                send_command("left_on")
            elif predicted_label == 2:  # right
                send_command("right_on")
            else:  # stop or any other action
                send_command("forward_off")
                send_command("right_off")
                send_command("left_off")

        # Show the binary video feed with consistent resolution
        #binary_display = cv2.resize(binary_frame, (frame.shape[1], frame.shape[0]))
        cv2.imshow("processed_frame", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
