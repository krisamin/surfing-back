from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel

from app.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_token"
    user_id = Column(Integer, nullable=False)
    refresh_token = Column(String(36), primary_key=True, unique=True, index=True, nullable=False)

class RefreshTokenInterface(BaseModel):
    user_id: int
    refresh_token: str