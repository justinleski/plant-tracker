from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd

# Imports
import os, warnings
import matplotlib.pyplot as plt
from matplotlib import gridspecho

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory






# Load dataset
dataset_path = "house_plant_species"

# only keep supported formats like .jpg, .jpeg, .png
valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']



# TEST!!!!!!! : https://stackoverflow.com/questions/68191448/unknown-image-file-format-one-of-jpeg-png-gif-bmp-required
# data_dir = dataset_path
# image_extensions = valid_extensions  # add there all your images file extensions

# img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
# for filepath in Path(data_dir).rglob("*"):
#     if filepath.suffix.lower() in image_extensions:
#         img_type = imghdr.what(filepath)
#         if img_type is None:
#             print(f"{filepath} is not an image")
#             os.remove(filepath)
#         elif img_type not in img_type_accepted_by_tf:
#             print(f"{filepath} is a {img_type}, not accepted by TensorFlow")
#             os.remove(filepath)
        

# Function to filter valid image files
# def filter_valid_images(directory):
#     valid_image_paths = []
#     labels = []
#     for class_idx, class_dir in enumerate(Path(directory).iterdir()):
#         if class_dir.is_dir():
#             for img_path in class_dir.iterdir():
#                 if img_path.suffix.lower() in image_extensions:
#                     img_type = imghdr.what(img_path)
#                     if img_type and img_type in img_type_accepted_by_tf:
#                         valid_image_paths.append(str(img_path))
#                         labels.append(class_idx)
#                     else:
#                         print(f"Skipping invalid or unsupported image: {img_path}")
#     return valid_image_paths, labels

# def filter_images(directory_path):
#     valid_files = []
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             if any(file.lower().endswith(ext) for ext in valid_extensions):
#                 valid_files.append(os.path.join(root, file))
#     return valid_files

# # Filter valid image files (excluding .webp)
# valid_files = filter_images(dataset_path)

# # Function to load valid images and labels
# def load_valid_images(valid_files, image_size=(128, 128)):
#     images = []
#     labels = []
    
#     for file_path in valid_files:
#         try:
#             # Load image
#             image = tf.keras.preprocessing.image.load_img(file_path, target_size=image_size)
#             image = tf.keras.preprocessing.image.img_to_array(image)
#             images.append(image)
            
#             # Get label from the folder name (assuming folder names are class labels)
#             label = os.path.basename(os.path.dirname(file_path))
#             labels.append(label)
#         except Exception as e:
#             print(f"Error loading image {file_path}: {e}")
#             continue  # Skip invalid images
    
#     images = np.array(images)
#     labels = np.array(labels)
#     return images, labels

# # Load valid images and labels
# images, labels = load_valid_images(valid_files)





# Set up reproducibility
def set_seed(seed=31415):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
set_seed()

ds_train_ = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    labels='inferred',
    label_mode='categorical',
    image_size=[128, 128],
    interpolation='nearest',
    batch_size=64,
    shuffle=True,
)
ds_valid_ = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    labels='inferred',
    label_mode='categorical',
    image_size=[128, 128],
    interpolation='nearest',
    batch_size=64,
    shuffle=False,
)

# Data Pipeline
def convert_to_float(image, label):
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    return image, label

AUTOTUNE = tf.data.experimental.AUTOTUNE
ds_train = (
    ds_train_
    .map(convert_to_float)
    .cache()
    .prefetch(buffer_size=AUTOTUNE)
)
ds_valid = (
    ds_valid_
    .map(convert_to_float)
    .cache()
    .prefetch(buffer_size=AUTOTUNE)
)

# Define the model
num_classes = 47  # Update this based on your dataset's number of classes

model = keras.Sequential([
    layers.InputLayer(shape=[128, 128, 3]),

    # Data Augmentation
    layers.RandomFlip(mode='horizontal'),
    layers.RandomRotation(factor=0.10),

    # Block One
    layers.BatchNormalization(),
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Two
    layers.BatchNormalization(),
    layers.Conv2D(filters=128, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Block Three
    layers.BatchNormalization(),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPool2D(),

    # Head
    layers.BatchNormalization(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax'),  # Multi-class classification
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',  # Use categorical crossentropy for multi-class
    metrics=['accuracy'],
)

# Train the model
history = model.fit(
    ds_train,
    validation_data=ds_valid,
    epochs=30,
    verbose=0,
)

# Plot training history
history_frame = pd.DataFrame(history.history)
history_frame.loc[:, ['loss', 'val_loss']].plot()
history_frame.loc[:, ['accuracy', 'val_accuracy']].plot()

# Print model summary to verify architecture
model.summary()
