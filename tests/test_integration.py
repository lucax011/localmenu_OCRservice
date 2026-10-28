import shutil

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_rejeita_arquivo_que_nao_e_imagem():
    resp = client.post("/ocr/extract", files={"file": ("menu.txt", b"oi", "text/plain")})
    assert resp.status_code == 415


@pytest.mark.skipif(shutil.which("tesseract") is None, reason="Tesseract não instalado")
def test_extrai_itens_de_um_cardapio(menu_png):
    resp = client.post("/ocr/extract", files={"file": ("menu.png", menu_png, "image/png")})
    assert resp.status_code == 200
    items = {i["name"]: i for i in resp.json()["items"]}
    assert items["X-Burger"]["price"] == 24.9
    assert items["X-Burger"]["category"] == "Lanches"
    assert items["X-Salada"]["price"] == 27.5
    assert items["Refrigerante lata"]["category"] == "Bebidas"
