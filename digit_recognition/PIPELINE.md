# Model pipeline

The eight scripts separate data inspection, preprocessing, model construction, training, evaluation, report generation, inference-image preparation, and the local interface.

## Run order

From the repository root, use the project's virtual environment:

1. `step_01_data.py` — inspect MNIST shapes and labels.
2. `step_02_prepare_images.py` — scale pixels and add the channel dimension.
3. `step_03_model.py` — construct the CNN and print its layer summary.
4. `step_04_train.py` — train and save the model.
5. `step_05_evaluate.py` — evaluate on the held-out MNIST test set.
6. `step_06_report.py` — create the evaluation report and plots from saved results.
7. `step_07_prepare_upload.py` — convert an uploaded image to model input.
8. `step_08_app.py` — run the local Streamlit interface.

The trained model and measured outputs are included under `artifacts/`, so the app can be opened without retraining.

```powershell
.\.venv\Scripts\python.exe .\digit_recognition\step_04_train.py
.\.venv\Scripts\python.exe .\digit_recognition\step_05_evaluate.py
.\.venv\Scripts\python.exe .\digit_recognition\step_06_report.py
.\.venv\Scripts\python.exe -m streamlit run .\digit_recognition\step_08_app.py
```

See [MODEL_ARCHITECTURE.md](MODEL_ARCHITECTURE.md) for the model and data-flow details and [MODEL_EVALUATION.md](MODEL_EVALUATION.md) for results and limitations.
