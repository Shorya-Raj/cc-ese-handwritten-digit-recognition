r"""Step 3: build the CNN and inspect its layers without training it yet.

Run from the repository root in the VS Code terminal:
    .\.venv\Scripts\python.exe .\digit_recognition\step_03_model.py

CNN means convolutional neural network. It learns small visual patterns such
as strokes and curves, then combines them to recognize a complete digit.
"""

import tensorflow as tf


# SECTION 1 — Set the picture size and the possible answers
# Each MNIST image is 28 pixels high, 28 pixels wide, and grayscale (1 channel).
IMAGE_SHAPE = (28, 28, 1)
NUMBER_OF_DIGITS = 10  # The possible labels are 0, 1, ..., 9.


def build_model() -> tf.keras.Model:
    """Create an untrained network that returns 10 digit probabilities."""

    # SECTION 2 — Tell Keras what one prepared image looks like
    model = tf.keras.Sequential(name="handwritten_digit_cnn")
    model.add(tf.keras.Input(shape=IMAGE_SHAPE))

    # SECTION 3 — Find simple marks, then shrink the feature maps
    # 32 filters learn different 3-by-3 pixel patterns. ReLU helps the model
    # learn relationships beyond simple straight-line combinations.
    model.add(tf.keras.layers.Conv2D(32, kernel_size=3, activation="relu"))
    # Pooling keeps the strongest signal in each 2-by-2 region and reduces size.
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))

    # SECTION 4 — Combine simple marks into more useful digit features
    # This second convolution uses 64 filters to learn richer patterns.
    model.add(tf.keras.layers.Conv2D(64, kernel_size=3, activation="relu"))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))

    # SECTION 5 — Turn visual features into one score per digit
    # Flatten makes one long list of the learned visual features.
    model.add(tf.keras.layers.Flatten())
    # During training, Dropout randomly hides 25% of these features to reduce
    # over-reliance on any one feature. It is inactive during prediction.
    model.add(tf.keras.layers.Dropout(0.25))
    # Softmax converts 10 scores into probabilities that add up to 1.
    model.add(tf.keras.layers.Dense(NUMBER_OF_DIGITS, activation="softmax"))

    return model


if __name__ == "__main__":
    # SECTION 6 — Display each layer's output shape and parameter count
    # This builds the network in memory; it does not fit/train or save weights.
    digit_model = build_model()
    digit_model.summary()
