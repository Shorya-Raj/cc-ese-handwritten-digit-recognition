# Handwritten Digit Recognition

**Cloud Computing Essentials ESE project** · MNIST convolutional neural network · local Streamlit demo

## Project status

The model has been trained and evaluated, the local demo and detailed report are included, and the next project step is to try the app with real handwriting from the team. Cloud deployment is deferred.

**Start here:** [open the quick visual project map](guided_build/PROJECT_OVERVIEW.md).

## Results at a glance

- **98.92% test accuracy** on the held-out 10,000-image MNIST test set: 9,892 correct and 108 incorrect.
- **99.08% best validation accuracy** at epoch 7.
- **34,826 trainable parameters** in the CNN.
- Among the 108 errors, 25 still received a top softmax score of 90% or higher. These scores are not calibrated probabilities.

These are MNIST benchmark results. They do **not** establish the model’s accuracy on the team’s handwriting or on arbitrary camera images. See [the training report](guided_build/TRAINING_REPORT.md) for the full evaluation, plots, mistakes, limitations, and cited research review.

## Run the local demo

Requirements: Python compatible with the pinned packages in `requirements.txt`. Clone the private repository, then run these commands in PowerShell:

```powershell
git clone https://github.com/Shorya-Raj/cc-ese-handwritten-digit-recognition.git
cd cc-ese-handwritten-digit-recognition
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run .\guided_build\step_08_app.py
```

The app uses the included trained model at `guided_build/artifacts/digit_model.keras`. The first time you run the data or training steps, TensorFlow downloads MNIST. The raw MNIST dataset is not committed.

To retrain and regenerate the evaluation outputs, run these from the repository root:

```powershell
.\.venv\Scripts\python.exe .\guided_build\step_04_train.py
.\.venv\Scripts\python.exe .\guided_build\step_05_evaluate.py
.\.venv\Scripts\python.exe .\guided_build\step_06_report.py
```

Training takes longer than opening the demo; use the committed model for the first walkthrough.

## What is in this repository?

- `guided_build/step_01_data.py` through `step_08_app.py`: commented, numbered learning steps.
- `guided_build/MODEL_WALKTHROUGH.md`: plain-language explanation of data, preprocessing, CNN layers, and training.
- `guided_build/BUILD_JOURNAL.md`: chronological record of project actions, observations, and next steps.
- `guided_build/TRAINING_REPORT.md`: results, graphs, error analysis, comparison, limitations, and research review.
- `guided_build/REAL_HANDWRITING_PLAN.md`: the next small team evaluation.
- `guided_build/artifacts/`: trained model, evaluation records, and plots.

## Team workflow

1. Discuss an issue or task before starting larger changes.
2. Create a short branch from `main`, make a focused change, and open a pull request.
3. Ask a teammate to review the change and check the report or demo when relevant.
4. Merge after review so `main` stays usable.

See [CONTRIBUTING.md](CONTRIBUTING.md). The repository owner can add teammates in **Settings → Collaborators** using their GitHub usernames.

## Data and privacy

Do not commit secrets, virtual environments, or personal handwriting originals. The local example folder `guided_build/artifacts/real_handwriting/` is ignored by Git; get each writer’s agreement before collecting examples. Summarized results and plots can be shared with the team without uploading original images.

## License

No license has been selected. This private repository is for the course project; agree as a group before adding a license or making the code public.
