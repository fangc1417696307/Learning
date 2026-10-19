import sqlite3

DB_PATH = "student.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
     create table if not exists students(
        id integer primary key autoincrement,
        name text not null,
        major text not null,
        age integer default 0,
        goal text default '未填写'
        )
    """)

    conn.commit()
    conn.close()
