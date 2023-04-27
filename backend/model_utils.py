import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelBinarizer

def load_and_preprocess_data(lines_folder, no_lines_folder):
    X = []
    y = []

    for file in os.listdir(lines_folder):
        filepath = os.path.join(lines_folder, file)
        image = cv2.imread(filepath)
        preprocessed_image = preprocess_image(image)
        X.append(preprocessed_image)
        y.append(1)

    for file in os.listdir(no_lines_folder):
        filepath = os.path.join(no_lines_folder, file)
        image = cv2.imread(filepath)
        preprocessed_image = preprocess_image(image)
        X.append(preprocessed_image)
        y.append(0)

    return np.array(X), np.array(y)

def preprocess_image(image):
    resized_image = cv2.resize(image, (224, 224))
    return resized_image / 255.0

def create_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(2, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def train_model(model, X_train, y_train, X_val, y_val):
    model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

def save_model(model, model_path):
    model.save(model_path)

def predict_line(model, frame):
    resized_frame = cv2.resize(frame, (224, 224))
    input_data = np.expand_dims(resized_frame, axis=0)
    input_data = input_data / 255.0
    return model.predict(input_data)

