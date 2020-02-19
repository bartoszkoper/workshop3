from django.conf.urls import url
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime
from django.views import View
from reservationapp.models import Sala, Reservation


class IndexView(View):
    """Jako użytkownik chcę po wejściu na stronę główną widzieć wszystkie sale konferencyjne i ich status danego dnia: zajęte lub wolne.
    Obok nazwy każdej sali chcę mieć link do modyfikacji danych sali oraz do jej usunięcia."""

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

        # New object has been built and success message on your face.
        new_room = Sala.objects.create(name=name, capacity=capacity, projector=projector)
        messages.success(request, f"New conference room has been added: {new_room.name}")

        return render(request, 'add_sala.html', context=self.response)


class RoomView(View):
    """Jako użytkownik po kliknięciu w nazwę sali chcę zobaczyć wszystkie dane sali:
    jej nazwę, pojemność oraz informację, czy ma rzutnik. Dodatkowo chcę zobaczyć listę dni, w które sala będzie zajęta.
    Nie chcę widzieć dni, które minęły. Chcę widzieć link, który pozwoli zarezerwować tę salę."""

    response = dict()
    response['title'] = f"Room details"

    def get(self, request, id):
        self.response['room'] = Sala.objects.get(pk=id)
        self.response['reservations'] = Reservation.objects.filter(sala=id, date__gte=datetime.today())
        self.response['edit'] = False  # Tylko do wyświetlania
        return render(request, 'room_view.html', context=self.response)


class RoomModifyView(RoomView):  # A może do edycji przydałoby się dziedziczenie, ale z flagą edit=True ?
    """Obok nazwy każdej sali chcę mieć link do modyfikacji danych sali oraz do jej usunięcia.
    Jako użytkownik po wejściu na stronę edycji sali chcę móc podać dane sali (nazwa, pojemność, rzutnik, ew. inne dane)."""

    def get(self, request, id):
        super().get(request, id)
        self.response['edit'] = True
        return render(request, 'room_view.html', context=self.response)

    def post(self, request, id):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector') == 'on'
        sala = Sala.objects.get(pk=id)
        sala.name = name
        sala.capacity = capacity
        sala.projector = projector
        sala.save()
        messages.success(request,
                         f"Room has been modified. New name: {name} | Capacity {capacity} Projector?: {projector}")

        return redirect('room_modify', id)


class RoomAddReservationView(View):
    """Rezerwacja sali."""

    def get(self, request, id):
        sala = Sala.objects.get(pk=id)
        date = datetime.today().date()

        if sala.is_unavailable(date) == False:
            comment = f"Auto-booking na dzień: {date}"
            Reservation.objects.create(sala=sala, comment=comment, date=date)
            messages.success(request, f"Conference room: {sala.name} has been booked for today!")
        else:
            messages.add_message(request, 100,
                                 f"Conference room for selected date is booked already. Please select another day.",
                                 extra_tags='danger')
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

        else:
            # Message is the date is already selected* (Information should be improved)
            messages.add_message(request, 100,
                                 f"Conference room for selected date is booked already. Please select another day.",
                                 extra_tags='danger')
        return redirect('room_view', id=id)


class RoomDeleteView(View):
    """Obok nazwy każdej sali chcę mieć link do modyfikacji danych sali oraz do jej usunięcia."""

    def get(self, request, id):
        sala = Sala.objects.get(pk=id)
        sala.delete()
        messages.info(request, f'Conference room {sala.name} has been deleted.')
        return redirect('main')


class RoomSearchView(View):
    """Jako użytkownik chcę móc wyszukać sale z podaniem następujących warunków: nazwa sali, dzień, pojemność sali,
       dostępność rzutnika."""

    response = dict()
    response['title'] = f"Search Results"

    def get(self, request):
        return redirect('main')

    def post(self, request):
        name = request.POST.get('name')
        date = str(request.POST.get('date', default=datetime.today()))
        capacity = 0 if request.POST.get('capacity') == '' else request.POST.get('capacity')
        projector = request.POST.getlist('projector')

        # Searching for all rooms meets the criteria
        rooms = Sala.objects.filter(name__icontains=name, reservations__date__gte=date, capacity__gte=capacity,
                                    projector__in=projector).distinct()

        # Searching for all reservation to show as output.
        reservations = Reservation.objects.filter(sala__in=rooms).order_by('sala__name')
        self.response['reservations'] = reservations

        return render(request, 'search_view.html', context=self.response)
