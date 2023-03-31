# surfing-back/app/apis/auth_api.py

from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas import base_schema, auth_schema
from app.utils import jwt, dimi_api
from app.cruds import auth_crud, circle_admin_crud
from app.models.user_model import UserInterface
from app.database import get_db
from app import setting

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    )

@router.post("/login", responses={
    200: {"model": auth_schema.TokenResponse},
    400: {"model": base_schema.GeneralErrorResponse}
})
def login(
    user_login_data: auth_schema.LoginRequest,
    db: Session = Depends(get_db),
):
    
    login_result = dimi_api.login(user_login_data.username, user_login_data.password)
    if isinstance(login_result, str):
        return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error=login_result).to_json_str())
    user_id = login_result.user_id
    user_email = login_result.email
    user: UserInterface | None = auth_crud.get_user_by_id(db, user_id)
    if user is None:
        user_detail_info = dimi_api.get_user_info(user_id)
        if user_detail_info == None:
            return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error="DimiAPI Error").to_json_str())
        circle_data = auth_crud.check_user_is_circle_admin(db, user_login_data.username)
        if circle_data is not None:
            circle = circle_admin_crud.get_circle_by_id(db, circle_data.circle_id)
            if circle is None:
                return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error="Circle is not found").to_json_str())
            if circle_data.role == "CIRCLE_ADMIN":
                circle.owner_id = user_id
            elif circle_data.role == "CIRCLE_VICE_ADMIN":
                circle.subowner_id = user_id
            else:
                return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error="Circle Admin Role is not valid").to_json_str())
            user_role = circle_data.role
            auth_crud.create_user(db, user_id, circle_data.role, user_email, circle_data.user_realname, circle_data.user_grade, circle_data.user_class)
        else:
            user_role = "STUDENT"
            auth_crud.create_user(db, user_id, "STUDENT", user_email, user_detail_info.user_realname, user_detail_info.user_grade, user_detail_info.user_class)
    else:
        user_role = user.role
        
    new_access_token = jwt.surfingJWT.encode_token(user_id, user_role)
    new_refresh_token = auth_crud.create_refresh_token(db, user_id)

    return auth_schema.TokenResponse(
        access_token=new_access_token,
        expire_in=setting.JWT_EXPIRE,
        refresh_token=new_refresh_token
    )

@router.get("/refresh", responses={
    200: {"model": auth_schema.AccessTokenResponse},
    404: {"model": auth_schema.UserNotFound}
})
def refresh(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    refresh_token_result = auth_crud.get_user_info_by_refresh_token(db, refresh_token)
    
    if refresh_token_result == None:
        return JSONResponse(status_code=404, content=auth_schema.UserNotFound(error="User Not Found").to_json_str())
    new_access_token = jwt.surfingJWT.encode_token(refresh_token_result.user_id, refresh_token_result.role)
    return auth_schema.AccessTokenResponse(
        access_token=new_access_token,
        expire_in=setting.JWT_EXPIRE
    )

@router.get("/logout", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    404: {"model": auth_schema.UserNotFound}
})
def logout(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    refresh_token_result: bool = auth_crud.delete_refresh_token(db, refresh_token)
    if not refresh_token_result:
        return JSONResponse(status_code=404, content=auth_schema.UserNotFound(error="User Not Found").to_json_str())
    return base_schema.GeneralSuccessResponse(message="Logout Success")

@router.get("/me", responses={
    200: {"model": auth_schema.UserInfoResponse},
    403: {"model": base_schema.JWTBearerError}
    })
def get_my_info(
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    user: UserInterface | None = auth_crud.get_user_by_id(db, user_info.user_id)
    if user == None:
        return JSONResponse(status_code=403, content=base_schema.GeneralErrorResponse(error="User Not Found").to_json_str())
    return auth_schema.UserInfoResponse(user_id=user.user_id, real_name=user.user_realname, role=user_info.role, email=user.user_email, user_grade=user.user_grade, user_class=user.user_class, user_student_no=user.user_student_no)

@router.post("/student_info", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    400: {"model": base_schema.GeneralErrorResponse},
})
def set_student_info(
    user_info_data: auth_schema.SetUserInfoRequest,
    user_info: jwt.UserInfo = Depends(jwt.JWTBearer()),
    db: Session = Depends(get_db),
):
    user: UserInterface | None = auth_crud.get_user_by_id(db, user_info.user_id)
    if user == None:
        return JSONResponse(status_code=403, content=base_schema.GeneralErrorResponse(error="User Not Found").to_json_str())
    for letter in range(0, len(user.user_realname)):
        if user.user_realname[letter] != user_info_data.user_realname[letter] and user.user_realname[letter] != "*":
            return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error="Realname Not Match").to_json_str())
    result: bool = auth_crud.set_user_student_info(db, user, user_info_data.user_student_no, user_info_data.user_realname)
    if result == False:
        return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error="Set Student Info Error").to_json_str())
    return base_schema.GeneralSuccessResponse(message="Set User Student Info Success")