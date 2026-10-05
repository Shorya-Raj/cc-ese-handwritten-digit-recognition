r"""Step 1: meet the handwritten-digit dataset before building a model.

Run from the project folder in the VS Code terminal:
    .\.venv\Scripts\python.exe .\guided_build\step_01_data.py

This step loads MNIST, prints a few facts, and saves one enlarged sample image.
It does not train or change the existing model.
"""

from pathlib import Path

import tensorflow as tf
from PIL import Image


# SECTION 1 — Load the pictures and their correct answers
# Each image is a small picture of one handwritten digit. The matching label
# says which digit (0 through 9) is shown in that picture.
(train_images, train_labels), (test_images, test_labels) = (
    tf.keras.datasets.mnist.load_data()
)

# SECTION 2 — Inspect the dataset before changing or training anything
# A shape such as (60000, 28, 28) means 60,000 pictures, each 28 pixels square.
# The test images are kept separate so we can check the trained model later.
print("Training images:", train_images.shape)
print("Training labels:", train_labels.shape)
print("Test images:", test_images.shape)
print("Test labels:", test_labels.shape)
print("First image size:", train_images[0].shape)
print("First image label:", int(train_labels[0]))
print("Pixel value range:", int(train_images.min()), "to", int(train_images.max()))

# SECTION 3 — Save one picture we can inspect by eye
# Enlarge the first 28-by-28 image so its pixels are easy to see in VS Code.
# NEAREST keeps the original square pixels visible instead of blurring them.
sample_path = Path(__file__).with_name("first_mnist_digit.png")
Image.fromarray(train_images[0]).resize(
    (280, 280), resample=Image.Resampling.NEAREST
).save(sample_path)
print("Sample image saved to:", sample_path)
