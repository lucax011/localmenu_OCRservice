from src.core.preprocessing import preprocess_image


def test_preprocess_aplica_os_passos(menu_png):
    img, steps = preprocess_image(menu_png, ["grayscale", "threshold"])
    assert steps == ["grayscale", "threshold"]
    assert img.ndim == 2


def test_imagem_invalida_devolve_none():
    img, steps = preprocess_image(b"isto nao e uma imagem", ["grayscale"])
    assert img is None and steps == []
