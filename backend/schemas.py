from pydantic import BaseModel


class ProfileRequest(BaseModel):
    name: str
    major: str
    age: int = 0
    goal: str = "未填写"


class ProfileResponse(BaseModel):
    id: int
    name: str
    major: str
    age: int
    goal: str
