import pytest
from src.core.preprocessing import preprocess_image

with open("tests/assets/menu1.jpg", "rb") as f:
    img_bytes = f.read()

def test_preprocess_grayscale():
    img, steps = preprocess_image(img_bytes, ["grayscale"])
    assert "grayscale" in steps
    assert img is not None
