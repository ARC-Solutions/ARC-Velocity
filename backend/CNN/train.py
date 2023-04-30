import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import tensorflow as tf
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

model_path = r"D:\priv\Programming\ARCV2\Model"
model = tf.keras.models.load_model(model_path)

def display_images(images, labels, num_images=5):
    plt.figure(figsize=(15, 15))
    for i in range(num_images):
        index = random.randint(0, len(images) - 1)
        img = images[index].reshape(img_size, img_size)
        label = labels[index]
        plt.subplot(1, num_images, i + 1)
        plt.imshow(img, cmap='gray')
        plt.title(f"Label: {label}")
        plt.axis('off')
    plt.show()

def visualize_activations(model, input_image, layer_names):
    plt.figure(figsize=(20, 20))
    for i, layer_name in enumerate(layer_names):
        layer_output = model.get_layer(layer_name).output
        activation_model = Model(inputs=model.input, outputs=layer_output)
        activations = activation_model.predict(input_image)
        activations = np.squeeze(activations)
        num_filters = activations.shape[-1]

        for j in range(num_filters):
            plt.subplot(len(layer_names), num_filters, i * num_filters + j + 1)
            plt.imshow(activations[:, :, j], cmap='viridis')
            plt.axis('off')
    plt.show()


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

    img_size = 25

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

# Reshape the images and labels to be compatible with the ImageDataGenerator
images = images.reshape(images.shape[0], img_size, img_size, 1)
labels = tf.keras.utils.to_categorical(labels)

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# Create an instance of ImageDataGenerator with the desired augmentations
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

batch_size = 1
epochs = 5000

# Prepare the data generator for training data
train_datagen = datagen.flow(X_train, y_train, batch_size=batch_size)

# Train the model using the augmented data
history = model.fit(train_datagen,
                    steps_per_epoch=len(X_train) // batch_size,
                    epochs=epochs,
                    validation_data=(X_val, y_val))

# Save the trained model
model.save(model_path)
display_images(images, labels, num_images=5)  # You can change the number of images to display
input_image = images[0]  # Choose any image from your dataset
input_image = input_image[np.newaxis, :, :, np.newaxis]  # Add batch and channel dimensions

# Choose the names of the convolutional layers in your model
layer_names = ['conv2d', 'conv2d_1']

visualize_activations(model, input_image, layer_names)

