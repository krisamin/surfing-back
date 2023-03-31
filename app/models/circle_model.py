from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel

from app.database import Base

class Circle(Base):
    __tablename__ = "circle"
    circle_id = Column(Integer, primary_key=True, index=True, unique=True)
    owner_id = Column(Integer, nullable=False, unique=True)
    subowner_id = Column(Integer, nullable=True, unique=True)

class CircleInterface(BaseModel):
    circle_id: int
    owner_id: int
    subowner_id: int