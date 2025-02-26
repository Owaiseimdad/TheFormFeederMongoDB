from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from core.database.strategy import DatabaseStrategy
from core.config import settings
import secrets

# API Key security scheme
api_key_scheme = APIKeyHeader(
    name=settings.API_KEY_HEADER,
    auto_error=False
)

def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_hex(32) 
    
async def validate_api_key(
    api_key: str = Depends(api_key_scheme),
    db_strategy: DatabaseStrategy = Depends()
) -> bool:
    """Validate API key against database"""
    if not api_key:
        return False
    user = None
    for db_Choice in db_strategy.values():
        if db_Choice:
            user = await db_Choice.get_record_by_field(
                api_path="/users",
                field="api_key",
                value=api_key
            )
    return user is not None

async def get_current_user(
    api_key: str = Depends(api_key_scheme),
    db_strategy: DatabaseStrategy = Depends()
):
    """Get full user details from API key"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing"
        )
    
    user = await db_strategy.get_record_by_field(
        api_path="/users",
        field="api_key",
        value=api_key
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return user