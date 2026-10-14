from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ProfileRequest(BaseModel):
    name: str
    major: str
    age: int = 0
    goal: str = "未填写"


@app.get("/")
def read_root():
    return {"message": "这是我第一个 FastAPI 应用程序！"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"你好，{name}"}


@app.post("/profile")
def create_profile(req: ProfileRequest):
    return {
        "student": req.name,
        "profile": {
            "年龄": req.age,
            "专业": req.major,
            "学习目标": req.goal,
        },
    }
