from django.urls import path
from .views import RSVPListCreateView, RSVPDetailView, RSVPByEventView

urlpatterns = [
    # GET (list all) and POST (create new)
    path('', RSVPListCreateView.as_view(), name='rsvp-list-create'),
    
    # GET (retrieve), PUT/PATCH (update), DELETE (destroy) for single RSVP
    path('<int:pk>/', RSVPDetailView.as_view(), name='rsvp-detail'),
    
    # Additional useful endpoints:
    path('users/<int:user_id>/rsvps/', RSVPListCreateView.as_view(), name='user-rsvps'),
    path('events/<int:event_id>/rsvps/', RSVPListCreateView.as_view(), name='event-rsvps'),
    path('rsvps/<int:pk>/', RSVPDetailView.as_view(), name='rsvp-detail'),
    path("rsvp/event/<int:event_id>/", RSVPByEventView.as_view(), name="rsvp-by-event"),
]