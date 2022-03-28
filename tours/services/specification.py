"""This module allow creating some specifications for filter information in iterable objects"""

__author__ = 'Artikov A.K.'


from typing import Iterator


class Specification:
    def is_satisfied(self, item) -> bool:
        pass

    def __and__(self, other: 'Specification') -> 'AndSpecification':
        return AndSpecification(self, other)


class SpecificationFilter:
    @staticmethod
    def filter(items, spec: Specification) -> Iterator:
        for item in items:
            if spec.is_satisfied(item):
                yield item


class AndSpecification(Specification):
    def __init__(self, *specifications: Specification):
        self.specifications = specifications

    def is_satisfied(self, item) -> bool:
        return all(map(
            lambda spec: spec.is_satisfied(item), self.specifications
        ))


class DepartureSpecification(Specification):
    def __init__(self, departure: str):
        super().__init__()
        self.departure = departure

    def is_satisfied(self, item) -> bool:
        return self.departure == item.departure


class NightsSpecification(Specification):
    def __init__(self, nights: str):
        super().__init__()
        self.nights = nights

    def is_satisfied(self, item) -> bool:
        return self.nights == item.nights


class SpecificationFactory:
    specification_types = {
        'departure': DepartureSpecification,
        'nights': NightsSpecification,
    }
    @staticmethod
    def constract_from_name_and_value(spec_name: str, spec_value) -> Specification:
        specification = SpecificationFactory.specification_types.get(spec_name)
        if specification:
            return specification(spec_value)
        raise Exception(f'Specification for {spec_name} does not exist')
