import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

db.init_db()

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
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "insert into students(name, major, age, goal) values(?,?,?,?)",
            (req.name, req.major, req.age, req.goal),
        )
        new_id = cur.lastrowid

    return {
        "id": new_id,
    }


@app.get("/profile/{student_id}")
def get_profile(student_id: int):
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "select id, name, major, age, goal from students where id =?", (student_id,)
        )
        row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="不存在这个学生")
    return {
        "id": row[0],
        "name": row[1],
        "major": row[2],
        "age": row[3],
        "goal": row[4],
    }
