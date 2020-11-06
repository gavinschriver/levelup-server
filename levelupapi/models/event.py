from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

class Event(models.Model):
    organizer = models.ForeignKey('Gamer', on_delete=CASCADE)
    description = models.CharField(max_length=500)          
    location = models.CharField(max_length=50)
    game = models.ForeignKey('Game', on_delete=CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value