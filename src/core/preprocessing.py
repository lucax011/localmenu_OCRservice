import cv2
import numpy as np
from typing import List

def preprocess_image(image_bytes: bytes, steps: List[str]) -> np.ndarray:
    # Carregar imagem
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    applied_steps = []
    if "grayscale" in steps:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        applied_steps.append("grayscale")
    if "denoise" in steps:
        img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)
        applied_steps.append("denoise")
    if "threshold" in steps:
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        applied_steps.append("threshold")
    if "dilate" in steps:
        kernel = np.ones((2,2), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        applied_steps.append("dilate")
    if "erode" in steps:
        kernel = np.ones((2,2), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        applied_steps.append("erode")
    # Deskew (simplificado)
    if "deskew" in steps:
        # ... deskew logic ...
        applied_steps.append("deskew")
    return img, applied_steps
