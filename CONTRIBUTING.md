# Contributing to the CC ESE project

Thanks for helping with the handwritten digit recognition project. Keep changes small and easy to explain during the presentation.

## Workflow

1. Check the open issues and agree on the task with the group.
2. Create a branch from the latest `main`, for example `docs/clarify-test-results` or `evaluation/real-handwriting`.
3. Make one focused change. Keep comments and section headings that help a beginner follow the code.
4. If model behavior or evaluation changes, update the report and record the dataset split, settings, and results.
5. Open a pull request with a clear summary, relevant checks, and screenshots or plots when useful.
6. Have at least one teammate review it. Merge when the explanation and evidence are clear.

## Project safeguards

- Keep the held-out MNIST test set for final evaluation; use the training/validation split for model decisions.
- State clearly whether a result is measured on MNIST or on newly collected handwriting.
- Do not commit virtual environments, credentials, or original personal handwriting samples.
- Ask contributors before collecting their handwriting. Use labels instead of names where possible.
- Keep cloud deployment deferred until the group and course requirements are ready to address it.
- There is currently no automated test suite. For relevant changes, run the affected script or launch the local app and describe what you checked in the pull request.
