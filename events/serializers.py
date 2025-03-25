from rest_framework import serializers
from .models import  Eventsz



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventsz
        fields = ['title', 'description', 'date', 'time', 'location', 'price', 'artist']
