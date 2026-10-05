r"""Step 2: prepare MNIST images for a convolutional neural network (CNN).

Run from the project folder in the VS Code terminal:
    .\.venv\Scripts\python.exe .\guided_build\step_02_prepare_images.py

This step changes the image numbers and shape. It does not train a model.
"""

import numpy as np
import tensorflow as tf


# SECTION 1 — Load the original images and inspect their format
# "raw" means we have not scaled the pixel values or added a channel yet.
(raw_train, train_labels), (raw_test, test_labels) = (
    tf.keras.datasets.mnist.load_data()
)

print("Before preparation:")
print("  training shape:", raw_train.shape)
print("  data type:", raw_train.dtype)
print("  pixel range:", int(raw_train.min()), "to", int(raw_train.max()))

# SECTION 2 — Scale brightness values to the 0–1 range
# The first dimension counts pictures; the next two are height and width.
# Dividing by 255 converts pixels from 0..255 to 0..1.
# We use the same change for training and test images.
train_images = raw_train.astype("float32") / 255.0
test_images = raw_test.astype("float32") / 255.0

# SECTION 3 — Tell the CNN that each picture has one color channel
# A CNN's Conv2D layer also expects a channel dimension. These images are
# grayscale, so each picture has exactly one channel. The final shape will be
# (number of pictures, height, width, channels).
train_images = train_images[..., np.newaxis]
test_images = test_images[..., np.newaxis]

# SECTION 4 — Show what changed, and check that labels did not change
print("After preparation:")
print("  training shape:", train_images.shape)
print("  test shape:", test_images.shape)
print("  data type:", train_images.dtype)
print("  pixel range:", float(train_images.min()), "to", float(train_images.max()))

# Compare the same non-black pixel before and after scaling.
row, column = np.argwhere(raw_train[0] > 0)[0]
print("One pixel before:", int(raw_train[0, row, column]))
print("Same pixel after:", float(train_images[0, row, column, 0]))
print("First label is still:", int(train_labels[0]))
