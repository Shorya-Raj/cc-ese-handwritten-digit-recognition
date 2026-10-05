r"""Step 7: turn one uploaded digit picture into a MNIST-shaped model input.

Run from the repository root in the VS Code terminal:
    .\.venv\Scripts\python.exe .\digit_recognition\step_07_prepare_upload.py

The default demonstration reprocesses our saved MNIST example. You can pass
the path to a team member's digit photo instead when one is available.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


# SECTION 1 — State the target format the CNN expects
CANVAS_SIZE = 28  # Final picture width and height in pixels.
DIGIT_BOX_SIZE = 20  # Leave a margin around the ink, like MNIST examples.


def prepare_image(image: Image.Image) -> Image.Image:
    """Return one centered, bright digit on a dark 28-by-28 canvas."""

    # SECTION 2 — Make photo orientation, transparency, and colors consistent
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        white_paper = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        white_paper.alpha_composite(rgba)
        image = white_paper.convert("RGB")
    gray = ImageOps.autocontrast(ImageOps.grayscale(image))
    pixels = np.asarray(gray, dtype=np.uint8)

    # SECTION 3 — Match MNIST's bright-ink-on-dark-background convention
    # A light border usually means dark ink on white paper. Invert that case.
    border = np.concatenate(
        (pixels[0, :], pixels[-1, :], pixels[:, 0], pixels[:, -1])
    )
    ink = 255 - pixels if float(np.median(border)) > 127 else pixels.copy()
    # Remove faint background noise while keeping antialiased pen strokes.
    ink = np.clip((ink.astype(np.float32) - 24.0) * (255.0 / 231.0), 0, 255)
    ink[ink < 20] = 0
    ink_picture = Image.fromarray(ink.astype(np.uint8))

    # SECTION 4 — Crop around the digit, then fit it inside a 28-pixel canvas
    bounds = ink_picture.point(lambda value: 255 if value > 24 else 0).getbbox()
    if bounds is None:
        raise ValueError("No clear digit found. Try a darker, larger digit.")
    digit = ink_picture.crop(bounds)
    digit.thumbnail((DIGIT_BOX_SIZE, DIGIT_BOX_SIZE), Image.Resampling.LANCZOS)
    canvas = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), color=0)
    canvas.paste(
        digit,
        ((CANVAS_SIZE - digit.width) // 2, (CANVAS_SIZE - digit.height) // 2),
    )

    # SECTION 5 — Move the center of the ink toward the center of the picture
    # This is useful for narrow digits such as 1, which can sit off-center.
    canvas_pixels = np.asarray(canvas, dtype=np.float32)
    mass = float(canvas_pixels.sum())
    rows, columns = np.indices(canvas_pixels.shape)
    center_x = float((columns * canvas_pixels).sum() / mass)
    center_y = float((rows * canvas_pixels).sum() / mass)
    shift_x = int(round((CANVAS_SIZE - 1) / 2 - center_x))
    shift_y = int(round((CANVAS_SIZE - 1) / 2 - center_y))
    centered = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), color=0)
    centered.paste(canvas, (shift_x, shift_y))
    return centered


def to_model_batch(prepared: Image.Image) -> np.ndarray:
    """Convert the picture into one float32 array of shape (1, 28, 28, 1)."""
    # SECTION 6 — Use the same 0–1 scaling and channel shape as training
    return np.asarray(prepared, dtype=np.float32)[np.newaxis, ..., np.newaxis] / 255.0


if __name__ == "__main__":
    # SECTION 7 — Preview what the model would see before any prediction
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "image_path", nargs="?", type=Path,
        default=Path(__file__).with_name("first_mnist_digit.png"),
    )
    image_path = parser.parse_args().image_path
    with Image.open(image_path) as original:
        prepared_image = prepare_image(original)
    preview_path = Path(__file__).with_name("artifacts") / "prepared_preview.png"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    prepared_image.resize((280, 280), Image.Resampling.NEAREST).save(preview_path)
    print("Input image:", image_path)
    print("Prepared picture size:", prepared_image.size)
    print("Model input shape:", to_model_batch(prepared_image).shape)
    print("Model input pixel range:", float(to_model_batch(prepared_image).min()),
          "to", float(to_model_batch(prepared_image).max()))
    print("Prepared preview:", preview_path)
