import os
import cv2
import numpy as np
from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import Adam



def rename_files(folder, prefix):
    index = 0
    for filename in os.listdir(folder):
        new_filename = f"{prefix}{index}.jpg"
        while os.path.exists(os.path.join(folder, new_filename)):
            index += 1
            new_filename = f"{prefix}{index}.jpg"

        old_filepath = os.path.join(folder, filename)
        new_filepath = os.path.join(folder, new_filename)
        os.rename(old_filepath, new_filepath)
        index += 1


def load_images(folder, label_prefix, label, img_size):
    images = []
    labels = []

    print(f"Loading images from folder: {folder}")
    print(f"Label prefix: {label_prefix}")

    for filename in os.listdir(folder):
        print(f"Checking filename: {filename}")
        if filename.startswith(label_prefix):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            img_resized = cv2.resize(img, (img_size, img_size))
            images.append(img_resized)
            labels.append(label)

    return images, labels


def load_dataset():
    forward_folder = r"D:\priv\Programming\ARCV2\backend\CNN\Forward"
    left_folder = r"D:\priv\Programming\ARCV2\backend\CNN\Left"
    right_folder = r"D:\priv\Programming\ARCV2\backend\CNN\Right"
    no_tape_folder = r"D:\priv\Programming\ARCV2\backend\CNN\No_Tape"

    img_size = 224

    # Rename the files before loading the images
    rename_files(forward_folder, "forward_")
    rename_files(left_folder, "left_")
    rename_files(right_folder, "right_")
    rename_files(no_tape_folder, "no_tape_")

    forward_images, forward_labels = load_images(forward_folder, "forward", 0, img_size)
    left_images, left_labels = load_images(left_folder, "left", 1, img_size)
    right_images, right_labels = load_images(right_folder, "right", 2, img_size)
    no_tape_images, no_tape_labels = load_images(no_tape_folder, "no_tape", 3, img_size)

    images = forward_images + left_images + right_images + no_tape_images
    labels = forward_labels + left_labels + right_labels + no_tape_labels

    images = np.array(images)
    labels = np.array(labels)

    shuffle_indices = np.random.permutation(len(images))
    images = images[shuffle_indices]
    labels = labels[shuffle_indices]

    print(f"Forward images: {len(forward_images)}")
    print(f"Left images: {len(left_images)}")
    print(f"Right images: {len(right_images)}")
    print(f"No Tape images: {len(no_tape_images)}")

    print(f"Total images: {len(images)}")
    print(f"Total labels: {len(labels)}")
    return images, labels, img_size


# After loading the dataset:
images, labels, img_size = load_dataset()

# Load the pre-trained MobileNetV2 model without the top layers
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))

# Add custom layers on top
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(4, activation='softmax')(x)

# Combine the base model and the custom layers into a new model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the layers in the base model
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(lr=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(images, labels, batch_size=32, epochs=20, validation_split=0.2)

# Save the model
model.save(r"D:\priv\Programming\ARCV2\PreTrainedModel")
