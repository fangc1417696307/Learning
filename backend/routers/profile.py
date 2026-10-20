import db
from fastapi import APIRouter, HTTPException
from schemas import ProfileRequest, ProfileResponse

router = APIRouter(prefix="/profile", tags=["学生画像"])


@router.post("", response_model=ProfileResponse)
def create_profile(req: ProfileRequest):
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "insert into students(name, major, age, goal) values(?,?,?,?)",
            (req.name, req.major, req.age, req.goal),
        )
        new_id = cur.lastrowid

    return ProfileResponse(
        id=new_id,
        name=req.name,
        major=req.major,
        age=req.age,
        goal=req.goal,
    )


@router.get("/{student_id}", response_model=ProfileResponse)
def get_profile(student_id: int):
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "select id, name, major, age, goal from students where id =?", (student_id,)
        )
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="不存在这个学生")
        return ProfileResponse(
            id=row[0],
            name=row[1],
            major=row[2],
            age=row[3],
            goal=row[4],
        )
