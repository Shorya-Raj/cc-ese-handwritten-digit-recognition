# Real handwriting check — what the team will do

The 98.92% result in `TRAINING_REPORT.md` was measured on MNIST. This short check tells us how the actual app performs on images closer to our demonstration: a digit on paper, a camera photo, or a PNG drawn by a person.

## 1. Collect a small, balanced set

Before collecting, tell each writer what the examples are for and get their agreement. Names are not needed: use simple contributor labels. Keep original handwriting images on the local machine; the repository ignores `guided_build/artifacts/real_handwriting/`, so those personal samples stay out of GitHub.

Ask each available teammate to write digits **0 through 9 once**, using their normal handwriting. If time allows, repeat them with a second input style, such as a phone photo and a Paint drawing. Aim for roughly **30–50 labelled examples** across the team before drawing conclusions. This is a practical demo check, not a statistically representative accuracy study.

For paper images, use one digit per picture, dark ink, plain light background, and enough space around the digit. Keep a few ordinary, imperfect photos too; they show whether the app handles realistic inputs. Do not quietly discard failures.

## 2. Use the guided app

From the Desktop project folder in the VS Code terminal:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\guided_build\step_08_app.py
```

For each example, inspect the **original image** and the **28 × 28 model input** shown side by side. If the processed image loses a stroke, cuts off the digit, or keeps background marks, record that as a preparation problem. Choose the digit actually written and press **Save this labelled example locally**. The local run saves both images and one CSV row under `guided_build/artifacts/real_handwriting/`.

## 3. Review outcomes honestly

Count correct predictions by digit and by input type. For every wrong result, review the saved original and processed images together. Use these plain categories:

| Category | What to look for | Possible next action |
| --- | --- | --- |
| Preparation problem | Digit cropped, too faint, inverted incorrectly, or background included | Adjust image preparation and repeat the same saved examples |
| Handwriting shape | Processed digit is clear, but the shape differs from MNIST examples | Collect more examples of that style; consider targeted shifts or rotations |
| Ambiguous digit | A person also struggles to identify it | Record it; avoid claiming the model should always know |
| Consistent class mix-up | The same true digit repeatedly becomes another digit | Target that pair when gathering examples and evaluating changes |

## 4. Decide whether to train again

Only add augmentation or new training examples if this check reveals a repeated, fixable pattern. Compare a changed model on the **same saved real-handwriting examples** and retain both result sets. Keep the original MNIST test set separate from training. Extra images that do not improve the actual use case are not worth the training cost.

## 5. What to show in the presentation

Show the live app with the original and processed images side by side. Report the MNIST test score as **98.92% on 10,000 held-out MNIST pictures**. Report the real-handwriting result separately once examples have been collected. Include at least one honest failure case and explain whether it came from preparation or model recognition.
