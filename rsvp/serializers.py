from rest_framework import serializers
from .models import RSVP

class RSVPSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    event = serializers.StringRelatedField(read_only=True)  # Show event title instead of ID

    class Meta:
        model = RSVP
        fields = '__all__'
