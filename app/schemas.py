from typing import Any, List, Union

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    body: str


class Book(BookCreate):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
