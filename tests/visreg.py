import logging
import os
from pathlib import Path
from typing import TypeVar

import numpy as np
from PIL import Image, ImageChops

logging.basicConfig(level=logging.INFO, format=r"[%(levelname)s] %(message)s")

BASELINE_IMG_DIR = Path(__file__).resolve().parent / "baseline"
CURRENT_IMG_DIR = Path(__file__).resolve().parent / "current"

if not CURRENT_IMG_DIR.exists():
    CURRENT_IMG_DIR.mkdir()
    logging.info(f"Made {CURRENT_IMG_DIR}")


WebElement = TypeVar("WebElement")


def _are_images_the_same(base: Image, other: Image, threshold: float = 0.0):
    image_ops_diff = ImageChops.difference(base, other).getdata()
    pixel_diff = np.array(image_ops_diff).sum()
    return pixel_diff <= threshold


def web_element_image_regression(element: WebElement, name: str):
    """
    It will capture an image of the element when the environment variable UPDATE_BASELINE=1,
    otherwise it will check whether the element matches the latest image
    """
    baseline_image_path = str(BASELINE_IMG_DIR / f"{name}.png")
    if int(os.environ.get("UPDATE_BASELINE", 0)) == 1:
        element.screenshot(baseline_image_path)
        logging.info(f"Captured image to {baseline_image_path}")
    else:
        current_image_path = str(CURRENT_IMG_DIR / f"{name}.png")
        element.screenshot(current_image_path)

        base_image = Image.open(baseline_image_path)
        current_image = Image.open(current_image_path)
        assert _are_images_the_same(
            base_image, current_image
        ), f'[Visual Regression "{name}"] Images are not the same.'
