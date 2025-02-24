from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class DatabaseStrategy(ABC):
    @abstractmethod
    async def connect(self):
        """Establish a database connection."""
        pass

    @abstractmethod
    async def create_record(self, api_path: str, data: Dict) -> Dict:
        """Create a record in a dynamically selected collection based on API path."""
        pass

    @abstractmethod
    async def get_record_by_field(self, api_path: str, field: str, value: str) -> Optional[Dict]:
        """Retrieve a record from a dynamically selected collection using a specific field."""
        pass
    
    @abstractmethod
    async def get_info_by_id(self, info_id: str) -> Optional[Dict]:
        """Retrieve a user by ID from the database."""
        pass