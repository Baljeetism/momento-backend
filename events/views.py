from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Eventsz
from .serializers import EventSerializer

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Eventsz.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]  # Only admin users create/edit events

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
