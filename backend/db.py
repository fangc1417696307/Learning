import sqlite3

from config import setting

DB_PATH = setting.db_path


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_db() as conn:
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


class DBConnection:
    """用 with 管理的数据库连接。"""

    def __init__(self, path):
        self.path = path  # str，数据库文件路径
        self.conn = None  # sqlite3.Connection，进入时才创建

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn  # ← with ... as conn 拿到的就是它

    def __exit__(self, exc_type, exc_value, traceback):
        # exc_type 是 None → 没出错；否则就是异常的类型
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
        # 返回 None（假值）→ 异常继续往外抛，不被吞掉


def get_db():
    return DBConnection(DB_PATH)
