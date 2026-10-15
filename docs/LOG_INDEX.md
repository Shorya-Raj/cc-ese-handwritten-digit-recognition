# Project log and evidence index

**Reconciled:** 15 October 2026
**Canonical location:** GitHub repository clone at `CC ESE 2/cc-ese-handwritten-digit-recognition/`. GitHub reported the repository as public on 14 October 2026.

This index separates chronological logs from reports and source evidence. The canonical clone is the versioned team source. Similar files in the parent `CC ESE 2` folder are convenient synchronized copies, not independent histories. The Desktop guided project is another separate copy and is not automatically synchronized.

## Chronological logs and audits

| Record | What it covers | Status/authority |
| --- | --- | --- |
| [`PROJECT_AUDIT.md`](PROJECT_AUDIT.md) | Folder/repository inventory, model identity, architecture, status, risks, open course/deployment facts. | Historical audit sections preserved; latest snapshot appended for 14 October. Current status should be read from the appended snapshot and dated work log. |
| [`WORK_LOG.md`](WORK_LOG.md) | Project-wide dated actions: model build, seven-writer experiment, course/repository audit, Git PRs, AWS preparation/deployment/recheck, and the 15 October Git/launcher review. | Master chronological project record. AWS evidence is last dated 13 October. |
| [`../digit_recognition/DEVELOPMENT_LOG.md`](../digit_recognition/DEVELOPMENT_LOG.md) | Numbered model/application implementation stages and their purposes, settings, results, and learning notes. | Detailed model-build chronology; defers later repository/cloud history to `WORK_LOG.md`. |
| `guided_build/BUILD_JOURNAL.md` (parent/Desktop guided copy) | Original teaching-oriented step-by-step build journal from the guided project. | Historical build diary; it predates hybrid deployment and is not current status. The parent copy has not been moved into GitHub. |

## Experiment reports and evidence (not activity logs)

| Record | What it contains | Important limit |
| --- | --- | --- |
| [`MODEL_AND_EXPERIMENTS.md`](MODEL_AND_EXPERIMENTS.md) | Guided MNIST benchmark, seven-writer fine-tuning pilot, artifact provenance, saved Paint example, and safe next evaluation. | Pilot is exploratory and small; no new classmate collection is evidenced. |
| `digit_recognition/MODEL_EVALUATION.md` | Detailed MNIST evaluation, metrics, graphs, research notes, and citations. | MNIST benchmark results do not establish real-world handwriting accuracy. |
| `artifacts/handwriting_finetune_2026-10-06/REPORT.md` (parent workspace) | Fine-tuning result tables, plots, and prediction evidence. | Separate candidate; not adopted by the app. Raw source pages are not included there. |
| `training_history.json`, `test_results.json`, `confusion_matrix.csv`, plot files | Machine-readable training/evaluation outputs. | Evidence artifacts, not narrative logs. Preserve with the exact model/run they describe. |
| `cloud/verify_deployment.py` and `WORK_LOG.md` dated entries | Deployment validation procedure and recorded check outcomes. | Script is executable evidence procedure, not proof of a fresh run by itself. Last recorded run is 13 October. |

## What was updated in this reconciliation

- Added a current-status snapshot to `docs/PROJECT_AUDIT.md`.
- Added the 14 October reconciliation entry to `docs/WORK_LOG.md`.
- Added later hybrid-inference chronology and cross-links to `digit_recognition/DEVELOPMENT_LOG.md`.
- Added this inventory and corrected the current repository-visibility description. Historical entries remain dated; no new experiment, deployment check, or cloud action is claimed.
- Parent workspace copies of `docs/PROJECT_AUDIT.md`, `docs/WORK_LOG.md`, and `docs/MODEL_AND_EXPERIMENTS.md` were synchronized from this canonical clone.
- Added a presentation-day explanation of project/log dates versus GitHub commit dates. No earlier dates or commit history were altered.
- Removed computer-specific absolute paths from the current README and PowerShell scripts; older commits keep their original versions.

## Current checks still needed

1. For a live presentation, recheck the Lambda endpoint and local-to-AWS path shortly before the demo; the latest saved check is still dated 13 October, and local inference remains the fallback.
2. Record any professor deployment guidance and any new handwriting collection with its date, consent/data handling, sample counts, and evaluation split.
3. Choose one of the parent-workspace 12-slide deck variants, align the four speaker guides to it, confirm actual speaker assignments, then rehearse against the course brief and rubric. The current plan names an earlier export while newer variants exist, so the presentation package is not yet unambiguous.
4. After the final demonstration, run the documented teardown and verify that the temporary resources were removed.
