# Import additional libraries
import cv2
import numpy as np
import time
import urllib.request
from urllib.error import URLError, HTTPError
from arduino_Connection import arduino as ser


def send_command(command):
    ser.write(f"{command}\n".encode())

def start_ai_car(arduino_serial):

    video_url = "http://192.168.0.164:8080/video"
    cap = cv2.VideoCapture(video_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess the frame (convert to grayscale and apply Gaussian blur)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Define a region of interest (ROI)
        height, width = edges.shape
        mask = np.zeros_like(edges)
        roi_corners = np.array([[
            (0, height - 85),
            (width // 3, height - 1.5 * height // 3),

            (2 * width // 3, height - 1.5 * height // 3),
            (width, height - 85)
        ]], dtype=np.int32)

        cv2.fillPoly(mask, roi_corners, 255)
        roi = cv2.bitwise_and(edges, mask)

        # Find lines using the Hough transform
        lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 20, np.array([]), minLineLength=5, maxLineGap=2)

        if lines is not None:
            # Filter out lines with a zero difference in their x-coordinates
            valid_lines = [line for line in lines for x1, y1, x2, y2 in line if (x2 - x1) != 0]

            if valid_lines:
                # Draw the detected lines on the original frame
                for line in valid_lines:
                    for x1, y1, x2, y2 in line:
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Calculate the average slope and position of the lines
                slope_avg = np.nanmean([(y2 - y1) / (x2 - x1) for line in valid_lines for x1, y1, x2, y2 in line])
                x_avg = np.mean([(x1 + x2) / 2 for line in valid_lines for x1, y1, x2, y2 in line])

                # Decide on the direction to move
                if slope_avg > 0:
                    if x_avg < width // 2:
                        send_command("right_on")
                        send_command("left_off")
                    else:
                        send_command("right_off")
                        send_command("left_on")
                else:
                    if x_avg < width // 2:
                        send_command("right_on")
                        send_command("left_off")
                    else:
                        send_command("right_off")
                        send_command("left_on")
                    send_command("forward_on")
            else:
                send_command("forward_off")
                send_command("right_off")
                send_command("left_off")
        # Draw the ROI polygon on the frame
        cv2.polylines(frame, roi_corners, True, (0, 255, 255), 2)

        # Show the processed video feed
        cv2.imshow("processed_frame", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()