from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel

from app.database import Base

class Period(Base):
    __tablename__ = "period"
    period = Column(String(20), primary_key=True)

class PeriodInterface(BaseModel):
    period: str