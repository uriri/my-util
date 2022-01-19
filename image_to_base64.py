import base64
from argparse import ArgumentParser
from logging import DEBUG, Formatter, StreamHandler, getLogger
from pathlib import Path

import pyperclip


def image_to_base64(img_file):
    with open(img_file, "rb") as f:
        data = base64.b64encode(f.read())
    return data.decode("utf-8")


if __name__ == "__main__":
    app_logger = getLogger(__name__)

    handler = StreamHandler()
    handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    app_logger.addHandler(handler)
    app_logger.setLevel(DEBUG)
    app_logger.propagate = False

    parser = ArgumentParser(description="show each directory size")
    parser.add_argument("-f", "--file", help="image file path")

    args = parser.parse_args()

    img_file = Path(args.file)

    pyperclip.copy(image_to_base64(img_file))
    app_logger.info("copy to clipboard")
