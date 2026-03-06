from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from src.core.database import engine
from src.core.cache import init_cache
from fastapi_cache import FastAPICache
from src.auth.users import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.links.router import router as links_router
from src.links.redirect import router as redirect_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Проверка БД
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e
    # Инициализация Redis
    await init_cache()
    print("✅ Redis cache initialized")
    yield
    await FastAPICache.clear()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Подключаем роутеры аутентификации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(redirect_router)  # для редиректа без префикса
app.include_router(links_router, prefix="/links")

@app.get("/")
async def root():
    return {"message": "Hello from Render!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

from sqlalchemy import text

@app.get("/debug/check-expires-at")
async def check_expires_at():
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT column_name FROM information_schema.columns WHERE table_name='links' AND column_name='expires_at'")
        )
        row = result.fetchone()
        if row:
            return {"exists": True}
        else:
            return {"exists": False}