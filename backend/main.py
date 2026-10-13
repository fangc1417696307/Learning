from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "我的第一个 FastAPI 应用程序!"}