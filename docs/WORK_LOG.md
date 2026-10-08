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

## Next recorded steps

- Make further app changes in the clone and push a reviewed branch to the existing repository. Check whether Git command-line authentication can push from this computer.
- Review issue #1 against the completed handwriting pilot and record any remaining evaluation work.
- Decide hosting, public access, image retention, instructor acceptance and the final date before deployment. The current local model and app remain available for course preparation.

## Documentation rule for future work

For each material change, record **date, goal, files changed, reason, settings or data used, observed result, where evidence is saved, limitations, and next decision**. When the model changes, also record dataset splits and the exact model artifact identity. Do not silently rewrite a previous experiment's result after a new run; create a new dated run record.

