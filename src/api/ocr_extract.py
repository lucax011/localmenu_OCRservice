from fastapi import APIRouter, File, UploadFile, Header, Query, Request
from src.api.schemas import OCRExtractResponse, SourceInfo, Item, Metadata
from src.core.preprocessing import preprocess_image
from src.core.ocr import OCRExtractor
from src.core.nlp import parse_menu_items
from src.config.settings import settings
import time

router = APIRouter(prefix="/ocr", tags=["ocr"])

@router.post("/extract", response_model=OCRExtractResponse)
async def extract_ocr(
    request: Request,
    file: UploadFile = File(...),
    lang: str = Query("por"),
    use_paddle: bool = Query(False),
    preprocess: bool = Query(True),
    return_bboxes: bool = Query(True),
    x_request_id: str = Header(None)
):
    start = time.time()
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        return {"error": "File too large"}
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Invalid content type"}
    steps = ["grayscale", "denoise", "threshold"] if preprocess else []
    img, applied_steps = preprocess_image(content, steps)
    engine = "paddle" if use_paddle else settings.extractor_engine
    ocr = OCRExtractor(engine=engine, lang=lang)
    ocr_result = ocr.extract(img, return_bboxes=return_bboxes)
    items = parse_menu_items(ocr_result["results"])
    source = SourceInfo(filename=file.filename, size_bytes=len(content), content_type=file.content_type)
    metadata = Metadata(
        engine=ocr_result["engine"],
        lang=lang,
        processing_ms=int((time.time()-start)*1000),
        preprocessing={"applied": preprocess, "steps": applied_steps}
    )
    return OCRExtractResponse(source=source, items=items, metadata=metadata)
