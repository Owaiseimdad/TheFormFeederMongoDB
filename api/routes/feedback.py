from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import APIKeyHeader
from core.security import validate_api_key
from core.database import get_db_strategy
from services.feedback import FeedbackService
from api.models.feedback import FeedbackCreate, FeedbackResponse
from core.config import settings
from core.database.strategy import DatabaseStrategy

router = APIRouter(tags=["Feedback"])

# API Key Security Scheme
api_key_scheme = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_scheme)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )
    return api_key

@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback",
    description="Submit user feedback with rating",
    responses={
        401: {"description": "Invalid or missing API key"},
        400: {"description": "Invalid input data"},
        500: {"description": "Internal server error"}
    }
)
async def create_feedback(
    feedback: FeedbackCreate,
    api_key: str = Depends(get_api_key),
    db_strategy: DatabaseStrategy = Depends(get_db_strategy)
):
    # Validate API key against database
    if not await validate_api_key(api_key, db_strategy):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    try:
        feedback_service = FeedbackService(db_strategy)
        return await feedback_service.create_feedback(feedback)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )