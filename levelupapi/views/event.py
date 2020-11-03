from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.utils import field_mapping
from rest_framework.viewsets import ViewSet
from levelupapi.models import Game, Event, Gamer
from levelupapi.views.game import GameSerializer

class Events(ViewSet):
    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event()
        event.time = request.data["time"]
        event.date = request.data["date"]
        event.description = request.data["description"]
        event.organizer = gamer
        event.game = Game.objects.get(pk=request.data["gameId"])

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try: 
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def update(self, request, pk=None):
        organizer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.descripton = request.data["description"]
        event.time = request.data["time"]
        event.organizer = organizer
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]})
        except Exception as ex:
            return Response({'message': ex.arg[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self, request):
        events = Event.objects.all()
        game = self.request.query_params.get('gameId', None)
        if game is not None:
            events = events.filter(game__id=game)
        
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

## defining all sub-serializers first to stop VS code from yelling at me?

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EventGamerSerializer(serializers.ModelSerializer):
    user = EventUserSerializer(many=False)
    class Meta:
        model = Gamer
        fields = ['user']


class EventGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'numebr_of_players', 'skill_level')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    organizer = EventGamerSerializer(many=False)
    game = EventGameSerializer(many=False)
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name = 'event',
            lookup_field = 'id'
        )
        fields = ('id', 'url', 'game', 'organizer', 'description', 'date', 'time')
        depth = 1







 