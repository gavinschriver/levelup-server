from levelupapi.models.game import Game
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer

class Profile(ViewSet):
    def list(self, req):
        gamer = Gamer.objects.get(user=req.auth.user)
        events = Event.objects.filter(attendee__gamer=gamer)
        events = EventSerializer(events, many=True, context={'request': req})
        gamer = GamerSerializer(gamer, many=False, context={'request': req})
        profile = {}
        profile["gamer"] = gamer.data
        profile["events"] = events.data
        return Response(profile)

# Create serializers for Gamer entry in Profile dictionary 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class GamerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Gamer
        fields = ('bio', 'user')

# Create serializers for Events entry in Profile dictionary 
class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(view_name='game',lookup_field='id')
        fields = ('title', 'url')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    game = GameSerializer(many=False)
    class Meta: 
        model = Event
        url = serializers.HyperlinkedIdentityField(view_name='event', lookup_field='id')
        fields = ('id', 'game', 'url', 'description', 'date', 'time', 'location')

