from datetime import datetime
from core.exceptions import NotFoundError
from api.models.feedback import FeedbackResponse

class FeedbackService:
    def __init__(self, db_strategies):
        # Temporary in-memory storage
       self.db_strategies = db_strategies  
    
    async def create_feedback(self, feedback):
        feedback_data = feedback.dict()
        for strategy in self.db_strategies.values():
            if strategy:
                feedback_data["created_at"] = datetime.utcnow().isoformat()
                created = await strategy.create_record(
                    api_path="/feedbacks",
                    data=feedback_data
                )
        return FeedbackResponse(**feedback_data)