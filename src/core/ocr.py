import pytesseract
from paddleocr import PaddleOCR
import numpy as np
from typing import Dict, Any

class OCRExtractor:
    def __init__(self, engine: str = "tesseract", lang: str = "por"):
        self.engine = engine
        self.lang = lang
        if engine == "paddle":
            self.paddle = PaddleOCR(lang=lang)
        else:
            self.paddle = None

    def extract(self, image: np.ndarray, return_bboxes: bool = True) -> Dict[str, Any]:
        if self.engine == "tesseract":
            data = pytesseract.image_to_data(image, lang=self.lang, output_type=pytesseract.Output.DICT)
            results = []
            for i in range(len(data["text"])):
                if int(data["conf"][i]) > 0 and data["text"][i].strip():
                    item = {
                        "text": data["text"][i],
                        "conf": float(data["conf"][i]) / 100.0,
                    }
                    if return_bboxes:
                        item["bbox"] = {
                            "x": int(data["left"][i]),
                            "y": int(data["top"][i]),
                            "w": int(data["width"][i]),
                            "h": int(data["height"][i]),
                        }
                    results.append(item)
            return {"engine": "tesseract", "results": results}
        elif self.engine == "paddle" and self.paddle:
            ocr_result = self.paddle.ocr(image)
            results = []
            for line in ocr_result:
                text = line[1][0]
                conf = line[1][1]
                bbox = line[0]
                item = {"text": text, "conf": conf}
                if return_bboxes:
                    item["bbox"] = bbox
                results.append(item)
            return {"engine": "paddleocr", "results": results}
        else:
            raise ValueError("Invalid OCR engine")
