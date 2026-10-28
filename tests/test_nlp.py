from src.core.nlp import parse_menu_items, parse_price


def lines(*texts):
    return [{"text": t, "conf": 0.9} for t in texts]


def test_item_com_preco():
    items = parse_menu_items(lines("Pizza Margherita R$ 39,90"))
    assert items == [
        {
            "name": "Pizza Margherita",
            "price": 39.9,
            "description": None,
            "category": None,
            "confidence": 0.9,
            "bbox": None,
        }
    ]


def test_pontilhado_e_formatos_de_preco():
    items = parse_menu_items(
        lines("X-Burger ........ 24,90", "Combo família - R$ 1.234,50", "Suco | 8.00")
    )
    assert [(i["name"], i["price"]) for i in items] == [
        ("X-Burger", 24.9),
        ("Combo família", 1234.5),
        ("Suco", 8.0),
    ]


def test_categorias_e_descricoes():
    items = parse_menu_items(
        lines("LANCHES", "X-Salada R$ 27,50", "Pão, carne, alface e tomate", "BEBIDAS", "Água 4,00")
    )
    assert items[0]["category"] == "Lanches"
    assert items[0]["description"] == "Pão, carne, alface e tomate"
    assert items[1]["category"] == "Bebidas"
    assert items[1]["description"] is None


def test_linhas_sem_item_sao_ignoradas():
    assert parse_menu_items(lines("Bem-vindo ao nosso restaurante!", "", "R$ 10,00")) == []


def test_parse_price():
    assert parse_price("1.234,50") == 1234.5
    assert parse_price("12.90") == 12.9
