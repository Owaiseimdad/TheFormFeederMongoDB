from core.database.mongodb import MongoDBStrategy
from core.config import settings

def create_db_strategy(db_type: str, connection_uri: str):
    """Factory method to return the appropriate database strategy instance."""
    if db_type == "mongodb":
        return MongoDBStrategy(connection_uri, settings.DB_NAMES[0])
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
