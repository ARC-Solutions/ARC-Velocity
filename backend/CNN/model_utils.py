import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from train import load_dataset


images, labels, img_size = load_dataset()

# Assuming images and labels are already loaded and preprocessed
images = np.array(images)
labels = np.array(labels).reshape(-1, 1)

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# One-hot encode the labels
encoder = OneHotEncoder()
y_train = encoder.fit_transform(y_train).toarray()
y_val = encoder.transform(y_val).toarray()

# Define the CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')  # Change this line to have 4 neurons instead of 3
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)

# Save the model
model_path = r"D:\priv\Programming\ARCV2\Model"
model.save(model_path)

# Load the saved model
loaded_model = tf.keras.models.load_model(model_path)

# Test the loaded model on some sample data
sample_image = X_val[0]
sample_image = np.expand_dims(sample_image, axis=0)  # Add a batch dimension
prediction = loaded_model.predict(sample_image)

print(f"Prediction: {prediction}")
