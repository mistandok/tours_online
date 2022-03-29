from django.shortcuts import render

import data
from .services.api import (
    is_tour_exists, is_departure_exists, get_main_data,
    get_tours_data, get_departures_data, get_min_max_attr_for_tours
)


def main_view(request):
    context = dict(
        departures=get_departures_data(),
        main_info=get_main_data(),
        tours=get_tours_data({'random': 6})
    )
    return render(request, 'tours/index.html', context=context)


def departure_view(request, departure: str):
    if not is_departure_exists(departure):
        return handler404_view(request)

    departures = get_departures_data()
    current_departure = get_departures_data({'id': departure})[-1]
    tours = get_tours_data({'departure': departure})
    min_max_attributes = get_min_max_attr_for_tours(tours, 'price', 'nights')

    context = dict(
        departures=departures,
        city_departure=current_departure.city_departure,
        count_tours=len(tours),
        tours=tours,
        min_max_attributes=min_max_attributes
    )

    return render(request, 'tours/departure.html', context=context)


def tour_view(request, tour_id: int):
    if not is_tour_exists(tour_id):
        return handler404_view(request)

    departures = get_departures_data()
    tour = get_tours_data({'id': tour_id})[-1]
    departure = get_departures_data({'id': tour.departure})[-1]

    context = dict(
        departures=departures,
        tour=tour,
        departure=departure
    )

    return render(request, 'tours/tour.html', context=context)


def handler404_view(request, *args, **kwargs):
    departures = get_departures_data()
    response = render(
        request,
        'tours/404.html',
        context={
            'information': 'Страница не найдена :(',
            'departures': departures
        }
    )
    response.status_code = 404
    return response
