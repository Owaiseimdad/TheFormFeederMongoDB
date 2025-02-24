from pydantic import BaseModel, Field, EmailStr

class FeedbackBase(BaseModel):
    user_email: EmailStr
    comment: str = Field(..., min_length=1, max_length=500)
    rating: int = Field(..., ge=0, le=5)

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: str
    created_at: str