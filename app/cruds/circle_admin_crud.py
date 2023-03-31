# surfing-back/app/cruds/circle_admin_crud.py

from typing import List
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.submit_model import Submit, SubmitInterface
from app.models.circle_model import Circle, CircleInterface

from app.cruds import auth_crud

from app.schemas.circle_admin_schema import AdminSubmitResponse

def get_user_circle_id(db: Session, owner_id: int) -> int:
    circle = db.query(Circle).filter((Circle.owner_id == owner_id) | (Circle.subowner_id == owner_id)).first()
    if circle is None:
        raise Exception("Circle is not set")
    return circle.circle_id # type: ignore
    
def get_all_circle_submit(db: Session, circle_id: int) -> List[AdminSubmitResponse]:
    submit_list = db.query(Submit).filter(Submit.circle_id == circle_id).all()
    result: List[AdminSubmitResponse] = []
    for submit in submit_list:
        user: auth_crud.UserInterface | None = auth_crud.get_user_by_id(db, submit.user_id) # type: ignore
        if user is None:
            raise Exception("User is not found")
        user_email = user.user_email
        user_grade: int = user.user_grade
        user_class: int = user.user_class
        user_realname: str = user.user_realname
        result.append(
            AdminSubmitResponse(
                submit_id=submit.submit_id, # type: ignore
                submitter_email=user_email, 
                submitter_grade=user_grade,
                submitter_class=user_class,
                submitter_student_no=user.user_student_no,
                submitter_realname=user_realname,
                question1=submit.question1, # type: ignore
                question2=submit.question2, # type: ignore
                question3=submit.question3, # type: ignore
                question4=submit.question4, # type: ignore
                status=submit.status # type: ignore
            ))
    return result

def get_submit_by_id(db: Session, submit_id: int) -> SubmitInterface | None:
    return db.query(Submit).get(submit_id)

def first_confirm_submit(db: Session, submit: SubmitInterface) -> str:
    submit.status = "FIRST"
    db.commit()
    user: auth_crud.UserInterface | None = auth_crud.get_user_by_id(db, submit.user_id) # type: ignore
    if user is None:
        raise Exception("User is not found")
    
    return user.user_email

def first_reject_submit(db: Session, submit: SubmitInterface) -> None:
    submit.status = "REJECTED"
    db.commit()
    return

def second_confirm_submit(db: Session, submit: SubmitInterface) -> None:
    submit.status = "SECOND"
    db.commit()
    return

def second_reject_submit(db: Session, submit: SubmitInterface) -> None:
    submit.status = "SECONDREJECTED"
    db.commit()
    return

def get_circle_by_id(db: Session, circle_id: int) -> CircleInterface | None:
    return db.query(Circle).get(circle_id)