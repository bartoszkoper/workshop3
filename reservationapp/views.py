from django.conf.urls import url
from django.shortcuts import render

# Create your views here.
from django.views import View

from reservationapp.models import Sala

"""Stwórz widoki sali. 
Widoki powinny wyświetlać/odbierać formularze lub wyświetlać listę sal.
Nie zapomnij o przycisku Nowa sala i jego obsłudze na ekranie głównym.
"""
"""
Jako użytkownik chcę po wejściu na stronę główną widzieć wszystkie sale konferencyjne i 
ich status danego dnia: zajęte lub wolne. Obok nazwy każdej sali chcę mieć link do 
modyfikacji danych sali oraz do jej usunięcia.
"""

class IndexView(View):
    def get(self, request):
        salas = Sala.objects.all()
        response = dict()
        response['salas'] = salas
        response['msg'] = "ABCD"
        return render(request, 'add_sala.html', context=response)


class RoomNewView(View):
    def get(self, request):
        response = dict()
        response['msg'] = "ABCD"
        return render(request, 'add_sala.html', context=response)


class RoomModifyView(View):
    def get(self, request):
        pass


class RoomView(View):
    def get(self, request):
        pass


class RoomDeleteView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
