from django.conf.urls import url
from django.shortcuts import render

# Create your views here.
from django.utils.datetime_safe import datetime
from django.views import View

from reservationapp.models import Sala

"""Stwórz widoki sali. 
Widoki powinny wyświetlać/odbierać formularze lub wyświetlać listę sal.
Nie zapomnij o przycisku Nowa sala i jego obsłudze na ekranie głównym.
"""


class IndexView(View):
    """
    Jako użytkownik chcę po wejściu na stronę główną widzieć wszystkie sale konferencyjne i
    ich status danego dnia: zajęte lub wolne.
    Obok nazwy każdej sali chcę mieć link do modyfikacji danych sali oraz do jej usunięcia.
    """

    def get(self, request):
        rooms = Sala.objects.all()
        response = dict()
        json_builder = list()

        for room in rooms:
            json_builder.append({'room': room, 'status': room.is_unavailable(datetime.today())})

        response['rooms'] = json_builder

        return render(request, 'index.html', context=response)


class RoomNewView(View):
    """Jako użytkownik chcę móc dodać nową salę."""

    def get(self, request):
        response = dict()
        response['msg'] = "ABCD"
        return render(request, 'add_sala.html', context=response)


class RoomView(View):
    """Jako użytkownik po kliknięciu w nazwę sali chcę zobaczyć wszystkie dane sali:
    jej nazwę, pojemność oraz informację, czy ma rzutnik.
    Dodatkowo chcę zobaczyć listę dni, w które sala będzie zajęta.
    Nie chcę widzieć dni, które minęły.
    Chcę widzieć link, który pozwoli zarezerwować tę salę."""

    def get(self, request):
        pass


class RoomModifyView(View):
    """Obok nazwy każdej sali chcę mieć link do
    modyfikacji danych sali oraz do jej usunięcia."""
    """Jako użytkownik po wejściu na stronę edycji sali chcę móc podać 
    dane sali (nazwa, pojemność, rzutnik, ew. inne dane)."""

    def get(self, request):
        pass


class RoomDeleteView(View):
    """Obok nazwy każdej sali chcę mieć link do
    modyfikacji danych sali oraz do jej usunięcia."""

    def get(self, request):
        pass

    def post(self, request):
        pass


class RoomSearchView(View):
    """Jako użytkownik chcę móc wyszukać sale z podaniem następujących warunków:
        nazwa sali,
        dzień,
        pojemność sali,
        dostępność rzutnika."""

    def get(self, request):
        pass
