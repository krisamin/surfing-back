
from pydantic import Field

from app.schemas.base_schema import BaseSchema

class LoginRequest(BaseSchema):
    username: str = Field(title="ID", description="Student ID")
    password: str = Field(title="PW", description="Student Password")

class TokenResponse(BaseSchema):
    access_token: str = Field(title="Access Token", description="Access Token")
    expire_in: int = Field(title="Expires In", description="Access Token Expires In(sec)")
    refresh_token: str = Field(title="Refresh Token", description="Refresh Token")

class RefreshRequest(BaseSchema):
    refresh_token: str = Field(title="Refresh Token", description="Refresh Token")

class AccessTokenResponse(BaseSchema):
    access_token: str = Field(title="Access Token", description="Access Token")
    expire_in: int = Field(title="Expires In", description="Access Token Expires In(sec)")

class UserNotFound(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class UserInfoResponse(BaseSchema):
    user_id: int = Field(title="ID", description="ID")
    real_name: str = Field(title="Real Name", description="Real Name")
    email: str = Field(title="Email", description="Email")
    user_grade: int = Field(title="Grade", description="Grade")
    user_class: int = Field(title="Class", description="Class")
    user_student_no: int = Field(title="Student No", description="Student No")
    role: str = Field(title="Role", description="Role")

class SetUserInfoRequest(BaseSchema):
    user_student_no: int = Field(title="Student No", description="Student No", ge=1, le=33)
    user_realname: str = Field(title="Real Name", description="Real Name", min_length=2, max_length=5)