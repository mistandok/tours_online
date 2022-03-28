"""This module keeps api for tour application"""

__author__ = 'Artikov A.K'

from typing import List
import data
from .tour_services import TOUR_CONTROLLER, DEPARTURE_CONTROLLER


def is_departure_exists(departure: str) -> bool:
    """
    The function checks that departure exists on data
    :param departure: departure id
    :return: True if exists, else False
    """
    return bool(DEPARTURE_CONTROLLER.get({'id': departure}))


def is_tour_exists(tour_id: int) -> bool:
    """
    The function checks that departure exists on data
    :param tour_id: tour id
    :return: True if exists, else False
    """
    return bool(TOUR_CONTROLLER.get({'id': tour_id}))


def get_departure_card(departure_id: str, min_max_attributes: List[str] = None) -> tuple:
    """
    This function collects data about departure card
    :param departure_id: departure id
    :param min_max_attributes: attribute names for min\max search
    :return: list of tours, min\max values for attributes
    """
    tours = get_tours_cards({'departure': departure_id})

    if min_max_attributes:
        result_min_max_attributes = TOUR_CONTROLLER.get_min_max_attr_for_data(tours, min_max_attributes)
    else:
        result_min_max_attributes = None

    return tours, result_min_max_attributes


def get_main_data() -> dict:
    """
    The function returns data for filling main page
    :return:
    """
    title_data = dict(
        title=data.title,
        subtitle=data.subtitle,
        description=data.description
    )
    return title_data


def get_departures_data(departures_filter: list = None) -> List['Departure']:
    """
    The function returns cards with info about departure.
    :param departures_filter: filter for select departure
    :return:
    """
    return DEPARTURE_CONTROLLER.get(departures_filter)


def get_tours_cards(tours_filter: dict = None) -> List['Tour']:
    """
    The function returns cards with info about tour.
    :return: tour list
    """
    return TOUR_CONTROLLER.get(tours_filter)
