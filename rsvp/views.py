from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import RSVP
from events.models import Eventsz  # Fixed incorrect model name
from .serializers import RSVPSerializer
from accounts.models import User
from rest_framework.exceptions import NotFound, PermissionDenied

class RSVPListCreateView(generics.ListCreateAPIView):
    """
    List all RSVPs for an event or allow a user to RSVP to an event.
    """
    serializer_class = RSVPSerializer
    permission_classes = [permissions.AllowAny]  # Only logged-in users can RSVP

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return RSVP.objects.filter(event__id=event_id)

    def create(self, request, *args, **kwargs):
        event = get_object_or_404(Eventsz, id=self.kwargs['event_id'])  # Fixed incorrect model reference

        # Ensure only the logged-in user can RSVP
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to RSVP for an event.")

        # Check if RSVP already exists
        rsvp, created = RSVP.objects.get_or_create(
            user=request.user,
            event=event,
            defaults={'status': request.data.get('status', 'Going')}
        )

        if not created:
            return Response({"detail": "You have already RSVP'd for this event."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(RSVPSerializer(rsvp).data, status=status.HTTP_201_CREATED)


class RSVPDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an RSVP for a specific user and event.
    """
    serializer_class = RSVPSerializer
    permission_classes = [permissions.AllowAny]  # Ensure only authenticated users can access

    def get_object(self):
        event_id = self.kwargs['event_id']
        user_id = self.kwargs['user_id']

        # Ensure user exists
        user = get_object_or_404(User, id=user_id)

        # Ensure RSVP exists for the given event and user
        rsvp = RSVP.objects.filter(event__id=event_id, user__id=user_id).first()
        if not rsvp:
            raise NotFound({"detail": "No RSVP found for this event and user."})

        return rsvp
