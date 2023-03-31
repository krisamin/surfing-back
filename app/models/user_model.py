from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel

from app.database import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20), nullable=False)
    user_email = Column(String(200), nullable=False, unique=True)
    user_realname = Column(String(20), nullable=False)
    user_grade = Column(Integer, nullable=False)
    user_class = Column(Integer, nullable=False)
    user_student_no = Column(Integer)

class UserInterface(BaseModel):
    user_id: int
    role: str
    user_email: str
    user_realname: str
    user_grade: int
    user_class: int
    user_student_no: int


    
    