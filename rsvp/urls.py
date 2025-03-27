from django.urls import path
from .views import RSVPListCreateView, RSVPDetailView

urlpatterns = [
    path('<int:event_id>/', RSVPListCreateView.as_view(), name="rsvp-list-create"),  # List and create RSVPs for an event
    path('<int:event_id>/<int:user_id>/', RSVPDetailView.as_view(), name="rsvp-detail"),  # Retrieve, update, delete an RSVP
]
