from core.database.strategy import DatabaseStrategy
from core.database.db_factory import create_db_strategy
from core.config import settings

async def get_db_strategy() -> list[DatabaseStrategy]:
    strategies = []

    for db_type, db_uri in zip(settings.DB_TYPES, settings.DB_URIS):
        strategy = create_db_strategy(db_type, db_uri)
        await strategy.connect()
        strategies.append({db_type:strategy})

    return strategies

