import io
import os

import pytest
from PIL import Image, ImageDraw, ImageFont

FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
]

MENU_LINES = [
    "LANCHES",
    "X-Burger ........ R$ 24,90",
    "Pão, carne e queijo",
    "X-Salada ........ R$ 27,50",
    "BEBIDAS",
    "Refrigerante lata ..... 6,00",
]


def _font(size):
    for path in FONTS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return None


@pytest.fixture(scope="session")
def menu_png() -> bytes:
    """Um cardápio simples, preto no branco, gerado na hora."""
    font = _font(40)
    if font is None:
        pytest.skip("nenhuma fonte TrueType disponível para gerar a imagem")
    img = Image.new("RGB", (1000, 90 * len(MENU_LINES) + 60), "white")
    draw = ImageDraw.Draw(img)
    for i, line in enumerate(MENU_LINES):
        draw.text((50, 40 + i * 90), line, fill="black", font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
