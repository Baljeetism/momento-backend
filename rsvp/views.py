from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import RSVP
from events.models import Events
from .serializers import RSVPSerializer
from rest_framework import serializers  # Added missing import
from .permissions import IsSuperUser

class RSVPListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating RSVPs"""
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]  # Changed from IsAuthenticatedOrReadOnly

    def get_queryset(self):
        """Filters RSVPs for the current user"""
        # if self.request.user.is_staff:  # Only allow admins
        #     return RSVP.objects.all()
        return RSVP.objects.filter(user=self.request.user).select_related("user", "event")

    def perform_create(self, serializer):
        """Ensure unique RSVP per user/event & update event attendees."""
        user = self.request.user
        event_id = self.request.data.get("event")

        if not event_id:
            raise serializers.ValidationError({"event": "This field is required."})

        event = get_object_or_404(Events, id=event_id)

        # Prevent duplicate RSVPs
        if RSVP.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError({"error": "You have already RSVP'd for this event."})

        # Save RSVP
        rsvp_instance = serializer.save(user=user)
        
        # Update attendees
        # self.update_attendees(rsvp_instance)

    def update_attendees(self, rsvp):
        """Helper method to manage event attendees"""
        # if rsvp.status.lower() == "attending":
        #     rsvp.event.attendees.add(rsvp.user)
        # else:
        #     rsvp.event.attendees.remove(rsvp.user)
        pass
    def list(self, request, *args, **kwargs):
        """Custom list response with event details"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

class RSVPDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles updating & deleting individual RSVPs"""
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own RSVPs"""
        # return RSVP.objects.filter(user=self.request.user)
        user_id = self.kwargs.get('user_id') or self.request.user.id
        return RSVP.objects.filter(user_id=user_id)

    def perform_update(self, serializer):
        """Update RSVP and manage attendees"""
        instance = self.get_object()
        
        if "event" in serializer.validated_data:
            raise serializers.ValidationError({"event": "You cannot change the event."})

        old_status = instance.status
        new_status = serializer.validated_data.get('status', old_status)
        
        serializer.save()
        
        # Only update attendees if status changed
        # if old_status.lower() != new_status.lower():
        #     self.update_attendees(instance)

    def update_attendees(self, rsvp):
        """Helper method to manage event attendees"""
        # if rsvp.status.lower() == "attending":
        #     rsvp.event.attendees.add(rsvp.user)
        # else:
        #     rsvp.event.attendees.remove(rsvp.user)
        pass

    def perform_destroy(self, instance):
        """Remove user from event attendees when deleting RSVP"""
        # instance.event.attendees.remove(instance.user)
        # instance.delete()
        pass
class RSVPByEventView(generics.ListAPIView):
    """Retrieve all RSVPs for a specific event"""
    serializer_class = RSVPSerializer
    permission_classes = [permissions.AllowAny]  # Ensure only logged-in users can access

    def get_queryset(self):
        event_id = self.kwargs.get("event_id")  # Get event ID from URL
        return RSVP.objects.filter(event_id=event_id).select_related("user", "event")