"""This module keep busines logic for tour application"""

__author__ = 'Artikov A.K'

from typing import List, Dict
import data


def is_departure_exists(departure: str) -> bool:
    """
    The function checks that departure exists on data
    :param departure: departure id
    :return: True if exists, else False
    """
    return departure in data.departures


def is_tour_exists(tour_id: int) -> bool:
    """
    The function checks that departure exists on data
    :param tour_id: tour id
    :return: True if exists, else False
    """
    return tour_id in data.tours


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


def get_tours_cards() -> List[Dict]:
    """
    The function returns cards with info about tour.
    :return: tour list
    """
    tours = []
    for tour_id, tour in data.tours.items():
        tours.append(dict(
            tour_id=tour_id,
            title=tour.get('title'),
            star_range=range(int(tour.get('stars'))),
            description=tour.get('description'),
            picture=tour.get('picture')
        ))
    return tours

