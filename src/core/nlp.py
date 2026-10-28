import re
from typing import Any, Dict, List, Optional

# Preço no fim da linha: "R$ 24,90", "24,90", "1.234,50", "R$12.90"
PRICE_RE = re.compile(r"(?:R\s?\$\s*)?(\d{1,3}(?:\.\d{3})+,\d{2}|\d+[,.]\d{2})\s*$")
# Pontilhado ou traços entre o nome e o preço: "X-Burger ........ 24,90"
LEADER_RE = re.compile(r"[\s.\-_–—:|]+$")


def parse_price(raw: str) -> float:
    if "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    return round(float(raw), 2)


def is_heading(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and len(text) <= 40 and sum(c.isupper() for c in letters) / len(letters) > 0.8


def parse_menu_items(lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transforma linhas lidas pelo OCR em itens de cardápio.

    - linha que termina em preço: um item (nome = o texto antes do preço)
    - linha curta toda em maiúsculas, sem preço: título de categoria
    - outra linha sem preço logo depois de um item: descrição desse item
    """
    items: List[Dict[str, Any]] = []
    category: Optional[str] = None
    last: Optional[Dict[str, Any]] = None
    for line in lines:
        text = " ".join(str(line["text"]).split())
        if not text:
            continue
        match = PRICE_RE.search(text)
        if match:
            name = LEADER_RE.sub("", text[: match.start()]).strip(" .-")
            name = re.sub(r"R\s?\$\s*$", "", name).strip(" .-")
            if not name:
                continue
            last = {
                "name": name,
                "price": parse_price(match.group(1)),
                "description": None,
                "category": category,
                "confidence": float(line.get("conf", 0)),
                "bbox": line.get("bbox"),
            }
            items.append(last)
        elif is_heading(text):
            category = text.title()
            last = None
        elif last is not None:
            last["description"] = f"{last['description']} {text}" if last["description"] else text
    return items
