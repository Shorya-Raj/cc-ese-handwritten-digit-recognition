"""Check the live AWS endpoint against the included local model.

Run from the repository root after deployment:
    python cloud/verify_deployment.py
"""

import sys
import tomllib
from pathlib import Path

import numpy as np
import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "digit_recognition"))
from step_07_prepare_upload import prepare_image, to_model_batch  # noqa: E402


def main() -> None:
    with (ROOT / ".streamlit" / "secrets.toml").open("rb") as file:
        settings = tomllib.load(file)
    url = settings["inference_url"]
    token = settings["inference_token"]

    with Image.open(ROOT / "digit_recognition" / "first_mnist_digit.png") as image:
        batch = to_model_batch(prepare_image(image))
    payload = {"pixels": batch[0, :, :, 0].tolist()}

    unauthorized = requests.post(url, json=payload, timeout=40)
    assert unauthorized.status_code == 401, unauthorized.status_code

    invalid = requests.post(
        url, json={"pixels": [[0]]},
        headers={"Authorization": f"Bearer {token}"}, timeout=40,
    )
    assert invalid.status_code == 400, (invalid.status_code, invalid.text[:200])

    response = requests.post(
        url, json=payload,
        headers={"Authorization": f"Bearer {token}"}, timeout=40,
    )
    response.raise_for_status()
    cloud = np.asarray(response.json()["scores"], dtype=np.float32)
    assert cloud.shape == (10,) and np.isfinite(cloud).all()

    import tensorflow as tf

    local = tf.keras.models.load_model(
        ROOT / "digit_recognition" / "artifacts" / "digit_model.keras"
    ).predict(batch, verbose=0)[0]
    assert int(np.argmax(cloud)) == int(np.argmax(local))
    max_difference = float(np.max(np.abs(cloud - local)))
    assert max_difference < 1e-5, max_difference
    print(
        "Live AWS checks passed: unauthorized=401, malformed=400, "
        f"prediction={int(np.argmax(cloud))}, max_score_difference={max_difference:.3g}"
    )


if __name__ == "__main__":
    main()
