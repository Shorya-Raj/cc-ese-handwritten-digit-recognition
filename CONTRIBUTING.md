# Contributing

Keep pull requests focused and include evidence for changes to model behavior or evaluation results.

## Workflow

1. Review the open issues and agree on the task with the group.
2. Create a short branch from the latest `main`, such as `docs/test-results` or `evaluation/handwriting`.
3. Make one focused change. Preserve useful section comments and update documentation when behavior changes.
4. For model or evaluation changes, record the data split, settings, and results.
5. Open a pull request with a summary and relevant checks, plots, or screenshots.
6. Ask a teammate to review before merging.

## Project safeguards

- Keep the held-out MNIST test set for final evaluation; use training and validation data for model decisions.
- State whether a result comes from MNIST or newly collected handwriting.
- Do not commit virtual environments, credentials, or original personal handwriting samples.
- Get each contributor's agreement before collecting handwriting; labels are sufficient.
- Cloud deployment is outside the current project scope.
- There is no automated test suite. For relevant changes, run the affected script or launch the local app and describe what you checked in the pull request.
