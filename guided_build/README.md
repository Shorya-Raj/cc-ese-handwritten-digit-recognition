# Handwritten digit recognition: guided build

This is our new, learn-as-we-build version. We will add one small piece at a time in VS Code, discuss what it does, run it, and inspect the result before moving on.

## Our sequence

1. **Meet the data.** Load MNIST, read image shapes and labels, and look at one sample.
2. **Prepare the images.** Scale pixel values and add the grayscale channel expected by a CNN.
3. **Build the model.** Add and explain each layer.
4. **Train it.** Understand epochs, batches, validation, loss, and accuracy.
5. **Evaluate it.** Check held-out examples, mistakes, and limitations.
6. **Use it in an app.** Process an uploaded digit and show a prediction.
7. **Present the model.** Check the local demo, explain results and limits, and prepare for the viva. Cloud deployment is deferred.

## Step 1

Open `step_01_data.py` in VS Code. In VS Code's terminal, run:

```powershell
.\.venv\Scripts\python.exe .\guided_build\step_01_data.py
```

The script prints the dataset sizes, the first image's label, and the pixel range. It also saves `guided_build/first_mnist_digit.png` for you to open in VS Code.

## Current checkpoint: trained model, evaluation, and report

Open `guided_build/step_03_model.py` beside `guided_build/BUILD_JOURNAL.md`. The code is divided into numbered sections with comments. The journal explains what the printed layer shapes mean. To display the model structure yourself, run:

```powershell
.\.venv\Scripts\python.exe .\guided_build\step_03_model.py
```

The complete sequence now continues through `step_04_train.py`, `step_05_evaluate.py`, and `step_06_report.py`. Training and evaluation have been run for this project. The trained model and report are included in this repository. `step_07_prepare_upload.py` explains how an upload becomes model input, and `step_08_app.py` provides the upload/camera interface.

For the results, open [TRAINING_REPORT.md](TRAINING_REPORT.md) in VS Code's Markdown preview. It contains the graphs, tables, comparison with the earlier baseline, sample mistakes, an explanation of limits, and a cited review of research papers, dataset records, TensorFlow guidance, and community troubleshooting experiences. Open [BUILD_JOURNAL.md](BUILD_JOURNAL.md) to see the chronological record of what was done and why. The report can be regenerated from the saved results with:

For a simpler explanation of the data shapes, CNN layers, training, and image preparation, read [MODEL_WALKTHROUGH.md](MODEL_WALKTHROUGH.md) beside the code.

```powershell
.\.venv\Scripts\python.exe .\guided_build\step_06_report.py
```

You can also rerun `guided_build/step_02_prepare_images.py` to compare image shape and pixel values before reading the model.

## Run the local app

In the VS Code terminal, from the repository root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\guided_build\step_08_app.py
```

Open the local address printed by Streamlit. To gather and interpret team examples, follow [REAL_HANDWRITING_PLAN.md](REAL_HANDWRITING_PLAN.md). The app can save labelled examples locally when you press its save button.

This repository contains the guided project copy. Open the repository root in VS Code so the relative commands below resolve correctly.
