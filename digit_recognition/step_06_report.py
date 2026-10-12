r"""Step 6: turn saved training and test results into plots and a report.

Run from the repository root in the VS Code terminal:
    .\.venv\Scripts\python.exe .\digit_recognition\step_06_report.py

This script only reads recorded results. It does not retrain or change the model.
"""

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Save image files without opening a plot window.
import matplotlib.pyplot as plt
import numpy as np


# SECTION 1 — Load the numbers produced by the earlier pipeline scripts
HERE = Path(__file__).parent
ARTIFACTS = HERE / "artifacts"
PLOTS = ARTIFACTS / "plots"
PLOTS.mkdir(parents=True, exist_ok=True)
history = json.loads((ARTIFACTS / "training_history.json").read_text(encoding="utf-8"))
results = json.loads((ARTIFACTS / "test_results.json").read_text(encoding="utf-8"))
baseline = json.loads((HERE / "reference_baseline_metrics.json").read_text(encoding="utf-8"))
with (ARTIFACTS / "confusion_matrix.csv").open(newline="", encoding="utf-8") as source:
    rows = list(csv.reader(source))
matrix = np.array([[int(value) for value in row[1:]] for row in rows[1:]], dtype=int)
epochs = np.arange(1, len(history["loss"]) + 1)
best_epoch = int(np.argmin(history["val_loss"]) + 1)


# SECTION 2 — Plot how training and validation changed each epoch
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout="constrained")
axes[0].plot(epochs, np.array(history["accuracy"]) * 100, "o-", label="Training")
axes[0].plot(epochs, np.array(history["val_accuracy"]) * 100, "s-", label="Validation")
axes[0].set(title="Accuracy by epoch", xlabel="Epoch", ylabel="Accuracy (%)", xticks=epochs)
axes[0].grid(alpha=0.25)
axes[0].legend()
axes[1].plot(epochs, history["loss"], "o-", label="Training")
axes[1].plot(epochs, history["val_loss"], "s-", label="Validation")
axes[1].axvline(best_epoch, linestyle="--", color="gray", label=f"Best epoch: {best_epoch}")
axes[1].set(title="Loss by epoch (lower is better)", xlabel="Epoch", ylabel="Loss", xticks=epochs)
axes[1].grid(alpha=0.25)
axes[1].legend()
fig.savefig(PLOTS / "learning_curves.png", dpi=180)
plt.close(fig)


# SECTION 3 — Show how many test pictures of each digit were right or wrong
correct = np.diag(matrix)
wrong = matrix.sum(axis=1) - correct
fig, axis = plt.subplots(figsize=(10, 5), layout="constrained")
digit_positions = np.arange(10)
axis.bar(digit_positions, correct, label="Correct", color="#2474a6")
axis.bar(digit_positions, wrong, bottom=correct, label="Incorrect", color="#d95d39")
for digit in range(10):
    axis.text(digit, correct[digit] + wrong[digit] + 8,
              f"{correct[digit] / (correct[digit] + wrong[digit]):.2%}",
              ha="center", fontsize=8)
axis.set(title="Held-out MNIST accuracy by digit", xlabel="True digit", ylabel="Test pictures",
         xticks=digit_positions, ylim=(0, 1220))
axis.legend()
fig.savefig(PLOTS / "per_digit_results.png", dpi=180)
plt.close(fig)


# SECTION 4 — Plot the full confusion matrix and the mistakes alone
# Rows are actual digits and columns are predicted digits.
fig, axis = plt.subplots(figsize=(8, 7), layout="constrained")
image = axis.imshow(matrix, cmap="Blues")
for row in range(10):
    for column in range(10):
        value = matrix[row, column]
        if value:
            axis.text(column, row, str(value), ha="center", va="center",
                      color="white" if value > 500 else "black", fontsize=8)
axis.set(title="Confusion matrix: counts", xlabel="Predicted digit", ylabel="Actual digit",
         xticks=range(10), yticks=range(10))
fig.colorbar(image, ax=axis, label="Pictures")
fig.savefig(PLOTS / "confusion_matrix.png", dpi=180)
plt.close(fig)

errors_only = matrix.copy()
np.fill_diagonal(errors_only, 0)
fig, axis = plt.subplots(figsize=(8, 7), layout="constrained")
image = axis.imshow(errors_only, cmap="Oranges", vmin=0)
for row in range(10):
    for column in range(10):
        if errors_only[row, column]:
            axis.text(column, row, str(errors_only[row, column]),
                      ha="center", va="center", fontsize=8)
axis.set(title="Mistakes only: diagonal removed", xlabel="Predicted digit", ylabel="Actual digit",
         xticks=range(10), yticks=range(10))
fig.colorbar(image, ax=axis, label="Incorrect pictures")
fig.savefig(PLOTS / "mistake_patterns.png", dpi=180)
plt.close(fig)


# SECTION 5 — Compare the current model with the earlier saved baseline
fig, axis = plt.subplots(figsize=(7, 4.5), layout="constrained")
accuracy_values = [baseline["test_accuracy"] * 100, results["test_accuracy"] * 100]
bars = axis.bar(["Earlier baseline", "Current model"], accuracy_values,
                color=["#778899", "#2474a6"], width=0.5)
for bar, value in zip(bars, accuracy_values):
    axis.text(bar.get_x() + bar.get_width() / 2, value + 1,
              f"{value:.2f}%", ha="center", fontweight="bold")
axis.set(title="Held-out MNIST accuracy: two saved runs", ylabel="Accuracy (%)", ylim=(0, 105))
axis.grid(axis="y", alpha=0.25)
fig.savefig(PLOTS / "baseline_comparison.png", dpi=180)
plt.close(fig)


# SECTION 6 — Compare confidence distributions for right and wrong answers
# Each series is shown as a percentage of its own group, because there are
# many more correct answers than wrong ones.
bin_edges = np.array(results["confidence_bins"])
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
correct_distribution = np.array(results["correct_confidence_counts"]) / (results["test_examples"] - results["wrong_predictions"]) * 100
wrong_distribution = np.array(results["wrong_confidence_counts"]) / results["wrong_predictions"] * 100
fig, axis = plt.subplots(figsize=(10, 4.5), layout="constrained")
axis.bar(bin_centers - 0.021, correct_distribution, width=0.04,
         label="Correct answers", color="#2474a6")
axis.bar(bin_centers + 0.021, wrong_distribution, width=0.04,
         label="Wrong answers", color="#d95d39")
axis.set(title="Model confidence: correct versus wrong predictions",
         xlabel="Largest softmax output", ylabel="Share within each group (%)",
         xticks=bin_centers,
         xticklabels=[f"{int(left * 100)}–{int(right * 100)}" for left, right in zip(bin_edges[:-1], bin_edges[1:])])
axis.tick_params(axis="x", labelrotation=45)
axis.legend()
axis.grid(axis="y", alpha=0.25)
fig.savefig(PLOTS / "confidence_distribution.png", dpi=180)
plt.close(fig)


# SECTION 7 — Write a readable report beside the code and saved images
epoch_rows = "\n".join(
    f"| {epoch} | {history['accuracy'][epoch-1]:.2%} | {history['loss'][epoch-1]:.4f} "
    f"| {history['val_accuracy'][epoch-1]:.2%} | {history['val_loss'][epoch-1]:.4f} |"
    for epoch in epochs
)
digit_rows = "\n".join(
    f"| {digit} | {correct[digit]} | {wrong[digit]} | {correct[digit] + wrong[digit]} "
    f"| {correct[digit] / (correct[digit] + wrong[digit]):.2%} |"
    for digit in range(10)
)
metric_rows = "\n".join(
    f"| {digit} | {results['per_digit_metrics'][str(digit)]['precision']:.2%} "
    f"| {results['per_digit_metrics'][str(digit)]['recall']:.2%} "
    f"| {results['per_digit_metrics'][str(digit)]['f1']:.2%} |"
    for digit in range(10)
)
confusions = sorted(
    ((int(errors_only[actual, predicted]), actual, predicted)
     for actual in range(10) for predicted in range(10) if actual != predicted),
    reverse=True,
)[:5]
confusion_rows = "\n".join(
    f"| {actual} | {predicted} | {count} |" for count, actual, predicted in confusions
)
baseline_gap = (results["test_accuracy"] - baseline["test_accuracy"]) * 100
report = f"""# MNIST model evaluation

Generated from saved MNIST results. See `DEVELOPMENT_LOG.md` for implementation decisions and observed results.

## 1. Scope and data

The task is to classify a 28 × 28 grayscale image as digit 0–9. MNIST supplies 60,000 labelled training-set images and a separate 10,000-image test set. The training run used 54,000 images for weight updates and reserved 6,000 from the training set for validation. The test set was evaluated only after the model had been trained and saved. Its labels did not update model weights.

Images were converted from integer pixels 0–255 to `float32` pixels 0–1. A one-channel dimension changed their shape to `(28, 28, 1)`. Labels stayed as integer digit IDs.

## 2. Model and settings

| Item | Value and meaning |
| --- | --- |
| Architecture | Conv2D(32) → MaxPooling → Conv2D(64) → MaxPooling → Flatten → Dropout(0.25) → Dense(10, softmax) |
| Trainable parameters | 34,826 adjustable values |
| Optimizer | Adam, learning rate 0.001; adjusts weights after each batch |
| Loss | Sparse categorical cross-entropy; lower means predicted probability was closer to the correct digit |
| Batch size | 128 pictures per weight update |
| Maximum epochs | 8 full passes through the training subset |
| Random seed | 42, to make the run more repeatable |
| Early stopping | Monitored validation loss, patience 2, restored the best weights |
| Hardware | Native Windows CPU; TensorFlow reported no GPU support for this environment |

## 3. Training results

| Epoch | Training accuracy | Training loss | Validation accuracy | Validation loss |
| ---: | ---: | ---: | ---: | ---: |
{epoch_rows}

The lowest validation loss was **{min(history['val_loss']):.4f} at epoch {best_epoch}**, when validation accuracy was **{history['val_accuracy'][best_epoch-1]:.2%}**. Epoch 8's validation loss increased slightly, so the saved model uses the restored epoch {best_epoch} weights. Validation accuracy can be higher than training accuracy because dropout is active during training and inactive during validation; the two numbers are measured under different conditions.

![Training and validation accuracy and loss](artifacts/plots/learning_curves.png)

**How to read the graph:** both losses generally decreased while accuracy increased. The small late rise in validation loss is why saving the best weights matters. This graph alone cannot prove performance on phone photos or personal handwriting.

## 4. Held-out MNIST test results

| Measure | Result |
| --- | ---: |
| Test pictures | {results['test_examples']:,} |
| Correct predictions | {results['test_examples'] - results['wrong_predictions']:,} |
| Incorrect predictions | {results['wrong_predictions']:,} |
| Test accuracy | **{results['test_accuracy']:.2%}** |
| Test loss | {results['test_loss']:.4f} |

The percentage describes this **MNIST test set**. It is not a measured accuracy for photos, drawings in the future app, or handwriting from our team.

### Accuracy by digit

| True digit | Correct | Incorrect | Total | Accuracy |
| ---: | ---: | ---: | ---: | ---: |
{digit_rows}

![Correct and incorrect counts by digit](artifacts/plots/per_digit_results.png)

Digit 9 had the lowest accuracy ({correct[9] / (correct[9] + wrong[9]):.2%}), followed by digit 6 ({correct[6] / (correct[6] + wrong[6]):.2%}). Class sizes differ, so compare both percentages and counts.

### Precision, recall, and F1

**Recall** asks: of the pictures that truly show a digit, how many did we find? Here it equals the per-digit accuracy above. **Precision** asks: when the model predicts a digit, how often is that prediction correct? **F1** combines both into one number. These are useful when a model predicts one digit too often or misses it too often.

| Digit | Precision | Recall | F1 |
| ---: | ---: | ---: | ---: |
{metric_rows}

The unweighted average F1 across the ten digits was **{results['macro_f1']:.2%}**. It gives each digit equal importance, while overall accuracy gives each individual picture equal importance.

### Where the model confused digits

The confusion matrix has true digits on rows and predicted digits on columns. Its diagonal counts correct predictions. The second plot removes that diagonal so smaller error patterns are visible.

![Full confusion matrix](artifacts/plots/confusion_matrix.png)

![Incorrect predictions only](artifacts/plots/mistake_patterns.png)

The five largest directed confusions in this run were:

| Actual digit | Predicted digit | Pictures |
| ---: | ---: | ---: |
{confusion_rows}

These counts describe MNIST examples only. To inspect shapes behind the numbers, open the sheet below. It shows the first 25 incorrect test images in dataset order, labelled `true → predicted`; it is a set of examples, not a random sample.

![Twenty-five actual prediction mistakes](artifacts/example_mistakes.png)

### How confident was the model?

The mean largest softmax output was **{results['average_confidence_correct']:.2%}** for correct answers and **{results['average_confidence_wrong']:.2%}** for wrong ones. **{results['wrong_predictions_at_or_above_90pct_confidence']} of the {results['wrong_predictions']} wrong predictions** still had a largest output of at least 90%. The plot divides each group into ten confidence bands; it uses percentages within each group because correct answers greatly outnumber mistakes.

![Confidence distribution for correct and wrong predictions](artifacts/plots/confidence_distribution.png)

This score is useful for comparing model outputs, but it is not proof that a stated 90% is correct 90% of the time. We have not calibrated confidence, and the picture is based only on MNIST.

## 5. Comparison with the earlier saved run

| Saved run | MNIST test size | Test accuracy | Test loss |
| --- | ---: | ---: | ---: |
| Earlier baseline | {baseline['test_examples']:,} | {baseline['test_accuracy']:.2%} | {baseline['test_loss']:.4f} |
| Current model | {results['test_examples']:,} | {results['test_accuracy']:.2%} | {results['test_loss']:.4f} |

**Difference in reported test accuracy: {baseline_gap:+.2f} percentage points.** The current model matches the earlier saved baseline at the displayed precision. The baseline numbers were copied from the earlier project's `artifacts/metrics.json` into `reference_baseline_metrics.json`; this is a comparison of two saved runs, not a controlled study of a single change. The tiny loss difference should not be treated as meaningful evidence of improvement.

![Earlier baseline versus current model](artifacts/plots/baseline_comparison.png)

## 6. Interpretation, limits, and next decision

- The CNN learned MNIST well and reproduced the earlier 98.92% test accuracy.
- The current model used all 60,000 images in the standard MNIST training split. Other labeled handwriting datasets exist, but a larger count by itself does not show that those examples match our intended users.
- A phone photo or drawn digit can differ in background, thickness, position, size, lighting, and color from MNIST. The local app now prepares and displays these inputs, but the team still needs to try genuine handwriting.
- The displayed softmax value is a model output, not proof that the predicted probability is calibrated. An uncertain or wrong real-world image still needs visible handling in the app.
- This report records the MNIST training run. A later handwriting pilot and the temporary AWS inference deployment are documented in the root README and docs/WORK_LOG.md; neither changes the MNIST result reported here.

**Next action:** try the local app with labeled team examples, inspect original and prepared pictures, and decide whether the observed failures call for preprocessing changes, targeted augmentation, or more labeled examples. Keep the 10,000 MNIST test images out of training.

## 7. What published work and other builders found

This research review was completed on 5 October 2026. It covers the original MNIST/CNN work, later robustness and dataset studies, official dataset and TensorFlow documentation, and public troubleshooting discussions. Papers and maintained dataset/documentation pages are stronger evidence than individual forum reports; forum reports below are included as practical anecdotes, not controlled experiments.

### 7.1 Why CNNs and image distortions became standard

**LeCun, Bottou, Bengio, and Haffner (1998), “Gradient-Based Learning Applied to Document Recognition.”** This foundational work explains trainable convolutional networks for document tasks such as handwritten character recognition. The practical idea is to learn visual features from pixels instead of manually writing rules for every stroke. The original MNIST description also matters: the benchmark is already converted into small grayscale images with bounding-box normalization and centering. It is not a raw photograph benchmark. [Paper and author PDF](https://bottou.org/papers/lecun-98h), [MNIST dataset notes](https://yann.lecun.org/exdb/mnist/index.html)

**Simard, Steinkraus, and Platt (2003), “Best Practices for Convolutional Neural Networks Applied to Visual Document Analysis.”** The paper compared practical network choices on MNIST and emphasized CNNs and adding plausible distorted training examples. They studied transformations including shifts, rotations, skew, and elastic deformations, which approximate natural variation in handwriting. The purpose is to make the model tolerate label-preserving changes without collecting a new human-written sample for every small variation. This is useful precedent, but it does not mean every transformation helps every input style; changes that turn a digit into another digit would teach the wrong label. [Microsoft Research paper record and PDF](https://www.microsoft.com/en-us/research/publication/best-practices-for-convolutional-neural-networks-applied-to-visual-document-analysis/)

**TensorFlow's training and augmentation guides.** Their official Keras examples demonstrate distinct training, validation, and test roles. Their augmentation guide describes operations such as rotation, zoom, crop, and contrast, and says to apply random augmentation to training data only. It also explains an engineering choice: preprocessing inside the saved model can travel with that model; preprocessing outside it has to be reproduced consistently at prediction time. That matters for our app because the MNIST training path currently scales and reshapes images, while uploaded pictures also go through crop, contrast, inversion, and centering. [Training and evaluation guide](https://www.tensorflow.org/guide/keras/training_with_built_in_methods), [data augmentation guide](https://www.tensorflow.org/tutorials/images/data_augmentation)

### 7.2 Larger and more varied handwriting datasets

**EMNIST and NIST Special Database 19.** NIST describes EMNIST as handwriting derived from NIST Special Database 19 and converted into an MNIST-compatible 28 × 28 format. The EMNIST Digits split contains 280,000 balanced digit examples; NIST SD19 describes over 800,000 checked character images from 3,600 writers. These datasets exist to provide more writers and a broader character collection in a convenient format. They are candidates for later experiments if our own checks reveal missing handwriting variety. Their size alone does not guarantee a match to our team's writing or photo conditions; labels, split, preprocessing, and source should be documented. [NIST EMNIST page](https://www.nist.gov/itl/products-and-services/emnist-dataset), [NIST SD19 page](https://www.nist.gov/srd/nist-special-database-19), [EMNIST paper](https://arxiv.org/abs/1702.05373)

**HWD+ high-resolution handwritten digits study.** The authors collected about 13,580 digit images from 97 writers, recorded writer characteristics, and asked participants to write repeated digits using a controlled sheet and pen. They note that the volunteer group was smaller and not randomly sampled, so it cannot support broad population claims. Their 28 × 28 version enables direct MNIST-style experiments. Their comparison found higher-resolution images could improve some classification results, but training one CNN on 100 × 100 images took about 25 times as long as on low-resolution images. The lesson for our project is to record how examples were collected and balance realism against cost; a higher resolution is not automatically worth that cost for this small demo. [HWD+ study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9702948/)

**Kannada-MNIST and its Dig-MNIST set.** This project released a drop-in Kannada numeral dataset plus a separate 10,000-image real-world test set. Its baseline CNN scored 96.8% on the main test set and 76.1% on Dig-MNIST. Those numerals use a different script, so these scores cannot be compared directly with our Arabic-digit MNIST result. The useful part is the study design: make a separate evaluation set from a different collection process to expose a domain shift that an in-domain test can hide. [Kannada-MNIST paper](https://arxiv.org/abs/1908.01242)

### 7.3 Image corruption and domain shift

**MNIST-C (Mu and Gilmer, 2019).** This benchmark applies 15 broad image corruptions to MNIST test pictures, including noise, blur, brightness, pixelation, and elastic changes. The paper reports that a tested CNN's mean accuracy fell from 99.22% on clean MNIST to 91.21% on the corruption suite; it also reports that error increased by roughly a factor of ten. The authors show that training on the benchmark's held-out corruption conditions defeats the purpose of testing out-of-distribution robustness. For us, this supports testing real input conditions and keeping an evaluation set separate from augmentation experiments. The corruption benchmark is not the same thing as testing actual handwriting from our team. [MNIST-C paper](https://arxiv.org/abs/1906.02337)

### 7.4 What people reported when they tried their own writing

These are public self-reports, so they help generate troubleshooting ideas but do not establish general performance claims.

- In a Stack Overflow thread, one builder reported about 96% on MNIST but 80% on their own handwriting after cropping, resizing to 28 × 28, centering, and inverting the background. They described thinner strokes and contrast differences; their thresholding and contrast enhancement attempts did not solve the gap. The replies discussed normalizing training and test images consistently or adding representative target examples. This is a useful warning that resizing and inversion alone may not erase writer/style differences. [Thread and follow-up discussion](https://stackoverflow.com/questions/27925358/pre-processing-before-digit-recognition-for-nn-cnn-trained-with-mnist-dataset)
- In a newer Stack Overflow report about a canvas app and a Flask prediction service, the builder said their local MNIST accuracy was about 98% but deployed canvas predictions were often wrong. The post's follow-up identifies reversed foreground/background polarity: scaling values by 255 did not correct the inversion. The author reports that inverting the image and visually comparing saved preprocessed samples with MNIST resolved the issue. This directly supports showing the processed 28 × 28 image in our app. [Question, answer, and author's follow-up](https://stackoverflow.com/questions/79980878/cnn-digit-recognition-model-high-local-accuracy-but-poor-predictions-after-depl)
- A Reddit learner described roughly 98% MNIST test accuracy but unreliable predictions in a Tkinter drawing interface, particularly for 9, 7, and 1. Replies raised possible issues with drawing color, thresholding, and model setup; the discussion did not provide a controlled comparison, so treat those remedies as hypotheses. The practical theme is the same: benchmark accuracy and interactive-input accuracy are different measurements. [Discussion](https://www.reddit.com/r/learnmachinelearning/comments/t22q50/)

### 7.5 Takeaways for this project

1. **Inspect preprocessing visually before changing the CNN.** Our sample currently passes through the upload-preparation function and remains recognizable, but this is only one MNIST example. When using real images, compare the original and 28 × 28 processed version and inspect polarity, crop, centering, stroke thickness, and contrast.
2. **Keep the test conditions honest.** The 98.92% result is for the 10,000 held-out MNIST examples. Team handwriting should have its own separate labeled results. If there are enough writers, keep some writers out of the tuning examples; otherwise report simple counts and call the check exploratory.
3. **Prefer a targeted fix over indiscriminately making the dataset bigger.** Fix an inversion or crop problem in preprocessing. If clear inputs repeatedly fail because the writing differs, then consider representative new samples or gentle, label-preserving transformations. Generate them only from training data and inspect the transformed digits before training.
4. **Consider EMNIST Digits only as a candidate follow-up dataset.** It is larger and compatible in image size, but its source does not guarantee it matches our users. A comparison should use the same held-out real-handwriting set and report the outcome by input style and digit.
5. **Do not over-read a high softmax score.** Our own MNIST evaluation found 25 wrong predictions whose top score was at least 90%. The app therefore calls it a model score and displays alternatives rather than treating it as a guarantee.

These are research-informed options, not changes made to the model. A later handwriting pilot and temporary AWS inference deployment are documented in the root README and docs/WORK_LOG.md. A new-writer check would give more independent handwriting evidence.

## 8. Reproduce the saved results and plots

From the repository root in the VS Code terminal:

```powershell
.\\.venv\\Scripts\\python.exe .\\digit_recognition\\step_03_model.py
.\\.venv\\Scripts\\python.exe .\\digit_recognition\\step_04_train.py
.\\.venv\\Scripts\\python.exe .\\digit_recognition\\step_05_evaluate.py
.\\.venv\\Scripts\\python.exe .\\digit_recognition\\step_06_report.py
```

`step_04_train.py` retrains and may produce slightly different values on another machine; the saved JSON, CSV, model, and plots document this particular run. `step_06_report.py` redraws plots from those saved result files without retraining.
"""
(HERE / "MODEL_EVALUATION.md").write_text(report, encoding="utf-8")
print(f"Report saved to: {HERE / 'MODEL_EVALUATION.md'}")
print(f"Plots saved to: {PLOTS}")
