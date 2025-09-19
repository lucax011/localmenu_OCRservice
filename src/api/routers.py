from fastapi import APIRouter
from .schemas import OCRExtractResponse

router = APIRouter(prefix="/ocr", tags=["ocr"])

@router.post("/extract", response_model=OCRExtractResponse)
def extract_ocr():
    # Implementação será adicionada
    pass
