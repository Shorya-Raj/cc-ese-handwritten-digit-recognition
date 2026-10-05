r"""Step 4: train the CNN on MNIST and save the learned model.

Run from the repository root in the VS Code terminal:
    .\.venv\Scripts\python.exe .\digit_recognition\step_04_train.py

The 10,000 test pictures are deliberately kept out of this step. Step 5 will
use them to check how the trained model performs on unseen MNIST pictures.
"""

import json
from pathlib import Path

import numpy as np
import tensorflow as tf

from step_03_model import build_model


# SECTION 1 — Choose the training settings
RANDOM_SEED = 42  # Makes shuffling and starting weights more repeatable.
EPOCHS = 8  # One epoch means one pass through the training pictures.
BATCH_SIZE = 128  # Update the model after each group of 128 pictures.
VALIDATION_FRACTION = 0.10  # Reserve 6,000 of 60,000 pictures for progress checks.
OUTPUT_DIR = Path(__file__).with_name("artifacts")


# SECTION 2 — Load and prepare the pictures exactly as in Step 2
tf.keras.utils.set_random_seed(RANDOM_SEED)
(raw_train, train_labels), (raw_test, test_labels) = (
    tf.keras.datasets.mnist.load_data()
)
train_images = raw_train.astype("float32") / 255.0
train_images = train_images[..., np.newaxis]

# We load the test pictures so we can report their count, but do not pass them
# to model.fit(). Their answers stay hidden from the training process.
print(f"MNIST training set: {len(train_images):,} pictures")
print(f"Reserved for validation: {int(len(train_images) * VALIDATION_FRACTION):,}")
print(f"Held-out test set: {len(raw_test):,} pictures (not used here)")


# SECTION 3 — Build and configure the model for learning
model = build_model()
# Adam decides how to adjust the model's parameters after each batch.
# The loss measures how far the predicted digit probabilities are from the
# correct integer labels. Accuracy counts how often the top digit is correct.
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)


# SECTION 4 — Train while checking progress on separate validation pictures
# If validation loss stops improving for two epochs, stop early and keep the
# best weights. This avoids spending extra time after progress stalls.
stop_when_stalled = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=2, restore_best_weights=True
)
history = model.fit(
    train_images,
    train_labels,
    validation_split=VALIDATION_FRACTION,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    shuffle=True,
    callbacks=[stop_when_stalled],
    verbose=2,
)


# SECTION 5 — Save the model and the numbers behind the training chart
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
model_path = OUTPUT_DIR / "digit_model.keras"
history_path = OUTPUT_DIR / "training_history.json"
model.save(model_path)
history_path.write_text(
    json.dumps(
        {name: [float(value) for value in values] for name, values in history.history.items()},
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
print(f"Training finished after {len(history.history['loss'])} epoch(s).")
print(f"Saved model: {model_path}")
print(f"Saved learning history: {history_path}")
