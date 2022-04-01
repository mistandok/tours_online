"""
This module describes work with tours
"""


__author__ = 'Artikov A.K.'


import random
from abc import ABC, abstractmethod
from typing import List, Dict, Union, Optional, Type

import data
from .specification import SpecificationFilter, SpecificationFactory
from ..data_models import BaseModel, Tour, Departure


class AttrMinMax:
    """
    Storage for min and max attribute values.
    """
    def __init__(self, min_value=None, max_value=None):
        self.min = min_value
        self.max = max_value

    def try_set_min(self, value) -> None:
        """
        The method allows set new min value, if this value is less than current.
        :param value: new MIN value
        :return:
        """
        self.min = min(value, self.min) if self.min is not None else value

    def try_set_max(self, value) -> None:
        """
        The method allows set new MAX value, if this value is more than current.
        :param value: new MAX value
        :return:
        """
        self.max = max(value, self.max) if self.max is not None else value


class BaseController(ABC):
    """
    Base data controller.
    """
    def __init__(self, dict_data: dict):
        """
        Initialisation controller
        :param dict_data: data for control
        """
        self._base_model = self._get_base_model()
        self._data = self._get_init_data(dict_data)

    def get(self, data_filter: dict = None) -> Union[List[BaseModel], None]:
        """
        The method allows get data from Controller data
        :param data_filter: filter for select data.
        :return:
        """
        if data_filter is None:
            result = self._data.values()
        elif 'random' in data_filter:
            result = self._get_by_random(data_filter.get('random'))
        elif 'id' in data_filter:
            result = self._get_by_id(data_filter.get('id'))
            result = [result] if result else []
        else:
            result = self._get_by_filter(data_filter)

        return result

    @staticmethod
    def get_min_max_attr_for_data(list_of_data: List[BaseModel], *attr_names: str) -> Optional[Dict[str, AttrMinMax]]:
        """
        The method return min and max value for attributes in list of data
        :param list_of_data: list of data
        :param attr_names: attribute names
        :return:
        """
        result = {attr_name: AttrMinMax() for attr_name in attr_names}

        for current_data in list_of_data:
            for attr, min_max in result.items():
                tour_attr_value = getattr(current_data, attr)
                min_max.try_set_min(tour_attr_value)
                min_max.try_set_max(tour_attr_value)

        return result

    @abstractmethod
    def _get_base_model(self) -> Type[BaseModel]:
        """
        The method return Base model for controller.
        :return:
        """
        pass

    def _get_init_data(self, dict_data: dict) -> Dict[int, BaseModel]:
        """
        Init data for controller from dict
        :param dict_data:
        :return:
        """
        result = dict()
        for data_id, current_data in dict_data.items():
            result[data_id] = self._base_model.construct_from_dict(dict_data={**{'id': data_id}, **current_data})
        return result

    def _get_by_filter(self, data_filter: dict) -> List[BaseModel]:
        """
        Return data from controller by filter.
        :param data_filter: filter
        :return:
        """
        specification = None
        for name, value in data_filter.items():
            if not specification:
                specification = SpecificationFactory.constract_from_name_and_value(name, value)
            else:
                specification = specification & SpecificationFactory.constract_from_name_and_value(name, value)

        tf = SpecificationFilter()

        return list(tf.filter(self._data.values(), specification))

    def _get_by_id(self, data_id: int) -> BaseModel:
        """
        Return data from controller by id
        :param data_id: data id
        :return:
        """
        return self._data.get(data_id)

    def _get_by_random(self, random_count: int) -> List[BaseModel]:
        """
        Return random data from controller
        :param random_count: count random data
        :return:
        """
        allow_data_keys = self._data.keys()
        random_data_keys = set(random.sample(allow_data_keys, random_count))
        return [key_data for key, key_data in self._data.items() if key in random_data_keys]


class TourController(BaseController):
    """
    The class allows manipulating with tours data.
    """
    def _get_base_model(self) -> Type[BaseModel]:
        return Tour


class DepartureController(BaseController):
    """
    The class allows manipulating with departures data.
    """
    def _get_base_model(self) -> Type[BaseModel]:
        return Departure

    def _get_init_data(self, dict_data: dict) -> Dict[int, Tour]:
        result = dict()
        for data_id, current_data in dict_data.items():
            result[data_id] = self._base_model.construct_from_dict(dict_data={
                **{'id': data_id, 'city_departure': current_data}
            })
        return result


TOUR_CONTROLLER = TourController(data.tours)
DEPARTURE_CONTROLLER = DepartureController(data.departures)
