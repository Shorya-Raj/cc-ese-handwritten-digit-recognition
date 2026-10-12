# Project work log

This log records completed actions, evidence, decisions and open work. It is a review record of the build, not a claim that every proposed item has been implemented. For the numbered training and app stages from 5 October, see the existing `guided_build/BUILD_JOURNAL.md` in the guided project and `digit_recognition/DEVELOPMENT_LOG.md` in GitHub.

## 5 October 2026 — Guided model and local application

- A separate Desktop project was created for learning the model step by step in VS Code.
- Numbered scripts inspected MNIST, prepared images, constructed a 34,826-parameter CNN, trained it, evaluated it and generated figures. The guided model reached 98.92% on the 10,000-image MNIST test set.
- The local Streamlit app was built to accept an uploaded image or camera photo, show the processed 28 × 28 input and model scores, and optionally save a labelled example locally.
- A private GitHub repository was created with a reorganized `digit_recognition/` project, the guided model, plots, report, README and contributor instructions. The original Desktop and workspace folders were not converted into Git checkouts.

**Source records:** saved `training_history.json`, `test_results.json`, confusion matrix, model artifact, training report and GitHub commit history. These dates and outcomes come from those existing records; they were not rerun on 8 October.

## 6 October 2026 — Seven-writer handwriting pilot

- Two contributor sheets supplied 140 labelled crops across seven writers, two rounds and digits 0–9.
- The original guided model and a separate fine-tuned copy were compared on writer 6 validation, writer 7 pilot holdout and the MNIST test set.
- Writer scores did not improve: 60% remained 60% on writer 6; 50% remained 50% on writer 7. MNIST changed from 98.92% to 98.98%.
- The candidate stayed separate. The app continued loading the original guided model.

**Source records:** `fine_tune_handwriting.py`, `artifacts/handwriting_finetune_2026-10-06/metrics.json`, `REPORT.md`, prediction CSV and plots. The source photographs were not put in the saved result folder.

## 8 October 2026 — Course and repository audit

1. Reviewed the course evaluation plan, syllabus, CO/PO mapping, session plan, question bank and relevant unit notes. Wrote `STREAMLIT_CLOUD_COURSE_ALIGNMENT_REPORT.html`. It concludes that Streamlit Community Cloud appears compatible with the written cloud-application brief, conditional on instructor confirmation and additional CO3/CO4 explanation. No cloud app was deployed.
2. Listed the original workspace and Desktop guided project. Both have project files but no `.git` directory. The Desktop folder has one saved labelled example; its `.gitignore` originally missed that example directory.
3. Read the private GitHub repository through the connected GitHub app. At audit time it had `main` at `ecd3c14e28cb33875d8c6cc5eca138d15dc1dd98`, three commits, 33 tracked files, and an open real-handwriting issue. Its `.gitignore` does exclude the repository's handwriting sample folder.
4. Compared artifact identities. The GitHub model Git blob ID matches the Desktop guided model. The original workspace baseline and fine-tuned candidate are different files, each with its own SHA-256 recorded in `PROJECT_AUDIT.md` and `MODEL_AND_EXPERIMENTS.md`.
5. Compared saved MNIST result summaries between Desktop and GitHub; the core values agree: 98.92%, 108 wrong, eight epochs and best validation accuracy 99.08%.
6. Inspected training, preprocessing, app and fine-tuning source. Confirmed the app still has a local sample-save button; the fine-tuning pilot used a separate copy and did not change the active app model.
7. Checked local Git CLI. Git is installed (2.53.0.windows.3). The normal sandboxed command could not connect to GitHub on port 443. A later elevated check with credential prompts disabled reached GitHub but lacked a Git CLI username for the private repository. No `git init`, clone, push or merge was executed through the CLI. A new local history was deliberately not created over the existing GitHub repository.
8. Wrote this audit, a model-and-experiment record, and a plain-language Git/GitHub guide with source links and safe commands.
9. Created GitHub branch `docs/project-audit-2026-10-08` from the verified `main` commit. It is a separate review branch; `main` was not changed by branch creation.
10. Added `guided_build/artifacts/real_handwriting/` to the Desktop project's `.gitignore` so the existing personal sample folder is excluded if that old folder is ever staged under Git. No sample files were moved or deleted.
11. Added four current project documents and corrected stale README, model, handwriting and development-log wording on that GitHub branch. Compared the branch with `main`: 11 documentation files changed, no model or Python source files changed. Opened draft pull request [#2](https://github.com/Shorya-Raj/cc-ese-handwritten-digit-recognition/pull/2) for review; it has not been merged.
12. Copied the four new project records into the Desktop guided project's `docs/` folder and added a root `README.md` there, so they can be opened beside the app in VS Code. These Desktop copies are not automatically synchronized with the GitHub branch.

## 9 October 2026 — Working-copy reconciliation

- Found a Git clone nested at `CC ESE 2/cc-ese-handwritten-digit-recognition/`. Its `origin` is the existing private GitHub repository; local `main` and GitHub `main` both pointed to `c1396be724dca6485128cbdc44cffe0ae6ccba88`. Pull request #2 was merged on 8 October. The parent workspace itself remains outside Git.
- Compared the eight guided Python steps in the parent workspace with the clone. Their model, evaluation, preprocessing and app logic match; the report output name and wording were adapted for the repository. The original baseline model and the fine-tuned candidate are different artifacts by design and are not the app model.
- Chose the clone as the working source for the team app and its future GitHub deployment. Updated the repository, parent-workspace and Desktop guidance to identify the correct folder. No baseline model, candidate model, source photograph, personal sample or per-writer prediction file was moved into Git.

## 10 October 2026 — Hybrid AWS inference preparation

- Added an optional AWS inference client to the local Streamlit app. It sends the preprocessed 28 × 28 grayscale pixels to the endpoint and shows whether predictions run locally or in AWS. Local model inference remains available when `.streamlit/secrets.toml` is absent.
- Prepared an initial Lambda container handler, Dockerfile and AWS SAM template in the parent workspace. This prototype was superseded by the ONNX ZIP deployment recorded on 12 October; the container files are not part of this repository update. The deployed handler checks a random bearer token, validates input shape/range, and returns ten scores without storing request images or predictions.
- Updated the root README and project docs with the data flow, setup, teardown, and current deployment status. No AWS resources were created: Docker, AWS CLI, SAM CLI, and local AWS credentials are not present on this computer. The endpoint and live cloud inference therefore remain pending.

## 12 October 2026 — Temporary hybrid AWS deployment

- Installed the project's full local Python requirements and verified that TensorFlow loads the guided Keras model. The user's AWS CLI 2.37.12 was already installed; signed in with `aws login` for `ap-southeast-2` and confirmed the account's active Free plan. A later API read in the same session reported $120 remaining credits; consult the billing console for the current value rather than treating a screenshot or earlier reading as fixed.
- Exported the guided Keras model to `cloud/digit_model.onnx`. On 1,000 MNIST test images, ONNX and Keras agreed on all top-1 and top-3 predictions; maximum score difference was `7.15e-7`. Built a Python 3.12 x86_64 Lambda ZIP with Linux wheels, about 62 MiB compressed and 192 MiB uncompressed. Docker and SAM were unnecessary.
- Created a dedicated execution role, private S3 package bucket, Lambda function `cc-ese-digit-inference` in `ap-southeast-2`, Function URL, random bearer token held in the Lambda environment and ignored local `.streamlit/secrets.toml`, and a three-day CloudWatch log retention policy. The account rejected an optional two-execution reserved-concurrency limit because it would leave fewer than ten unreserved executions; no concurrency cap was installed.
- Live checks returned 401 without a token, 400 for a malformed 28 × 28 array, and digit 5 for the included sample. Cloud and local Keras scores differed by at most `1.19e-7` on that sample. The existing Streamlit server on `127.0.0.1:8502` returned HTTP 200 and its page displayed `Inference: AWS Lambda`. Uploading `first_mnist_digit.png` through the Streamlit page produced digit 5 with a 98.7% largest model score, completing the local page to AWS endpoint to result check.
- Replaced the earlier container instructions with the ZIP build and named-resource teardown script. The app remains hybrid, and the endpoint should be rechecked before the test and presentation days, then deleted after evaluation. Secrets and the generated ZIP are ignored by Git.
- Added `setup-local.ps1` and `start-demo.ps1` so the user can recheck/install packages and launch the app independently. The setup script ran successfully and found all application packages and AWS CLI. Python could not create a `.venv` inside this OneDrive checkout; the incomplete folder was removed, and the scripts use the working Python 3.12 user installation. The start script ran successfully while the app was already on port 8502 and opened the existing server rather than failing on the occupied port.

## 12 October 2026 — Repository handoff

- Reviewed the local AWS demo changes for a GitHub update. The versioned files include the optional Streamlit client, Lambda handler, ONNX model export, ZIP builder, deployment verification and teardown scripts, local launch scripts, requirements, and dated documentation.
- Rechecked that the Lambda function was active and its last update successful in `ap-southeast-2`; the Function URL was configured with `AuthType NONE`, and the CloudWatch log group had three-day retention. The bearer token check runs inside the handler, so the endpoint still consumes an invocation for an unauthorized request.
- Updated the historical audit and generated MNIST report wording so their original results remain dated while the current hybrid demo status is clear. The interface remains local and the seven-writer pilot results have not changed.
- Checked the files intended for Git against the ignored local URL and bearer token. The `.streamlit/secrets.toml` file, generated deployment ZIP, build directory, and personal handwriting samples are excluded from the GitHub update.

## Next recorded steps

- Make further app changes in the clone and use a reviewed branch and pull request in the existing repository.
- Review issue #1 against the completed handwriting pilot and record any remaining evaluation work.
- Rehearse the final live presentation with a new agreed handwritten sample, confirm professor-facing presentation material, and run the teardown script after the final demo. The current local model and app remain available as a fallback.

## Documentation rule for future work

For each material change, record **date, goal, files changed, reason, settings or data used, observed result, where evidence is saved, limitations, and next decision**. When the model changes, also record dataset splits and the exact model artifact identity. Do not silently rewrite a previous experiment's result after a new run; create a new dated run record.

