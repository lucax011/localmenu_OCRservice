from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.ocr_extract import router as ocr_router
from src.api.health import router as health_router
from src.api.version import router as version_router


origins = [
	"http://localhost:19006",
	"http://localhost:5173"
]

app = FastAPI(title="LocalMenu OCR Service", version="0.1.0")
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(version_router)
app.include_router(ocr_router)
