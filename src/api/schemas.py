from pydantic import BaseModel, Field
from typing import List, Optional

class BBox(BaseModel):
    x: int
    y: int
    w: int
    h: int

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str]
    confidence: float
    bbox: Optional[BBox]

class SourceInfo(BaseModel):
    filename: str
    size_bytes: int
    content_type: str

class Metadata(BaseModel):
    engine: str
    lang: str
    processing_ms: int
    preprocessing: dict

class OCRExtractResponse(BaseModel):
    source: SourceInfo
    items: List[Item]
    metadata: Metadata
