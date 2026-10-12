"""Build the Python 3.12 x86_64 AWS Lambda ZIP from Windows.

Run from the repository root with Python 3.12:
    python cloud/build_zip.py

The cross-platform pip flags download Linux wheels. Docker and SAM are not
needed. The output ZIP is ignored by Git and uploaded to private S3.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


CLOUD = Path(__file__).resolve().parent


def main() -> None:
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("Build with Python 3.12 for the Lambda Python 3.12 runtime.")
    with tempfile.TemporaryDirectory(prefix="digit-lambda-") as temp:
        package = Path(temp) / "package"
        package.mkdir()
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--platform",
             "manylinux_2_27_x86_64", "--implementation", "cp",
             "--python-version", "3.12", "--only-binary=:all:",
             "--target", str(package), "-r", str(CLOUD / "requirements.txt")],
            check=True,
        )
        shutil.copy2(CLOUD / "lambda_function.py", package / "lambda_function.py")
        shutil.copy2(CLOUD / "digit_model.onnx", package / "digit_model.onnx")
        unzipped = sum(file.stat().st_size for file in package.rglob("*") if file.is_file())
        if unzipped > 250 * 1024 * 1024:
            raise SystemExit("Unzipped Lambda package exceeds the 250 MB limit.")
        archive = shutil.make_archive(str(Path(temp) / "digit_lambda"), "zip", package)
        output = CLOUD / "digit_lambda.zip"
        shutil.copy2(archive, output)
        print(f"Built {output.name}: {output.stat().st_size / 1048576:.1f} MiB")


if __name__ == "__main__":
    main()
