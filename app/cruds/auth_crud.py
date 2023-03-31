# surfing-back/app/cruds/auth_crud.py

from typing import List
from dataclasses import dataclass

import uuid

from sqlalchemy.orm import Session

from app.models.user_model import User, UserInterface
from app.models.refresh_token_model import RefreshToken, RefreshTokenInterface
from app.models.circle_admin_model import CircleAdmin, CircleAdminInterface

@dataclass
class UserInfo:
    user_id: int
    role: str

def get_user_by_id(db: Session, user_id: int) -> UserInterface | None:
    return db.query(User).get(user_id)

def create_user(db: Session, user_id: int, user_role: str, user_email: str, user_realname: str, user_grade: int, user_class: int) -> None:
    new_user = User(user_id=user_id, role=user_role, user_email=user_email, user_realname=user_realname, user_grade=user_grade, user_class=user_class, user_student_no=0)
    db.add(new_user)
    db.commit()
    return

def create_refresh_token(db: Session, user_id: int) -> str:
    refresh_token = uuid.uuid4().hex
    new_refresh_token = RefreshToken(user_id=user_id, refresh_token=refresh_token)
    db.add(new_refresh_token)
    db.commit()
    return refresh_token

def delete_refresh_token(db: Session, refresh_token: str) -> bool:
    try:
        db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).delete()
        db.commit()
        return True
    except:
        return False

def get_user_info_by_refresh_token(db: Session, refresh_token: str) -> UserInfo | None:
    user_refresh_token: RefreshTokenInterface | None = db.query(RefreshToken).get(refresh_token)
    if user_refresh_token is None:
        return None
    user = get_user_by_id(db, user_refresh_token.user_id)
    if user is None:
        return None
    return UserInfo(user_id=user.user_id, role=user.role)

def set_user_student_info(db: Session, user: UserInterface, student_no: int, student_realname: str) -> bool:
    same_user_no_list: List[User]= db.query(User).filter(User.user_grade == user.user_grade, User.user_class == user.user_class, User.user_student_no == student_no).all()
    if len(same_user_no_list) != 0:
        return False
    user.user_student_no = student_no
    user.user_realname = student_realname
    db.commit()
    return True

def check_user_is_circle_admin(db: Session, user_username: str) -> CircleAdminInterface | None:
    circle_admin: CircleAdminInterface | None = db.query(CircleAdmin).get(user_username)
    if circle_admin is None:
        return None
    circle_admin.complete = True
    db.commit()
    db.refresh(circle_admin)
    return circle_admin
