# Handwritten Digit Recognition

**Cloud Computing Essentials ESE** · MNIST convolutional neural network · local Streamlit application

## Overview

This repository contains a CNN that classifies grayscale images of handwritten digits 0–9, an evaluation on MNIST, and a local interface for image upload or camera input. The app and report use the included trained model.

[Project workflow and current status](digit_recognition/PROJECT_OVERVIEW.md)

## Results

- **98.92% test accuracy** on the held-out 10,000-image MNIST test set: 9,892 correct and 108 incorrect.
- **99.08% best validation accuracy** at epoch 7.
- **34,826 trainable parameters**.
- Of the 108 test errors, 25 received a top softmax score of at least 90%. These scores are not calibrated probabilities.

These figures describe performance on MNIST. They do not establish accuracy on the team's handwriting or on arbitrary camera images. A 140-crop, seven-writer handwriting pilot has since been run. It did not improve either writer check after fine-tuning, so the original guided model remains the app model. Read [the model and experiment record](docs/MODEL_AND_EXPERIMENTS.md) for the split, results, and limitations. Cloud hosting is under review and has not been deployed.

## Current project records

- [Project audit and remaining work](docs/PROJECT_AUDIT.md)
- [Model and experiments](docs/MODEL_AND_EXPERIMENTS.md)
- [Git and GitHub guide](docs/GIT_AND_GITHUB.md)
- [Dated work log](docs/WORK_LOG.md)

This repository is the team's versioned source for the current app, guided model, and evaluation. The original course workspace contains a distinct baseline and a later experimental fine-tuning run; the Desktop guided folder is another local copy. On the project computer, an existing clone of this repository is nested inside `CC ESE 2`. Work in that clone, or make a fresh clone on another computer. Compare any older copy before transferring a change; do not replace the guided app or model with the separate baseline or fine-tuned candidate.

For a future Streamlit Community Cloud deployment, select this GitHub repository, branch `main`, and entrypoint `digit_recognition/step_08_app.py`. The dependency file is the root `requirements.txt`, and the app loads `digit_recognition/artifacts/digit_model.keras`. Local edits become part of the GitHub source only after they are committed and pushed. Hosting has not been completed; review the app's local sample-saving feature before public deployment.

## Run the application

The repository is private. After you have access, clone it and run these commands in PowerShell:

```powershell
git clone https://github.com/Shorya-Raj/cc-ese-handwritten-digit-recognition.git
cd cc-ese-handwritten-digit-recognition
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run .\digit_recognition\step_08_app.py
```

The app loads `digit_recognition/artifacts/digit_model.keras`. TensorFlow downloads MNIST on the first run of a data or training script; the raw dataset is not stored in this repository.

To retrain and regenerate the evaluation files:

```powershell
.\.venv\Scripts\python.exe .\digit_recognition\step_04_train.py
.\.venv\Scripts\python.exe .\digit_recognition\step_05_evaluate.py
.\.venv\Scripts\python.exe .\digit_recognition\step_06_report.py
```

## Repository contents

- `digit_recognition/step_01_data.py` through `step_08_app.py`: data, model, training, evaluation, preprocessing, and application scripts.
- [Model architecture](digit_recognition/MODEL_ARCHITECTURE.md): input processing, CNN layers, and training setup.
- [Evaluation report](digit_recognition/MODEL_EVALUATION.md): metrics, plots, error analysis, limitations, and cited research.
- [Development log](digit_recognition/DEVELOPMENT_LOG.md): implementation decisions, observations, and remaining work.
- [Pipeline notes](digit_recognition/PIPELINE.md): script order and run commands.
- `digit_recognition/artifacts/`: saved guided model, evaluation files, and plots.
- `docs/`: current audit, Git workflow, and handwriting experiment record.

## Contributing

Review [CONTRIBUTING.md](CONTRIBUTING.md) before making changes. Use a short branch and pull request for group changes. The repository owner can invite team members through **Settings → Collaborators**.

## Data handling

Do not commit credentials, virtual environments, or original personal handwriting samples. The local folder `digit_recognition/artifacts/real_handwriting/` is ignored by Git. Get contributors' agreement before collecting examples, and use labels rather than names where possible.

## License

No license has been selected. Keep the repository private unless the group agrees on its distribution and licensing.
