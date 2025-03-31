from rest_framework import serializers
from .models import RSVP
from django.contrib.auth import get_user_model

User = get_user_model()

class RSVPSerializer(serializers.ModelSerializer):
    # Read-only user field that gets value from request.user
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    
    # Event field remains as is
    # event = serializers.PrimaryKeyRelatedField(queryset=Eventsz.objects.all())

    class Meta:
        model = RSVP
        fields = ['id', 'user', 'event', 'status']
        read_only_fields = ['id', 'user']  # These fields can't be modified via API

    def create(self, validated_data):
        """
        Create RSVP instance, automatically setting the user from the request.
        """
        # Get the user from the request context
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Use get_or_create to handle potential race conditions
        rsvp, created = RSVP.objects.get_or_create(
            user=user,
            event=validated_data['event'],
            defaults={'status': validated_data['status']}
        )
        
        if not created:
            # If RSVP already exists, update the status
            rsvp.status = validated_data['status']
            rsvp.save()
            
        return rsvp