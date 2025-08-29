# create_schema.py
from app.models.database import engine, Base

async def create_db_tables():
    """
    Connects to the database and creates all tables based on the SQLAlchemy models.
    """
    print("--- Connecting to database and creating schema ---")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("--- Schema creation complete ---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_db_tables())