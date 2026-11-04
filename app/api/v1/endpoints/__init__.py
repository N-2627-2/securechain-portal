from fastapi import APIRouter
from app.api.v1.endpoints.quarantine import router as quarantine_router

router = APIRouter()
router.include_router(quarantine_router)