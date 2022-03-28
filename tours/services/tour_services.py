"""
This module describes work with Tour
"""

from typing import List, Dict, Union, Optional, Type
from abc import ABC, abstractmethod
import data
from ..data_models import BaseModel, Tour, Departure
from .specification import SpecificationFilter, SpecificationFactory


class AttrMinMax:
    def __init__(self, min_value=None, max_value=None):
        self.min = min_value
        self.max = max_value

    def try_set_min(self, value) -> None:
        self.min = min(value, self.min) if self.min is not None else value

    def try_set_max(self, value) -> None:
        self.max = max(value, self.max) if self.max is not None else value


class BaseController(ABC):
    def __init__(self, dict_data: dict):
        self._base_model = self._get_base_model()
        self._data = self._get_init_data(dict_data)

    def get(self, data_filter: dict = None) -> Union[List[Tour], None]:
        if data_filter is None:
            return self._data.values()
        elif 'id' in data_filter:
            result_data = self._get_by_id(data_filter.get('id'))
            return [result_data] if result_data else []
        else:
            return self._get_by_filter(data_filter)

    @staticmethod
    def get_min_max_attr_for_data(list_of_data: List[BaseModel], *attr_names: str) -> Optional[Dict[str, AttrMinMax]]:
        result = {attr_name: AttrMinMax() for attr_name in attr_names}

        for current_data in list_of_data:
            for attr, min_max in result.items():
                tour_attr_value = getattr(current_data, attr)
                min_max.try_set_min(tour_attr_value)
                min_max.try_set_max(tour_attr_value)

        return result

    @abstractmethod
    def _get_base_model(self) -> Type[BaseModel]:
        pass

    def _get_init_data(self, dict_data: dict) -> Dict[int, Tour]:
        result = dict()
        for data_id, current_data in dict_data.items():
            result[data_id] = self._base_model.construct_from_dict(dict_data={**{'id': data_id}, **current_data})
        return result

    def _get_by_filter(self, data_filter: dict) -> List[Tour]:
        specification = None
        for name, value in data_filter.items():
            if not specification:
                specification = SpecificationFactory.constract_from_name_and_value(name, value)
            else:
                specification = specification & SpecificationFactory.constract_from_name_and_value(name, value)

        tf = SpecificationFilter()

        return list(tf.filter(self._data.values(), specification))

    def _get_by_id(self, data_id: int) -> BaseModel:
        return self._data.get(data_id)


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
