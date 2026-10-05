r"""Step 8: run the guided digit-recognition app in Streamlit.

Run from the Desktop project folder in the VS Code terminal:
    .\.venv\Scripts\python.exe -m streamlit run .\guided_build\step_08_app.py

Upload one handwritten digit or take a photo. The app shows both the original
picture and the exact 28-by-28 picture passed to the saved CNN.
"""

import csv
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from step_07_prepare_upload import prepare_image, to_model_batch


# SECTION 1 — Point the app to the model trained in our guided build
MODEL_PATH = Path(__file__).with_name("artifacts") / "digit_model.keras"


@st.cache_resource(show_spinner="Loading the trained model...")
def load_model() -> tf.keras.Model:
    """Load the model once and reuse it for later image uploads."""
    return tf.keras.models.load_model(MODEL_PATH)


def main() -> None:
    # SECTION 2 — Give the student simple instructions and an input choice
    st.set_page_config(page_title="Handwritten Digit Recognition", page_icon="✍️")
    st.title("Handwritten Digit Recognition")
    st.write("Show the model **one handwritten digit**. Use dark ink on plain white paper, or draw one digit in Paint and upload the saved PNG. Keep the digit large and centered.")

    if not MODEL_PATH.is_file():
        st.error("The guided model file is missing. Run step_04_train.py first.")
        st.stop()

    input_method = st.radio("How will you provide the digit?", ["Upload an image", "Take a photo"], horizontal=True)
    if input_method == "Upload an image":
        supplied_image = st.file_uploader("Choose a PNG or JPEG image", type=["png", "jpg", "jpeg"], max_upload_size=5)
    else:
        supplied_image = st.camera_input("Photograph one handwritten digit")
    if supplied_image is None:
        st.info("Choose an image to see the model's prediction.")
        return

    # SECTION 3 — Prepare the picture using exactly the function from Step 7
    try:
        with Image.open(supplied_image) as image:
            original = image.copy()
        prepared = prepare_image(original)
        model_input = to_model_batch(prepared)
    except (OSError, ValueError) as error:
        st.error(f"Could not find a clear digit: {error}")
        return

    # SECTION 4 — Ask the saved CNN for ten digit scores
    scores = load_model().predict(model_input, verbose=0)[0]
    predicted_digit = int(np.argmax(scores))
    highest_score = float(scores[predicted_digit])
    top_three = np.argsort(scores)[::-1][:3]

    # SECTION 5 — Show the original input and what the model actually received
    left, right = st.columns(2)
    with left:
        st.image(original, caption="Your original picture", use_container_width=True)
    with right:
        st.image(prepared.resize((280, 280), Image.Resampling.NEAREST),
                 caption="The model's 28 × 28 input, enlarged so you can see it",
                 use_container_width=True)

    st.metric("Predicted digit", predicted_digit)
    st.progress(highest_score, text=f"Largest model score: {highest_score:.1%}")
    st.caption("This score is not a guarantee. Some wrong MNIST answers had scores above 90%, and photos may differ from the training images.")

    # SECTION 6 — Show alternative answers so close calls are visible
    st.write("Three highest-scoring digits")
    st.table([
        {"Digit": int(digit), "Model score": f"{float(scores[digit]):.1%}"}
        for digit in top_three
    ])
    with st.expander("How the picture became a prediction"):
        st.markdown(
            "1. Correct orientation, remove transparency, and make the picture grayscale.\n"
            "2. Change it to bright ink on a dark background, like MNIST.\n"
            "3. Crop and center the ink on a 28 × 28 canvas.\n"
            "4. Scale pixel values to 0–1 and ask the CNN for ten digit scores.\n"
            "5. Show the digit with the highest score."
        )

    # SECTION 7 — Optionally record a labelled example for real-handwriting review
    st.subheader("Help us check real handwriting")
    st.write("If you know the digit you wrote, choose it and save this result. In our local Desktop run it goes into this project's `artifacts/real_handwriting` folder.")
    actual_digit = st.selectbox("Digit actually shown in your picture", range(10))
    if st.button("Save this labelled example locally"):
        sample_dir = MODEL_PATH.parent / "real_handwriting"
        sample_dir.mkdir(parents=True, exist_ok=True)
        sample_id = uuid4().hex[:12]
        original_name = f"{sample_id}_original.png"
        prepared_name = f"{sample_id}_prepared.png"
        original.convert("RGB").save(sample_dir / original_name)
        prepared.save(sample_dir / prepared_name)
        log_path = sample_dir / "results.csv"
        is_new_log = not log_path.exists()
        with log_path.open("a", newline="", encoding="utf-8") as log_file:
            writer = csv.writer(log_file)
            if is_new_log:
                writer.writerow(["sample_id", "recorded_utc", "input_method", "actual_digit",
                                 "predicted_digit", "correct", "model_score", "original_image",
                                 "prepared_image"])
            writer.writerow([sample_id, datetime.now(timezone.utc).isoformat(), input_method,
                             actual_digit, predicted_digit, int(actual_digit == predicted_digit),
                             highest_score, original_name, prepared_name])
        st.success(f"Saved sample {sample_id}. Correct prediction: {'yes' if actual_digit == predicted_digit else 'no'}.")


if __name__ == "__main__":
    main()
