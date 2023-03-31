# surfing-back/app/utils/dimi_api.py

from dataclasses import dataclass

import requests

from app import setting


@dataclass
class DimiAPIUserInfo:
    user_id: int
    email: str

@dataclass
class UserDetailInfo: 
    user_realname: str
    user_grade: int
    user_class: int

def login(username: str, password: str) -> DimiAPIUserInfo | str:
    res: requests.Response = requests.get(setting.DIMIAPI_URL + "/v1/users/identify", params={"username": username, "password": password}, auth=(setting.DIMIAPI_ID, setting.DIMIAPI_PW))
    if res.status_code == 404:
        return "User not found"
    if res.status_code != 200:
        return "Student API Error"
    res_dcit: dict = res.json()
    if res_dcit["user_type"] != "S":
        return "Not a student"
    return DimiAPIUserInfo(user_id=res_dcit["id"], email=res_dcit["email"])

def get_realname(user_id: int) -> str | None:
    res: requests.Response = requests.get(setting.DIMIAPI_URL + "/v1/user-students/search", params={"user_id": user_id},  auth=(setting.DIMIAPI_ID, setting.DIMIAPI_PW))
    if res.status_code != 200:
        return None
    res_dict: dict = res.json()
    return res_dict[0]["name"]

def get_user_info(user_id: int) -> UserDetailInfo | None:
    res: requests.Response = requests.get(setting.DIMIAPI_URL + "/v1/user-students/search", params={"user_id": user_id},  auth=(setting.DIMIAPI_ID, setting.DIMIAPI_PW))
    if res.status_code != 200:
        return None
    res_dict: dict = res.json()
    return UserDetailInfo(user_realname=res_dict[0]["name"], user_grade=res_dict[0]["grade"], user_class=res_dict[0]["class"])