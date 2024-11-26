from datetime import date, time, datetime
from typing import Annotated

from fastui.forms import Textarea
from pydantic import BaseModel, Field

from config import parsers_names


class ParserBase(BaseModel):
    id: int
    name: str = Field(title="Название")
    info: Annotated[str | None, Textarea(rows=5)] = Field(title="Описание")
    startDate: date = Field(title="Дата запуска")
    startTime: time = Field(title="Время запуска")
    status: str = Field(default="Ожидание", title="Статус")
    last_run_time: datetime | None = Field(default=None, title="Последнее время запуска")
    selected: parsers_names = Field(title="Парсер")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }


class AddParser(BaseModel):
    name: str = Field(title="Название")
    info: Annotated[str | None, Textarea(rows=5)] = Field(title="Описание")
    startDate: date = Field(title="Дата запуска")
    startTime: time = Field(title="Время запуска")
    selected: parsers_names = Field(title="Парсер")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None,
            parsers_names: lambda v: v.replace(".py", "") if v else None
        }


class DeleteParser(BaseModel):
    id: int
