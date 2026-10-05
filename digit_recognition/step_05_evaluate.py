r"""Step 5: check the saved model on MNIST pictures kept out of training.

Run from the repository root in the VS Code terminal:
    .\.venv\Scripts\python.exe .\digit_recognition\step_05_evaluate.py

This checks MNIST test pictures. Real phone photos and personal handwriting
will need their own check before we claim the app works well for those inputs.
"""

import csv
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw


# SECTION 1 — Find the trained model and choose where results will go
OUTPUT_DIR = Path(__file__).with_name("artifacts")
MODEL_PATH = OUTPUT_DIR / "digit_model.keras"
RESULTS_PATH = OUTPUT_DIR / "test_results.json"
MATRIX_PATH = OUTPUT_DIR / "confusion_matrix.csv"
MISTAKES_PATH = OUTPUT_DIR / "example_mistakes.png"
if not MODEL_PATH.is_file():
    raise FileNotFoundError("Run step_04_train.py first to save the model.")


# SECTION 2 — Prepare the untouched test pictures in the same way as training
(_, _), (raw_test, test_labels) = tf.keras.datasets.mnist.load_data()
test_images = raw_test.astype("float32") / 255.0
test_images = test_images[..., np.newaxis]
print(f"Evaluating {len(test_images):,} held-out MNIST pictures")


# SECTION 3 — Measure overall accuracy and get one prediction per picture
model = tf.keras.models.load_model(MODEL_PATH)
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
probabilities = model.predict(test_images, verbose=0)
predictions = np.argmax(probabilities, axis=1)
print(f"Test accuracy: {test_accuracy:.2%}")
print(f"Test loss: {test_loss:.4f}")


# SECTION 4 — Count errors by true digit and predicted digit
# Matrix rows are correct answers; columns are model predictions.
matrix = np.zeros((10, 10), dtype=int)
np.add.at(matrix, (test_labels, predictions), 1)
per_digit_accuracy = np.diag(matrix) / matrix.sum(axis=1)
per_digit_precision = np.divide(
    np.diag(matrix), matrix.sum(axis=0),
    out=np.zeros(10, dtype=float), where=matrix.sum(axis=0) != 0,
)
per_digit_f1 = np.divide(
    2 * per_digit_precision * per_digit_accuracy,
    per_digit_precision + per_digit_accuracy,
    out=np.zeros(10, dtype=float),
    where=(per_digit_precision + per_digit_accuracy) != 0,
)
for digit, accuracy in enumerate(per_digit_accuracy):
    print(f"Digit {digit}: {accuracy:.2%} correct ({matrix[digit, digit]}/{matrix[digit].sum()})")


# SECTION 5 — Save the numbers for the journal, presentation, and later review
confidence = probabilities.max(axis=1)
correct_mask = predictions == test_labels
# Ten bins show how often predictions landed in each 10% confidence band.
confidence_bins = np.linspace(0, 1, 11)
correct_confidence_counts, _ = np.histogram(confidence[correct_mask], bins=confidence_bins)
wrong_confidence_counts, _ = np.histogram(confidence[~correct_mask], bins=confidence_bins)
results = {
    "dataset": "MNIST held-out test set",
    "test_examples": len(test_images),
    "test_loss": float(test_loss),
    "test_accuracy": float(test_accuracy),
    "wrong_predictions": int(np.count_nonzero(predictions != test_labels)),
    "per_digit_accuracy": {
        str(digit): float(accuracy)
        for digit, accuracy in enumerate(per_digit_accuracy)
    },
    "per_digit_metrics": {
        str(digit): {
            "precision": float(per_digit_precision[digit]),
            "recall": float(per_digit_accuracy[digit]),
            "f1": float(per_digit_f1[digit]),
            "support": int(matrix[digit].sum()),
        }
        for digit in range(10)
    },
    "macro_f1": float(per_digit_f1.mean()),
    "average_confidence_correct": float(confidence[correct_mask].mean()),
    "average_confidence_wrong": float(confidence[~correct_mask].mean()),
    "wrong_predictions_at_or_above_90pct_confidence": int(
        np.count_nonzero((~correct_mask) & (confidence >= 0.9))
    ),
    "confidence_bins": [float(value) for value in confidence_bins],
    "correct_confidence_counts": correct_confidence_counts.tolist(),
    "wrong_confidence_counts": wrong_confidence_counts.tolist(),
}
RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
with MATRIX_PATH.open("w", newline="", encoding="utf-8") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["actual/predicted", *range(10)])
    for digit, row in enumerate(matrix):
        writer.writerow([digit, *row])


# SECTION 6 — Make a visual sheet of the first 25 incorrect answers
# These examples make errors easier to discuss than one percentage alone.
wrong_indices = np.flatnonzero(predictions != test_labels)[:25]
sheet = Image.new("RGB", (5 * 104, 5 * 116), "white")
draw = ImageDraw.Draw(sheet)
for position, index in enumerate(wrong_indices):
    left = (position % 5) * 104
    top = (position // 5) * 116
    enlarged_digit = Image.fromarray(raw_test[index]).resize(
        (84, 84), resample=Image.Resampling.NEAREST
    )
    sheet.paste(enlarged_digit, (left + 10, top + 5))
    draw.text(
        (left + 10, top + 93),
        f"true {int(test_labels[index])} -> {int(predictions[index])}",
        fill="black",
    )
sheet.save(MISTAKES_PATH)

print(f"Incorrect predictions: {results['wrong_predictions']:,}")
print(f"Incorrect with at least 90% model confidence: {results['wrong_predictions_at_or_above_90pct_confidence']}")
print(f"Saved results: {RESULTS_PATH}")
print(f"Saved error counts: {MATRIX_PATH}")
print(f"Saved mistake examples: {MISTAKES_PATH}")
