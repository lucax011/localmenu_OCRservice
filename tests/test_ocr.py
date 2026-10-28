from src.core.ocr import group_lines


def test_palavras_viram_linhas_na_ordem_de_leitura():
    data = {
        "text": ["Suco", "8,00", "X-Burger", "24,90", ""],
        "conf": [90, 80, 95, 85, -1],
        "block_num": [1, 1, 1, 1, 1],
        "par_num": [1, 1, 1, 1, 1],
        "line_num": [2, 2, 1, 1, 3],
        "left": [10, 200, 10, 200, 0],
        "top": [60, 62, 10, 12, 0],
        "width": [80, 60, 150, 60, 0],
        "height": [20, 20, 20, 20, 0],
    }
    result = group_lines(data)
    assert [r["text"] for r in result] == ["X-Burger 24,90", "Suco 8,00"]
    assert result[0]["conf"] == 0.9
    assert result[0]["bbox"] == {"x": 10, "y": 10, "w": 250, "h": 22}
