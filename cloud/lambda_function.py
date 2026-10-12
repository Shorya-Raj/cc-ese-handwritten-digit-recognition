"""AWS Lambda handler for the project's single-digit CNN inference."""

import hmac
import json
import os
from pathlib import Path

import numpy as np

MODEL_PATH = Path(__file__).parent / "digit_model.onnx"
_MODEL = None


def _response(status: int, body: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def _load_model():
    global _MODEL
    if _MODEL is None:
        import onnxruntime as ort

        _MODEL = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
    return _MODEL


def handler(event, context):
    """Accept a Function URL request and return ten model scores."""
    expected = os.environ.get("INFERENCE_TOKEN", "")
    headers = {str(k).lower(): str(v) for k, v in (event.get("headers") or {}).items()}
    supplied = headers.get("authorization", "")
    if not expected or not hmac.compare_digest(supplied, f"Bearer {expected}"):
        return _response(401, {"error": "Unauthorized"})

    try:
        body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            import base64

            body = base64.b64decode(body).decode("utf-8")
        pixels = np.asarray(json.loads(body)["pixels"], dtype=np.float32)
        if pixels.shape != (28, 28) or not np.isfinite(pixels).all():
            return _response(400, {"error": "pixels must be a finite 28 by 28 array"})
        if pixels.min() < 0 or pixels.max() > 1:
            return _response(400, {"error": "pixel values must be between 0 and 1"})
        model = _load_model()
        input_name = model.get_inputs()[0].name
        scores = model.run(None, {input_name: pixels[np.newaxis, ..., np.newaxis]})[0][0]
        scores = np.asarray(scores, dtype=np.float32)
        if scores.shape != (10,) or not np.isfinite(scores).all():
            return _response(500, {"error": "model returned invalid scores"})
        return _response(200, {"prediction": int(np.argmax(scores)), "scores": scores.tolist()})
    except (KeyError, ValueError, TypeError, json.JSONDecodeError):
        return _response(400, {"error": "invalid request body"})
