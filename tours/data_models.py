"""This module describe data model for tours"""

__author__ = 'Artikov A.K.'

from dataclasses import dataclass

import dacite


@dataclass
class BaseModel:
    """
    Base data model
    """
    @classmethod
    def construct_from_dict(cls, dict_data: dict) -> 'BaseModel':
        """
        Create object for data model from dict
        :param dict_data:
        :return:
        """
        data_model = dacite.from_dict(cls, dict_data)
        return data_model

    def as_dict(self):
        return self.__dict__


@dataclass
class Tour(BaseModel):
    """
    Tour data model
    """
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
    """
    Departure model
    """
    id: str
    city_departure: str
