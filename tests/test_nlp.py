from src.core.nlp import parse_menu_items

def test_parse_menu_items():
    blocks = [{"text": "Pizza Margherita R$ 39,90", "conf": 0.95}]
    items = parse_menu_items(blocks)
    assert items[0]["name"] == "Pizza Margherita R$ 39,90" or items[0]["name"] == "Pizza Margherita"
    assert items[0]["price"] == 39.90
