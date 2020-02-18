from django.conf.urls import url
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime
from django.views import View

from reservationapp.models import Sala, Reservation

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
    response = dict()
    response['title'] = "Conference Room Reservation Platform"

    def get(self, request):
        rooms = Sala.objects.all()
        json_builder = list()

        # Build list with objects and statuses for each
        for room in rooms:
            json_builder.append({'room': room, 'status': room.is_unavailable(datetime.today())})
        self.response['rooms'] = json_builder

        return render(request, 'index.html', context=self.response)


class RoomNewView(View):
    """Jako użytkownik chcę móc dodać nową salę."""
    response = dict()
    response['title'] = 'Add new conference room.'

    def get(self, request):
        return render(request, 'add_sala.html', context=self.response)

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector') == 'on'

        # New object has been built.
        new_room = Sala.objects.create(name=name, capacity=capacity, projector=projector)
        messages.success(request, f"New conference room has been added: {new_room.name}")

        return render(request, 'add_sala.html', context=self.response)


class RoomView(View):
    """TODO:Jako użytkownik po kliknięciu w nazwę sali chcę zobaczyć wszystkie dane sali:
    jej nazwę, pojemność oraz informację, czy ma rzutnik.
    Dodatkowo chcę zobaczyć listę dni, w które sala będzie zajęta.
    Nie chcę widzieć dni, które minęły.
    Chcę widzieć link, który pozwoli zarezerwować tę salę."""
    response = dict()
    response['title'] = f"Room details"

    def get(self, request, id):
        self.response['room'] = Sala.objects.get(pk=id)
        self.response['reservations'] = Reservation.objects.filter(sala=id, date__gte=datetime.today())
        print(request)
        return render(request, 'room_view.html', context=self.response)


class RoomModifyView(View): #A może do edycji przydałoby się dziedziczenie, ale z flagą edit=True ?
    """TODO:Obok nazwy każdej sali chcę mieć link do
    modyfikacji danych sali oraz do jej usunięcia."""
    """Jako użytkownik po wejściu na stronę edycji sali chcę móc podać 
    dane sali (nazwa, pojemność, rzutnik, ew. inne dane)."""
    response = dict()
    def get(self, request, id):
        room = RoomView.get(self=self,request=request,id=id)
        self.response['edit'] = True
        return room


    def post(self, request):
        pass


class RoomAddReservationView(View):
    """Rezerwacja sali."""

    def get(self, request, id):
        sala = Sala.objects.get(pk=id)
        date = datetime.today()
        comment = f"Auto-booking na dzień: {date}"
        Reservation.objects.create(sala=sala, comment=comment, date=date)
        messages.success(request, f"Zarezerwowano salkę {sala.name} na dziś!")

        return redirect('/')

    def post(self, request, id):
        sala = Sala.objects.get(pk=id)
        comment = request.POST.get('comment')
        date = request.POST.get('date')

        # Check if user wants to book conference in the past.
        if date < str(datetime.today().date()):
            messages.add_message(request, 100, f"You cannot book the conference room in the past.",
                                 extra_tags='warning')
        # Check if there is no reservation for selected day.
        elif sala.is_unavailable(date) == False:
            Reservation.objects.create(sala=sala, date=date, comment=comment)
            messages.success(request, f"Reservation has been added.")
        # Message that the date is already selected* (Information should be improved)
        else:
            messages.add_message(request, 100, f"This date is reserved already. Please select another day.",
                                 extra_tags='danger')
        return redirect('room_view', id=id)


class RoomDeleteView(View):
    """Obok nazwy każdej sali chcę mieć link do
    modyfikacji danych sali oraz do jej usunięcia."""

    def get(self, request, id):
        sala = Sala.objects.get(pk=id)
        sala.delete()
        messages.info(request, f'Conference room {sala.name} has been deleted.')
        return redirect('main')


class RoomSearchView(View):
    """Jako użytkownik chcę móc wyszukać sale z podaniem następujących warunków:
        nazwa sali,
        dzień,
        pojemność sali,
        dostępność rzutnika."""

    def get(self, request):
        pass
