from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from src.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Проверка подключения к БД при старте
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        # Здесь можно решить, завершать приложение или нет
        # Для теста лучше завершить, чтобы Render показал ошибку
        raise e
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello from Render!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}