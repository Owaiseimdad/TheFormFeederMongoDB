from fastapi import HTTPException, status
from core.security import generate_api_key
from core.security_password import get_password_hash, verify_password
import uuid


class AuthService:
    def __init__(self, db_strategies: dict): 
        """
        db_strategies should be a dictionary where keys are database names and values are strategy instances.
        Example: {"mongodb": MongoDBStrategy(), "postgres": PostgresStrategy()}
        """
        self.db_strategies = db_strategies  

    async def register_user(self, user_data: dict) -> dict:
        """
        Registers a new user in all database strategies.
        """
        email = user_data["email"]

        # Check if user exists in any database
        for strategy in self.db_strategies.values():
            existing_user = await strategy.get_record_by_field("users", "email", email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
                
        user_id = str(uuid.uuid4())
        api_key = generate_api_key()
        
        new_user = {
            "user_id": user_id,
            "email": email,
            "hashed_password": get_password_hash(user_data["password"]),
            "api_key": api_key
        }
        
        created_users = []
        for strategy in self.db_strategies.values():
            created_users.append(await strategy.create_record("users", new_user))

        return created_users[0]  # Returning the first created user

    async def validate_user(self, user_data: dict) -> dict:
        """
        Validates a user by checking their user_id and API key in all available databases.
        """
        user_id = user_data["user_id"]
        api_key = user_data["api_key"]

        for strategy in self.db_strategies.values():
            existing_user = await strategy.get_record_by_field("users", "user_id", user_id)
            
            # Directly compare API keys (assuming they are stored as plain text)
            if existing_user and existing_user["api_key"] == api_key:
                return existing_user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
