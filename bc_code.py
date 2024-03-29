# -*- coding: utf-8 -*-
"""BC_code

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13fRf1f2DuufXke0KYJiij_K9ZB8wpZoC
"""

import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

import os
dataset_path = "/content/drive/MyDrive/Breast_cancer"

image_files = []
labels = []

for class_name in ['benign', 'malignant', 'normal']:
  class_path = os.path.join(dataset_path, class_name)
  for filename in os.listdir(class_path):
    image_path = os.path.join(class_path, filename)
    image_files.append(image_path)
    labels.append(class_name)

from tensorflow.keras.utils import to_categorical

label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)
labels = to_categorical(labels)
print(labels)
print(labels.shape)
print(len(image_files))

X_train, X_test, y_train, y_test = train_test_split(image_files, labels, test_size=0.3, random_state=42, stratify=labels)
print(len(X_train),len(y_train))
print(len(X_test),len(y_test))

def load_preprocess_image(image_path):
  image = Image.open(image_path)
  image = image.resize((150, 150))
  image = image.convert('L')
  image = np.array(image)
  image = image.reshape((150, 150, 1))
  image = image.astype('float32') / 255.0
  return image

X_train = [str(image_path) for image_path in X_train]
X_test = [str(image_path) for image_path in X_test]

X_train = [load_preprocess_image(image_path) for image_path in X_train]
X_train = np.array(X_train)
y_train= np.array(y_train)

X_test= [load_preprocess_image(image_path) for image_path in X_test]
X_test = np.array(X_test)
y_test = np.array(y_test)

train_datagen = ImageDataGenerator(
rotation_range=20,
width_shift_range=0.2,
height_shift_range=0.2,
shear_range=0.2,
zoom_range=0.2,
horizontal_flip=True,
fill_mode='nearest'
)

train_generator = train_datagen.flow(X_train, y_train, batch_size=32)

model = Sequential()

np.random.seed(42)

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Flatten())

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(train_generator, epochs=50, validation_data=(X_test, y_test))

train_loss, train_accuracy = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Training Accuracy: {train_accuracy*100:.2f}%')
print(f'Train Loss: {train_loss*100:.2f}%')
print(f'Test Accuracy: {test_accuracy*100:.2f}%')
print(f'Test Loss: {test_loss*100:.2f}%')

import numpy as np
from sklearn.metrics import classification_report, accuracy_score

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

print('Classification Report:')
print(classification_report(y_true, y_pred_classes))
print(f'Accuracy: {accuracy_score(y_true, y_pred_classes)*100:.2f}')

# Plotting accuracy and loss over epochs
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Test Accuracy')
plt.title('Training and Test Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Test Loss')
plt.title('Training and Test Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.show()

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Assuming y_true and X_test are appropriately defined

# Convert continuous-multioutput targets to integer labels if needed
y_true = np.argmax(y_true, axis=1) if len(y_true.shape) > 1 else y_true

# Calculate confusion matrix
y_pred = model.predict(X_test)
y_pred = np.argmax(y_pred, axis=1) if len(y_pred.shape) > 1 else y_pred

# Calculate confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues', fmt='g')  # Use 'fmt' to format the annotations
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

def plot_heatmap(X_train):
    plt.figure(figsize=(8, 6))
    plt.imshow(X_train, cmap='hot')
    plt.colorbar()
    plt.title('Heatmap of Image')
    plt.show()

# Plotting heatmap of a sample image
plot_heatmap(X_train[0])

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

image1_path = '/content/drive/MyDrive/Breast_cancer/benign/benign (10).png'
image2_path = '/content/drive/MyDrive/Breast_cancer/benign/benign (101).png'

def resize_and_flatten(image_path):
    # Read image using PIL (Pillow)
    image = Image.open(image_path)

    # Resize image to a common shape (you can choose the desired shape)
    target_shape = (150, 150)  # Change this to your desired shape
    resized_image = image.resize(target_shape)

    # Convert the resized image to a NumPy array and flatten it using ravel()
    flat_image = np.array(resized_image).ravel()

    return flat_image

def plot_scatter(image1_path, image2_path):
    # Resize and flatten images
    flat_image1 = resize_and_flatten(image1_path)
    flat_image2 = resize_and_flatten(image2_path)

    # Plotting scatter plot of pixel intensity between two images
    plt.figure(figsize=(8, 6))
    plt.scatter(flat_image1, flat_image2, color='blue', alpha=0.5)
    plt.xlabel('Pixel Intensity - Image 1')
    plt.ylabel('Pixel Intensity - Image 2')
    plt.title('Scatter Plot of Pixel Intensity')
    plt.show()

# Plotting scatter plot of pixel intensity between two images
plot_scatter(image1_path, image2_path)

import cv2
import matplotlib.pyplot as plt

def plot_histogram(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    target_shape = (100, 100)  # Change this to your desired shape
    resized_image = image.resize(target_shape)
    if image is None:
        print("Error: Unable to read the image.")
        return

    plt.figure(figsize=(10, 5))
    plt.hist(image.ravel(), bins=256, color='gray', alpha=0.8)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Pixel Intensity')
    plt.show()

# Example usage
image_path = "/content/drive/MyDrive/Breast_cancer/benign/benign (1).png"
plot_histogram(image_path)

def plot_learning_curve(history):
    plt.plot(history.history['accuracy'], label='train_accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Model Learning Curve')
    plt.legend()
    plt.show()

# Assuming you have history object from model training
plot_learning_curve(history)

def load_preprocess_single_image(image_path):
  image = Image.open(image_path)
  image = image.resize((150, 150))
  image = image.convert('L')
  image = np.array(image)
  image = image.reshape((1, 150, 150, 1))
  image = image.astype('float32') / 255.0
  return image

image_path = "/content/drive/MyDrive/b.webp"

test_image = load_preprocess_single_image(image_path)

predictions = model.predict(test_image)
predicted_class = np.argmax(predictions)

classes = ['benign', 'malignant', 'normal']
predicted_label = classes[predicted_class]
print(f"Predicted class: {predicted_label}")

if (predicted_label == 'normal'):
  print("You're in Normal condition no need to worry.")
elif (predicted_label == 'benign'):
  print("Benign the cells are not yet cancerous, but they have the potential to become malignant consult the doctor.")
elif (predicted_label == 'malignant'):
  print("Malignant the tumors are cancerous. The cells can grow and spread to other parts of the body.")
else:
  print("The Image which is under consideration is unpredictable by the model we will try again")

model.save('BCmodel.h5')