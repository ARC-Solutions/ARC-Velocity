import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from train import load_dataset
from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model

images, labels, img_size = load_dataset()

# Assuming images and labels are already loaded and preprocessed
images = np.array(images)
labels = np.array(labels).reshape(-1, 1)

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

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
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)

# Save the model
model_path = r"D:\priv\Programming\ARCV2\PreTrainedModel"
model.save(model_path)

# Load the saved model
loaded_model = tf.keras.models.load_model(model_path)

# Test the loaded model on some sample data
sample_image = X_val[0]
sample_image = np.expand_dims(sample_image, axis=0)  # Add a batch dimension
prediction = loaded_model.predict(sample_image)

print(f"Prediction: {prediction}")
