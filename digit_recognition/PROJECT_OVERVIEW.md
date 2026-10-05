# Project overview: from MNIST to the demo

Workflow, measured results, and the next evaluation task.

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
  APP --> NEXT["NEXT: evaluate team handwriting<br/>with consent and correct labels"]
  NEXT --> PRES["Presentation<br/>explain pipeline, results, errors, and limits"]
  APP -. "later, when the group is ready" .-> CLOUD["Cloud deployment deferred"]

  classDef complete fill:#eaf4ee,stroke:#547b62,color:#183a28
  classDef next fill:#fff4dc,stroke:#9a6f20,color:#4a3300
  classDef deferred fill:#f0f1f3,stroke:#858b95,color:#34383e
  class A,B,T,P,C,V,E,M,APP,PRES complete
  class NEXT next
  class CLOUD deferred
```

## What the results do and do not say

The **98.92%** score is on the standard, held-out MNIST test set. It is not a measurement of accuracy on our own handwriting or every phone photo. Of the 108 MNIST errors, **25 still had a top softmax score of at least 90%**; treat those scores as model scores, not calibrated certainty.

## Read the details

- [Training report, graphs, evaluation and cited research review](MODEL_EVALUATION.md)
- [Build journal: what changed and why](DEVELOPMENT_LOG.md)
- [Model architecture and data flow](MODEL_ARCHITECTURE.md)
- [Real-handwriting evaluation plan](HANDWRITING_EVALUATION.md)
- [Numbered, commented build scripts](.)

**Current stage:** benchmark and local demo are ready; real team handwriting evaluation remains. Cloud deployment is deferred.
