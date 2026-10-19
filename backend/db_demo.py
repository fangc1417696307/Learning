# import sqlite3

# conn = sqlite3.connect("student.db")
# cur = conn.cursor()

# cur.execute("""
# create table if not exists students(
#     id integer primary key autoincrement,
#     name text not null,
#     major text not null,
#     age integer default 0
#     )
# """)
# conn.commit()
# cur.execute("delete from students")
# conn.commit()

# cur.executemany(
#     """
# insert into students(name, major, age) values (?, ?, ?)""",
#     [
#         ("张三", "计算机", 20),
#         ("李四", "信息工程", 21),
#         ("王五", "软件工程", 22),
#     ],
# )
# conn.commit()

# cur.execute("select * from students where age >20")
# rows = cur.fetchall()
# print(rows)

# conn.close()
