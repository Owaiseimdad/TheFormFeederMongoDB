from fastapi import HTTPException, status
from core.security import generate_api_key
from core.security_password import get_password_hash
import uuid


class AuthService:
    def __init__(self, db_strategies): 
        self.db_strategies = db_strategies  

    async def register_user(self, user_data: dict) -> dict:
        # Check if user exists in any database
        for strategy in self.db_strategies:
            existing_user = await strategy.get_record_by_field("users", "email", user_data["email"])
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
                
        user_id = str(uuid.uuid4())
        api_key = generate_api_key()
        
        new_user = {
            "user_id": user_id,
            "email": user_data["email"],
            "hashed_password": get_password_hash(user_data["password"]),
            "api_key": api_key
        }
        
        created_users = []
        for strategy in self.db_strategies:
            created_users.append(await strategy.create_record("users", new_user))

        return created_users[0]
