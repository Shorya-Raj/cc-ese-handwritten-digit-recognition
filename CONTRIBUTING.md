# Contributing

Keep pull requests focused and include evidence for changes to model behavior or evaluation results.

## Workflow

1. Review the open issues and agree on the task with the group. Clone this existing private repository before using local Git; the older Desktop and course-workspace folders are separate, unversioned copies.
2. Create a short branch from the latest `main`, such as `docs/test-results` or `evaluation/handwriting`.
3. Make one focused change. Preserve useful section comments and update documentation when behavior changes.
4. For model or evaluation changes, record the data split, settings, artifact identity, observed results, and limits. Add a dated experiment record; do not overwrite an earlier run silently.
5. Open a pull request with a summary and relevant checks, plots, or screenshots.
6. Ask a teammate to review before merging.

## Project safeguards

- Keep the held-out MNIST test set for final evaluation; use training and validation data for model decisions.
- State whether a result comes from MNIST or newly collected handwriting.
- Do not commit virtual environments, credentials, or original personal handwriting samples.
- Get each contributor's agreement before collecting handwriting; labels are sufficient.
- The current demo has a local Streamlit page and temporary AWS Lambda inference. Keep the Function URL and bearer token out of Git. The local sample-save feature must be reviewed before any public hosting of the Streamlit page.
- See [the project audit](docs/PROJECT_AUDIT.md), [model and experiment record](docs/MODEL_AND_EXPERIMENTS.md), and [Git guide](docs/GIT_AND_GITHUB.md) before changing the app or its claims.
- There is no automated test suite. For relevant changes, run the affected script or launch the local app and describe what you checked in the pull request.
