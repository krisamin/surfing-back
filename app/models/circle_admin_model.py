from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel

from app.database import Base

class CircleAdmin(Base):
    __tablename__ = "circle_admin"
    owner_username = Column(String(100), primary_key=True, nullable=False, unique=True)
    circle_id = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)
    complete= Column(Boolean, nullable=False, default=False)
    user_realname = Column(String(10), nullable=False)
    user_grade = Column(Integer, nullable=False)
    user_class = Column(Integer, nullable=False)
    user_student_no = Column(Integer, nullable=False)

class CircleAdminInterface(BaseModel):
    owner_username: str
    circle_id: int
    role: str
    complete: bool
    user_realname: str
    user_grade: int
    user_class: int

