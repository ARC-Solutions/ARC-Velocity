import os
import cv2
import shutil

source_folder = r"D:\priv\Programming\ARCV2\ImagesToTrain"
lines_folder = r"D:\priv\Programming\ARCV2\ImagesToTrain\Lines"
no_lines_folder = r"D:\priv\Programming\ARCV2\ImagesToTrain\No_Lines"

os.makedirs(lines_folder, exist_ok=True)
os.makedirs(no_lines_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    image = cv2.imread(file_path)

    if image is None:
        print(f"Could not load image: {file_path}. Skipping...")
        continue

    cv2.imshow("Annotate", image)

    key = cv2.waitKey(0) & 0xFF

    if key == ord('l'):  # Press 'l' if the specific line is present
        shutil.move(file_path, os.path.join(lines_folder, filename))
    elif key == ord('n'):  # Press 'n' if the specific line is not present
        shutil.move(file_path, os.path.join(no_lines_folder, filename))
    elif key == ord('q'):  # Press 'q' to quit the annotation process
        break

cv2.destroyAllWindows()
