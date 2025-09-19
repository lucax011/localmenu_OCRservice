from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/version")
def version():
    version = "0.1.0"
    commit = os.getenv("GIT_COMMIT", None)
    return {"version": version, "commit": commit}
