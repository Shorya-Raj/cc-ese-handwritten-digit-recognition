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

## 13 October 2026 — Deployment and model recheck

- Refreshed the expired AWS CLI session and verified the temporary `cc-ese-digit-inference` function still reports `Active` and `Successful` in `ap-southeast-2` with Python 3.12, 1,024 MB memory, and a 30-second timeout. The deployed code SHA-256 matches the locally built `cloud/digit_lambda.zip` byte for byte; the ONNX model is included in the versioned repository.
- Confirmed the private deployment bucket still contains the 65,008,288-byte ZIP, blocks all four forms of public access, and uses SSE-S3 (`AES256`) encryption. The dedicated Lambda execution role remains present. CloudWatch retains its log group for three days.
- Confirmed the Function URL still uses `AuthType NONE`. Its two public resource-policy statements are limited respectively to `FunctionUrlAuthType=NONE` and `InvokedViaFunctionUrl=true`; the handler checks the bearer token. This remains a temporary public URL, and an unauthorized request can still invoke the handler before receiving 401. The AWS account API reported Free/Active with 120 USD credits at this check; the figure can change.
- Ran `cloud/verify_deployment.py` again: an unauthenticated request returned 401, a malformed pixel array returned 400, and the included sample returned digit 5. The maximum absolute difference between AWS and local Keras scores was `1.19e-7` on that sample. The local Streamlit health endpoint returned HTTP 200. Uploading `digit_recognition/first_mnist_digit.png` through the live Streamlit page showed `Inference: AWS Lambda`, digit 5, and a 98.7% top score.
- Fetched GitHub and confirmed local `main` and `origin/main` both pointed to merged PR #4 commit `c694bd4` before this dated log update. This check covers the included sample and current service state; it does not measure accuracy on new handwriting, test the camera path, or guarantee the endpoint will remain available on a later presentation day.

## Next recorded steps (current as of 14 October)

- Recheck the temporary AWS endpoint and local-to-AWS inference immediately before any presentation; retain local inference as fallback.
- Select one current 12-slide presentation deck, align the four speaker guides with it, confirm actual speaker assignments and instructor guidance, then rehearse against the course rubric and CO/PO mapping.
- Review issue #1 against the completed handwriting pilot and record any remaining evaluation work.
- Run the documented teardown after the final cloud demonstration and verify the named temporary resources are removed.

## Documentation rule for future work

For each material change, record **date, goal, files changed, reason, settings or data used, observed result, where evidence is saved, limitations, and next decision**. When the model changes, also record dataset splits and the exact model artifact identity. Do not silently rewrite a previous experiment's result after a new run; create a new dated run record.


## 14 October 2026 — Final log reconciliation

- Reviewed the canonical clone's audit, work log, development log, model/experiment report, current Git history, and duplicate parent-workspace records. No training run, model replacement, AWS deployment change, or endpoint check was performed for this reconciliation.
- Confirmed the local clone is on `main`, has a clean working tree before these documentation edits, and matched `origin/main` at `87cea5b6e59314d047760479149d90a3d42feb92`. This commit includes merged PR #5. The 13 October entry's reference to `c694bd4` accurately describes the point before PR #5's log update, but is not the current branch head.
- Added a current-status snapshot to the historical audit and a log index. The parent workspace copies of the audit, work log, and model/experiment report are synchronized to the canonical records.
- Latest AWS evidence remains dated 13 October. Present endpoint availability, the presentation-time recheck, additional classmate data, professor guidance, and final presentation/viva completion are not established by this documentation pass.

**Files updated:** canonical `docs/PROJECT_AUDIT.md`, `docs/WORK_LOG.md`, `docs/LOG_INDEX.md`, and `digit_recognition/DEVELOPMENT_LOG.md`; synchronized parent copies and a status pointer in `guided_build/BUILD_JOURNAL.md`. No model, training results, personal handwriting images, credentials, or AWS resources were changed.


## 14 October 2026 — Visibility and presentation-file review

- Refreshed GitHub `main`; the canonical clone matched `origin/main` at `87cea5b6e59314d047760479149d90a3d42feb92`, including merged PR #5. GitHub repository metadata reports the project repository as public. Updated current README, contributing, Git workflow, model provenance, audit, and index wording; older date-stamped records remain historical and this review did not determine when visibility became public.
- Found a 12-slide presentation plan, four speaker-guide documents, and several PowerPoint variants in the parent project folder. The plan names `Handwritten_Digit_Cloud_12_Slides_Updated.pptx`, while newer exports exist, so no slide deck or guides were copied into the repository. Select one deck and align the guides before adding a presentation package to GitHub.
- The latest AWS evidence remains the live recheck dated 13 October. This update did not invoke AWS, change resources, run the app, or perform a model experiment.
- Refreshed the parent-workspace reading copies for the audit, work log, model record, and development log. Kept the parent log index and Git guide as workspace-specific navigation documents, with their current visibility and presentation-status notes updated separately.

## 15 October 2026 — Presentation-day Git and launcher review

- Checked the live GitHub repository through its connected API. It is public, and main includes PR #6 at merge commit c76807952aae66bdea237deca1cc714879bca70e. Compared the GitHub commit/PR dates with the saved project logs and experiment results.
- Added a short explanation to the Git guide showing why an experiment date and its later documentation commit can differ. Kept all earlier work-log dates and Git commit timestamps unchanged.
- Removed this computer's absolute Windows paths from the README, setup, launcher and teardown scripts. The scripts now look for Python 3.12 in the usual per-user install location or through py, and for AWS CLI on PATH or its usual per-user install location. The launcher health request uses PowerShell's basic parsing option.
- A local Git fetch did not complete because the network resolver failed to start. GitHub showed remote main at c768079, while the local main and origin/main refs remained at 87cea5b and the active docs branch remained at 2454be1. The remote state was checked through GitHub; no local ref was advanced. No model training, app launch, AWS request, or presentation-day endpoint check was done as part of this review. The latest recorded live AWS check remains 13 October.

Files updated: README.md, setup-local.ps1, start-demo.ps1, cloud/teardown.ps1, docs/GIT_AND_GITHUB.md, docs/LOG_INDEX.md, and docs/WORK_LOG.md. Old revisions remain in Git history; this update changes only the current file versions. No credentials, model files, experiment results, or deployment resources were changed.
