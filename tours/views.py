from django.shortcuts import render

import data
from .services.api import (
    is_tour_exists, is_departure_exists, get_main_data,
    get_tours_cards, get_departures_data, get_departure_card
)


def main_view(request):
    context = dict(
        departures=get_departures_data(),
        main_info=get_main_data(),
        tours=get_tours_cards()
    )
    return render(request, 'tours/index.html', context=context)


def departure_view(request, departure: str):
    if not is_departure_exists(departure):
        return handler404_view(request)

    departures = get_departures_data()
    current_departure = get_departures_data({'id': departure})[-1]
    tours, min_max_attributes = get_departure_card(
        departure,
        ['price', 'nights']
    )

    context = dict(
        departures=departures,
        city_departure=current_departure.city_departure,
        count_tours=len(tours),
        min_price=min_max_attributes.get('price').min,
        max_price=min_max_attributes.get('price').max,
        min_nights=min_max_attributes.get('nights').min,
        max_nights=min_max_attributes.get('nights').max,
        tours=tours
    )

    return render(request, 'tours/departure.html', context=context)


def tour_view(request, tour_id: int):
    if not is_tour_exists(tour_id):
        return handler404_view(request)
    return render(request, 'tours/tour.html')


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
