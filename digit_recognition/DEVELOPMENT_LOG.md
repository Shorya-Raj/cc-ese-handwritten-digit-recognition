# Project development log

This log records implementation milestones, technical decisions, observed results, and open work for the handwritten digit-recognition project.

## 5 October 2026 — Milestone 0: environment and project structure

**Purpose:** establish a reproducible local environment and keep the model workflow in separable scripts.

- The project uses an isolated `.venv` with pinned packages in `requirements.txt`: Streamlit 1.65.0, TensorFlow 2.21.0, Pillow 12.3.0, and NumPy 2.5.3.
- The scripts separate MNIST inspection, image preparation, CNN construction, training, evaluation, reporting, upload preprocessing, and the Streamlit interface.
- MNIST is downloaded by TensorFlow when required. The raw dataset and local environment are not committed.
- Baseline metrics from the earlier model were retained for comparison.

## 5 October 2026 — Milestone 1: inspect the dataset

**Purpose:** Define the MNIST input and target label.

1. Created `digit_recognition/step_01_data.py`. It loads MNIST using TensorFlow/Keras, prints the shapes of the image and label arrays, prints one image's label and pixel range, and saves an enlarged sample as `digit_recognition/first_mnist_digit.png`. This step does **not** train a model.
2. Ran the script with the project's Python environment. MNIST downloaded on this first run in the new environment. The script completed successfully.
3. Observed:

   ```text
   Training images: (60000, 28, 28)
   Training labels: (60000,)
   Test images: (10000, 28, 28)
   Test labels: (10000,)
   First image size: (28, 28)
   First image label: 5
   Pixel value range: 0 to 255
   ```

4. The original script printed a harmless Python warning because a Windows path inside its opening docstring contained backslashes. Changed the docstring to a raw string and updated its instructions to say VS Code. The warning does not affect the dataset output; this source cleanup has not yet been rerun.

**What the result means:** the training set has 60,000 labelled 28-by-28 grayscale images. The held-out test set has 10,000 more. The first picture is labelled digit 5. Pixel values from 0 to 255 represent darkness/brightness; the next step will prepare these values for the model.

**Next checkpoint:** open `step_01_data.py` and `first_mnist_digit.png` in VS Code, discuss what the arrays and label mean, then write Step 2 for image preparation. We will add the CNN only after that explanation.

## 5 October 2026 — Milestone 2: prepare images for the CNN

**Purpose:** Prepare MNIST images in the format expected by the CNN.

1. Created `digit_recognition/step_02_prepare_images.py`. It divides each pixel by 255 after converting to `float32`, then adds a one-channel dimension to each grayscale image. Labels stay as integers from 0 to 9.
2. Ran the script with the project's Python environment. It completed successfully.
3. Observed:

   ```text
   Before: (60000, 28, 28), uint8, pixels 0 to 255
   After:  (60000, 28, 28, 1), float32, pixels 0.0 to 1.0
   Test:   (10000, 28, 28, 1)
   One sample pixel: 3 becomes 0.0117647061124444
   First label remains 5
   ```

**Why:** a convolution layer expects height, width, and channel dimensions. MNIST is grayscale, so its channel count is 1. Scaling to 0–1 gives the network consistently sized numeric inputs. We apply the same preparation to training and test images.

**Training-data decision:** use the available 60,000 labelled MNIST training images for the initial project implementation. The earlier model already reached 98.92% accuracy on the separate 10,000-image MNIST test set, so more data has no demonstrated benefit yet. First check performance on genuine team handwriting. If its errors show a repeatable issue, consider targeted rotations, shifts, or suitable additional examples and measure whether they improve that use case. Keep the held-out test set out of training.

**Next checkpoint:** review the Step 2 output and image shape in VS Code, then construct a small CNN layer by layer. No new model has been trained in the project yet.

## 5 October 2026 — Milestone 3: build and inspect the CNN

**Purpose:** Build the CNN and verify its layer shapes.

1. Added numbered sections and explanatory comments to Steps 1 and 2, as requested. The comments describe what each part receives, changes, and prints. These edits explain the existing operations; they do not change the dataset or calculations.
2. Created `digit_recognition/step_03_model.py` with the same section-and-comment style. It builds a compact CNN, then prints `model.summary()`. It does **not** train or save a model.
3. Ran Step 3 using the project's Python environment. It completed successfully and showed these layer shapes:

   ```text
   Input image                  (28, 28, 1)
       ↓
   Conv2D: 32 learned filters   (26, 26, 32)      320 parameters
       ↓
   MaxPooling2D                (13, 13, 32)        0 parameters
       ↓
   Conv2D: 64 learned filters   (11, 11, 64)   18,496 parameters
       ↓
   MaxPooling2D                  (5, 5, 64)        0 parameters
       ↓
   Flatten                           (1600)        0 parameters
       ↓
   Dropout (during training)          (1600)        0 parameters
       ↓
   Dense + softmax              10 probabilities  16,010 parameters

   Total trainable parameters: 34,826
   ```

**How to read this:** `Conv2D` learns visual patterns such as short strokes, curves, and their combinations. Pooling shrinks each pattern map so the next layer handles fewer positions. `Flatten` turns the final 5 × 5 × 64 maps into 1,600 numbers. `Dense` uses those numbers to produce one score for each digit, and `softmax` converts the scores into probabilities. `Dropout` hides some values while *training* to discourage reliance on a few features; it is inactive for prediction. In the printed Keras summary, `None` at the front of each shape stands for an adjustable batch size.

**Why this model size:** it is small enough to train on this computer while still learning spatial patterns. We use the earlier successful baseline architecture as a starting point, but the project is constructing it afresh and will measure its own results. The parameter count is the number of adjustable values the training step will learn; creating the model has not learned them yet.

**Training-image decision reaffirmed:** the initial training run will use MNIST's 60,000 labelled training images, with a validation portion separated during training. The separate 10,000-image test set will be used only after training. We will collect genuine handwriting examples for the application check before deciding whether more examples or augmentation justify extra training time.

**Next checkpoint:** read `step_03_model.py` from top to bottom in VS Code, then add the training step and explain the optimizer, loss, epochs, batch size, and validation split before starting training.

## 5 October 2026 — Milestone 4: train and save the trained model

**Purpose:** Train the CNN and track validation performance.

1. Created `digit_recognition/step_04_train.py` with numbered sections for settings, image preparation, training configuration, training, and saving. It imports the model architecture from Step 3. The script uses all 60,000 MNIST training-set images: 54,000 for weight updates and 6,000 for validation. The separate 10,000 test images are held out.
2. Set a repeatable random seed of 42, eight maximum epochs, batches of 128, Adam optimizer, sparse categorical cross-entropy loss, and accuracy as the easy-to-read metric. An epoch is one full pass through the 54,000 training images. A batch is one small group used for each weight update. The loss measures how wrong the predicted probabilities are; lower is better. Validation is a progress check on the 6,000 images that do not update weights.
3. Added early stopping on validation loss with patience 2 and restoration of the best weights. This limits wasted training if validation stops improving and preserves the best observed model.
4. The first run completed eight epochs, but saving failed with `PermissionError: [WinError 5]` because this environment needed extra permission to write inside the project folder. That run produced no saved model. After correcting the output-directory permissions, reran the script successfully and saved both files.
5. Observed on the successful run:

   ```text
   Epoch 1: train accuracy 90.93%, validation accuracy 97.87%, validation loss 0.0739
   Epoch 7: train accuracy 98.85%, validation accuracy 99.08%, validation loss 0.0332
   Epoch 8: train accuracy 98.87%, validation accuracy 99.00%, validation loss 0.0346
   Completed: 8 epochs; best weights restored from epoch 7
   Saved: digit_recognition/artifacts/digit_model.keras
   Saved: digit_recognition/artifacts/training_history.json
   ```

**What the result means:** the model improved substantially while learning, and the validation result suggests it can recognize MNIST images it did not train on. Validation is used to choose and monitor the model, so it is not the final unbiased result. The untouched 10,000-image test set is the next check.

**Next checkpoint:** load the saved model in a separate evaluation script, measure held-out test accuracy, and look at mistakes by digit. Do not describe it as working on real personal handwriting until we test those images too.

## 5 October 2026 — Milestone 5: evaluate on held-out MNIST images

**Purpose:** Measure performance on the held-out MNIST test set.

1. Created `digit_recognition/step_05_evaluate.py` with numbered sections for input paths, test-image preparation, overall evaluation, per-digit error counts, saved result files, and a visual mistake sheet. It applies exactly the same pixel scaling and grayscale-channel step used during training.
2. Loaded the saved trained model and evaluated the held-out test set. The script completed successfully and saved `test_results.json`, `confusion_matrix.csv`, and `example_mistakes.png` under `digit_recognition/artifacts/`.
3. Measured **98.92% test accuracy** and **0.0327 test loss**: 9,892 correct and 108 incorrect predictions out of 10,000. Per-digit accuracy ranged from 97.62% for digit 9 to about 99.80% for digits 0 and 4. Digit 6 scored 98.02%.
4. Inspected the first 25 misclassified test images in the generated image sheet. Several are visibly ambiguous. This provides examples for discussion, though it is not a random sample of all mistakes.

**How to read the result:** this is a measured result on MNIST test images. It does not establish the same accuracy on the team's handwriting or uploaded photos. The confusion matrix separates true labels (rows) from predicted labels (columns), so we can identify which specific digit pairs need attention.

## 5 October 2026 — Milestone 6: create graphs and detailed report

**Purpose:** Record training curves, test metrics, errors, and the baseline comparison.

1. Installed Matplotlib 3.11.2 in the project's Python environment and added it to `requirements.txt`. The original package list did not include plotting support.
2. Copied the earlier project's saved `artifacts/metrics.json` into `digit_recognition/reference_baseline_metrics.json` as a traceable comparison source. The baseline reported 98.92% MNIST test accuracy and 0.0328 test loss on 10,000 images. This is an earlier saved run, not a controlled experiment in which only one setting changed.
3. Created and ran the commented `digit_recognition/step_06_report.py`. It reads saved JSON and CSV results and writes `digit_recognition/MODEL_EVALUATION.md` plus five plots under `digit_recognition/artifacts/plots/`: learning curves, per-digit results, full confusion matrix, mistakes-only matrix, and baseline comparison. It does not retrain the model.
4. Visually inspected the learning-curves and mistakes-only plots. The best validation loss occurred at epoch 7; the largest directed confusion was actual 9 predicted as 4 (8 images). The trained model matched the earlier baseline's displayed 98.92% test accuracy, a 0.00 percentage-point difference.
5. The report records the data split, preprocessing, layer architecture, 34,826 parameters, optimizer and loss, batch and epoch settings, all eight epoch results, test metrics, per-digit table, confusion patterns, examples, baseline comparison, limits, and reproduction commands.
6. Expanded Step 5 to calculate precision, recall, and F1 for each digit and a confidence distribution for correct versus wrong answers. Re-ran evaluation and report generation; the model's MNIST accuracy remained 98.92%, and macro F1 was 98.91%. Of the 108 mistakes, 25 still had a largest softmax output of at least 90%. This shows why a high displayed model score should not be presented as certainty.
7. Added and visually inspected `confidence_distribution.png`. The written report now explains these extra metrics in plain language and includes six plots in total.

**Why we did not add more training images now:** the standard MNIST split already provided 60,000 labelled training-set images, and this current run matched the earlier measured result. We do not yet have evidence that extra augmentation improves the actual upload/drawing experience. The next useful data is labelled handwriting from the team, tested through the real application input path.

**Next checkpoint:** build and explain the image-upload/drawing preprocessing and prediction flow, then collect real team handwriting examples and record those outcomes separately from MNIST scores.

## 5 October 2026 — Milestone 7: prepare a user's picture for the CNN

**Purpose:** Match uploaded images to the model's input format.

1. Created `digit_recognition/step_07_prepare_upload.py` with numbered sections and comments. It corrects photo orientation, handles transparency, makes grayscale, matches MNIST's bright-digit-on-dark-background format, suppresses faint background noise, crops around the ink, fits the digit within a 20-by-20 area, and centers its pixel mass on a 28-by-28 canvas.
2. Added `to_model_batch()` to scale the prepared image to 0–1 and shape it as `(1, 28, 28, 1)`: one image, 28 rows, 28 columns, one grayscale channel.
3. Ran the script on our saved MNIST example. It produced `digit_recognition/artifacts/prepared_preview.png`, reported the expected shape and pixel range, and the preview visibly remained a digit 5. This demonstrates the conversion path on one familiar sample. It does not measure real-photo accuracy.

**Next checkpoint:** connect this same function to the user-facing app, then inspect genuine paper and drawn inputs.

## 5 October 2026 — Milestone 8: create the local app and real-handwriting check

**Purpose:** Connect the trained model to a local interface and define a handwriting check.

1. Created `digit_recognition/step_08_app.py` with numbered sections and comments. It offers image upload or camera input. A drawing made in Paint can be saved as PNG and uploaded. It shows the original image beside the processed model input, the predicted digit, and the three highest model scores. It explains that a high score is not a guarantee.
2. Added an optional labelled-example control. When a person selects the true digit and presses the save button, the local app records the original image, prepared image, and a CSV result under `digit_recognition/artifacts/real_handwriting/`. This will let us review errors instead of relying on memory or screenshots.
3. Created `digit_recognition/HANDWRITING_EVALUATION.md` with a small collection target, review categories, and the rule for deciding whether extra training data or augmentation is justified.

4. Started the local Streamlit server for the local app on port 8502. It reported `http://localhost:8502` as its local address. The server launch succeeded; the browser interaction and genuine uploaded-image path still need a person to try them.

**Current status:** the app server is running locally and the real-handwriting plan is ready. Genuine team examples have not been collected yet. No real-handwriting accuracy is claimed.

## 5 October 2026 — Milestone 9: explain the model for study and review

**Purpose:** Document the architecture, data flow, and evaluation.

1. Created `digit_recognition/MODEL_ARCHITECTURE.md` as a plain-language companion to the numbered code sections. It maps the data path, file reading order, array shapes, CNN layers, parameter counts, training loop, graphs, held-out results, upload preparation, and the decision rule for using more images.
2. Included a layer-flow diagram, tables showing where all 34,826 parameters come from, links to the actual training and error plots, and a short VS Code reading sequence. The explanations distinguish the measured MNIST result from the still-pending real-handwriting result.
3. Kept cloud deployment out of the current model work, as requested. The immediate next step depends on genuine handwritten samples being tried in the local app.

## 5 October 2026 — Milestone 10: research other digit recognizers and their failure cases

**Purpose:** Review prior work and common failure modes relevant to the project.

1. Read the original LeCun et al. document-recognition paper and MNIST dataset notes to understand the CNN precedent and the fact that MNIST is a standardized, centered 28-by-28 benchmark rather than raw photos.
2. Read Simard et al.'s visual-document CNN best-practices paper on elastic distortions and additional transformed training examples. Compared its recommendations with TensorFlow's current training/validation/test and augmentation guidance, including the instruction to augment training only and the option of packaging preprocessing with a saved model.
3. Read NIST's EMNIST and Special Database 19 dataset pages and the EMNIST paper. Recorded the 280,000-example balanced EMNIST Digits split and the broader NIST collection as possible later options, not as data already added to our training run.
4. Read studies of MNIST-C, Kannada-MNIST/Dig-MNIST, and HWD+. These demonstrate why clean benchmark scores can miss corruption or collection-domain shifts, how a separate data source can be a tougher evaluation, and how writer diversity, collection method, and image resolution affect results and compute.
5. Read public Stack Overflow and Reddit troubleshooting discussions. Recorded them explicitly as anecdotal reports: builders described poor performance on personal/canvas digits despite good MNIST test scores, with polarity, centering, stroke thickness, contrast, and train/inference preprocessing raised as possible causes. They are not controlled experiments.
6. Added Section 7 to `MODEL_EVALUATION.md` through the report generator. It has linked source citations, source purpose and method, observed issues/results, evidence-quality notes, and five takeaways tailored to this model. Regenerated the report successfully; it is now about 2,831 words.

**What this changes:** nothing in the trained model. The review strengthens the reason for checking actual team inputs before choosing more training data or augmentation. It also supports the app's side-by-side view of original and prepared images. Cloud deployment remains deferred.

## 8 October 2026 — Documentation and repository audit

The original guided model and saved MNIST results were compared with the private GitHub copy. The guided model bytes match exactly; the earlier course-workspace baseline is a different artifact with the same reported MNIST accuracy. A separate seven-writer, 140-crop fine-tuning pilot from 6 October is now documented in `docs/MODEL_AND_EXPERIMENTS.md`: writer 6 stayed at 60%, writer 7 stayed at 50%, and the candidate was not adopted. The local app still loads the guided original.

The Desktop project and original workspace are not Git checkouts. The existing private repository has its own `main` history; a fresh clone is the correct local Git setup when network/authentication allows it. The Desktop sample folder has personal handwriting and is not covered by that folder's short `.gitignore`; the repository's own ignore rule covers its corresponding path. See `docs/PROJECT_AUDIT.md` and `docs/GIT_AND_GITHUB.md` for the inventory and safe workflow.

No training, model replacement, cloud deployment, or merge to `main` was performed during this audit. The repository documentation changes are on branch `docs/project-audit-2026-10-08` for review.

## 12–13 October 2026 — Hybrid inference integration

The local Streamlit application gained an optional AWS Lambda inference path. Image orientation, cropping, centering, and 28×28 preparation stay in Python on the presenting computer; the API receives the prepared pixel array. If AWS settings are unavailable, the app uses the local Keras model. A converted ONNX model is packaged for Lambda. Conversion parity was recorded on 1,000 MNIST images (same top-1/top-3; maximum score difference `7.15e-7`).

The 12 October deployment and 13 October recheck are recorded in [`../docs/WORK_LOG.md`](../docs/WORK_LOG.md). On 13 October, the included sample completed the live local Streamlit → Lambda → prediction path; recorded score difference against local Keras was at most `1.19e-7` on that sample. This verifies that sample path at that time, not new-writer accuracy, camera input, or future endpoint availability. The local app/model remains fallback. No new training or active-model replacement occurred.

## 14 October 2026 — Log reconciliation

The numbered development history was cross-checked against the current repository and its chronological work log. The work log is authoritative for GitHub/Git, AWS deployment/rechecks, and current project status; this file remains the record of guided model-building stages. No code execution or model/deployment change was part of this documentation reconciliation. GitHub reports the repository as public on 14 October; the earlier private-repository wording above remains a dated historical record, and this review did not establish when visibility changed.
