from fastapi import APIRouter, Depends, status
from api.models.user import UserCreate, UserOut
from services.auth import AuthService
from core.database.strategy import DatabaseStrategy
from core.config import settings
from core.database import get_db_strategy

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db_strategy: DatabaseStrategy = Depends(get_db_strategy)
):
    auth_service = AuthService(db_strategy)
    created_user = await auth_service.register_user(user_data.dict())
    return {
        "user_id": created_user["user_id"],
        "email": created_user["email"],
        "api_key": created_user["api_key"]
    }