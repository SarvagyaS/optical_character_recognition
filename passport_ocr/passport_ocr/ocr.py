"""OCR helper using pytesseract and OpenCV."""
import os
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Allow overriding tesseract binary through env
tess_cmd = os.getenv('TESSERACT_CMD')
if tess_cmd:
    pytesseract.pytesseract.tesseract_cmd = tess_cmd


def extract_text(image):
    """
    Extract text from an image. `image` may be an OpenCV image (numpy array)
    or a file path string. Returns the extracted unicode text.
    """
    # If a filepath was passed, load it
    if isinstance(image, str):
        img = cv2.imread(image)
    else:
        img = image

    if img is None:
        return ""

    # If the image is single-channel, convert to RGB
    if len(img.shape) == 2:
        rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        # If it's BGR (cv2 default), convert to RGB for pytesseract
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image for pytesseract
    pil_img = Image.fromarray(rgb)

    # Use pytesseract to extract text from the image
    try:
        extracted_text = pytesseract.image_to_string(pil_img, lang='eng')
    except Exception:
        # Fallback to basic call
        extracted_text = pytesseract.image_to_string(pil_img)

    return extracted_text
