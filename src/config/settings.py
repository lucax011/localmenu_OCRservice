from pydantic import BaseSettings, Field
from typing import Literal

class Settings(BaseSettings):
    app_port: int = Field(8000, env="APP_PORT")
    extractor_engine: Literal["tesseract", "paddle"] = Field("tesseract", env="EXTRACTOR_ENGINE")
    enable_preprocessing: bool = Field(True, env="ENABLE_PREPROCESSING")
    return_bboxes: bool = Field(True, env="RETURN_BBOXES")
    max_upload_mb: int = Field(10, env="MAX_UPLOAD_MB")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
