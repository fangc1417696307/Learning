import db
from fastapi import FastAPI
from routers import profile

db.init_db()

app = FastAPI()

app.include_router(profile.router)


@app.get("/")
def read_root():
    return {"message": "这是我第一个 FastAPI 应用程序！"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"你好，{name}"}
