"""Dataclass для данных"""
from pydantic import BaseModel, Field
from typing import List, Optional,Union,Literal
from enum import Enum

# Добавьте новый перечислимый тип
class PropertyType(str,Enum):
    HOUSE = "Дом"
    APARTMENT = "Квартира"
    ROOM = "Комната"
    COTTAGE = "Коттедж"

class Query(BaseModel):
    object_name: Optional[str] = Field(None, description="Название объекта")
    name: Optional[str] = Field(None, description="Наименование")
    price: Optional[float] = Field(None, description="Цена")
    old_price: Optional[float] = Field(None, description="Старая цена")

    showcase_images: Optional[List[str]] = Field([], description="Картинки на витрине")
    room_count: Optional[int] = Field(0, description="Кол-во комнат")
    finishing: Optional[str] = Field(None, description="Отделка")
    status: Optional[str] = Field(None, description="Статус")
    area: Optional[Union[float,dict]] = Field(0.0, description="Площадь")
    floor: Optional[int] = Field(0, description="Этаж")
    discount_percent: Optional[Union[float,dict]] = Field(0.0, description="Скидки (%)")
    # type: Optional[str] = Field(None, description="Тип")
    # type: Optional[PropertyType] = Field(None, description="Тип")
    type: Optional[Literal["Дом", "Квартира", "Комната", "Коттедж"]] = Field(None, description="Тип")
    total_floors: Optional[int] = Field(0, description="Этажность")
    price_per_sqm: Optional[float] = Field(0.0, description="Цена за кв.м. в рублях")
    unique_id: Optional[str] = Field(None, description="Уникальный ID")
    advantages: Optional[List[str]] = Field([], description="Преимущества")
    explain: Optional[list[str]] = Field([], description="пояснения к ответу")
