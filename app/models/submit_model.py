from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel

from app.database import Base

class Submit(Base):
    __tablename__ = "submit"
    submit_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    circle_id = Column(Integer, index=True, nullable=False)
    question1 = Column(String(300), nullable=False)
    question2 = Column(String(300), nullable=False)
    question3 = Column(String(300), nullable=False)
    question4 = Column(String(300), nullable=False)
    status = Column(String(20), nullable=False)

class SubmitInterface(BaseModel):
    submit_id: int
    user_id: int
    circle_id: int
    question1: str
    question2: str
    question3: str
    question4: str
    status: str