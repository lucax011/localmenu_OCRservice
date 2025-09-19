import spacy
import re
from typing import List, Dict, Any

nlp = spacy.load("pt_core_news_sm")

PRICE_REGEX = re.compile(r"R\$\s?([\d.,]+)")

# Heurística simples para extrair itens de cardápio
def parse_menu_items(text_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = []
    for block in text_blocks:
        doc = nlp(block["text"])
        price_match = PRICE_REGEX.search(block["text"])
        price = None
        if price_match:
            price_str = price_match.group(1).replace(",", ".")
            try:
                price = float(price_str)
            except ValueError:
                price = None
        name = doc.ents[0].text if doc.ents else block["text"]
        item = {
            "name": name,
            "price": price,
            "description": None,
            "confidence": block["conf"],
            "bbox": block.get("bbox"),
        }
        items.append(item)
    return items
