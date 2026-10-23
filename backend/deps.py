from _collections_abc import Generator
from typing import Annotated

import db
from fastapi import Depends


def get_conn() -> Generator:
    """每个请求一个连接，请求结束后自动提交/回滚并关闭"""
    with db.get_db() as conn:
        yield conn


ConnDep = Annotated[object, Depends(get_conn)]
