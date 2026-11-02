from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify backend service status."""
    return {"status": "ok", "service": "SecureChain Portal API"}