from django.shortcuts import render
from .services.tours_services import is_tour_exists, is_departure_exists, get_main_data, get_tours_cards


def main_view(request):
    context = dict(
        main_info=get_main_data(),
        tours=get_tours_cards()
    )
    return render(request, 'tours/index.html', context=context)


def departure_view(request, departure: str):
    if not is_departure_exists(departure):
        return render(request, 'tours/404.html')
    return render(request, 'tours/departure.html')


def tour_view(request, tour_id: int):
    if not is_tour_exists(tour_id):
        return render(request, 'tours/404.html')
    return render(request, 'tours/tour.html')
