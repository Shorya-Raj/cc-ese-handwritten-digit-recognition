# Handwritten Digit Recognition

**Cloud Computing Essentials ESE** · MNIST convolutional neural network · local Streamlit interface with optional AWS inference

## Overview

This repository contains a CNN that classifies grayscale images of handwritten digits 0–9, an evaluation on MNIST, and a Streamlit interface for image upload or camera input. The interface can use the included model locally or send its prepared 28 × 28 pixel array to the AWS inference API described below.

[Project workflow and current status](digit_recognition/PROJECT_OVERVIEW.md)

## Results

- **98.92% test accuracy** on the held-out 10,000-image MNIST test set: 9,892 correct and 108 incorrect.
- **99.08% best validation accuracy** at epoch 7.
- **34,826 trainable parameters**.
- Of the 108 test errors, 25 received a top softmax score of at least 90%. These scores are not calibrated probabilities.

These figures describe performance on MNIST. They do not establish accuracy on the team's handwriting or on arbitrary camera images. A 140-crop, seven-writer handwriting pilot has since been run. It did not improve either writer check after fine-tuning, so the original guided model remains the app model. Read [the model and experiment record](docs/MODEL_AND_EXPERIMENTS.md) for the split, results, and limitations. A temporary hybrid AWS inference endpoint was deployed and checked on 12 October 2026; check its current AWS state before a later demo.

## Current project records

- [Project audit and remaining work](docs/PROJECT_AUDIT.md)
- [Model and experiments](docs/MODEL_AND_EXPERIMENTS.md)
- [Git and GitHub guide](docs/GIT_AND_GITHUB.md)
- [Dated work log](docs/WORK_LOG.md)

This repository is the team's versioned source for the current app, guided model, and evaluation. The original course workspace contains a distinct baseline and a later experimental fine-tuning run; the Desktop guided folder is another local copy. On the project computer, an existing clone of this repository is nested inside `CC ESE 2`. Work in that clone, or make a fresh clone on another computer. Compare any older copy before transferring a change; do not replace the guided app or model with the separate baseline or fine-tuned candidate.

## Hybrid demo: local Streamlit + AWS inference

The Streamlit page runs on the presenting laptop. Image cleanup and resizing happen there; only the resulting 28 × 28 grayscale pixel array is sent over HTTPS to an AWS Lambda function, which runs the CNN and returns ten scores. The AWS model is an ONNX export of the included Keras model. Its Lambda code, package builder, and live verification script are in `cloud/`. The original image is not sent by the app. The optional labelled-sample feature still saves images on the laptop.

The AWS Function URL is publicly reachable, but the handler requires a long random bearer token. Keep the token only in the Lambda environment and the ignored `.streamlit/secrets.toml`; never commit or paste it into source code. This is a small class-demo gate, not user accounts or strong abuse protection: even unauthorized requests can invoke Lambda before the handler rejects them. Use only agreed demo handwriting. The current AWS account was confirmed to have an active Free plan on 12 October 2026. Check the remaining credits in the AWS billing console before the demo, do not upgrade to a paid plan for this demo, and remove the resources after evaluation.

### Current deployment and demo

On 12 October 2026 the function `cc-ese-digit-inference` was created in `ap-southeast-2` with a private S3 package bucket, an execution role, a three-day CloudWatch log retention policy, and an HTTPS Function URL. The URL and token are saved only in the ignored `.streamlit/secrets.toml` on this computer. A fresh live check on 13 October returned 401 for an unauthenticated call, 400 for a malformed input, and the same sample prediction as local Keras with a maximum score difference of `1.19e-7`. The Streamlit upload flow also returned digit 5. The ONNX and Keras models agreed on top-1 and top-3 for 1,000 MNIST test images during the original model conversion.

The account did not permit reserving two Lambda concurrent executions because it would reduce unreserved concurrency below AWS's minimum of ten. The URL and random token have not been published, and the Free plan limits out-of-pocket spending while it remains active; this is still a temporary public endpoint, so delete it promptly after the course demo.

From the current repository on this computer, start or restart the app in PowerShell:

```powershell
cd 'C:\Users\shory\OneDrive\Documents\ChatGPT\CC ESE 2\cc-ese-handwritten-digit-recognition'
& .\start-demo.ps1
```

Open `http://127.0.0.1:8502/` on the same laptop. The page should say **Inference: AWS Lambda**. If port 8502 is already occupied by this app, use that open page instead of launching a second server. Run `python cloud/verify_deployment.py` from the repository root to repeat the live sample and rejection checks. The original image remains in the local Streamlit process; the 28 × 28 array goes to AWS.

To rebuild the AWS ZIP later, run `python cloud/build_zip.py` with Python 3.12. It downloads Linux wheels for Lambda, so Docker and SAM are not required. The resulting ZIP is about 62 MiB, above Lambda's 50 MB direct upload limit, and must be uploaded to private S3 before updating the function. A fresh clone does not contain `.streamlit/secrets.toml`; obtain the endpoint and create a new token safely rather than copying credentials into Git.

### After the evaluation

After the evaluation, run `.\cloud\teardown.ps1` from the repository root while signed in to the same AWS account. If the AWS CLI session expired, refresh it with `& 'C:\Users\shory\AppData\Local\Programs\Amazon\AWSCLIV2\aws.exe' login --region ap-southeast-2` first. The script deletes the named Lambda function, its CloudWatch log group, the one deployment ZIP and S3 bucket, and the dedicated execution role. Confirm they are gone in AWS, then remove `.streamlit/secrets.toml` to make the app use the included local model. Deleting AWS resources does not delete the source or local model. Check the AWS billing/free-plan page afterward for any final usage.

## Run the application

On this computer, Python 3.12, AWS CLI 2, Streamlit, TensorFlow, and the remaining packages have been installed and checked. Run the one-time setup again whenever you need to repair or check them:

```powershell
cd 'C:\Users\shory\OneDrive\Documents\ChatGPT\CC ESE 2\cc-ese-handwritten-digit-recognition'
& .\setup-local.ps1
& .\start-demo.ps1
```

The setup script installs the full `requirements.txt` into this computer's Python user packages, so both AWS inference and the local TensorFlow fallback work. A virtual environment could not be created inside this OneDrive checkout, so the launcher uses the already working Python 3.12 installation. The start script detects the existing server on port 8502 and opens it; otherwise it starts Streamlit in that PowerShell window. Keep the window open during the demo, then press `Ctrl+C` to stop the local page. Stopping Streamlit does not delete or stop the AWS function.

For a fresh computer, clone this repository, install Python 3.12, and run the following commands from the clone. The ignored AWS secrets file is specific to the current computer and is never included in a clone. These commands start the included model locally; configuring AWS inference requires a separate endpoint and token.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run digit_recognition/step_08_app.py
```

In local mode, the app loads `digit_recognition/artifacts/digit_model.keras`. TensorFlow downloads MNIST on the first run of a data or training script; the raw dataset is not stored in this repository.

To retrain and regenerate the evaluation files:

```powershell
& 'C:\Users\shory\AppData\Local\Programs\Python\Python312\python.exe' .\digit_recognition\step_04_train.py
& 'C:\Users\shory\AppData\Local\Programs\Python\Python312\python.exe' .\digit_recognition\step_05_evaluate.py
& 'C:\Users\shory\AppData\Local\Programs\Python\Python312\python.exe' .\digit_recognition\step_06_report.py
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
