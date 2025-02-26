from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: str
    email: EmailStr
    api_key: str

class UserInDB(BaseModel):
    user_id: str
    email: EmailStr
    hashed_password: str
    api_key: str
    
class UserValidate(BaseModel):
    user_id: str
    api_key: str