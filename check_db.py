import asyncio
from src.core.database import engine
from sqlalchemy import text

async def check():
    async with engine.connect() as conn:
        result = await conn.execute(text(
            "SELECT column_name FROM information_schema.columns WHERE table_name='links' AND column_name='expires_at'"
        ))
        row = result.fetchone()
        if row:
            print("✅ Поле expires_at существует")
        else:
            print("❌ Поля expires_at нет")

asyncio.run(check())