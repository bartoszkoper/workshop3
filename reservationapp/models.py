from django.db import models


# Create your models here.


class Sala(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

    def is_unavailable(self, date):
        response = self.reservations.filter(date=date).exists()
        return response


    def __str__(self):
        return f"Obiekt<{self.name} {self.capacity} {self.projector}"


class Reservation(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        return f"Dodano rezerwację dla: {self.sala} na dzien: {self.date} z komentarzem: {self.comment}"
