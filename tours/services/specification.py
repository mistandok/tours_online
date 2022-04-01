"""This module allows creating some specifications for filter information in iterable objects"""

__author__ = 'Artikov A.K.'


from abc import ABC, abstractmethod
from typing import Iterator


class Specification(ABC):
    """Class allows checking, that item is satisfied conditions"""
    @abstractmethod
    def is_satisfied(self, item) -> bool:
        """
        The method give info that item is satisfied conditions
        :param item: item for check conditions
        :return:
        """
        pass

    def __and__(self, other: 'Specification') -> 'AndSpecification':
        """
        The method return AND specification.
        :param other:
        :return:
        """
        return AndSpecification(self, other)


class SpecificationFilter:
    """
    Filter for items
    """
    @staticmethod
    def filter(items, spec: Specification) -> Iterator:
        """
        The method return items, which satisfied specifications
        :param items: items
        :param spec: specification
        :return:
        """
        for item in items:
            if spec.is_satisfied(item):
                yield item


class AndSpecification(Specification):
    """
    AND specification
    """
    def __init__(self, *specifications: Specification):
        self.specifications = specifications

    def is_satisfied(self, item) -> bool:
        """
        The method checks that ALL specifications for item is satisfied conditions
        """
        return all(map(
            lambda spec: spec.is_satisfied(item), self.specifications
        ))


class DepartureSpecification(Specification):
    """
    Departure specification
    """
    def __init__(self, departure: str):
        super().__init__()
        self.departure = departure

    def is_satisfied(self, item) -> bool:
        """
        The method give info that item is satisfied conditions
        :param item: item for check conditions
        :return:
        """
        if isinstance(self.departure, list):
            return item.departure in self.departure
        return self.departure == item.departure


class NightsSpecification(Specification):
    """
    Nights specification
    """
    def __init__(self, nights: str):
        super().__init__()
        self.nights = nights

    def is_satisfied(self, item) -> bool:
        """
        The method give info that item is satisfied conditions
        :param item: item for check conditions
        :return:
        """
        if isinstance(self.nights, list):
            return item.nights in self.nights
        return self.nights == item.nights


class SpecificationFactory:
    """
    Specification factory
    """
    specification_types = {
        'departure': DepartureSpecification,
        'nights': NightsSpecification,
    }

    @staticmethod
    def constract_from_name_and_value(spec_name: str, spec_value) -> Specification:
        """
        The method create specification object from name and value.
        :param spec_name: Specification name
        :param spec_value: Specification value
        :return:
        """
        specification = SpecificationFactory.specification_types.get(spec_name)
        if specification:
            return specification(spec_value)
        raise Exception(f'Specification for {spec_name} does not exist')
