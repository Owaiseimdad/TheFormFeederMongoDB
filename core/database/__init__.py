from core.database.strategy import DatabaseStrategy
from core.database.db_factory import create_db_strategy
from core.config import settings

db_strategies: dict[str, DatabaseStrategy] = {}

async def get_db_strategy() -> list[DatabaseStrategy]:
    global db_strategies
    # If already initialized, return cached strategies
    if db_strategies:
        return db_strategies

    for db_type, db_uri in zip(settings.DB_TYPES, settings.DB_URIS):
        strategy = create_db_strategy(db_type, db_uri)
        await strategy.connect()
        db_strategies[db_type] = strategy

    return db_strategies
