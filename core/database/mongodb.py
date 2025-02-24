from typing import Optional, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from core.database.strategy import DatabaseStrategy

class MongoDBStrategy(DatabaseStrategy):
    def __init__(self, connection_uri: str, db_name: str):
        self.client = None
        self.db = None
        self.connection_uri = connection_uri
        self.db_name = db_name

    async def connect(self):
        """Establish database connection."""
        self.client = AsyncIOMotorClient(self.connection_uri)
        self.db = self.client[self.db_name]

    def get_collection(self, api_path: str):
        """Dynamically determine the collection name based on API path."""
        collection_name = api_path.strip("/").replace("/", "_")
        return self.db[collection_name]

    async def create_record(self, api_path: str, data: Dict) -> Dict:
        """Insert a new record into a dynamically chosen collection."""
        collection = self.get_collection(api_path)
        result = await collection.insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def get_record_by_field(self, api_path: str, field: str, value: str) -> Optional[Dict]:
        """Fetch a record from a dynamically chosen collection based on a field."""
        collection = self.get_collection(api_path)
        return await collection.find_one({field: value})
    
    async def get_info_by_id(self, user_id: str) -> Optional[Dict]:
        """Retrieve a user by ID from the 'users' collection."""
        collection = self.db["users"]  # Assuming users are always stored in 'users' collection
        return await collection.find_one({"user_id": user_id})