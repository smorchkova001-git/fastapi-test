from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String
from src.core.database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    username = Column(String, unique=True, index=True, nullable=False)