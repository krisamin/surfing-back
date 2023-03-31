# surfing-back/app/cruds/submit_crud.py

from typing import List
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.submit_model import Submit, SubmitInterface
from app.models.circle_model import Circle, CircleInterface

from app.schemas.submit_schema import SubmitResponse


def get_user_all_submit(db: Session, user_id: int) -> List[SubmitResponse]:
    submit_list = db.query(Submit).filter(Submit.user_id == user_id).all()
    result: List[SubmitResponse] = []
    for submit in submit_list:
        result.append(
            SubmitResponse(
                circle_id=submit.circle_id, # type: ignore
                question1=submit.question1, # type: ignore
                question2=submit.question2, # type: ignore
                question3=submit.question3, # type: ignore
                question4=submit.question4, # type: ignore
                status=submit.status # type: ignore
            ))
    return result


        

def get_submit_count(db: Session, user_id: int) -> int:
    return db.query(Submit).filter(Submit.user_id == user_id).count()

def check_multiple_submit(db: Session, user_id: int, circle_id: int) -> bool:
    return db.query(Submit).filter(Submit.user_id == user_id, Submit.circle_id == circle_id).count() > 0

def check_circle_exist(db: Session, circle_id: int) -> bool:
    return db.query(Circle).get(circle_id) is not None

def check_final_choice(db: Session, user_id: int) -> bool:
    return db.query(Submit).filter(Submit.user_id == user_id, Submit.status == "FINALCHOICE").count() > 0

def get_submit(db: Session, user_id: int, circle_id: int) -> SubmitInterface | None:
    return db.query(Submit).filter(Submit.user_id == user_id, Submit.circle_id == circle_id).first()

def create_submit(db: Session, user_id: int, circle_id: int, question1: str, question2: str, question3: str, question4: str):
    new_submit = Submit(user_id=user_id, circle_id=circle_id, question1=question1, question2=question2, question3=question3, question4=question4, status="SUBMITTED")
    db.add(new_submit)
    db.commit()
    return

def update_submit_status(db: Session, submit: SubmitInterface, status: str):
    submit.status = status
    db.commit()
    return