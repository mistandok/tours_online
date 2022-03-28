"""This module describe data model for tours"""

__author__ = 'Artikov A.K.'

from dataclasses import dataclass
from typing import Union
import dacite


@dataclass()
class BaseModel:
    @classmethod
    def construct_from_dict(cls, dict_data: dict) -> 'BaseModel':
        data_model = dacite.from_dict(cls, dict_data)
        return data_model

    def as_dict(self):
        return self.__dict__


@dataclass
class Tour(BaseModel):
    id: int
    title: str
    description: str
    departure: str
    picture: str
    price: float
    stars: str
    country: str
    nights: int
    date: str
    star_range: range

    @classmethod
    def construct_from_dict(cls, dict_data: dict) -> 'Tour':
        if 'stars' in dict_data:
            dict_data['star_range'] = range(int(dict_data.get('stars')))
        tour = dacite.from_dict(cls, dict_data)
        return tour


@dataclass
class Departure(BaseModel):
    id: str
    city_departure: str

