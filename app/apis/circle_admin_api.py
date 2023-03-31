# surfing-back/app/apis/circle_admin_api.py

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas import base_schema, submit_schema, circle_admin_schema
from app.utils import jwt
from app.cruds import submit_crud, circle_admin_crud, period_crud
from app.models.user_model import UserInterface
from app.models.submit_model import SubmitInterface
from app.database import get_db
from app import setting

router = APIRouter(
    prefix="/circle_admin",
    tags=["circle_admin"],
)

@router.get("/submit", responses={
    200: {"model": List[circle_admin_schema.AdminSubmitResponse]},
    401: {"model": circle_admin_schema.NoPermissionError},
    403: {"model": base_schema.JWTBearerError},
})
def get_all_circle_submit(
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    if user_info.role != "CIRCLE_ADMIN" and user_info.role != "CIRCLE_VICE_ADMIN":
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    circle_id = circle_admin_crud.get_user_circle_id(db, user_info.user_id)
    submit_list: List[circle_admin_schema.AdminSubmitResponse] = circle_admin_crud.get_all_circle_submit(db, circle_id)
    return circle_admin_schema.AdminSubmitListResponse(submit_list=submit_list, circle_id=circle_id)

@router.get("/firstconfirm", responses={
    200: {"model": circle_admin_schema.FirstConfirmResponse},
    401: {"model": circle_admin_schema.NoPermissionError},
    402: {"model": circle_admin_schema.SubmitNotFoundError},
    403: {"model": base_schema.JWTBearerError},
    406: {"model": base_schema.NotPeriodError},
})
def confirm_first_submit(
    submit_id: int,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    if user_info.role != "CIRCLE_ADMIN":
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    if period_crud.get_period(db) != "FIRSTEVAL":
        return JSONResponse(status_code=406, content=base_schema.NotPeriodError(error="Not first evaluation period").to_json_str())
    circle_id = circle_admin_crud.get_user_circle_id(db, user_info.user_id)
    submit_object = circle_admin_crud.get_submit_by_id(db, submit_id)
    if submit_object == None or submit_object.status != "SUBMITTED" and submit_object.status != "REJECTED":
        return JSONResponse(status_code=402, content=circle_admin_schema.SubmitNotFoundError(error="Submit not found").to_json_str())
    if circle_id != submit_object.circle_id:
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    
    user_email = circle_admin_crud.first_confirm_submit(db, submit_object)
    return circle_admin_schema.FirstConfirmResponse(submitter_email=user_email)

@router.get("/firstreject", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    401: {"model": circle_admin_schema.NoPermissionError},
    402: {"model": circle_admin_schema.SubmitNotFoundError},
    403: {"model": base_schema.JWTBearerError},
    406: {"model": base_schema.NotPeriodError},
})
def reject_first_submit(
    submit_id: int,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    
    if user_info.role != "CIRCLE_ADMIN":
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    if period_crud.get_period(db) != "FIRSTEVAL":
        return JSONResponse(status_code=406, content=base_schema.NotPeriodError(error="Not first evaluation period").to_json_str())
    
    circle_id = circle_admin_crud.get_user_circle_id(db, user_info.user_id)
    submit_object = circle_admin_crud.get_submit_by_id(db, submit_id)
    if submit_object == None or submit_object.status != "SUBMITTED" and submit_object.status != "FIRST":
        return JSONResponse(status_code=402, content=circle_admin_schema.SubmitNotFoundError(error="Submit not found").to_json_str())
    if circle_id != submit_object.circle_id:
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    
    circle_admin_crud.first_reject_submit(db, submit_object)
    return base_schema.GeneralSuccessResponse(message="Reject success")

@router.get("/secondconfirm", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    401: {"model": circle_admin_schema.NoPermissionError},
    402: {"model": circle_admin_schema.SubmitNotFoundError},
    403: {"model": base_schema.JWTBearerError},
    406: {"model": base_schema.NotPeriodError},
})
def confirm_second_submit(
    submit_id: int,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    if user_info.role != "CIRCLE_ADMIN":
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    if period_crud.get_period(db) != "SECONDEVAL":
        return JSONResponse(status_code=406, content=base_schema.NotPeriodError(error="Not second evaluation period").to_json_str())
    
    circle_id = circle_admin_crud.get_user_circle_id(db, user_info.user_id)
    submit_object = circle_admin_crud.get_submit_by_id(db, submit_id)
    if submit_object == None or submit_object.status != "FIRST" and submit_object.status != "SECONDREJECTED":
        return JSONResponse(status_code=402, content=circle_admin_schema.SubmitNotFoundError(error="Submit not found").to_json_str())
    if circle_id != submit_object.circle_id:
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    
    circle_admin_crud.second_confirm_submit(db, submit_object)
    return base_schema.GeneralSuccessResponse(message="Confirm success")

@router.get("/secondreject", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    401: {"model": circle_admin_schema.NoPermissionError},
    402: {"model": circle_admin_schema.SubmitNotFoundError},
    403: {"model": base_schema.JWTBearerError},
    406: {"model": base_schema.NotPeriodError},
})
def reject_second_submit(
    submit_id: int,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    
    if user_info.role != "CIRCLE_ADMIN":
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    if period_crud.get_period(db) != "SECONDEVAL":
        return JSONResponse(status_code=406, content=base_schema.NotPeriodError(error="Not second evaluation period").to_json_str())
    
    circle_id = circle_admin_crud.get_user_circle_id(db, user_info.user_id)
    submit_object = circle_admin_crud.get_submit_by_id(db, submit_id)
    if submit_object == None or submit_object.status != "FIRST" and submit_object.status != "SECOND":
        return JSONResponse(status_code=402, content=circle_admin_schema.SubmitNotFoundError(error="Submit not found").to_json_str())
    if circle_id != submit_object.circle_id:
        return JSONResponse(status_code=401, content=circle_admin_schema.NoPermissionError(error="No permission").to_json_str())
    
    circle_admin_crud.second_reject_submit(db, submit_object)
    return base_schema.GeneralSuccessResponse(message="Reject success")

