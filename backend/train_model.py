import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from model_utils import load_and_preprocess_data, create_model, train_model, save_model
from keras.utils import to_categorical

# Define folders and model paths
lines_folder = r"D:\priv\Programming\ARCV2\ImagesToTrain\Lines"
no_lines_folder = r"D:\priv\Programming\ARCV2\ImagesToTrain\No_Lines"
model_path = r"D:\priv\Programming\ARCV2\Model"

# Load and preprocess data
data, labels = load_and_preprocess_data(lines_folder, no_lines_folder)

# Convert labels to one-hot encoded format
labels = to_categorical(labels)

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, random_state=42)

# Create and train the model
model = create_model()
train_model(model, X_train, y_train, X_val, y_val)

# Save the trained model
save_model(model, model_path)
