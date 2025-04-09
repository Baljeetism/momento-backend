from rest_framework import serializers
from .models import RSVP
from django.contrib.auth import get_user_model

User = get_user_model()

class RSVPSerializer(serializers.ModelSerializer):


    class Meta:
        model = RSVP
        fields = ['id', 'user', 'event', 'status']
        read_only_fields = ['id', 'user']  # These fields can't be modified via API

   