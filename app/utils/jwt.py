# clast/app/utils/logger.py
import datetime

from typing import Dict, Any
from dataclasses import dataclass

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from app import setting

ALGORITHM = "HS256"

@dataclass
class UserInfo:
    user_id: int
    role: str

@dataclass
class JWTIDInterface:
    success: bool
    user_info: UserInfo | None



class JWTAgent:
    secret=setting.JWT_SECRET
    expire_delta=datetime.timedelta(minutes=setting.JWT_EXPIRE/60)
    time_format = '%Y-%m-%d %H:%M:%S'

    def encode_token(self, id: int, role: str) -> str:
        to_encode: Dict[str, Any]  = {"id": id, "role": role}
        expire = datetime.datetime.utcnow() + self.expire_delta
        to_encode.update({"exp": expire})
        encoded_jwt: str = jwt.encode(claims=to_encode, key=self.secret, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> JWTIDInterface:
        try:
            decoded = jwt.decode(token=token, key=self.secret, algorithms=ALGORITHM)
        except JWTError:
            return JWTIDInterface(success=False, user_info=None)
        if "id" in decoded.keys() and type(decoded["id"]) == int:
                return JWTIDInterface(
                    success=True, 
                    user_info=UserInfo(user_id=decoded["id"], role=decoded["role"])
                )
        return JWTIDInterface(success=False, user_info=None)

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UserInfo:
        credentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Access token not found")
        if not credentials.scheme == "Bearer" or not credentials.credentials:
            raise HTTPException(status_code=403, detail="Invalid authentication scheme or access token")
        jwt_result = surfingJWT.decode_token(credentials.credentials)
        if not jwt_result.success or jwt_result.user_info is None:
            raise HTTPException(status_code=403, detail="Invalid access token")
        return jwt_result.user_info
        
surfingJWT = JWTAgent()
