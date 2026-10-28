from typing import Any, Dict, List

import numpy as np
import pytesseract


class OCRExtractor:
    """Lê o texto da imagem e devolve uma entrada por LINHA (não por palavra)."""

    def __init__(self, engine: str = "tesseract", lang: str = "por"):
        self.engine = engine
        self.lang = lang
        self.paddle = None
        if engine == "paddle":
            # PaddleOCR é opcional e pesado: só é importado quando pedido
            from paddleocr import PaddleOCR

            self.paddle = PaddleOCR(lang=lang)

    def extract(self, image: np.ndarray, return_bboxes: bool = True) -> Dict[str, Any]:
        if self.engine == "tesseract":
            data = pytesseract.image_to_data(
                image, lang=self.lang, output_type=pytesseract.Output.DICT
            )
            return {"engine": "tesseract", "results": group_lines(data, return_bboxes)}
        if self.engine == "paddle" and self.paddle:
            results = []
            for line in self.paddle.ocr(image)[0] or []:
                points, (text, conf) = line
                item = {"text": text, "conf": float(conf)}
                if return_bboxes:
                    xs = [int(p[0]) for p in points]
                    ys = [int(p[1]) for p in points]
                    item["bbox"] = {
                        "x": min(xs),
                        "y": min(ys),
                        "w": max(xs) - min(xs),
                        "h": max(ys) - min(ys),
                    }
                results.append(item)
            return {"engine": "paddleocr", "results": results}
        raise ValueError("Invalid OCR engine")


def group_lines(data: Dict[str, List[Any]], return_bboxes: bool = True) -> List[Dict[str, Any]]:
    """Junta as palavras do Tesseract em linhas, na ordem de leitura."""
    lines: Dict[tuple, Dict[str, Any]] = {}
    for i, word in enumerate(data["text"]):
        conf = float(data["conf"][i])
        if conf < 0 or not str(word).strip():
            continue
        key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        box = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
        line = lines.setdefault(key, {"words": [], "confs": [], "boxes": []})
        line["words"].append(str(word).strip())
        line["confs"].append(conf / 100.0)
        line["boxes"].append(box)

    results = []
    for line in lines.values():
        item = {
            "text": " ".join(line["words"]),
            "conf": round(sum(line["confs"]) / len(line["confs"]), 3),
        }
        if return_bboxes:
            x0 = min(b[0] for b in line["boxes"])
            y0 = min(b[1] for b in line["boxes"])
            x1 = max(b[0] + b[2] for b in line["boxes"])
            y1 = max(b[1] + b[3] for b in line["boxes"])
            item["bbox"] = {"x": int(x0), "y": int(y0), "w": int(x1 - x0), "h": int(y1 - y0)}
        results.append(item)
    results.sort(key=lambda r: (r.get("bbox") or {}).get("y", 0))
    return results
