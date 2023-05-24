import os
import cv2

source_folder = "D:\priv\Programming\ARCV2\Training"
output_folders = {
    "w": r"D:\priv\Programming\ARCV2\backend\CNN\Forward",
    "a": r"D:\priv\Programming\ARCV2\backend\CNN\Left",
    "d": r"D:\priv\Programming\ARCV2\backend\CNN\Right",
    "s": r"D:\priv\Programming\ARCV2\backend\CNN\No_Tape",
}
preview_max_width = 880
preview_max_height = 660

def display_image(image):
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    resized_image = resize_image(rotated_image, preview_max_width, preview_max_height)
    add_text(resized_image)
    cv2.imshow("Image", resized_image)

def wait_for_label():
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in [ord('w'), ord('a'), ord('d'), ord('s'), ord('q')]:
            return chr(key)

def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    aspect_ratio = float(width) / float(height)

    if width > height:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

def add_text(image):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_color = (255, 255, 255)
    font_thickness = 2
    text = "w: for forward\na: for left\nd: for right\ns: for no tape\nq: to quit"
    y0, dy = 30, 30
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        cv2.putText(image, line, (10, y), font, font_scale, font_color, font_thickness)

for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    image = cv2.imread(file_path)

    if image is None:
        print(f"Could not load image: {file_path}. Skipping...")
        continue

    display_image(image)
    label = wait_for_label()

    if label == 'q':
        break

    output_folder = output_folders[label]
    new_file_path = os.path.join(output_folder, filename)
    os.rename(file_path, new_file_path)

cv2.destroyAllWindows()
