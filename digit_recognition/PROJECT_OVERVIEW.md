# Project overview: from MNIST to the demo

Workflow, measured results, the completed handwriting pilot, and the proposed hosting step.

```mermaid
flowchart TB
  A["MNIST dataset<br/>70,000 labelled images"] --> B["Official training portion<br/>54,000 train + 6,000 validation"]
  A --> T["Separate held-out test set<br/>10,000 images"]
  B --> P["Prepare each image<br/>28 × 28 grayscale<br/>scale pixels to 0–1<br/>add channel dimension"]
  P --> C["CNN classifier<br/>34,826 trainable parameters"]
  C --> V["Validation checkpoint<br/>best: 99.08% at epoch 7"]
  V --> E["Final MNIST test result<br/>98.92% accuracy<br/>9,892 correct · 108 incorrect"]
  T --> E
  E --> M["Saved model<br/>digit_model.keras"]
  M --> APP["Local Streamlit demo<br/>upload or camera image<br/>preprocess → predict → show top 3"]
  APP --> PILOT["Pilot: 140 crops / 7 writers<br/>candidate not adopted"]
  PILOT --> PRES["Presentation<br/>explain pipeline, results, errors, and limits"]
  APP -. "proposed; approval and privacy review needed" .-> CLOUD["Streamlit hosting under review"]

  classDef complete fill:#eaf4ee,stroke:#547b62,color:#183a28
  classDef next fill:#fff4dc,stroke:#9a6f20,color:#4a3300
  classDef deferred fill:#f0f1f3,stroke:#858b95,color:#34383e
  class A,B,T,P,C,V,E,M,APP,PRES complete
  class PILOT complete
  class CLOUD deferred
```

## What the results do and do not say

The **98.92%** score is on the standard, held-out MNIST test set. It is not a measurement of accuracy on our own handwriting or every phone photo. Of the 108 MNIST errors, **25 still had a top softmax score of at least 90%**; treat those scores as model scores, not calibrated certainty.

The later seven-writer pilot yielded 60% on writer 6 and 50% on writer 7 for both the original and the fine-tuned candidate. These are small exploratory checks, not a general accuracy estimate. The original guided model remains the app model. No cloud deployment has been verified.

## Read the details

- [Training report, graphs, evaluation and cited research review](MODEL_EVALUATION.md)
- [Build journal: what changed and why](DEVELOPMENT_LOG.md)
- [Model architecture and data flow](MODEL_ARCHITECTURE.md)
- [Real-handwriting evaluation plan](HANDWRITING_EVALUATION.md)
- [Model and experiment record](../docs/MODEL_AND_EXPERIMENTS.md)
- [Project audit and Git status](../docs/PROJECT_AUDIT.md)
- [Numbered, commented build scripts](.)

**Current stage (8 October 2026):** guided MNIST benchmark and local demo exist; a seven-writer handwriting pilot is recorded; an independent new-writer check, Git working clone, and cloud deployment remain open.
