# surfing-back/app/apis/submit_api.py

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas import base_schema, submit_schema
from app.utils import jwt
from app.cruds import submit_crud, period_crud, auth_crud
from app.models.user_model import UserInterface
from app.models.submit_model import SubmitInterface
from app.database import get_db
from app import setting

router = APIRouter(
    prefix="/submit",
    tags=["submit"],
    )

@router.get("", responses={
    200: {"model": List[submit_schema.SubmitResponse]},
    403: {"model": base_schema.JWTBearerError},
})
def get_my_all_submit(
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    submit_list: List[submit_schema.SubmitResponse] = submit_crud.get_user_all_submit(db, user_info.user_id)
    current_period = period_crud.get_period(db)
    if current_period == "FIRSTEVAL":
        for submit in submit_list:
            submit.status = "SUBMITTED"
    elif current_period == "SECONDEVAL":
        for submit in submit_list:
            if submit.status != "REJECTED":
                submit.status = "FIRST"
    return submit_schema.SubmitListResponse(submit_list=submit_list)



@router.post("", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    400: {"model": submit_schema.SubmitCountOverError},
    401: {"model":submit_schema.OwnerCannotSubmitError},
    402: {"model": submit_schema.CircleNotFoundError},
    403: {"model": base_schema.JWTBearerError},
    405: {"model": submit_schema.MultipleSubmitError},
    406: {"model": base_schema.NotPeriodError},
    407: {"model": submit_schema.StudentNoNotSetError},

})
def submit(
    submit_data: submit_schema.SubmitRequest,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    user: UserInterface | None = auth_crud.get_user_by_id(db, user_info.user_id)
    if user is None:
        return JSONResponse(status_code=403, content=base_schema.JWTBearerError(detail="User Not Found").to_json_str())
    if user.user_student_no == 0:
        return JSONResponse(status_code=403, content=submit_schema.StudentNoNotSetError(error="Student no was not set").to_json_str())
    if user.role != "STUDENT":
        return JSONResponse(status_code=401, content=submit_schema.OwnerCannotSubmitError(error="Owner cannot submit").to_json_str())
    if period_crud.get_period(db) != "SUBMITTING":
        return JSONResponse(status_code=406, content=base_schema.NotPeriodError(error="Not submit period").to_json_str())
    if submit_crud.get_submit_count(db, user_info.user_id) >= 3:
        return JSONResponse(status_code=400, content=submit_schema.SubmitCountOverError(error="Submit count over").to_json_str())
    if submit_crud.check_multiple_submit(db, user_info.user_id, submit_data.circle_id) == True:
        return JSONResponse(status_code=405, content=submit_schema.MultipleSubmitError(error="Multiple submit").to_json_str())
    if submit_crud.check_circle_exist(db, submit_data.circle_id) == False:
        return JSONResponse(status_code=402, content=submit_schema.CircleNotFoundError(error="Circle not found").to_json_str())
    submit_crud.create_submit(db, user_info.user_id, submit_data.circle_id, submit_data.question1, submit_data.question2, submit_data.question3, submit_data.question4)
    return base_schema.GeneralSuccessResponse(message="Submit success")

@router.get("/final_choice", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    400: {"model": submit_schema.AlreadyFinalChoiceError},
    401: {"model": submit_schema.OwnerCannotSubmitError},
    402: {"model": submit_schema.NotSecondPassedError},
    403: {"model": base_schema.JWTBearerError},
})
def final_choice(
    circle_id: int,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    
    if user_info.role != "STUDENT":
        return JSONResponse(status_code=401, content=submit_schema.OwnerCannotSubmitError(error="Owner cannot final choice").to_json_str())
    if period_crud.get_period(db) != "FINAL":
        return JSONResponse(status_code=406, content=base_schema.NotPeriodError(error="Not submit period").to_json_str())
    if submit_crud.check_final_choice(db, user_info.user_id) == True:
        return JSONResponse(status_code=400, content=submit_schema.AlreadyFinalChoiceError(error="Aleady did final choice").to_json_str())
    submit_result: SubmitInterface | None = submit_crud.get_submit(db, user_info.user_id, circle_id)
    if submit_result is None or submit_result.status != "SECOND":
        return JSONResponse(status_code=402, content=submit_schema.NotSecondPassedError(error="Submit Not found").to_json_str())
    submit_crud.update_submit_status(db, submit_result, "FINALCHOICE")
    return base_schema.GeneralSuccessResponse(message="Final choice success")
    
    