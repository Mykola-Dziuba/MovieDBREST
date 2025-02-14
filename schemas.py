from typing import Any, List, Optional
import peewee
from pydantic import BaseModel
from pydantic.v1.utils import GetterDict  # Используем pydantic.v1 для совместимости


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ActorBase(BaseModel):
    name: str
    surname: str


class ActorCreate(ActorBase):
    pass


class Actor(ActorBase):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class MovieBase(BaseModel):
    title: str
    year: int
    director: Optional[str] = None
    description: Optional[str] = None
    actors: List[int]  # Должен быть **список ID актеров**, а не объекты


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    actors: List[Actor] = []  # Для возврата объектов при GET-запросе

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
